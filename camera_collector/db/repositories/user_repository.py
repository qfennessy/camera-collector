from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from camera_collector.models.user import User
from camera_collector.core.exceptions import NotFoundError, DatabaseError


class UserRepository:
    """Repository for user data operations in MongoDB."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users
    
    async def create(self, user: User) -> User:
        """Create a new user in the database.
        
        Args:
            user: The user model to create
            
        Returns:
            The created user with ID
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            user_dict = user.dict(exclude={"id"} if user.id is None else {})
            if user.id:
                user_dict["_id"] = ObjectId(user.id)
                
            result = await self.collection.insert_one(user_dict)
            user.id = str(result.inserted_id)
            return user
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    async def get_by_id(self, id: str) -> User:
        """Get a user by their ID.
        
        Args:
            id: The user ID
            
        Returns:
            The user if found
            
        Raises:
            NotFoundError: If user does not exist
            DatabaseError: If database operation fails
        """
        try:
            user_dict = await self.collection.find_one({"_id": ObjectId(id)})
            if not user_dict:
                raise NotFoundError(f"User with ID {id} not found")
                
            user_dict["id"] = str(user_dict.pop("_id"))
            return User(**user_dict)
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email.
        
        Args:
            email: The user's email
            
        Returns:
            The user if found, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            user_dict = await self.collection.find_one({"email": email})
            if not user_dict:
                return None
                
            user_dict["id"] = str(user_dict.pop("_id"))
            return User(**user_dict)
        except Exception as e:
            raise DatabaseError(f"Failed to get user by email: {str(e)}")
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username.
        
        Args:
            username: The user's username
            
        Returns:
            The user if found, None otherwise
            
        Raises:
            DatabaseError: If database operation fails
        """
        try:
            user_dict = await self.collection.find_one({"username": username})
            if not user_dict:
                return None
                
            user_dict["id"] = str(user_dict.pop("_id"))
            return User(**user_dict)
        except Exception as e:
            raise DatabaseError(f"Failed to get user by username: {str(e)}")
    
    async def update(self, id: str, user_update: User) -> User:
        """Update a user by their ID.
        
        Args:
            id: The user ID
            user_update: The updated user data
            
        Returns:
            The updated user
            
        Raises:
            NotFoundError: If user does not exist
            DatabaseError: If database operation fails
        """
        try:
            # Exclude None values and id from update
            update_data = {k: v for k, v in user_update.dict(exclude={"id"}).items() 
                          if v is not None}
            
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise NotFoundError(f"User with ID {id} not found")
                
            return await self.get_by_id(id)
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    async def delete(self, id: str) -> bool:
        """Delete a user by their ID.
        
        Args:
            id: The user ID
            
        Returns:
            True if user was deleted
            
        Raises:
            NotFoundError: If user does not exist
            DatabaseError: If database operation fails
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            
            if result.deleted_count == 0:
                raise NotFoundError(f"User with ID {id} not found")
                
            return True
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to delete user: {str(e)}")