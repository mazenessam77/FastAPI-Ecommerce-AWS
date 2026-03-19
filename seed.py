"""
Product seeder — populates categories and products.
Usage:
  python seed.py                    # reads .env automatically
  DB_URL=postgresql://... python seed.py
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL") or (
    f"postgresql://{os.getenv('db_username')}:{os.getenv('db_password')}"
    f"@{os.getenv('db_hostname')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
)

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Garden",
    "Sports & Outdoors",
    "Books",
    "Beauty & Health",
    "Toys & Games",
    "Automotive",
]

PRODUCTS = [
    # Electronics
    {
        "title": "Wireless Noise-Cancelling Headphones",
        "description": "Premium over-ear headphones with active noise cancellation, 30-hour battery life, and foldable design.",
        "price": 299,
        "discount_percentage": 15.0,
        "rating": 4.7,
        "stock": 85,
        "brand": "SoundMax",
        "thumbnail": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "images": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
            "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800",
        ],
        "category": "Electronics",
    },
    {
        "title": "4K Smart TV 55-inch",
        "description": "Ultra HD 4K LED Smart TV with built-in streaming apps, HDR10+, and Dolby Vision.",
        "price": 649,
        "discount_percentage": 10.0,
        "rating": 4.5,
        "stock": 40,
        "brand": "ViewPro",
        "thumbnail": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400",
        "images": [
            "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800",
        ],
        "category": "Electronics",
    },
    {
        "title": "Mechanical Gaming Keyboard",
        "description": "RGB mechanical keyboard with Cherry MX switches, full N-key rollover, and aluminum frame.",
        "price": 129,
        "discount_percentage": 5.0,
        "rating": 4.6,
        "stock": 120,
        "brand": "KeyForce",
        "thumbnail": "https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=400",
        "images": [
            "https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=800",
        ],
        "category": "Electronics",
    },
    {
        "title": "Smartphone 128GB",
        "description": "Flagship smartphone with 6.7-inch AMOLED display, triple-camera system, and 5G support.",
        "price": 899,
        "discount_percentage": 8.0,
        "rating": 4.8,
        "stock": 60,
        "brand": "PhoneTech",
        "thumbnail": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
        ],
        "category": "Electronics",
    },
    # Clothing
    {
        "title": "Classic Denim Jacket",
        "description": "Timeless denim jacket with a relaxed fit, two chest pockets, and button closure.",
        "price": 89,
        "discount_percentage": 20.0,
        "rating": 4.3,
        "stock": 200,
        "brand": "UrbanWear",
        "thumbnail": "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=400",
        "images": [
            "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=800",
        ],
        "category": "Clothing",
    },
    {
        "title": "Running Sneakers",
        "description": "Lightweight running shoes with responsive cushioning, breathable mesh upper, and durable outsole.",
        "price": 110,
        "discount_percentage": 12.0,
        "rating": 4.5,
        "stock": 150,
        "brand": "SwiftStep",
        "thumbnail": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
        ],
        "category": "Clothing",
    },
    # Home & Garden
    {
        "title": "Ceramic Coffee Mug Set",
        "description": "Set of 4 handcrafted ceramic mugs, 12oz each, microwave and dishwasher safe.",
        "price": 35,
        "discount_percentage": 0.0,
        "rating": 4.4,
        "stock": 300,
        "brand": "HomeCraft",
        "thumbnail": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400",
        "images": [
            "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800",
        ],
        "category": "Home & Garden",
    },
    {
        "title": "Bamboo Cutting Board Set",
        "description": "Set of 3 organic bamboo cutting boards in different sizes, with juice groove and hanging hole.",
        "price": 45,
        "discount_percentage": 10.0,
        "rating": 4.6,
        "stock": 180,
        "brand": "EcoKitchen",
        "thumbnail": "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=400",
        "images": [
            "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=800",
        ],
        "category": "Home & Garden",
    },
    # Sports & Outdoors
    {
        "title": "Yoga Mat Premium",
        "description": "Non-slip 6mm thick yoga mat with alignment lines, carrying strap, and eco-friendly TPE material.",
        "price": 55,
        "discount_percentage": 5.0,
        "rating": 4.7,
        "stock": 250,
        "brand": "FlexFit",
        "thumbnail": "https://images.unsplash.com/photo-1601925228269-e3a3b4cfb4f6?w=400",
        "images": [
            "https://images.unsplash.com/photo-1601925228269-e3a3b4cfb4f6?w=800",
        ],
        "category": "Sports & Outdoors",
    },
    {
        "title": "Adjustable Dumbbell Set 40kg",
        "description": "Quick-adjust dumbbell set from 2.5kg to 40kg, replaces 15 sets of weights, compact storage.",
        "price": 349,
        "discount_percentage": 18.0,
        "rating": 4.8,
        "stock": 30,
        "brand": "IronCore",
        "thumbnail": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400",
        "images": [
            "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800",
        ],
        "category": "Sports & Outdoors",
    },
    # Books
    {
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "description": "Robert C. Martin's classic guide to writing clean, readable, and maintainable code.",
        "price": 40,
        "discount_percentage": 0.0,
        "rating": 4.9,
        "stock": 500,
        "brand": "Prentice Hall",
        "thumbnail": "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400",
        "images": [
            "https://images.unsplash.com/photo-1589998059171-988d887df646?w=800",
        ],
        "category": "Books",
    },
    # Beauty & Health
    {
        "title": "Vitamin C Serum 30ml",
        "description": "Brightening vitamin C serum with hyaluronic acid and niacinamide for glowing skin.",
        "price": 28,
        "discount_percentage": 0.0,
        "rating": 4.5,
        "stock": 400,
        "brand": "GlowLab",
        "thumbnail": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400",
        "images": [
            "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800",
        ],
        "category": "Beauty & Health",
    },
    # Toys & Games
    {
        "title": "Building Blocks Set 500pcs",
        "description": "Classic colorful building blocks compatible with major brands, 500 pieces, ages 4+.",
        "price": 49,
        "discount_percentage": 10.0,
        "rating": 4.6,
        "stock": 220,
        "brand": "BrickFun",
        "thumbnail": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400",
        "images": [
            "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800",
        ],
        "category": "Toys & Games",
    },
    # Automotive
    {
        "title": "Car Dashboard Camera 4K",
        "description": "Wide-angle 4K dash cam with night vision, loop recording, G-sensor, and Wi-Fi connectivity.",
        "price": 129,
        "discount_percentage": 7.0,
        "rating": 4.4,
        "stock": 95,
        "brand": "DriveSafe",
        "thumbnail": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400",
        "images": [
            "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800",
        ],
        "category": "Automotive",
    },
]


def seed():
    db = Session()
    try:
        # Insert categories
        category_map = {}
        for name in CATEGORIES:
            result = db.execute(
                text("INSERT INTO categories (name) VALUES (:name) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id, name"),
                {"name": name}
            ).fetchone()
            category_map[result.name] = result.id
        db.commit()
        print(f"✅ {len(CATEGORIES)} categories seeded")

        # Insert products
        inserted = 0
        for p in PRODUCTS:
            category_id = category_map[p["category"]]
            existing = db.execute(
                text("SELECT id FROM products WHERE title = :title"),
                {"title": p["title"]}
            ).fetchone()
            if existing:
                continue

            db.execute(
                text("""
                    INSERT INTO products
                      (title, description, price, discount_percentage, rating, stock, brand,
                       thumbnail, images, is_published, category_id)
                    VALUES
                      (:title, :description, :price, :discount_percentage, :rating, :stock, :brand,
                       :thumbnail, :images, true, :category_id)
                """),
                {
                    "title": p["title"],
                    "description": p["description"],
                    "price": p["price"],
                    "discount_percentage": p["discount_percentage"],
                    "rating": p["rating"],
                    "stock": p["stock"],
                    "brand": p["brand"],
                    "thumbnail": p["thumbnail"],
                    "images": "{" + ",".join(p["images"]) + "}",
                    "category_id": category_id,
                }
            )
            inserted += 1

        db.commit()
        print(f"✅ {inserted} products seeded ({len(PRODUCTS) - inserted} already existed)")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
