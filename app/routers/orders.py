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
    "Office Supplies", "Pet Supplies", "Food & Beverages", "Music & Instruments",
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
    # ── Electronics (extra) ───────────────────────────────────────────────────────
    {"title": "Gaming Headset 7.1 Surround", "description": "Wired 7.1 surround sound gaming headset with noise-cancelling mic, LED lighting, and memory foam earcups.", "price": 69, "discount_percentage": 10.0, "rating": 4.5, "stock": 160, "brand": "SoundMax", "thumbnail": "https://images.unsplash.com/photo-1612536057832-2ff7ead58194?w=400", "images": ["https://images.unsplash.com/photo-1612536057832-2ff7ead58194?w=800"], "category": "Electronics"},
    {"title": "Wireless Charging Pad 15W", "description": "Fast-charge 15W Qi wireless charging pad compatible with all Qi-enabled devices, LED indicator, anti-slip base.", "price": 29, "discount_percentage": 0.0, "rating": 4.4, "stock": 400, "brand": "ChargeFast", "thumbnail": "https://images.unsplash.com/photo-1600490036275-29411738d8e4?w=400", "images": ["https://images.unsplash.com/photo-1600490036275-29411738d8e4?w=800"], "category": "Electronics"},
    {"title": "Action Camera 4K", "description": "Waterproof 4K action camera with image stabilization, wide-angle lens, touchscreen, and 2-hour battery.", "price": 199, "discount_percentage": 12.0, "rating": 4.6, "stock": 75, "brand": "ActionPro", "thumbnail": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400", "images": ["https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800"], "category": "Electronics"},
    {"title": "Portable SSD 1TB", "description": "Ultra-fast portable SSD with 1050MB/s read speeds, USB-C, shock-resistant, and compact pocket-size design.", "price": 89, "discount_percentage": 8.0, "rating": 4.8, "stock": 200, "brand": "StorePro", "thumbnail": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400", "images": ["https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800"], "category": "Electronics"},
    {"title": "Smart Home Hub", "description": "Central smart home controller compatible with Alexa, Google Home, Zigbee, and Z-Wave devices.", "price": 129, "discount_percentage": 15.0, "rating": 4.4, "stock": 110, "brand": "SmartNest", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Electronics"},
    {"title": "Monitor 27-inch 144Hz", "description": "27-inch QHD IPS gaming monitor, 144Hz refresh rate, 1ms response time, AMD FreeSync Premium, HDR400.", "price": 329, "discount_percentage": 10.0, "rating": 4.7, "stock": 55, "brand": "ViewPro", "thumbnail": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400", "images": ["https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800"], "category": "Electronics"},
    # ── Clothing (extra) ──────────────────────────────────────────────────────────
    {"title": "Merino Wool Sweater", "description": "100% extra-fine merino wool crew neck sweater, itch-free, temperature-regulating, available in 8 colors.", "price": 119, "discount_percentage": 0.0, "rating": 4.7, "stock": 130, "brand": "WoolCraft", "thumbnail": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400", "images": ["https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800"], "category": "Clothing"},
    {"title": "Waterproof Hiking Jacket", "description": "3-layer Gore-Tex waterproof jacket with sealed seams, pit zips, and helmet-compatible hood.", "price": 189, "discount_percentage": 15.0, "rating": 4.8, "stock": 80, "brand": "TrailMaster", "thumbnail": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400", "images": ["https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800"], "category": "Clothing"},
    {"title": "Linen Dress Shirt", "description": "Relaxed-fit 100% linen dress shirt, breathable and lightweight, perfect for warm weather.", "price": 55, "discount_percentage": 5.0, "rating": 4.4, "stock": 210, "brand": "StyleCo", "thumbnail": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=400", "images": ["https://images.unsplash.com/photo-1603252109303-2751441dd157?w=800"], "category": "Clothing"},
    {"title": "High-Waist Yoga Leggings", "description": "Buttery-soft high-waist leggings with squat-proof fabric, 4-way stretch, and side pocket.", "price": 49, "discount_percentage": 0.0, "rating": 4.6, "stock": 320, "brand": "FlexFit", "thumbnail": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400", "images": ["https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800"], "category": "Clothing"},
    # ── Home & Garden (extra) ─────────────────────────────────────────────────────
    {"title": "Air Purifier HEPA H13", "description": "True HEPA H13 air purifier covers 400 sq ft, removes 99.97% of particles, ultra-quiet sleep mode.", "price": 149, "discount_percentage": 10.0, "rating": 4.7, "stock": 90, "brand": "CleanAir", "thumbnail": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400", "images": ["https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800"], "category": "Home & Garden"},
    {"title": "Robot Vacuum Cleaner", "description": "Smart robot vacuum with LiDAR mapping, 4000Pa suction, auto-empty base, and app control.", "price": 399, "discount_percentage": 20.0, "rating": 4.6, "stock": 45, "brand": "CleanBot", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Home & Garden"},
    {"title": "Wooden Desk Lamp LED", "description": "Minimalist wood-and-metal LED desk lamp with 5 color temperatures, 10 brightness levels, and USB-A charging port.", "price": 65, "discount_percentage": 0.0, "rating": 4.5, "stock": 190, "brand": "LumaBurn", "thumbnail": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400", "images": ["https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800"], "category": "Home & Garden"},
    {"title": "Non-Stick Cookware Set 7pc", "description": "7-piece granite-coated non-stick cookware set, PFOA-free, oven-safe to 450°F, glass lids included.", "price": 89, "discount_percentage": 15.0, "rating": 4.6, "stock": 140, "brand": "EcoKitchen", "thumbnail": "https://images.unsplash.com/photo-1584990347449-39e8f16cc0dc?w=400", "images": ["https://images.unsplash.com/photo-1584990347449-39e8f16cc0dc?w=800"], "category": "Home & Garden"},
    {"title": "Memory Foam Pillow", "description": "Cervical contour memory foam pillow with cooling gel layer and washable bamboo cover.", "price": 45, "discount_percentage": 0.0, "rating": 4.5, "stock": 280, "brand": "DreamNight", "thumbnail": "https://images.unsplash.com/photo-1631048501851-8f64da3a4f40?w=400", "images": ["https://images.unsplash.com/photo-1631048501851-8f64da3a4f40?w=800"], "category": "Home & Garden"},
    # ── Sports & Outdoors (extra) ─────────────────────────────────────────────────
    {"title": "Pull-Up Bar Doorframe", "description": "No-screw doorframe pull-up bar, holds up to 150kg, multi-grip positions for pull-ups, chin-ups, sit-ups.", "price": 35, "discount_percentage": 0.0, "rating": 4.5, "stock": 380, "brand": "IronCore", "thumbnail": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=400", "images": ["https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=800"], "category": "Sports & Outdoors"},
    {"title": "Foam Roller Deep Tissue", "description": "High-density EVA foam roller for deep tissue massage, muscle recovery, and myofascial release — 60cm.", "price": 28, "discount_percentage": 0.0, "rating": 4.6, "stock": 420, "brand": "FlexFit", "thumbnail": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=400", "images": ["https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?w=800"], "category": "Sports & Outdoors"},
    {"title": "Hiking Boots Waterproof", "description": "Mid-cut waterproof leather hiking boots with Vibram outsole and ankle support.", "price": 145, "discount_percentage": 10.0, "rating": 4.7, "stock": 95, "brand": "TrailMaster", "thumbnail": "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=400", "images": ["https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=800"], "category": "Sports & Outdoors"},
    {"title": "Sleeping Bag -10°C", "description": "Mummy-style sleeping bag rated to -10°C, 800-fill duck down, packable to 4L, with compression sack.", "price": 119, "discount_percentage": 8.0, "rating": 4.7, "stock": 65, "brand": "TrailMaster", "thumbnail": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400", "images": ["https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800"], "category": "Sports & Outdoors"},
    # ── Books (extra) ─────────────────────────────────────────────────────────────
    {"title": "The Pragmatic Programmer", "description": "Hunt & Thomas's timeless guide to software craftsmanship — updated 20th anniversary edition.", "price": 45, "discount_percentage": 0.0, "rating": 4.8, "stock": 400, "brand": "Addison-Wesley", "thumbnail": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400", "images": ["https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800"], "category": "Books"},
    {"title": "Psychology of Money", "description": "Morgan Housel's exploration of how people think about money and the role of emotions in financial decisions.", "price": 16, "discount_percentage": 5.0, "rating": 4.8, "stock": 700, "brand": "Harriman House", "thumbnail": "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400", "images": ["https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800"], "category": "Books"},
    {"title": "Sapiens: A Brief History of Humankind", "description": "Yuval Noah Harari's sweeping narrative of how Homo sapiens came to dominate Earth.", "price": 18, "discount_percentage": 0.0, "rating": 4.7, "stock": 600, "brand": "Harper Perennial", "thumbnail": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=400", "images": ["https://images.unsplash.com/photo-1476275466078-4007374efbbe?w=800"], "category": "Books"},
    # ── Beauty & Health (extra) ───────────────────────────────────────────────────
    {"title": "Electric Toothbrush Sonic", "description": "Sonic electric toothbrush with 5 modes, 40,000 strokes/min, pressure sensor, and 30-day battery.", "price": 49, "discount_percentage": 10.0, "rating": 4.7, "stock": 250, "brand": "SkinSonic", "thumbnail": "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=400", "images": ["https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=800"], "category": "Beauty & Health"},
    {"title": "Collagen Peptides Powder 300g", "description": "Grass-fed hydrolysed collagen peptides, unflavoured, mixes instantly in hot or cold drinks.", "price": 34, "discount_percentage": 0.0, "rating": 4.6, "stock": 380, "brand": "VitaBoost", "thumbnail": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400", "images": ["https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800"], "category": "Beauty & Health"},
    {"title": "Jade Facial Roller & Gua Sha Set", "description": "Natural jade facial roller and gua sha stone set for lymphatic drainage, depuffing, and skin glow.", "price": 22, "discount_percentage": 0.0, "rating": 4.5, "stock": 450, "brand": "GlowLab", "thumbnail": "https://images.unsplash.com/photo-1556228841-a3c527ebefe5?w=400", "images": ["https://images.unsplash.com/photo-1556228841-a3c527ebefe5?w=800"], "category": "Beauty & Health"},
    {"title": "Vitamin D3+K2 Supplement", "description": "High-strength Vitamin D3 5000IU + K2 200mcg supplement, 365 softgels for 12-month supply.", "price": 19, "discount_percentage": 0.0, "rating": 4.7, "stock": 600, "brand": "VitaBoost", "thumbnail": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400", "images": ["https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800"], "category": "Beauty & Health"},
    # ── Toys & Games (extra) ──────────────────────────────────────────────────────
    {"title": "STEM Robot Building Kit", "description": "Educational robotics kit for ages 8+, program with Scratch or Python, includes sensors and servo motors.", "price": 79, "discount_percentage": 0.0, "rating": 4.7, "stock": 120, "brand": "BrickFun", "thumbnail": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400", "images": ["https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800"], "category": "Toys & Games"},
    {"title": "Card Game: Party Edition", "description": "Hilarious party card game for 4–10 players, ages 17+, with 600 cards and endless replayability.", "price": 25, "discount_percentage": 0.0, "rating": 4.8, "stock": 300, "brand": "PlayMind", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Toys & Games"},
    {"title": "Drone with Camera HD", "description": "Foldable mini drone with 1080p camera, 20-min flight time, altitude hold, headless mode, and carry bag.", "price": 89, "discount_percentage": 15.0, "rating": 4.4, "stock": 85, "brand": "TurboKid", "thumbnail": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400", "images": ["https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800"], "category": "Toys & Games"},
    # ── Office Supplies ───────────────────────────────────────────────────────────
    {"title": "Ergonomic Office Chair", "description": "Mesh-back ergonomic office chair with lumbar support, adjustable armrests, headrest, and 4D tilt mechanism.", "price": 299, "discount_percentage": 20.0, "rating": 4.6, "stock": 50, "brand": "DeskPro", "thumbnail": "https://images.unsplash.com/photo-1505843513577-22bb7d21e455?w=400", "images": ["https://images.unsplash.com/photo-1505843513577-22bb7d21e455?w=800"], "category": "Office Supplies"},
    {"title": "Standing Desk Converter", "description": "Height-adjustable desk converter (35–50cm lift range), fits monitors up to 32 inches, gas-spring lift.", "price": 149, "discount_percentage": 10.0, "rating": 4.5, "stock": 70, "brand": "DeskPro", "thumbnail": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400", "images": ["https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800"], "category": "Office Supplies"},
    {"title": "Desk Organiser Set", "description": "5-piece bamboo desk organiser set with pen holder, paper tray, phone stand, and two small trays.", "price": 38, "discount_percentage": 0.0, "rating": 4.5, "stock": 240, "brand": "HomeCraft", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Office Supplies"},
    {"title": "Wireless Keyboard & Mouse Combo", "description": "Slim wireless keyboard and mouse combo, 2.4GHz with single USB receiver, quiet keys, and 2-year battery.", "price": 49, "discount_percentage": 5.0, "rating": 4.4, "stock": 310, "brand": "KeyForce", "thumbnail": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400", "images": ["https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800"], "category": "Office Supplies"},
    {"title": "A4 Laser Printer", "description": "Monochrome laser printer, 34ppm, 1200dpi, Wi-Fi, duplex printing, and 250-sheet input tray.", "price": 179, "discount_percentage": 8.0, "rating": 4.5, "stock": 60, "brand": "PrintMaster", "thumbnail": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400", "images": ["https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800"], "category": "Office Supplies"},
    # ── Pet Supplies ──────────────────────────────────────────────────────────────
    {"title": "Automatic Pet Feeder 6L", "description": "Programmable automatic pet feeder with 6L capacity, portion control, timed scheduling, and voice recorder.", "price": 59, "discount_percentage": 10.0, "rating": 4.5, "stock": 140, "brand": "PetCare", "thumbnail": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400", "images": ["https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=800"], "category": "Pet Supplies"},
    {"title": "Pet Grooming Kit", "description": "5-in-1 cordless pet grooming kit with trimmer, nail grinder, deshedding tool, and comb attachments.", "price": 45, "discount_percentage": 0.0, "rating": 4.6, "stock": 200, "brand": "PetCare", "thumbnail": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=400", "images": ["https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800"], "category": "Pet Supplies"},
    {"title": "Orthopedic Dog Bed Large", "description": "Memory foam orthopedic dog bed with waterproof liner and machine-washable cover, 90×70cm.", "price": 69, "discount_percentage": 5.0, "rating": 4.7, "stock": 110, "brand": "PetCare", "thumbnail": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400", "images": ["https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800"], "category": "Pet Supplies"},
    {"title": "Interactive Cat Toy Set", "description": "Set of 5 electronic interactive cat toys including feather wand, laser, and motorised ball.", "price": 28, "discount_percentage": 0.0, "rating": 4.5, "stock": 350, "brand": "PetCare", "thumbnail": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400", "images": ["https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800"], "category": "Pet Supplies"},
    # ── Food & Beverages ──────────────────────────────────────────────────────────
    {"title": "Specialty Coffee Beans 1kg", "description": "Single-origin Ethiopian Yirgacheffe whole-bean coffee, light roast, with tasting notes of blueberry and jasmine.", "price": 28, "discount_percentage": 0.0, "rating": 4.8, "stock": 500, "brand": "BrewMaster", "thumbnail": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400", "images": ["https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800"], "category": "Food & Beverages"},
    {"title": "Premium Matcha Powder 100g", "description": "Ceremonial-grade Japanese matcha powder from Uji, Kyoto — vibrant green colour, smooth umami taste.", "price": 32, "discount_percentage": 0.0, "rating": 4.7, "stock": 350, "brand": "TeaCraft", "thumbnail": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400", "images": ["https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=800"], "category": "Food & Beverages"},
    {"title": "Raw Honey 500g", "description": "Cold-extracted wildflower raw honey, unfiltered, packed with natural enzymes and antioxidants.", "price": 18, "discount_percentage": 0.0, "rating": 4.9, "stock": 600, "brand": "NatureFarm", "thumbnail": "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=400", "images": ["https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800"], "category": "Food & Beverages"},
    {"title": "Protein Bar Box (24 bars)", "description": "Box of 24 high-protein bars, 20g protein each, low sugar, gluten-free, available in chocolate and peanut butter.", "price": 36, "discount_percentage": 10.0, "rating": 4.6, "stock": 450, "brand": "VitaBoost", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Food & Beverages"},
    # ── Music & Instruments ───────────────────────────────────────────────────────
    {"title": "Acoustic Guitar Beginner Set", "description": "Full-size spruce-top acoustic guitar bundle with gig bag, tuner, picks, strap, and extra strings.", "price": 129, "discount_percentage": 10.0, "rating": 4.5, "stock": 80, "brand": "MelodyPro", "thumbnail": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400", "images": ["https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800"], "category": "Music & Instruments"},
    {"title": "MIDI Keyboard 25-Key", "description": "Compact 25-key USB MIDI keyboard controller with velocity-sensitive keys, 8 drum pads, and arpeggiator.", "price": 79, "discount_percentage": 5.0, "rating": 4.5, "stock": 120, "brand": "MelodyPro", "thumbnail": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=400", "images": ["https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=800"], "category": "Music & Instruments"},
    {"title": "Ukulele Soprano Bundle", "description": "Soprano ukulele with mahogany body, aquila strings, gig bag, tuner, and chord chart — great for beginners.", "price": 59, "discount_percentage": 0.0, "rating": 4.6, "stock": 160, "brand": "MelodyPro", "thumbnail": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", "images": ["https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"], "category": "Music & Instruments"},
    {"title": "Studio Monitor Headphones", "description": "Professional closed-back studio headphones with 40mm drivers, flat frequency response, and coiled cable.", "price": 99, "discount_percentage": 0.0, "rating": 4.7, "stock": 140, "brand": "SoundMax", "thumbnail": "https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=400", "images": ["https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=800"], "category": "Music & Instruments"},
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
