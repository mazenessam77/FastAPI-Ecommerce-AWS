from fastapi import APIRouter, Depends, Query, Header, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.services.orders import OrderService
from app.schemas.orders import CheckoutRequest, OrderResponse, OrdersListResponse
from app.core.config import settings

router = APIRouter(tags=["Orders"], prefix="/orders")
auth_scheme = HTTPBearer()


@router.post("/checkout", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return OrderService.checkout(token, db, request)


@router.get("/", status_code=status.HTTP_200_OK, response_model=OrdersListResponse)
def get_orders(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return OrderService.get_orders(token, db, page, limit)


@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    return OrderService.get_order(token, db, order_id)


# ── Seed endpoint ──────────────────────────────────────────────────────────────

CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden",
    "Sports & Outdoors", "Books", "Beauty & Health",
    "Toys & Games", "Automotive",
]

PRODUCTS = [
    # ── Electronics ──────────────────────────────────────────────────────────────
    {"title": "Wireless Noise-Cancelling Headphones", "description": "Premium over-ear headphones with active noise cancellation, 30-hour battery life, and foldable design.", "price": 299, "discount_percentage": 15.0, "rating": 4.7, "stock": 85, "brand": "SoundMax", "thumbnail": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800", "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=800"], "category": "Electronics"},
    {"title": "4K Smart TV 55-inch", "description": "Ultra HD 4K LED Smart TV with built-in streaming apps, HDR10+, and Dolby Vision.", "price": 649, "discount_percentage": 10.0, "rating": 4.5, "stock": 40, "brand": "ViewPro", "thumbnail": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400", "images": ["https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800"], "category": "Electronics"},
    {"title": "Mechanical Gaming Keyboard", "description": "RGB mechanical keyboard with Cherry MX switches, full N-key rollover, and aluminum frame.", "price": 129, "discount_percentage": 5.0, "rating": 4.6, "stock": 120, "brand": "KeyForce", "thumbnail": "https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=400", "images": ["https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=800"], "category": "Electronics"},
    {"title": "Smartphone 128GB", "description": "Flagship smartphone with 6.7-inch AMOLED display, triple-camera system, and 5G support.", "price": 899, "discount_percentage": 8.0, "rating": 4.8, "stock": 60, "brand": "PhoneTech", "thumbnail": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400", "images": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"], "category": "Electronics"},
    {"title": "Wireless Gaming Mouse", "description": "Ultra-lightweight 68g wireless gaming mouse with 25K DPI sensor, 70-hour battery, and 6 programmable buttons.", "price": 79, "discount_percentage": 10.0, "rating": 4.7, "stock": 140, "brand": "SwiftClick", "thumbnail": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400", "images": ["https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800"], "category": "Electronics"},
    {"title": "True Wireless Earbuds", "description": "Active noise-cancelling earbuds with 8-hour playtime, IPX5 water resistance, and 24-hour charging case.", "price": 149, "discount_percentage": 20.0, "rating": 4.6, "stock": 200, "brand": "SoundMax", "thumbnail": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400", "images": ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800"], "category": "Electronics"},
    {"title": "Laptop Stand Aluminium", "description": "Adjustable aluminium laptop stand, compatible with 11–17 inch laptops, foldable and portable.", "price": 45, "discount_percentage": 0.0, "rating": 4.5, "stock": 300, "brand": "DeskPro", "thumbnail": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400", "images": ["https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"], "category": "Electronics"},
    {"title": "Portable Bluetooth Speaker", "description": "360° surround sound speaker, 20W output, waterproof IPX7, 24-hour battery, and built-in microphone.", "price": 89, "discount_percentage": 12.0, "rating": 4.6, "stock": 175, "brand": "BoomBox", "thumbnail": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400", "images": ["https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800"], "category": "Electronics"},
    {"title": "Smartwatch Series X", "description": "Advanced smartwatch with health monitoring, GPS, AMOLED always-on display, and 7-day battery life.", "price": 249, "discount_percentage": 15.0, "rating": 4.7, "stock": 90, "brand": "TimeTech", "thumbnail": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800"], "category": "Electronics"},
    {"title": "USB-C Hub 7-in-1", "description": "Compact 7-in-1 hub with 4K HDMI, 100W PD charging, USB 3.0×3, SD card reader, and Ethernet port.", "price": 59, "discount_percentage": 0.0, "rating": 4.5, "stock": 260, "brand": "ConnectPro", "thumbnail": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400", "images": ["https://images.unsplash.com/photo-1625842268584-8f3296236761?w=800"], "category": "Electronics"},
    # ── Clothing ─────────────────────────────────────────────────────────────────
    {"title": "Classic Denim Jacket", "description": "Timeless denim jacket with a relaxed fit, two chest pockets, and button closure.", "price": 89, "discount_percentage": 20.0, "rating": 4.3, "stock": 200, "brand": "UrbanWear", "thumbnail": "https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=400", "images": ["https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=800"], "category": "Clothing"},
    {"title": "Running Sneakers", "description": "Lightweight running shoes with responsive cushioning, breathable mesh upper, and durable outsole.", "price": 110, "discount_percentage": 12.0, "rating": 4.5, "stock": 150, "brand": "SwiftStep", "thumbnail": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "images": ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800"], "category": "Clothing"},
    {"title": "Premium Cotton T-Shirt", "description": "100% organic cotton crew-neck tee, pre-shrunk, available in 12 colors, unisex fit.", "price": 29, "discount_percentage": 0.0, "rating": 4.4, "stock": 500, "brand": "PureCotton", "thumbnail": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400", "images": ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800"], "category": "Clothing"},
    {"title": "Slim Fit Chino Pants", "description": "Stretch-cotton slim-fit chinos with a modern tapered leg, wrinkle-resistant finish.", "price": 65, "discount_percentage": 10.0, "rating": 4.3, "stock": 180, "brand": "StyleCo", "thumbnail": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400", "images": ["https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=800"], "category": "Clothing"},
    {"title": "Leather Ankle Boots", "description": "Full-grain leather ankle boots with a chunky sole, side zipper, and cushioned insole.", "price": 159, "discount_percentage": 15.0, "rating": 4.6, "stock": 90, "brand": "LeatherCraft", "thumbnail": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=400", "images": ["https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=800"], "category": "Clothing"},
    {"title": "Hooded Zip-Up Sweatshirt", "description": "Heavyweight 380gsm fleece hoodie with a kangaroo pocket, ribbed cuffs, and double-lined hood.", "price": 75, "discount_percentage": 5.0, "rating": 4.5, "stock": 220, "brand": "UrbanWear", "thumbnail": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400", "images": ["https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=800"], "category": "Clothing"},
    # ── Home & Garden ─────────────────────────────────────────────────────────────
    {"title": "Ceramic Coffee Mug Set", "description": "Set of 4 handcrafted ceramic mugs, 12oz each, microwave and dishwasher safe.", "price": 35, "discount_percentage": 0.0, "rating": 4.4, "stock": 300, "brand": "HomeCraft", "thumbnail": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400", "images": ["https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=800"], "category": "Home & Garden"},
    {"title": "Bamboo Cutting Board Set", "description": "Set of 3 organic bamboo cutting boards in different sizes, with juice groove and hanging hole.", "price": 45, "discount_percentage": 10.0, "rating": 4.6, "stock": 180, "brand": "EcoKitchen", "thumbnail": "https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=400", "images": ["https://images.unsplash.com/photo-1588854337115-1c67d9247e4d?w=800"], "category": "Home & Garden"},
    {"title": "Scented Soy Candle Set", "description": "Set of 3 hand-poured soy wax candles in amber jars — vanilla, cedarwood, and lavender.", "price": 42, "discount_percentage": 0.0, "rating": 4.8, "stock": 350, "brand": "LumaBurn", "thumbnail": "https://images.unsplash.com/photo-1602178989027-fe9bc3a5f054?w=400", "images": ["https://images.unsplash.com/photo-1602178989027-fe9bc3a5f054?w=800"], "category": "Home & Garden"},
    {"title": "Indoor Plant Pot Set", "description": "Set of 5 minimalist matte ceramic plant pots with drainage holes and matching saucers.", "price": 38, "discount_percentage": 5.0, "rating": 4.5, "stock": 270, "brand": "GreenSpace", "thumbnail": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400", "images": ["https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=800"], "category": "Home & Garden"},
    {"title": "Electric Kettle 1.7L", "description": "Stainless steel electric kettle with temperature control, keep-warm function, and 360° base.", "price": 55, "discount_percentage": 8.0, "rating": 4.6, "stock": 200, "brand": "BrewMaster", "thumbnail": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400", "images": ["https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800"], "category": "Home & Garden"},
    {"title": "Blackout Curtains Pair", "description": "Thermal-insulated blackout curtains, 100% light blocking, energy-saving, noise-reducing.", "price": 49, "discount_percentage": 15.0, "rating": 4.4, "stock": 160, "brand": "DreamNight", "thumbnail": "https://images.unsplash.com/photo-1556909211-36987daf7b4d?w=400", "images": ["https://images.unsplash.com/photo-1556909211-36987daf7b4d?w=800"], "category": "Home & Garden"},
    # ── Sports & Outdoors ─────────────────────────────────────────────────────────
    {"title": "Yoga Mat Premium", "description": "Non-slip 6mm thick yoga mat with alignment lines, carrying strap, and eco-friendly TPE material.", "price": 55, "discount_percentage": 5.0, "rating": 4.7, "stock": 250, "brand": "FlexFit", "thumbnail": "https://images.unsplash.com/photo-1601925228269-e3a3b4cfb4f6?w=400", "images": ["https://images.unsplash.com/photo-1601925228269-e3a3b4cfb4f6?w=800"], "category": "Sports & Outdoors"},
    {"title": "Adjustable Dumbbell Set 40kg", "description": "Quick-adjust dumbbell set from 2.5kg to 40kg, replaces 15 sets of weights, compact storage.", "price": 349, "discount_percentage": 18.0, "rating": 4.8, "stock": 30, "brand": "IronCore", "thumbnail": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400", "images": ["https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800"], "category": "Sports & Outdoors"},
    {"title": "Resistance Bands Set (5 levels)", "description": "Set of 5 latex resistance bands from extra-light to extra-heavy, with carry bag and exercise guide.", "price": 25, "discount_percentage": 0.0, "rating": 4.6, "stock": 400, "brand": "FlexFit", "thumbnail": "https://images.unsplash.com/photo-1598971861713-54ad16a7e72e?w=400", "images": ["https://images.unsplash.com/photo-1598971861713-54ad16a7e72e?w=800"], "category": "Sports & Outdoors"},
    {"title": "Insulated Water Bottle 1L", "description": "Triple-wall vacuum-insulated stainless steel bottle keeps drinks cold 48h or hot 24h, leak-proof lid.", "price": 39, "discount_percentage": 0.0, "rating": 4.8, "stock": 450, "brand": "HydroFlow", "thumbnail": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400", "images": ["https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800"], "category": "Sports & Outdoors"},
    {"title": "Camping Backpack 60L", "description": "Waterproof 60L trekking backpack with ergonomic frame, hip belt, rain cover, and hydration sleeve.", "price": 149, "discount_percentage": 10.0, "rating": 4.7, "stock": 70, "brand": "TrailMaster", "thumbnail": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "images": ["https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800"], "category": "Sports & Outdoors"},
    {"title": "Jump Rope Speed Cable", "description": "Adjustable speed jump rope with steel cable, 360° spin bearings, and comfortable foam grips.", "price": 18, "discount_percentage": 0.0, "rating": 4.5, "stock": 600, "brand": "IronCore", "thumbnail": "https://images.unsplash.com/photo-1601233749202-95d04d5b3c00?w=400", "images": ["https://images.unsplash.com/photo-1601233749202-95d04d5b3c00?w=800"], "category": "Sports & Outdoors"},
    # ── Books ─────────────────────────────────────────────────────────────────────
    {"title": "Clean Code: A Handbook of Agile Software Craftsmanship", "description": "Robert C. Martin's classic guide to writing clean, readable, and maintainable code.", "price": 40, "discount_percentage": 0.0, "rating": 4.9, "stock": 500, "brand": "Prentice Hall", "thumbnail": "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400", "images": ["https://images.unsplash.com/photo-1589998059171-988d887df646?w=800"], "category": "Books"},
    {"title": "Atomic Habits", "description": "James Clear's proven framework for building good habits and breaking bad ones — a global bestseller.", "price": 18, "discount_percentage": 5.0, "rating": 4.9, "stock": 800, "brand": "Penguin Random House", "thumbnail": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400", "images": ["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800"], "category": "Books"},
    {"title": "The Design of Everyday Things", "description": "Don Norman's seminal exploration of human-centered design and why so many products frustrate us.", "price": 22, "discount_percentage": 0.0, "rating": 4.7, "stock": 350, "brand": "Basic Books", "thumbnail": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400", "images": ["https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800"], "category": "Books"},
    {"title": "Deep Work: Rules for Focused Success", "description": "Cal Newport's guide to cultivating focused work in a distracted world and achieving peak productivity.", "price": 17, "discount_percentage": 0.0, "rating": 4.8, "stock": 600, "brand": "Grand Central Publishing", "thumbnail": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400", "images": ["https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800"], "category": "Books"},
    # ── Beauty & Health ───────────────────────────────────────────────────────────
    {"title": "Vitamin C Serum 30ml", "description": "Brightening vitamin C serum with hyaluronic acid and niacinamide for glowing skin.", "price": 28, "discount_percentage": 0.0, "rating": 4.5, "stock": 400, "brand": "GlowLab", "thumbnail": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400", "images": ["https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800"], "category": "Beauty & Health"},
    {"title": "Retinol Night Cream 50ml", "description": "Anti-aging retinol night cream with peptides and ceramides — reduces fine lines and evens skin tone.", "price": 45, "discount_percentage": 10.0, "rating": 4.6, "stock": 320, "brand": "GlowLab", "thumbnail": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400", "images": ["https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800"], "category": "Beauty & Health"},
    {"title": "Electric Facial Cleanser", "description": "Sonic vibration facial cleansing brush with 3 modes, waterproof, and 30-day battery life.", "price": 59, "discount_percentage": 15.0, "rating": 4.5, "stock": 180, "brand": "SkinSonic", "thumbnail": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400", "images": ["https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800"], "category": "Beauty & Health"},
    {"title": "Hyaluronic Acid Moisturiser 50ml", "description": "Lightweight gel-cream moisturiser with 2% hyaluronic acid complex for all-day hydration.", "price": 32, "discount_percentage": 0.0, "rating": 4.7, "stock": 500, "brand": "AquaDerm", "thumbnail": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400", "images": ["https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800"], "category": "Beauty & Health"},
    {"title": "Natural Sunscreen SPF50", "description": "Mineral sunscreen with SPF50, zinc oxide formula, reef-safe, fragrance-free, for sensitive skin.", "price": 22, "discount_percentage": 0.0, "rating": 4.6, "stock": 450, "brand": "SunGuard", "thumbnail": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400", "images": ["https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=800"], "category": "Beauty & Health"},
    # ── Toys & Games ─────────────────────────────────────────────────────────────
    {"title": "Building Blocks Set 500pcs", "description": "Classic colorful building blocks compatible with major brands, 500 pieces, ages 4+.", "price": 49, "discount_percentage": 10.0, "rating": 4.6, "stock": 220, "brand": "BrickFun", "thumbnail": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400", "images": ["https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800"], "category": "Toys & Games"},
    {"title": "Strategy Board Game", "description": "Award-winning strategy board game for 2–4 players, ages 10+. Average play time 60–90 minutes.", "price": 39, "discount_percentage": 5.0, "rating": 4.7, "stock": 150, "brand": "PlayMind", "thumbnail": "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=400", "images": ["https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=800"], "category": "Toys & Games"},
    {"title": "Remote Control Racing Car", "description": "1:16 scale RC car with 2.4GHz control, 30km/h top speed, rechargeable battery, and all-terrain tires.", "price": 65, "discount_percentage": 0.0, "rating": 4.4, "stock": 130, "brand": "TurboKid", "thumbnail": "https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=400", "images": ["https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=800"], "category": "Toys & Games"},
    {"title": "Jigsaw Puzzle 1000pcs", "description": "High-quality 1000-piece panoramic jigsaw puzzle with vivid print and precise cut pieces.", "price": 22, "discount_percentage": 0.0, "rating": 4.5, "stock": 340, "brand": "PuzzleCo", "thumbnail": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400", "images": ["https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=800"], "category": "Toys & Games"},
    # ── Automotive ────────────────────────────────────────────────────────────────
    {"title": "Car Dashboard Camera 4K", "description": "Wide-angle 4K dash cam with night vision, loop recording, G-sensor, and Wi-Fi connectivity.", "price": 129, "discount_percentage": 7.0, "rating": 4.4, "stock": 95, "brand": "DriveSafe", "thumbnail": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400", "images": ["https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800"], "category": "Automotive"},
    {"title": "Car Phone Mount Magnetic", "description": "Strong magnetic dashboard phone mount with 360° rotation, compatible with all smartphones.", "price": 19, "discount_percentage": 0.0, "rating": 4.5, "stock": 500, "brand": "GripTech", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Automotive"},
    {"title": "Portable Tyre Inflator", "description": "Cordless digital tyre inflator with auto shut-off, LED light, and built-in battery for 6 car tyres.", "price": 55, "discount_percentage": 12.0, "rating": 4.6, "stock": 120, "brand": "AirMax", "thumbnail": "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400", "images": ["https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=800"], "category": "Automotive"},
    {"title": "Car Seat Organiser", "description": "Multi-pocket back-seat car organiser with tablet holder, foldable tray, and two insulated cup holders.", "price": 28, "discount_percentage": 5.0, "rating": 4.4, "stock": 280, "brand": "DriveSafe", "thumbnail": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=400", "images": ["https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=800"], "category": "Automotive"},
]


@router.get("/db/inspect", status_code=status.HTTP_200_OK, include_in_schema=False)
def inspect_db(
    x_seed_key: str = Header(alias="x-seed-key"),
    db: Session = Depends(get_db),
):
    if x_seed_key != settings.seed_secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid seed key")

    # All tables with row counts
    tables = db.execute(text("""
        SELECT
            t.table_name,
            (xpath('/row/cnt/text()',
                   query_to_xml(format('SELECT COUNT(*) AS cnt FROM %I', t.table_name), true, true, ''))
            )[1]::text::int AS row_count
        FROM information_schema.tables t
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name
    """)).fetchall()

    # Column definitions per table
    columns = db.execute(text("""
        SELECT
            c.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default
        FROM information_schema.columns c
        WHERE c.table_schema = 'public'
        ORDER BY c.table_name, c.ordinal_position
    """)).fetchall()

    schema: dict = {}
    for col in columns:
        schema.setdefault(col.table_name, []).append({
            "column": col.column_name,
            "type": col.data_type,
            "nullable": col.is_nullable,
            "default": col.column_default,
        })

    return {
        "tables": [
            {"table": row.table_name, "rows": row.row_count, "columns": schema.get(row.table_name, [])}
            for row in tables
        ]
    }


@router.post("/seed", status_code=status.HTTP_200_OK, include_in_schema=False)
def seed_data(
    x_seed_key: str = Header(alias="x-seed-key"),
    db: Session = Depends(get_db),
):
    if x_seed_key != settings.seed_secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid seed key")

    # Seed categories
    category_map: dict[str, int] = {}
    for name in CATEGORIES:
        row = db.execute(
            text("INSERT INTO categories (name) VALUES (:name) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING id, name"),
            {"name": name},
        ).fetchone()
        category_map[row.name] = row.id
    db.commit()

    # Seed products
    inserted = 0
    for p in PRODUCTS:
        existing = db.execute(
            text("SELECT id FROM products WHERE title = :title"),
            {"title": p["title"]},
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
                "category_id": category_map[p["category"]],
            },
        )
        inserted += 1
    db.commit()

    return {
        "message": f"Seeded {len(CATEGORIES)} categories and {inserted} products ({len(PRODUCTS) - inserted} already existed)"
    }
