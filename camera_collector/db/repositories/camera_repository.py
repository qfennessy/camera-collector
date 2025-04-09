from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from camera_collector.models.camera import Camera
from camera_collector.core.exceptions import NotFoundError, DatabaseError


class CameraRepository:
    """Repository for camera data operations in MongoDB."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.cameras
    
    async def create(self, camera: Camera) -> Camera:
        """Create a new camera in the database.
        
        Args:
            camera: The camera model to create
            
        Returns:
            The created camera with ID
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            camera_dict = camera.dict(exclude={"id"} if camera.id is None else {})
            if camera.id:
                camera_dict["_id"] = ObjectId(camera.id)
                
            result = await self.collection.insert_one(camera_dict)
            camera.id = str(result.inserted_id)
            return camera
        except Exception as e:
            raise DatabaseError(f"Failed to create camera: {str(e)}")
    
    async def get_by_id(self, id: str) -> Camera:
        """Get a camera by its ID.
        
        Args:
            id: The camera ID
            
        Returns:
            The camera if found
            
        Raises:
            NotFoundError: If camera does not exist
            DatabaseError: If database operation fails
        """
        try:
            camera_dict = await self.collection.find_one({"_id": ObjectId(id)})
            if not camera_dict:
                raise NotFoundError(f"Camera with ID {id} not found")
                
            camera_dict["id"] = str(camera_dict.pop("_id"))
            return Camera(**camera_dict)
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get camera: {str(e)}")
    
    async def get_all(self, skip: int = 0, limit: int = 100, 
                      filters: Optional[Dict[str, Any]] = None) -> List[Camera]:
        """Get all cameras with pagination and optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Optional filter conditions
            
        Returns:
            List of cameras
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            query = filters or {}
            cursor = self.collection.find(query).skip(skip).limit(limit)
            
            cameras = []
            async for camera_dict in cursor:
                camera_dict["id"] = str(camera_dict.pop("_id"))
                cameras.append(Camera(**camera_dict))
                
            return cameras
        except Exception as e:
            raise DatabaseError(f"Failed to get cameras: {str(e)}")
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count cameras with optional filtering.
        
        Args:
            filters: Optional filter conditions
            
        Returns:
            Number of matching cameras
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            query = filters or {}
            return await self.collection.count_documents(query)
        except Exception as e:
            raise DatabaseError(f"Failed to count cameras: {str(e)}")
    
    async def update(self, id: str, camera_update: Camera) -> Camera:
        """Update a camera by its ID.
        
        Args:
            id: The camera ID
            camera_update: The updated camera data
            
        Returns:
            The updated camera
            
        Raises:
            NotFoundError: If camera does not exist
            DatabaseError: If database operation fails
        """
        try:
            # Exclude None values and id from update
            update_data = {k: v for k, v in camera_update.dict(exclude={"id"}).items() 
                          if v is not None}
            
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError(f"Camera with ID {id} not found")
                
            return await self.get_by_id(id)
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update camera: {str(e)}")
    
    async def delete(self, id: str) -> bool:
        """Delete a camera by its ID.
        
        Args:
            id: The camera ID
            
        Returns:
            True if camera was deleted
            
        Raises:
            NotFoundError: If camera does not exist
            DatabaseError: If database operation fails
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            
            if result.deleted_count == 0:
                raise NotFoundError(f"Camera with ID {id} not found")
                
            return True
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to delete camera: {str(e)}")
    
    async def get_stats_by_brand(self) -> List[Dict[str, Any]]:
        """Get camera statistics grouped by brand.
        
        Returns:
            List of brand statistics (brand name and count)
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            pipeline = [
                {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"brand": "$_id", "count": 1, "_id": 0}}
            ]
            
            result = []
            async for doc in self.collection.aggregate(pipeline):
                result.append(doc)
                
            return result
        except Exception as e:
            raise DatabaseError(f"Failed to get brand statistics: {str(e)}")
    
    async def get_stats_by_type(self) -> List[Dict[str, Any]]:
        """Get camera statistics grouped by type.
        
        Returns:
            List of type statistics (type name and count)
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            pipeline = [
                {"$group": {"_id": "$type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"type": "$_id", "count": 1, "_id": 0}}
            ]
            
            result = []
            async for doc in self.collection.aggregate(pipeline):
                result.append(doc)
                
            return result
        except Exception as e:
            raise DatabaseError(f"Failed to get type statistics: {str(e)}")
    
    async def get_stats_by_decade(self) -> List[Dict[str, Any]]:
        """Get camera statistics grouped by decade of manufacture.
        
        Returns:
            List of decade statistics (decade and count)
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            pipeline = [
                {
                    "$project": {
                        "decade": {
                            "$concat": [
                                {"$substr": [{"$subtract": [{"$year": {"$toDate": {"$year": "$year_manufactured"}}}, {"$mod": [{"$year": {"$toDate": {"$year": "$year_manufactured"}}}, 10]}]}, 0, -1]},
                                "0s"
                            ]
                        }
                    }
                },
                {"$group": {"_id": "$decade", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$project": {"decade": "$_id", "count": 1, "_id": 0}}
            ]
            
            result = []
            async for doc in self.collection.aggregate(pipeline):
                result.append(doc)
                
            return result
        except Exception as e:
            raise DatabaseError(f"Failed to get decade statistics: {str(e)}")
    
    async def get_total_value(self) -> float:
        """Get total estimated value of all cameras.
        
        Returns:
            Total estimated value
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            pipeline = [
                {"$match": {"estimated_value": {"$exists": True, "$ne": None}}},
                {"$group": {"_id": None, "total_value": {"$sum": "$estimated_value"}}}
            ]
            
            result = await self.collection.aggregate(pipeline).to_list(length=1)
            if not result:
                return 0.0
                
            return result[0].get("total_value", 0.0)
        except Exception as e:
            raise DatabaseError(f"Failed to get total value: {str(e)}")