// MongoDB initialization script for testing

db = db.getSiblingDB('camera_collector_test');

// Create collections
db.createCollection('cameras');
db.createCollection('users');

// Create indexes for better performance
db.cameras.createIndex({ "brand": 1 });
db.cameras.createIndex({ "type": 1 });
db.cameras.createIndex({ "year_manufactured": 1 });
db.cameras.createIndex({ "film_format": 1 });

db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });

// Create an admin user for testing
db.users.insertOne({
  username: "admin_test",
  email: "admin_test@example.com",
  hashed_password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", // "password"
  is_active: true,
  created_at: new Date(),
  updated_at: new Date()
});

// Insert sample cameras for testing
db.cameras.insertMany([
  {
    brand: "Nikon",
    model: "F3",
    year_manufactured: 1980,
    type: "SLR",
    film_format: "35mm",
    condition: "excellent",
    special_features: ["high-speed", "titanium shutter"],
    notes: "Classic professional SLR",
    acquisition_date: new Date("2023-01-15"),
    acquisition_price: 450.00,
    estimated_value: 500.00,
    images: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    brand: "Leica",
    model: "M3",
    year_manufactured: 1954,
    type: "rangefinder",
    film_format: "35mm",
    condition: "good",
    special_features: ["double stroke"],
    notes: "Iconic rangefinder camera",
    acquisition_date: new Date("2022-11-10"),
    acquisition_price: 1200.00,
    estimated_value: 1500.00,
    images: [],
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    brand: "Hasselblad",
    model: "500C/M",
    year_manufactured: 1970,
    type: "medium format",
    film_format: "120",
    condition: "excellent",
    special_features: ["interchangeable backs"],
    notes: "Professional medium format camera",
    acquisition_date: new Date("2023-02-20"),
    acquisition_price: 1800.00,
    estimated_value: 2000.00,
    images: [],
    created_at: new Date(),
    updated_at: new Date()
  }
]);

print("Test database initialization completed!");