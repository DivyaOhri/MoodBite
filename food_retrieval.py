"""
Person 3: Vector DB + Food Retrieval — COMPLETE REAL LOCAL DATA
Smart Food Recommender — Emotion-Aware Analysis
CSU2217 | Yogananda School of AI, Shoolini University

COMPLETE real menu data from ALL 16 restaurants near Shoolini University, Solan.

HOW TO RUN:
    pip install chromadb sentence-transformers
    python person3_food_retrieval.py

HOW OTHER PERSONS CALL THIS:
    from person3_food_retrieval import build_database, search_foods
    build_database()
    results = search_foods(food_intent=["comfort","warm","light"], budget=150)
"""

import chromadb
from sentence_transformers import SentenceTransformer

# ═══════════════════════════════════════════════════════════
# RESTAURANT REGISTRY — 16 real places near Shoolini
# ═══════════════════════════════════════════════════════════
RESTAURANTS = {
    "Desi Urban Cafe":        {"location":"On-campus, Shoolini University",      "distance_km":0.0, "timing":"All day",               "delivery":False},
    "Wok N Roll Cafe":        {"location":"On-campus, Shoolini University",      "distance_km":0.0, "timing":"All day (dinner tiffin)","delivery":False},
    "Nescafe":                {"location":"On-campus, Shoolini University",      "distance_km":0.1, "timing":"All day",               "delivery":False},
    "Chaudhary Juice Corner": {"location":"Near main gate, Shoolini",            "distance_km":0.2, "timing":"Daytime",               "delivery":False},
    "Zaika Restaurant":       {"location":"Near Dream Villa, Shoolini, Solan",   "distance_km":0.3, "timing":"All day",               "delivery":False},
    "Friends Corner":         {"location":"Near Shoolini campus, Solan",         "distance_km":0.4, "timing":"9AM–9PM",               "delivery":False},
    "Chai Vyanjan":           {"location":"Near Shoolini campus, Solan",         "distance_km":0.5, "timing":"All day",               "delivery":True },
    "Laziz Pizza":            {"location":"Shoolini University Bajhol",          "distance_km":0.5, "timing":"All day",               "delivery":True },
    "Food Point":             {"location":"Near Shoolini campus, Solan",         "distance_km":0.5, "timing":"All day",               "delivery":False},
    "Yellow Chilly":          {"location":"Near Shoolini campus, Solan",         "distance_km":0.6, "timing":"All day",               "delivery":False},
    "Laxmi Bakers":           {"location":"Near Shoolini campus, Solan",         "distance_km":0.6, "timing":"All day",               "delivery":False},
    "Aru's Cafe":             {"location":"Walking distance, Shoolini area",     "distance_km":0.7, "timing":"All day",               "delivery":False},
    "Cheers to Chai":         {"location":"Near Shoolini campus, Solan",         "distance_km":0.7, "timing":"All day",               "delivery":False},
    "Mishti":                 {"location":"Near Shoolini campus, Solan",         "distance_km":0.8, "timing":"All day",               "delivery":False},
    "Kiyansh Cafe":           {"location":"Near Shoolini campus, Solan",         "distance_km":0.8, "timing":"All day",               "delivery":True },
    "Wonder Hills Cafe":      {"location":"Near Shoolini campus, Solan",         "distance_km":0.9, "timing":"All day",               "delivery":False},
    "Alpine Espresso":        {"location":"Near Shoolini campus, Solan",         "distance_km":1.0, "timing":"All day",               "delivery":False},
    "Pizza Town":             {"location":"Near Shoolini campus, Solan",         "distance_km":1.0, "timing":"All day (delivery till 11PM)","delivery":True},
    "Domino's":               {"location":"Near Shoolini campus, Solan",         "distance_km":1.2, "timing":"11AM–11PM",             "delivery":True },
}

# ═══════════════════════════════════════════════════════════
# COMPLETE FOOD DATASET — All 16 restaurants, real items
# Tags map emotions→food:
#   comfort, warm, light, heavy, quick, easy, healthy, fun,
#   indulgent, spicy, soothing, energy, fresh, filling,
#   sweet, morning, protein, crispy, creamy, cooling
# ═══════════════════════════════════════════════════════════
foods = [

    # ── NESCAFE (on-campus, cheapest hot drinks on campus) ──────────
    {"name":"Nescafe Regular",        "place":"Nescafe","price":25, "tags":["energy","warm","quick","comfort"],       "category":"Hot Coffee"},
    {"name":"Cappuccino NC",          "place":"Nescafe","price":35, "tags":["energy","warm","creamy","comfort"],      "category":"Hot Coffee"},
    {"name":"Cafe Mocha NC",          "place":"Nescafe","price":30, "tags":["comfort","sweet","warm","indulgent"],    "category":"Hot Coffee"},
    {"name":"Cafe Latte NC",          "place":"Nescafe","price":30, "tags":["comfort","creamy","warm","easy"],        "category":"Hot Coffee"},
    {"name":"Hot Chocolate NC",       "place":"Nescafe","price":25, "tags":["comfort","sweet","warm","soothing"],     "category":"Hot Coffee"},
    {"name":"Espresso NC",            "place":"Nescafe","price":20, "tags":["energy","strong","quick","warm"],        "category":"Hot Coffee"},
    {"name":"Nestea Masala Tea",      "place":"Nescafe","price":20, "tags":["comfort","warm","spicy","soothing"],     "category":"Tea"},
    {"name":"Nestea Cardamom Tea",    "place":"Nescafe","price":15, "tags":["comfort","warm","soothing","light"],     "category":"Tea"},
    {"name":"Hot Lemon Tea NC",       "place":"Nescafe","price":20, "tags":["soothing","light","warm","healthy"],     "category":"Tea"},
    {"name":"Nestea Tea Bag",         "place":"Nescafe","price":10, "tags":["light","warm","quick","soothing"],       "category":"Tea"},
    {"name":"Nescafe Ice",            "place":"Nescafe","price":50, "tags":["energy","refreshing","cold","quick"],    "category":"Cold Coffee"},
    {"name":"Frappe Hazelnut",        "place":"Nescafe","price":60, "tags":["energy","sweet","refreshing","fun"],     "category":"Cold Coffee"},
    {"name":"Frappe Caramel",         "place":"Nescafe","price":60, "tags":["energy","sweet","refreshing","fun"],     "category":"Cold Coffee"},
    {"name":"Lemon Ice Tea NC",       "place":"Nescafe","price":40, "tags":["refreshing","light","cooling","quick"],  "category":"Cold Refreshers"},
    {"name":"Cold Chocolate NC",      "place":"Nescafe","price":50, "tags":["sweet","comfort","refreshing","fun"],    "category":"Cold Refreshers"},
    {"name":"Veg Grill Sandwich NC",  "place":"Nescafe","price":40, "tags":["quick","light","easy","comfort"],        "category":"Bakery"},
    {"name":"Veg Burger NC",          "place":"Nescafe","price":50, "tags":["quick","comfort","light","easy"],        "category":"Bakery"},
    {"name":"Cheese Burger NC",       "place":"Nescafe","price":60, "tags":["fun","cheesy","filling","quick"],        "category":"Bakery"},
    {"name":"Paneer Burger NC",       "place":"Nescafe","price":70, "tags":["fun","filling","comfort","quick"],       "category":"Bakery"},
    {"name":"White Sauce Pasta NC",   "place":"Nescafe","price":60, "tags":["comfort","creamy","filling","warm"],     "category":"Bakery"},
    {"name":"French Fries Masala NC", "place":"Nescafe","price":50, "tags":["spicy","snack","quick","fun"],           "category":"Bakery"},
    {"name":"Paneer Kulcha NC",       "place":"Nescafe","price":50, "tags":["comfort","warm","filling","quick"],      "category":"Bakery"},

    # ── DESI URBAN CAFE (on-campus) ─────────────────────────────────
    {"name":"Aloo Tikki Burger DUC",  "place":"Desi Urban Cafe","price":40,  "tags":["quick","light","snack","comfort"],      "category":"Burger"},
    {"name":"Veg Burger DUC",         "place":"Desi Urban Cafe","price":50,  "tags":["quick","filling","comfort","easy"],     "category":"Burger"},
    {"name":"Cheese Burger DUC",      "place":"Desi Urban Cafe","price":70,  "tags":["fun","cheesy","indulgent","filling"],   "category":"Burger"},
    {"name":"Paneer Burger DUC",      "place":"Desi Urban Cafe","price":80,  "tags":["fun","filling","cheesy","comfort"],     "category":"Burger"},
    {"name":"Maharaja Burger DUC",    "place":"Desi Urban Cafe","price":120, "tags":["heavy","indulgent","filling","fun"],    "category":"Burger"},
    {"name":"Butter Bread Toast DUC", "place":"Desi Urban Cafe","price":50,  "tags":["light","quick","easy","morning"],       "category":"Sandwich"},
    {"name":"Cheese Corn Sandwich",   "place":"Desi Urban Cafe","price":90,  "tags":["comfort","cheesy","filling","quick"],   "category":"Sandwich"},
    {"name":"Pizza S/W DUC",          "place":"Desi Urban Cafe","price":130, "tags":["fun","cheesy","filling","comfort"],     "category":"Sandwich"},
    {"name":"Red Sauce Pasta DUC",    "place":"Desi Urban Cafe","price":90,  "tags":["comfort","filling","tangy","warm"],     "category":"Pasta"},
    {"name":"White Sauce Pasta DUC",  "place":"Desi Urban Cafe","price":110, "tags":["comfort","creamy","filling","warm"],    "category":"Pasta"},
    {"name":"Makhani Pasta DUC",      "place":"Desi Urban Cafe","price":150, "tags":["rich","comfort","warm","indulgent"],    "category":"Pasta"},
    {"name":"Cheese Onion Pizza S",   "place":"Desi Urban Cafe","price":100, "tags":["fun","cheesy","light","quick"],         "category":"Pizza"},
    {"name":"Cheese Paneer Pizza M",  "place":"Desi Urban Cafe","price":210, "tags":["fun","cheesy","heavy","indulgent"],     "category":"Pizza"},
    {"name":"Farm Fresh Pizza S",     "place":"Desi Urban Cafe","price":190, "tags":["fun","fresh","cheesy","heavy"],         "category":"Special Pizza"},
    {"name":"Tandoori Paneer Pizza S","place":"Desi Urban Cafe","price":190, "tags":["spicy","fun","heavy","indulgent"],      "category":"Special Pizza"},
    {"name":"Zingy Parcel DUC",       "place":"Desi Urban Cafe","price":50,  "tags":["quick","spicy","snack","light"],        "category":"Snack"},
    {"name":"Plain Garlic Bread DUC", "place":"Desi Urban Cafe","price":100, "tags":["comfort","quick","warm","snack"],       "category":"Snack"},
    {"name":"Calzone Pocket DUC",     "place":"Desi Urban Cafe","price":140, "tags":["filling","cheesy","fun","indulgent"],   "category":"Snack"},
    {"name":"Veg Noodle DUC",         "place":"Desi Urban Cafe","price":80,  "tags":["quick","light","comfort","easy"],       "category":"Chinese"},
    {"name":"Hakka Noodle DUC",       "place":"Desi Urban Cafe","price":120, "tags":["fun","spicy","filling","comfort"],      "category":"Chinese"},
    {"name":"Veg Momos DUC",          "place":"Desi Urban Cafe","price":80,  "tags":["comfort","warm","light","quick"],       "category":"Chinese"},
    {"name":"Paneer Momos DUC",       "place":"Desi Urban Cafe","price":120, "tags":["comfort","warm","filling","fun"],       "category":"Chinese"},
    {"name":"Chilli Potato DUC",      "place":"Desi Urban Cafe","price":100, "tags":["spicy","fun","snack","indulgent"],      "category":"Chinese"},
    {"name":"Veg Manchurian DUC",     "place":"Desi Urban Cafe","price":110, "tags":["spicy","fun","comfort","heavy"],        "category":"Chinese"},
    {"name":"Chilli Paneer DUC",      "place":"Desi Urban Cafe","price":170, "tags":["spicy","fun","heavy","indulgent"],      "category":"Chinese"},
    {"name":"Sweet Lassi DUC",        "place":"Desi Urban Cafe","price":50,  "tags":["soothing","light","refreshing","sweet"],"category":"Lassi"},
    {"name":"Mango Lassi DUC",        "place":"Desi Urban Cafe","price":60,  "tags":["refreshing","sweet","light","energy"],  "category":"Lassi"},
    {"name":"Fresh Lime Soda DUC",    "place":"Desi Urban Cafe","price":50,  "tags":["refreshing","light","quick","energy"],  "category":"Mocktail"},
    {"name":"Mango Shake DUC",        "place":"Desi Urban Cafe","price":80,  "tags":["sweet","energy","refreshing","fun"],    "category":"Shake"},
    {"name":"Cold Coffee DUC",        "place":"Desi Urban Cafe","price":90,  "tags":["energy","refreshing","fun","quick"],    "category":"Shake"},
    {"name":"Chaat Pav Bhaji DUC",    "place":"Desi Urban Cafe","price":80,  "tags":["comfort","spicy","filling","fun"],      "category":"Chaat"},
    {"name":"Aloo Paratha DUC",       "place":"Desi Urban Cafe","price":40,  "tags":["comfort","warm","filling","morning"],   "category":"Paratha"},
    {"name":"Paneer Paratha DUC",     "place":"Desi Urban Cafe","price":60,  "tags":["comfort","warm","filling","protein"],   "category":"Paratha"},
    {"name":"Plain Dosa DUC",         "place":"Desi Urban Cafe","price":70,  "tags":["light","crispy","quick","healthy"],     "category":"South Indian"},
    {"name":"Masala Dosa DUC",        "place":"Desi Urban Cafe","price":90,  "tags":["comfort","filling","crispy","warm"],    "category":"South Indian"},
    {"name":"Rajma Chawal DUC",       "place":"Desi Urban Cafe","price":50,  "tags":["comfort","filling","warm","protein"],   "category":"Rice"},
    {"name":"Masala Chai DUC",        "place":"Desi Urban Cafe","price":30,  "tags":["comfort","warm","quick","soothing"],    "category":"Chai"},
    {"name":"Veg Thali DUC",          "place":"Desi Urban Cafe","price":80,  "tags":["filling","comfort","warm","value"],     "category":"Thali"},
    {"name":"Veg Supreme Thali DUC",  "place":"Desi Urban Cafe","price":120, "tags":["filling","rich","complete","value"],    "category":"Thali"},

    # ── WOK N ROLL CAFE (on-campus) ─────────────────────────────────
    {"name":"Lacha Parantha WNR",     "place":"Wok N Roll Cafe","price":30,  "tags":["comfort","warm","light","morning"],     "category":"Breakfast"},
    {"name":"Aloo Pyaj Parantha WNR", "place":"Wok N Roll Cafe","price":40,  "tags":["comfort","warm","filling","morning"],   "category":"Breakfast"},
    {"name":"Gobhi Parantha WNR",     "place":"Wok N Roll Cafe","price":50,  "tags":["comfort","warm","filling","morning"],   "category":"Breakfast"},
    {"name":"Paneer Parantha WNR",    "place":"Wok N Roll Cafe","price":80,  "tags":["comfort","filling","warm","protein"],   "category":"Breakfast"},
    {"name":"Poha WNR",               "place":"Wok N Roll Cafe","price":80,  "tags":["light","easy","comfort","morning"],     "category":"Breakfast"},
    {"name":"Hot Coffee WNR",         "place":"Wok N Roll Cafe","price":30,  "tags":["energy","warm","quick","comfort"],      "category":"Coffee"},
    {"name":"Cold Coffee WNR",        "place":"Wok N Roll Cafe","price":80,  "tags":["energy","refreshing","quick","fun"],    "category":"Coffee"},
    {"name":"Veg Soup WNR",           "place":"Wok N Roll Cafe","price":50,  "tags":["light","warm","soothing","healthy"],    "category":"Soup"},
    {"name":"Sweet Corn Soup WNR",    "place":"Wok N Roll Cafe","price":50,  "tags":["light","warm","soothing","comfort"],    "category":"Soup"},
    {"name":"Cheese Paneer Kulcha",   "place":"Wok N Roll Cafe","price":95,  "tags":["comfort","filling","cheesy","warm"],    "category":"Kulcha"},
    {"name":"Kulcha with Chana",      "place":"Wok N Roll Cafe","price":70,  "tags":["filling","comfort","warm","protein"],   "category":"Kulcha"},
    {"name":"Aaloo Patty WNR",        "place":"Wok N Roll Cafe","price":30,  "tags":["quick","light","snack","comfort"],      "category":"Patty"},
    {"name":"Butter Grilled Sandwich","place":"Wok N Roll Cafe","price":95,  "tags":["comfort","warm","quick","filling"],     "category":"Sandwich"},
    {"name":"Veg Burger WNR",         "place":"Wok N Roll Cafe","price":65,  "tags":["quick","filling","comfort","easy"],     "category":"Burger"},
    {"name":"Cheese Burger WNR",      "place":"Wok N Roll Cafe","price":80,  "tags":["fun","cheesy","filling","indulgent"],   "category":"Burger"},
    {"name":"Veg Noodles WNR",        "place":"Wok N Roll Cafe","price":90,  "tags":["quick","light","comfort","easy"],       "category":"Noodles"},
    {"name":"Hakka Noodles WNR",      "place":"Wok N Roll Cafe","price":110, "tags":["fun","spicy","filling","comfort"],      "category":"Noodles"},
    {"name":"Spring Rolls WNR",       "place":"Wok N Roll Cafe","price":90,  "tags":["light","crispy","fun","quick"],         "category":"Snacks"},
    {"name":"Honey Chilli Potato WNR","place":"Wok N Roll Cafe","price":110, "tags":["spicy","fun","indulgent","snack"],      "category":"Snacks"},
    {"name":"French Fries WNR",       "place":"Wok N Roll Cafe","price":80,  "tags":["comfort","quick","snack","fun"],        "category":"Snacks"},
    {"name":"Veg Momos WNR",          "place":"Wok N Roll Cafe","price":90,  "tags":["comfort","warm","light","quick"],       "category":"Momos"},
    {"name":"Veg Fried Momos WNR",    "place":"Wok N Roll Cafe","price":105, "tags":["fun","crispy","comfort","warm"],        "category":"Momos"},
    {"name":"Spl Honey Chilli Momos", "place":"Wok N Roll Cafe","price":150, "tags":["fun","spicy","indulgent","special"],    "category":"Momos"},
    {"name":"White Sauce Pasta WNR",  "place":"Wok N Roll Cafe","price":90,  "tags":["comfort","creamy","filling","warm"],    "category":"Pasta"},
    {"name":"Veg Macaroni WNR",       "place":"Wok N Roll Cafe","price":80,  "tags":["comfort","light","easy","warm"],        "category":"Pasta"},
    {"name":"Plain Maggi WNR",        "place":"Wok N Roll Cafe","price":40,  "tags":["comfort","quick","light","easy"],       "category":"Maggi"},
    {"name":"Tadka Maggi WNR",        "place":"Wok N Roll Cafe","price":65,  "tags":["comfort","spicy","quick","warm"],       "category":"Maggi"},
    {"name":"Double Masala Maggi WNR","place":"Wok N Roll Cafe","price":65,  "tags":["comfort","spicy","filling","fun"],      "category":"Maggi"},
    {"name":"Butter Masala Chaap WNR","place":"Wok N Roll Cafe","price":90,  "tags":["rich","comfort","warm","protein"],      "category":"Chaap"},
    {"name":"Malai Chaap WNR",        "place":"Wok N Roll Cafe","price":110, "tags":["rich","comfort","warm","indulgent"],    "category":"Chaap"},
    {"name":"Dahi Bhalla WNR",        "place":"Wok N Roll Cafe","price":65,  "tags":["light","soothing","cooling","comfort"], "category":"Chaat"},
    {"name":"Hot Gulab Jamun WNR",    "place":"Wok N Roll Cafe","price":40,  "tags":["sweet","warm","comfort","indulgent"],   "category":"Sweets"},
    {"name":"Sweet Lassi WNR",        "place":"Wok N Roll Cafe","price":60,  "tags":["soothing","light","refreshing","sweet"],"category":"Lassi"},
    {"name":"Masala Tea WNR",         "place":"Wok N Roll Cafe","price":20,  "tags":["comfort","warm","quick","soothing"],    "category":"Tea"},
    {"name":"Green Tea WNR",          "place":"Wok N Roll Cafe","price":25,  "tags":["healthy","light","warm","calming"],     "category":"Tea"},
    {"name":"Mango Shake WNR",        "place":"Wok N Roll Cafe","price":90,  "tags":["sweet","energy","refreshing","fun"],    "category":"Shake"},
    {"name":"Chocolate Shake WNR",    "place":"Wok N Roll Cafe","price":75,  "tags":["sweet","comfort","indulgent","fun"],    "category":"Shake"},

    # ── CHAUDHARY JUICE CORNER ──────────────────────────────────────
    {"name":"Banana Shake CJC",       "place":"Chaudhary Juice Corner","price":50, "tags":["energy","light","quick","healthy"],    "category":"Shake"},
    {"name":"Mango Shake CJC",        "place":"Chaudhary Juice Corner","price":50, "tags":["refreshing","energy","sweet","light"], "category":"Shake"},
    {"name":"Chocolate Shake CJC",    "place":"Chaudhary Juice Corner","price":60, "tags":["comfort","sweet","indulgent","fun"],   "category":"Shake"},
    {"name":"Strawberry Shake CJC",   "place":"Chaudhary Juice Corner","price":60, "tags":["refreshing","sweet","light","fun"],    "category":"Shake"},
    {"name":"Blueberry Shake CJC",    "place":"Chaudhary Juice Corner","price":70, "tags":["refreshing","sweet","healthy","fun"],  "category":"Shake"},
    {"name":"Oreo Shake CJC",         "place":"Chaudhary Juice Corner","price":60, "tags":["sweet","comfort","indulgent","fun"],   "category":"Shake"},
    {"name":"Mosambi Juice",          "place":"Chaudhary Juice Corner","price":50, "tags":["healthy","fresh","light","energy"],    "category":"Juice"},
    {"name":"Mixed Fruit Juice",      "place":"Chaudhary Juice Corner","price":50, "tags":["healthy","fresh","energy","light"],    "category":"Juice"},
    {"name":"Pomegranate Juice",      "place":"Chaudhary Juice Corner","price":80, "tags":["healthy","fresh","energy","rich"],     "category":"Juice"},
    {"name":"Orange Juice",           "place":"Chaudhary Juice Corner","price":50, "tags":["healthy","fresh","light","quick"],     "category":"Juice"},
    {"name":"Carrot Juice",           "place":"Chaudhary Juice Corner","price":40, "tags":["healthy","light","fresh","energy"],    "category":"Juice"},
    {"name":"Mix Vegetable Juice",    "place":"Chaudhary Juice Corner","price":50, "tags":["healthy","light","fresh","energy"],    "category":"Juice"},

    # ── FRIENDS CORNER ──────────────────────────────────────────────
    {"name":"Aloo Parantha FC",       "place":"Friends Corner","price":50,  "tags":["comfort","warm","filling","morning"],    "category":"Breakfast"},
    {"name":"Poha FC",                "place":"Friends Corner","price":100, "tags":["light","easy","comfort","morning"],      "category":"Breakfast"},
    {"name":"Chole Bhature FC",       "place":"Friends Corner","price":80,  "tags":["heavy","filling","comfort","fun"],       "category":"Breakfast"},
    {"name":"Dal Makhani FC",         "place":"Friends Corner","price":200, "tags":["rich","comfort","warm","protein"],       "category":"Main Course"},
    {"name":"Paneer Butter Masala FC","place":"Friends Corner","price":250, "tags":["rich","comfort","warm","indulgent"],     "category":"Main Course"},
    {"name":"Kadahi Panner FC",       "place":"Friends Corner","price":230, "tags":["spicy","comfort","warm","rich"],         "category":"Main Course"},
    {"name":"Rajma Chawal FC",        "place":"Friends Corner","price":50,  "tags":["comfort","filling","warm","protein"],    "category":"Rice"},
    {"name":"Friends Corner Thali",   "place":"Friends Corner","price":180, "tags":["filling","comfort","complete","value"],  "category":"Thali"},
    {"name":"Regular Thali FC",       "place":"Friends Corner","price":140, "tags":["comfort","filling","value","complete"],  "category":"Thali"},
    {"name":"Veg Thupka FC",          "place":"Friends Corner","price":80,  "tags":["warm","soothing","light","comfort"],     "category":"Thupka"},
    {"name":"Mix Veg Soup FC",        "place":"Friends Corner","price":70,  "tags":["light","warm","healthy","soothing"],     "category":"Soup"},
    {"name":"Hot Sour Soup FC",       "place":"Friends Corner","price":70,  "tags":["spicy","warm","light","comfort"],        "category":"Soup"},
    {"name":"Veg Momos FC",           "place":"Friends Corner","price":50,  "tags":["comfort","warm","light","quick"],        "category":"Momos"},
    {"name":"Peri Peri Momos FC",     "place":"Friends Corner","price":100, "tags":["spicy","fun","comfort","warm"],          "category":"Momos"},
    {"name":"Veg Burger FC",          "place":"Friends Corner","price":50,  "tags":["quick","easy","comfort","light"],        "category":"Burger"},
    {"name":"Veg Noodles FC",         "place":"Friends Corner","price":60,  "tags":["quick","light","comfort","easy"],        "category":"Noodles"},
    {"name":"Hakka Noodles FC",       "place":"Friends Corner","price":130, "tags":["fun","spicy","filling","comfort"],       "category":"Noodles"},
    {"name":"White Sauce Pasta FC",   "place":"Friends Corner","price":180, "tags":["comfort","creamy","filling","warm"],     "category":"Pasta"},
    {"name":"Tea FC",                 "place":"Friends Corner","price":20,  "tags":["comfort","warm","quick","soothing"],     "category":"Beverage"},
    {"name":"Cold Coffee FC",         "place":"Friends Corner","price":60,  "tags":["energy","refreshing","quick","fun"],     "category":"Beverage"},
    {"name":"Banana Shake FC",        "place":"Friends Corner","price":70,  "tags":["energy","sweet","light","healthy"],      "category":"Shake"},

    # ── CHAI VYANJAN ────────────────────────────────────────────────
    {"name":"Adrak Chai CV",          "place":"Chai Vyanjan","price":20,  "tags":["comfort","warm","soothing","quick"],      "category":"Chai"},
    {"name":"Masala Chai CV",         "place":"Chai Vyanjan","price":22,  "tags":["comfort","warm","spicy","soothing"],      "category":"Chai"},
    {"name":"Kesar Chai CV",          "place":"Chai Vyanjan","price":22,  "tags":["comfort","warm","soothing","special"],    "category":"Chai"},
    {"name":"Butter Scotch Chai CV",  "place":"Chai Vyanjan","price":24,  "tags":["comfort","sweet","warm","special"],       "category":"Chai"},
    {"name":"Cold Coffee CV",         "place":"Chai Vyanjan","price":105, "tags":["energy","refreshing","fun","quick"],      "category":"Cold Coffee"},
    {"name":"Hot Coffee CV",          "place":"Chai Vyanjan","price":45,  "tags":["energy","warm","quick","comfort"],        "category":"Coffee"},
    {"name":"Maska Bun CV",           "place":"Chai Vyanjan","price":49,  "tags":["light","quick","comfort","easy"],         "category":"Burger"},
    {"name":"Veg Surprise Burger CV", "place":"Chai Vyanjan","price":75,  "tags":["fun","filling","comfort","quick"],        "category":"Burger"},
    {"name":"Paneer Wow Burger CV",   "place":"Chai Vyanjan","price":149, "tags":["fun","filling","cheesy","indulgent"],     "category":"Burger"},
    {"name":"French Fries CV",        "place":"Chai Vyanjan","price":105, "tags":["comfort","quick","snack","fun"],          "category":"Fries"},
    {"name":"Peri Peri Fries CV",     "place":"Chai Vyanjan","price":115, "tags":["spicy","fun","snack","indulgent"],        "category":"Fries"},
    {"name":"Pizza Puff CV",          "place":"Chai Vyanjan","price":149, "tags":["fun","cheesy","quick","snack"],           "category":"Snacks"},
    {"name":"Bombay Kaccha Sandwich", "place":"Chai Vyanjan","price":109, "tags":["comfort","quick","light","fresh"],        "category":"Sandwich"},
    {"name":"Veg Grill Sandwich CV",  "place":"Chai Vyanjan","price":125, "tags":["comfort","warm","quick","filling"],       "category":"Sandwich"},
    {"name":"CV Special Sandwich",    "place":"Chai Vyanjan","price":139, "tags":["filling","comfort","cheesy","warm"],      "category":"Sandwich"},
    {"name":"Herb Chilli Wrap CV",    "place":"Chai Vyanjan","price":125, "tags":["spicy","fun","filling","quick"],          "category":"Wrap"},
    {"name":"Paneer Wow Wrap CV",     "place":"Chai Vyanjan","price":189, "tags":["filling","fun","cheesy","indulgent"],     "category":"Wrap"},
    {"name":"Hostel Maggi CV",        "place":"Chai Vyanjan","price":50,  "tags":["comfort","quick","light","easy"],         "category":"Maggi"},
    {"name":"Tandoori Maggi CV",      "place":"Chai Vyanjan","price":75,  "tags":["comfort","spicy","warm","quick"],         "category":"Maggi"},
    {"name":"CV Special Maggi",       "place":"Chai Vyanjan","price":75,  "tags":["comfort","spicy","filling","special"],    "category":"Maggi"},
    {"name":"Red Sauce Pasta CV",     "place":"Chai Vyanjan","price":115, "tags":["comfort","tangy","filling","warm"],       "category":"Pasta"},
    {"name":"Choco Lava Cake CV",     "place":"Chai Vyanjan","price":109, "tags":["sweet","indulgent","comfort","special"],  "category":"Dessert"},
    {"name":"Choco Walnut Brownie",   "place":"Chai Vyanjan","price":109, "tags":["sweet","comfort","indulgent","fun"],      "category":"Dessert"},
    {"name":"Mango Shake CV",         "place":"Chai Vyanjan","price":105, "tags":["refreshing","sweet","energy","fun"],      "category":"Shake"},

    # ── ZAIKA RESTAURANT ────────────────────────────────────────────
    {"name":"Aloo Pyaaz Paratha ZR",  "place":"Zaika Restaurant","price":35, "tags":["comfort","warm","light","morning"],    "category":"Breakfast"},
    {"name":"Plain Paratha ZR",       "place":"Zaika Restaurant","price":20, "tags":["light","easy","comfort","morning"],    "category":"Breakfast"},
    {"name":"Samosa ZR",              "place":"Zaika Restaurant","price":15, "tags":["quick","light","snack","spicy"],       "category":"Snack"},
    {"name":"Chole Bhature ZR",       "place":"Zaika Restaurant","price":90, "tags":["heavy","filling","comfort","fun"],     "category":"Breakfast"},
    {"name":"Plain Maggi ZR",         "place":"Zaika Restaurant","price":30, "tags":["comfort","quick","light","easy"],      "category":"Maggi"},
    {"name":"Masla Maggi ZR",         "place":"Zaika Restaurant","price":50, "tags":["comfort","spicy","quick","warm"],      "category":"Maggi"},
    {"name":"Paneer Roll ZR",         "place":"Zaika Restaurant","price":80, "tags":["filling","comfort","quick","fun"],     "category":"Quick Bite"},
    {"name":"Veg Steam Momos ZR",     "place":"Zaika Restaurant","price":60, "tags":["comfort","warm","light","quick"],      "category":"Chinese"},
    {"name":"Veg Fried Rice ZR",      "place":"Zaika Restaurant","price":90, "tags":["comfort","filling","quick","fun"],     "category":"Chinese"},
    {"name":"Crispy Chilli Potato ZR","place":"Zaika Restaurant","price":130,"tags":["spicy","fun","snack","indulgent"],     "category":"Chinese"},
    {"name":"Dal Yellow ZR",          "place":"Zaika Restaurant","price":120,"tags":["light","protein","warm","healthy"],    "category":"Indian"},
    {"name":"Veg Thali ZR",           "place":"Zaika Restaurant","price":120,"tags":["comfort","filling","complete","value"],"category":"Indian"},
    {"name":"Special Thali ZR",       "place":"Zaika Restaurant","price":180,"tags":["rich","filling","complete","value"],   "category":"Indian"},
    {"name":"Masala Tea ZR",          "place":"Zaika Restaurant","price":15, "tags":["comfort","warm","quick","soothing"],   "category":"Beverage"},
    {"name":"Cold Coffee ZR",         "place":"Zaika Restaurant","price":40, "tags":["energy","refreshing","quick","fun"],   "category":"Beverage"},
    {"name":"Lemon Mojito ZR",        "place":"Zaika Restaurant","price":50, "tags":["refreshing","light","cooling","quick"],"category":"Mojito"},
    {"name":"Veg Pizza ZR",           "place":"Zaika Restaurant","price":220,"tags":["fun","cheesy","heavy","indulgent"],    "category":"Pizza"},

    # ── YELLOW CHILLY ───────────────────────────────────────────────
    {"name":"Aloo Prantha YC",        "place":"Yellow Chilly","price":40,  "tags":["comfort","warm","filling","morning"],   "category":"Breakfast"},
    {"name":"Poha YC",                "place":"Yellow Chilly","price":60,  "tags":["light","easy","comfort","morning"],     "category":"Breakfast"},
    {"name":"Plain Maggi YC",         "place":"Yellow Chilly","price":30,  "tags":["comfort","quick","light","easy"],       "category":"Maggi"},
    {"name":"Magic Maggi YC",         "place":"Yellow Chilly","price":80,  "tags":["comfort","spicy","warm","indulgent"],   "category":"Maggi"},
    {"name":"Paneer Butter Masala YC","place":"Yellow Chilly","price":200, "tags":["rich","comfort","warm","indulgent"],    "category":"Main Course"},
    {"name":"Dal Makhani YC",         "place":"Yellow Chilly","price":120, "tags":["rich","comfort","warm","protein"],      "category":"Main Course"},
    {"name":"Dal Tadka YC",           "place":"Yellow Chilly","price":90,  "tags":["light","protein","warm","comfort"],     "category":"Main Course"},
    {"name":"Rajma Chawal YC half",   "place":"Yellow Chilly","price":50,  "tags":["comfort","filling","warm","protein"],   "category":"Meal Deal"},
    {"name":"Veg Thali YC",           "place":"Yellow Chilly","price":100, "tags":["filling","comfort","complete","value"], "category":"Thali"},
    {"name":"Special Thali YC",       "place":"Yellow Chilly","price":180, "tags":["filling","comfort","complete","rich"],  "category":"Thali"},
    {"name":"Veg Momos YC half",      "place":"Yellow Chilly","price":50,  "tags":["comfort","warm","light","quick"],       "category":"Momos"},
    {"name":"Veg Burger YC",          "place":"Yellow Chilly","price":50,  "tags":["quick","comfort","light","easy"],       "category":"Snacks"},
    {"name":"Paneer Pakora YC",       "place":"Yellow Chilly","price":70,  "tags":["warm","crispy","comfort","snack"],      "category":"Snacks"},
    {"name":"Noodles Manchurian Momo","place":"Yellow Chilly","price":180, "tags":["heavy","fun","filling","value"],        "category":"Combo"},

    # ── FOOD POINT ──────────────────────────────────────────────────
    {"name":"Aloo Prantha FP",         "place":"Food Point","price":30,  "tags":["comfort","warm","light","morning"],      "category":"Breakfast"},
    {"name":"Gobhi Prantha FP",        "place":"Food Point","price":35,  "tags":["comfort","warm","filling","morning"],    "category":"Breakfast"},
    {"name":"Paneer Prantha FP",       "place":"Food Point","price":50,  "tags":["comfort","filling","warm","protein"],    "category":"Breakfast"},
    {"name":"Poori Bhaji FP",          "place":"Food Point","price":90,  "tags":["comfort","warm","heavy","fun"],          "category":"Breakfast"},
    {"name":"Channa Bhatura FP",       "place":"Food Point","price":100, "tags":["heavy","filling","comfort","fun"],       "category":"Breakfast"},
    {"name":"Butter Toast FP",         "place":"Food Point","price":30,  "tags":["light","quick","easy","morning"],        "category":"Breakfast"},
    {"name":"Veg Soup FP",             "place":"Food Point","price":50,  "tags":["light","warm","soothing","healthy"],     "category":"Soup"},
    {"name":"Sweet Corn Soup FP",      "place":"Food Point","price":50,  "tags":["warm","light","soothing","comfort"],     "category":"Soup"},
    {"name":"Veg Chowmein FP",         "place":"Food Point","price":50,  "tags":["quick","light","comfort","easy"],        "category":"Chinese"},
    {"name":"Veg Momos FP",            "place":"Food Point","price":80,  "tags":["comfort","warm","light","quick"],        "category":"Chinese"},
    {"name":"Fried Momos FP",          "place":"Food Point","price":100, "tags":["fun","crispy","comfort","warm"],         "category":"Chinese"},
    {"name":"Paneer Momos FP",         "place":"Food Point","price":120, "tags":["comfort","warm","filling","protein"],    "category":"Chinese"},
    {"name":"Honey Chilli Potato FP",  "place":"Food Point","price":140, "tags":["spicy","fun","snack","indulgent"],       "category":"Chinese"},
    {"name":"Veg Manchurian FP",       "place":"Food Point","price":120, "tags":["spicy","fun","comfort","heavy"],         "category":"Chinese"},
    {"name":"Chilli Paneer FP",        "place":"Food Point","price":200, "tags":["spicy","fun","heavy","indulgent"],       "category":"Chinese"},
    {"name":"Veg Fried Rice FP",       "place":"Food Point","price":90,  "tags":["comfort","filling","quick","fun"],       "category":"Chinese"},
    {"name":"Spring Roll FP",          "place":"Food Point","price":100, "tags":["light","crispy","fun","quick"],          "category":"Chinese"},
    {"name":"Dal Tadka FP",            "place":"Food Point","price":140, "tags":["light","protein","warm","comfort"],      "category":"Indian Veg"},
    {"name":"Dal Makhani FP",          "place":"Food Point","price":160, "tags":["rich","comfort","warm","protein"],       "category":"Indian Veg"},
    {"name":"Paneer Butter Masala FP", "place":"Food Point","price":190, "tags":["rich","comfort","warm","indulgent"],     "category":"Indian Veg"},
    {"name":"Kadai Paneer FP",         "place":"Food Point","price":200, "tags":["spicy","rich","warm","comfort"],         "category":"Indian Veg"},
    {"name":"Aloo Jeera FP",           "place":"Food Point","price":100, "tags":["light","comfort","warm","easy"],         "category":"Indian Veg"},
    {"name":"Rajma Masala FP",         "place":"Food Point","price":130, "tags":["comfort","filling","warm","protein"],    "category":"Indian Veg"},
    {"name":"Veg Biryani FP",          "place":"Food Point","price":170, "tags":["heavy","filling","comfort","indulgent"], "category":"Biryani"},
    {"name":"Veg Pizza FP",            "place":"Food Point","price":160, "tags":["fun","cheesy","heavy","indulgent"],      "category":"Pizza"},
    {"name":"Onion Capsicum Pizza FP", "place":"Food Point","price":140, "tags":["fun","cheesy","light","quick"],          "category":"Pizza"},
    {"name":"White Sauce Pasta FP",    "place":"Food Point","price":160, "tags":["comfort","creamy","filling","warm"],     "category":"Pasta"},
    {"name":"Red Sauce Pasta FP",      "place":"Food Point","price":150, "tags":["comfort","tangy","filling","warm"],      "category":"Pasta"},
    {"name":"Special Thali FP",        "place":"Food Point","price":180, "tags":["filling","comfort","complete","rich"],   "category":"Thali"},
    {"name":"Rajma Rice FP",           "place":"Food Point","price":50,  "tags":["comfort","filling","warm","protein"],    "category":"Rice Combo"},
    {"name":"Kadi Chawal FP",          "place":"Food Point","price":50,  "tags":["comfort","light","warm","easy"],         "category":"Rice Combo"},
    {"name":"Tea FP",                  "place":"Food Point","price":15,  "tags":["comfort","warm","quick","soothing"],     "category":"Beverage"},
    {"name":"Cold Coffee FP",          "place":"Food Point","price":50,  "tags":["energy","refreshing","quick","fun"],     "category":"Beverage"},
    {"name":"Banana Shake FP",         "place":"Food Point","price":40,  "tags":["energy","sweet","light","healthy"],      "category":"Shake"},
    {"name":"Mango Shake FP",          "place":"Food Point","price":60,  "tags":["refreshing","sweet","energy","fun"],     "category":"Shake"},
    {"name":"Veg Burger FP",           "place":"Food Point","price":50,  "tags":["quick","comfort","light","easy"],        "category":"Burger"},
    {"name":"Cheese Burger FP",        "place":"Food Point","price":70,  "tags":["fun","cheesy","filling","indulgent"],    "category":"Burger"},
    {"name":"Veg Sandwich FP",         "place":"Food Point","price":90,  "tags":["light","quick","easy","fresh"],          "category":"Sandwich"},
    {"name":"Malai Chaap FP",          "place":"Food Point","price":170, "tags":["rich","comfort","warm","protein"],       "category":"Soya Chaap"},
    {"name":"Afghani Chaap FP",        "place":"Food Point","price":170, "tags":["spicy","rich","warm","comfort"],         "category":"Soya Chaap"},
    {"name":"Masala Chaap FP",         "place":"Food Point","price":170, "tags":["spicy","comfort","warm","fun"],          "category":"Soya Chaap"},
    {"name":"Veg Pakora FP",           "place":"Food Point","price":90,  "tags":["warm","crispy","comfort","snack"],       "category":"Indian Snacks"},
    {"name":"Paneer Pakora FP",        "place":"Food Point","price":170, "tags":["warm","crispy","rich","snack"],          "category":"Indian Snacks"},
    {"name":"French Fries FP",         "place":"Food Point","price":60,  "tags":["comfort","quick","snack","fun"],         "category":"Fries"},
    {"name":"Masala Fries FP",         "place":"Food Point","price":120, "tags":["spicy","fun","snack","comfort"],         "category":"Fries"},
    {"name":"Paneer Roll FP",          "place":"Food Point","price":120, "tags":["comfort","filling","quick","fun"],       "category":"Wrap Roll"},
    {"name":"Afghani Chaap Roll FP",   "place":"Food Point","price":120, "tags":["spicy","comfort","filling","fun"],       "category":"Wrap Roll"},

    # ── LAXMI BAKERS ────────────────────────────────────────────────
    {"name":"Plain Chai LB",          "place":"Laxmi Bakers","price":15,  "tags":["comfort","warm","quick","soothing"],     "category":"Tea"},
    {"name":"Masala Chai LB",         "place":"Laxmi Bakers","price":25,  "tags":["comfort","warm","spicy","soothing"],     "category":"Tea"},
    {"name":"Strong Coffee LB",       "place":"Laxmi Bakers","price":35,  "tags":["energy","warm","quick","strong"],        "category":"Coffee"},
    {"name":"Choco Coffee LB",        "place":"Laxmi Bakers","price":40,  "tags":["comfort","sweet","warm","fun"],          "category":"Coffee"},
    {"name":"Aloo Parantha LB",       "place":"Laxmi Bakers","price":30,  "tags":["comfort","warm","light","morning"],      "category":"Parantha"},
    {"name":"Plain Maggi LB",         "place":"Laxmi Bakers","price":50,  "tags":["comfort","quick","light","easy"],        "category":"Maggi"},
    {"name":"Makhani Maggi LB",       "place":"Laxmi Bakers","price":80,  "tags":["rich","comfort","warm","indulgent"],     "category":"Maggi"},
    {"name":"Steam Momos LB",         "place":"Laxmi Bakers","price":80,  "tags":["comfort","warm","light","quick"],        "category":"Momos"},
    {"name":"Peri Peri Momos LB",     "place":"Laxmi Bakers","price":120, "tags":["spicy","fun","warm","comfort"],          "category":"Momos"},
    {"name":"Veg Noodles LB",         "place":"Laxmi Bakers","price":60,  "tags":["quick","light","comfort","easy"],        "category":"Noodles"},
    {"name":"Hakka Noodles LB",       "place":"Laxmi Bakers","price":70,  "tags":["fun","spicy","filling","comfort"],       "category":"Noodles"},
    {"name":"French Fries LB",        "place":"Laxmi Bakers","price":80,  "tags":["comfort","quick","snack","fun"],         "category":"Fries"},
    {"name":"Peri Peri Fries LB",     "place":"Laxmi Bakers","price":90,  "tags":["spicy","fun","snack","indulgent"],       "category":"Fries"},
    {"name":"Veg Grill Sandwich LB",  "place":"Laxmi Bakers","price":80,  "tags":["comfort","warm","quick","light"],        "category":"Sandwich"},
    {"name":"Veg Pizza LB",           "place":"Laxmi Bakers","price":100, "tags":["fun","cheesy","light","quick"],          "category":"Pizza"},
    {"name":"Margherita LB",          "place":"Laxmi Bakers","price":150, "tags":["fun","cheesy","filling","comfort"],      "category":"Pizza"},
    {"name":"White Sauce Pasta LB",   "place":"Laxmi Bakers","price":150, "tags":["comfort","creamy","filling","warm"],     "category":"Pasta"},
    {"name":"Oreo Shake LB",          "place":"Laxmi Bakers","price":70,  "tags":["sweet","comfort","indulgent","fun"],     "category":"Shake"},
    {"name":"Mango Shake LB",         "place":"Laxmi Bakers","price":80,  "tags":["refreshing","sweet","energy","light"],   "category":"Shake"},
    {"name":"Sweet Lassi LB",         "place":"Laxmi Bakers","price":30,  "tags":["refreshing","light","soothing","sweet"], "category":"Lassi"},
    {"name":"Mint Mojito LB",         "place":"Laxmi Bakers","price":120, "tags":["refreshing","light","cooling","fun"],    "category":"Mojito"},

    # ── ARU'S CAFE ──────────────────────────────────────────────────
    {"name":"Tea Aru",                "place":"Aru's Cafe","price":15,  "tags":["comfort","warm","quick","soothing"],       "category":"Beverage"},
    {"name":"Ginger Honey Tea Aru",   "place":"Aru's Cafe","price":25,  "tags":["healthy","warm","soothing","comfort"],     "category":"Beverage"},
    {"name":"Cold Coffee Aru",        "place":"Aru's Cafe","price":40,  "tags":["energy","refreshing","quick","fun"],       "category":"Beverage"},
    {"name":"Plain Prantha Aru",      "place":"Aru's Cafe","price":25,  "tags":["light","easy","comfort","morning"],        "category":"Breakfast"},
    {"name":"Aloo Prantha Aru",       "place":"Aru's Cafe","price":30,  "tags":["comfort","warm","filling","morning"],      "category":"Breakfast"},
    {"name":"Paneer Prantha Aru",     "place":"Aru's Cafe","price":50,  "tags":["comfort","filling","warm","protein"],      "category":"Breakfast"},
    {"name":"Pav Bhaji Aru",          "place":"Aru's Cafe","price":80,  "tags":["comfort","filling","warm","fun"],          "category":"Breakfast"},
    {"name":"Plain Maggi Aru",        "place":"Aru's Cafe","price":30,  "tags":["comfort","quick","light","easy"],          "category":"Quick Bites"},
    {"name":"Veg Masala Maggi Aru",   "place":"Aru's Cafe","price":40,  "tags":["comfort","spicy","quick","warm"],          "category":"Quick Bites"},
    {"name":"Veg Sandwich Aru",       "place":"Aru's Cafe","price":40,  "tags":["light","quick","easy","fresh"],            "category":"Quick Bites"},
    {"name":"Cheese Grilled Sandwich","place":"Aru's Cafe","price":100, "tags":["comfort","warm","cheesy","filling"],       "category":"Quick Bites"},
    {"name":"Plain Dosa Aru",         "place":"Aru's Cafe","price":80,  "tags":["light","crispy","quick","healthy"],        "category":"South Indian"},
    {"name":"Masala Dosa Aru",        "place":"Aru's Cafe","price":100, "tags":["comfort","filling","crispy","warm"],       "category":"South Indian"},
    {"name":"Idli Sambar Aru",        "place":"Aru's Cafe","price":70,  "tags":["light","healthy","warm","comfort"],        "category":"South Indian"},
    {"name":"Dal Tadka Aru",          "place":"Aru's Cafe","price":100, "tags":["light","protein","warm","comfort"],        "category":"Main Course"},
    {"name":"Kadhai Paneer Aru",      "place":"Aru's Cafe","price":180, "tags":["spicy","rich","warm","comfort"],           "category":"Main Course"},
    {"name":"Manchow Soup Aru",       "place":"Aru's Cafe","price":40,  "tags":["light","warm","soothing","quick"],         "category":"Soup"},
    {"name":"Thupka Veg Aru",         "place":"Aru's Cafe","price":50,  "tags":["warm","soothing","light","comfort"],       "category":"Soup"},
    {"name":"Special Veg Thali Aru",  "place":"Aru's Cafe","price":160, "tags":["filling","comfort","complete","value"],    "category":"Thali"},
    {"name":"Veg Biryani Aru",        "place":"Aru's Cafe","price":170, "tags":["heavy","filling","comfort","indulgent"],   "category":"Biryani"},

    # ── CHEERS TO CHAI ──────────────────────────────────────────────
    {"name":"Adrak Chai CTC",         "place":"Cheers to Chai","price":25, "tags":["comfort","warm","soothing","quick"],    "category":"Chai"},
    {"name":"Elaichi Chai CTC",       "place":"Cheers to Chai","price":30, "tags":["comfort","warm","soothing","special"],  "category":"Chai"},
    {"name":"Kesar Chai CTC",         "place":"Cheers to Chai","price":30, "tags":["comfort","warm","soothing","special"],  "category":"Chai"},
    {"name":"Masala Chai CTC",        "place":"Cheers to Chai","price":30, "tags":["comfort","warm","spicy","soothing"],    "category":"Chai"},
    {"name":"Tulsi Chai CTC",         "place":"Cheers to Chai","price":30, "tags":["healthy","warm","soothing","calming"],  "category":"Chai"},
    {"name":"Paan Chai CTC",          "place":"Cheers to Chai","price":30, "tags":["fun","warm","special","comfort"],       "category":"Chai"},
    {"name":"Cold Coffee CTC",        "place":"Cheers to Chai","price":80, "tags":["energy","refreshing","quick","fun"],    "category":"Cold Coffee"},
    {"name":"Choco Coffee CTC",       "place":"Cheers to Chai","price":90, "tags":["comfort","sweet","refreshing","fun"],   "category":"Cold Coffee"},
    {"name":"Hazelnut Coffee CTC",    "place":"Cheers to Chai","price":120,"tags":["comfort","sweet","special","indulgent"],"category":"Cold Coffee"},
    {"name":"Aaloo Prantha CTC",      "place":"Cheers to Chai","price":30, "tags":["comfort","warm","filling","morning"],   "category":"Prantha"},
    {"name":"Gobhi Prantha CTC",      "place":"Cheers to Chai","price":45, "tags":["comfort","warm","filling","morning"],   "category":"Prantha"},
    {"name":"Paneer Prantha CTC",     "place":"Cheers to Chai","price":80, "tags":["comfort","filling","warm","protein"],   "category":"Prantha"},
    {"name":"Cholle Bhature CTC",     "place":"Cheers to Chai","price":100,"tags":["heavy","filling","comfort","fun"],      "category":"Brunch"},
    {"name":"Cholle Puri CTC",        "place":"Cheers to Chai","price":80, "tags":["filling","comfort","warm","fun"],       "category":"Brunch"},
    {"name":"Aalu Puri CTC",          "place":"Cheers to Chai","price":80, "tags":["filling","comfort","warm","fun"],       "category":"Brunch"},
    {"name":"Plain Rice CTC",         "place":"Cheers to Chai","price":70, "tags":["light","easy","comfort","simple"],      "category":"Rice"},
    {"name":"Rajma Rice CTC",         "place":"Cheers to Chai","price":50, "tags":["comfort","filling","warm","protein"],   "category":"Combo"},
    {"name":"Dal Rice CTC",           "place":"Cheers to Chai","price":50, "tags":["light","comfort","warm","easy"],        "category":"Combo"},
    {"name":"Veg Thali CTC",          "place":"Cheers to Chai","price":90, "tags":["filling","comfort","complete","value"], "category":"Thali"},
    {"name":"Special Thali CTC",      "place":"Cheers to Chai","price":150,"tags":["filling","rich","complete","value"],    "category":"Thali"},
    {"name":"Dal Makhni CTC",         "place":"Cheers to Chai","price":190,"tags":["rich","comfort","warm","protein"],      "category":"Indian Zaika"},
    {"name":"Kadhai Paneer CTC",      "place":"Cheers to Chai","price":300,"tags":["spicy","rich","comfort","indulgent"],   "category":"Indian Zaika"},
    {"name":"Rajmaah CTC",            "place":"Cheers to Chai","price":160,"tags":["comfort","filling","warm","protein"],   "category":"Indian Zaika"},
    {"name":"Veg Noodles CTC",        "place":"Cheers to Chai","price":50, "tags":["quick","light","comfort","easy"],       "category":"Chinese"},
    {"name":"Veg Momos CTC",          "place":"Cheers to Chai","price":50, "tags":["comfort","warm","light","quick"],       "category":"Chinese"},
    {"name":"Fried Momos CTC",        "place":"Cheers to Chai","price":120,"tags":["fun","crispy","comfort","warm"],        "category":"Chinese"},
    {"name":"Kurkure Momos CTC",      "place":"Cheers to Chai","price":150,"tags":["fun","crispy","spicy","indulgent"],     "category":"Chinese"},
    {"name":"Veg Thupka CTC",         "place":"Cheers to Chai","price":80, "tags":["warm","soothing","light","comfort"],    "category":"Chinese"},
    {"name":"Red Sauce Pasta CTC",    "place":"Cheers to Chai","price":119,"tags":["comfort","tangy","filling","warm"],     "category":"Pasta"},
    {"name":"White Sauce Pasta CTC",  "place":"Cheers to Chai","price":129,"tags":["comfort","creamy","filling","warm"],    "category":"Pasta"},
    {"name":"French Fries CTC",       "place":"Cheers to Chai","price":80, "tags":["comfort","quick","snack","fun"],        "category":"Snacks"},
    {"name":"Honey Chilli Potato CTC","place":"Cheers to Chai","price":120,"tags":["spicy","fun","snack","indulgent"],      "category":"Snacks"},
    {"name":"Chilli Mushroom CTC",    "place":"Cheers to Chai","price":120,"tags":["spicy","fun","comfort","warm"],         "category":"Snacks"},
    {"name":"Cheese Corn Balls CTC",  "place":"Cheers to Chai","price":120,"tags":["cheesy","fun","snack","crispy"],        "category":"Snacks"},
    {"name":"Paneer Roll CTC",        "place":"Cheers to Chai","price":100,"tags":["comfort","filling","quick","fun"],      "category":"Snacks"},
    {"name":"Oreo Shake CTC",         "place":"Cheers to Chai","price":99, "tags":["sweet","comfort","indulgent","fun"],    "category":"Shakes"},
    {"name":"Banana Shake CTC",       "place":"Cheers to Chai","price":59, "tags":["energy","sweet","light","healthy"],     "category":"Shakes"},
    {"name":"Chocolate Shake CTC",    "place":"Cheers to Chai","price":89, "tags":["comfort","sweet","indulgent","fun"],    "category":"Shakes"},
    {"name":"Mango Shake CTC",        "place":"Cheers to Chai","price":89, "tags":["refreshing","sweet","energy","fun"],    "category":"Shakes"},
    {"name":"Margherita Pizza CTC",   "place":"Cheers to Chai","price":119,"tags":["fun","cheesy","light","classic"],       "category":"Pizza"},
    {"name":"Onion Pizza CTC",        "place":"Cheers to Chai","price":119,"tags":["fun","cheesy","light","quick"],         "category":"Pizza"},
    {"name":"Farm House Pizza CTC",   "place":"Cheers to Chai","price":279,"tags":["fun","cheesy","heavy","indulgent"],     "category":"Pizza"},
    {"name":"Plain Maggi CTC",        "place":"Cheers to Chai","price":30, "tags":["comfort","quick","light","easy"],       "category":"Maggi"},
    {"name":"Double Masala Maggi CTC","place":"Cheers to Chai","price":40, "tags":["comfort","spicy","quick","warm"],       "category":"Maggi"},
    {"name":"Cheese Corn Maggi CTC",  "place":"Cheers to Chai","price":60, "tags":["comfort","cheesy","filling","fun"],     "category":"Maggi"},
    {"name":"Sweet Lassi CTC",        "place":"Cheers to Chai","price":40, "tags":["refreshing","light","soothing","sweet"],"category":"Drinks"},
    {"name":"Mint Mojito CTC",        "place":"Cheers to Chai","price":89, "tags":["refreshing","light","cooling","fun"],   "category":"Drinks"},
    {"name":"Vegge Sandwich CTC",     "place":"Cheers to Chai","price":50, "tags":["light","quick","easy","fresh"],         "category":"Sandwiches"},
    {"name":"Paneer Tikka Sandwich",  "place":"Cheers to Chai","price":80, "tags":["comfort","warm","filling","spicy"],     "category":"Sandwiches"},
    {"name":"Aalu Tikki Burger CTC",  "place":"Cheers to Chai","price":40, "tags":["quick","light","snack","comfort"],      "category":"Burger"},
    {"name":"Veg Burger CTC",         "place":"Cheers to Chai","price":50, "tags":["quick","comfort","light","easy"],       "category":"Burger"},
    {"name":"Veg Paneer Burger CTC",  "place":"Cheers to Chai","price":80, "tags":["fun","filling","cheesy","comfort"],     "category":"Burger"},
    {"name":"Pina Colada CTC",        "place":"Cheers to Chai","price":149,"tags":["fun","refreshing","special","sweet"],   "category":"Special Drink"},

    # ── MISHTI ──────────────────────────────────────────────────────
    {"name":"Normal Tea Mishti",      "place":"Mishti","price":20,  "tags":["comfort","warm","quick","soothing"],        "category":"Breakfast"},
    {"name":"Coffee Mishti",          "place":"Mishti","price":35,  "tags":["energy","warm","quick","comfort"],          "category":"Breakfast"},
    {"name":"Butter Toast Mishti",    "place":"Mishti","price":40,  "tags":["light","quick","easy","morning"],           "category":"Breakfast"},
    {"name":"Aaloo Parantha Mishti",  "place":"Mishti","price":30,  "tags":["comfort","warm","filling","morning"],       "category":"Breakfast"},
    {"name":"Paneer Prantha Mishti",  "place":"Mishti","price":50,  "tags":["comfort","filling","warm","protein"],       "category":"Breakfast"},
    {"name":"Chana Bhatura Mishti",   "place":"Mishti","price":100, "tags":["heavy","filling","comfort","fun"],          "category":"Breakfast"},
    {"name":"Veg Soup Mishti",        "place":"Mishti","price":60,  "tags":["light","warm","soothing","healthy"],        "category":"Soup"},
    {"name":"Sweet Corn Soup Mishti", "place":"Mishti","price":70,  "tags":["warm","light","soothing","comfort"],        "category":"Soup"},
    {"name":"Dal Makhani Mishti",     "place":"Mishti","price":140, "tags":["rich","comfort","warm","protein"],          "category":"Veg Indian"},
    {"name":"Paneer Butter Masala M", "place":"Mishti","price":200, "tags":["rich","comfort","warm","indulgent"],        "category":"Veg Indian"},
    {"name":"Rajmah Masala Mishti",   "place":"Mishti","price":130, "tags":["comfort","filling","warm","protein"],       "category":"Veg Indian"},
    {"name":"Dal Mix Mishti",         "place":"Mishti","price":100, "tags":["light","protein","warm","healthy"],         "category":"Veg Indian"},
    {"name":"Masala Chaap Mishti",    "place":"Mishti","price":180, "tags":["spicy","warm","comfort","fun"],             "category":"Veg Indian"},
    {"name":"Veg Biryani Mishti",     "place":"Mishti","price":200, "tags":["heavy","filling","comfort","special"],      "category":"Rice"},
    {"name":"Dal Rice Mishti half",   "place":"Mishti","price":50,  "tags":["light","comfort","warm","easy"],            "category":"Rice"},
    {"name":"Veg Thali Mishti",       "place":"Mishti","price":90,  "tags":["filling","comfort","complete","value"],     "category":"Thali"},
    {"name":"Special Thali Mishti",   "place":"Mishti","price":170, "tags":["filling","comfort","complete","rich"],      "category":"Thali"},
    {"name":"Chicken Biryani Mishti", "place":"Mishti","price":240, "tags":["heavy","filling","special","indulgent"],    "category":"Rice"},
    {"name":"Mango Shake Mishti",     "place":"Mishti","price":60,  "tags":["refreshing","sweet","energy","light"],      "category":"Shake"},
    {"name":"Red Sauce Pasta Mishti", "place":"Mishti","price":130, "tags":["comfort","filling","tangy","warm"],         "category":"Pasta"},
    {"name":"Veg Chowmein Mishti",    "place":"Mishti","price":90,  "tags":["quick","light","comfort","fun"],            "category":"Chinese"},
    {"name":"Veg Momos Mishti",       "place":"Mishti","price":90,  "tags":["comfort","warm","light","quick"],           "category":"Chinese"},

    # ── KIYANSH CAFE ────────────────────────────────────────────────
    {"name":"Steam Momos KC",         "place":"Kiyansh Cafe","price":50,  "tags":["comfort","warm","light","quick"],      "category":"Momos Veg"},
    {"name":"Fried Momos KC",         "place":"Kiyansh Cafe","price":60,  "tags":["fun","crispy","comfort","warm"],       "category":"Momos Veg"},
    {"name":"Jhol Momos KC",          "place":"Kiyansh Cafe","price":90,  "tags":["comfort","warm","soothing","special"], "category":"Momos Veg"},
    {"name":"Chilly Momos KC",        "place":"Kiyansh Cafe","price":100, "tags":["spicy","fun","comfort","warm"],        "category":"Momos Veg"},
    {"name":"Veg Fried Rice KC",      "place":"Kiyansh Cafe","price":70,  "tags":["comfort","filling","quick","fun"],     "category":"Chinese"},
    {"name":"Paneer Fried Rice KC",   "place":"Kiyansh Cafe","price":80,  "tags":["comfort","filling","protein","fun"],   "category":"Chinese"},
    {"name":"Veg Manchurian KC",      "place":"Kiyansh Cafe","price":80,  "tags":["spicy","fun","comfort","heavy"],       "category":"Chinese"},
    {"name":"Chilli Paneer KC",       "place":"Kiyansh Cafe","price":150, "tags":["spicy","fun","heavy","indulgent"],     "category":"Chinese"},
    {"name":"Honey Chilli Potato KC", "place":"Kiyansh Cafe","price":120, "tags":["spicy","fun","snack","indulgent"],     "category":"Chinese"},
    {"name":"Veg Chowmein KC",        "place":"Kiyansh Cafe","price":50,  "tags":["quick","light","comfort","easy"],      "category":"Noodles"},
    {"name":"Paneer Chowmein KC",     "place":"Kiyansh Cafe","price":80,  "tags":["comfort","filling","protein","fun"],   "category":"Noodles"},
    {"name":"Plain Maggi KC",         "place":"Kiyansh Cafe","price":40,  "tags":["comfort","quick","light","easy"],      "category":"Maggi"},
    {"name":"Veggie Maggi KC",        "place":"Kiyansh Cafe","price":50,  "tags":["comfort","healthy","light","easy"],    "category":"Maggi"},
    {"name":"Cheese Maggi KC",        "place":"Kiyansh Cafe","price":60,  "tags":["comfort","cheesy","filling","fun"],    "category":"Maggi"},
    {"name":"Veggie Wai Wai KC",      "place":"Kiyansh Cafe","price":50,  "tags":["comfort","quick","light","special"],   "category":"Maggi"},
    {"name":"Plain Paratha KC",       "place":"Kiyansh Cafe","price":25,  "tags":["light","easy","comfort","morning"],    "category":"Paratha"},
    {"name":"Aloo Paratha KC",        "place":"Kiyansh Cafe","price":40,  "tags":["comfort","warm","filling","morning"],  "category":"Paratha"},
    {"name":"Paneer Paratha KC",      "place":"Kiyansh Cafe","price":60,  "tags":["comfort","filling","warm","protein"],  "category":"Paratha"},
    {"name":"Veg Burger KC",          "place":"Kiyansh Cafe","price":40,  "tags":["quick","comfort","light","easy"],      "category":"Burger"},
    {"name":"Cheese Burger KC",       "place":"Kiyansh Cafe","price":60,  "tags":["fun","cheesy","filling","indulgent"],  "category":"Burger"},
    {"name":"Double Cheese Burger KC","place":"Kiyansh Cafe","price":80,  "tags":["fun","cheesy","heavy","indulgent"],    "category":"Burger"},
    {"name":"Black Tea KC",           "place":"Kiyansh Cafe","price":10,  "tags":["light","warm","quick","soothing"],     "category":"Beverage"},
    {"name":"Milk Tea KC",            "place":"Kiyansh Cafe","price":15,  "tags":["comfort","warm","quick","soothing"],   "category":"Beverage"},
    {"name":"Cold Coffee KC",         "place":"Kiyansh Cafe","price":60,  "tags":["energy","refreshing","quick","fun"],   "category":"Beverage"},
    {"name":"Oreo Shake KC",          "place":"Kiyansh Cafe","price":80,  "tags":["sweet","comfort","indulgent","fun"],   "category":"Beverage"},
    {"name":"Lassi Sweet KC",         "place":"Kiyansh Cafe","price":40,  "tags":["soothing","light","refreshing","sweet"],"category":"Beverage"},
    {"name":"French Fries KC",        "place":"Kiyansh Cafe","price":70,  "tags":["comfort","quick","snack","fun"],       "category":"Snacks"},
    {"name":"Spring Roll KC",         "place":"Kiyansh Cafe","price":80,  "tags":["light","crispy","fun","quick"],        "category":"Snacks"},
    {"name":"Chowmein Manchurian KC", "place":"Kiyansh Cafe","price":160, "tags":["heavy","fun","filling","value"],       "category":"Combo"},

    # ── WONDER HILLS CAFE ───────────────────────────────────────────
    {"name":"Smoky Paneer Tikka WH",  "place":"Wonder Hills Cafe","price":200,"tags":["spicy","rich","warm","protein"],   "category":"Tandoori"},
    {"name":"Classic Tandoori Chaap", "place":"Wonder Hills Cafe","price":150,"tags":["comfort","warm","protein","spicy"],"category":"Tandoori"},
    {"name":"Smoked Mushroom Tikka",  "place":"Wonder Hills Cafe","price":150,"tags":["rich","warm","comfort","special"], "category":"Tandoori"},
    {"name":"Tomato Comfort Soup",    "place":"Wonder Hills Cafe","price":70, "tags":["warm","soothing","light","comfort"],"category":"Soup"},
    {"name":"Golden Sweet Corn WH",   "place":"Wonder Hills Cafe","price":80, "tags":["warm","light","soothing","sweet"],  "category":"Soup"},
    {"name":"Hot Sour Hill Brew",     "place":"Wonder Hills Cafe","price":80, "tags":["spicy","warm","light","comfort"],   "category":"Soup"},
    {"name":"Red Sauce Pasta WH",     "place":"Wonder Hills Cafe","price":150,"tags":["comfort","tangy","filling","warm"], "category":"Pasta"},
    {"name":"White Sauce Pasta WH",   "place":"Wonder Hills Cafe","price":150,"tags":["comfort","creamy","filling","warm"],"category":"Pasta"},
    {"name":"Margherita Magic WH",    "place":"Wonder Hills Cafe","price":119,"tags":["fun","cheesy","light","classic"],   "category":"Pizza"},
    {"name":"Corn Crunch Pizza WH",   "place":"Wonder Hills Cafe","price":149,"tags":["fun","cheesy","crispy","light"],    "category":"Pizza"},
    {"name":"Himalayan Paneer Delight","place":"Wonder Hills Cafe","price":249,"tags":["rich","special","indulgent","fun"],"category":"Pizza"},
    {"name":"Veggie Treat Burger WH", "place":"Wonder Hills Cafe","price":59, "tags":["quick","light","comfort","easy"],   "category":"Burger"},
    {"name":"Tikki Power Burger WH",  "place":"Wonder Hills Cafe","price":69, "tags":["comfort","filling","quick","fun"],  "category":"Burger"},
    {"name":"Paneer Supreme Burger",  "place":"Wonder Hills Cafe","price":99, "tags":["fun","filling","cheesy","comfort"], "category":"Burger"},
    {"name":"Veg Steamed Momos WH",   "place":"Wonder Hills Cafe","price":80, "tags":["comfort","warm","light","quick"],   "category":"Momos"},
    {"name":"Paneer Momos WH",        "place":"Wonder Hills Cafe","price":100,"tags":["comfort","warm","filling","protein"],"category":"Momos"},
    {"name":"Honey Chilli Momos WH",  "place":"Wonder Hills Cafe","price":120,"tags":["spicy","fun","indulgent","warm"],   "category":"Momos"},
    {"name":"Kurkure Momos WH",       "place":"Wonder Hills Cafe","price":100,"tags":["fun","crispy","spicy","indulgent"], "category":"Momos"},
    {"name":"Creamy Dal Makhani WH",  "place":"Wonder Hills Cafe","price":180,"tags":["rich","comfort","warm","protein"],  "category":"Indian"},
    {"name":"Kadhai Paneer Special WH","place":"Wonder Hills Cafe","price":200,"tags":["spicy","rich","warm","comfort"],   "category":"Indian"},
    {"name":"Special Wonder Thali",   "place":"Wonder Hills Cafe","price":150,"tags":["filling","rich","complete","value"],"category":"Thali"},
    {"name":"Regular Hill Thali",     "place":"Wonder Hills Cafe","price":99, "tags":["filling","comfort","value","easy"], "category":"Thali"},
    {"name":"Veg Hakka Noodles WH",   "place":"Wonder Hills Cafe","price":90, "tags":["quick","light","comfort","fun"],    "category":"Chinese"},
    {"name":"Chilli Garlic Noodles WH","place":"Wonder Hills Cafe","price":110,"tags":["spicy","fun","filling","comfort"], "category":"Chinese"},
    {"name":"Tea WH",                 "place":"Wonder Hills Cafe","price":15, "tags":["comfort","warm","quick","soothing"],"category":"Beverages"},
    {"name":"Masala Tea WH",          "place":"Wonder Hills Cafe","price":20, "tags":["comfort","warm","spicy","soothing"],"category":"Beverages"},
    {"name":"Cold Coffee WH",         "place":"Wonder Hills Cafe","price":80, "tags":["energy","refreshing","quick","fun"],"category":"Beverages"},
    {"name":"Banana Shake WH",        "place":"Wonder Hills Cafe","price":80, "tags":["energy","sweet","light","healthy"], "category":"Beverages"},
    {"name":"Oreo Delight Shake WH",  "place":"Wonder Hills Cafe","price":90, "tags":["sweet","comfort","indulgent","fun"],"category":"Beverages"},
    {"name":"Veg Sandwich WH",        "place":"Wonder Hills Cafe","price":79, "tags":["light","quick","easy","fresh"],     "category":"Sandwich"},
    {"name":"Paneer Tikka Sandwich WH","place":"Wonder Hills Cafe","price":149,"tags":["comfort","warm","filling","spicy"],"category":"Sandwich"},
    {"name":"Vanilla Ice Cream WH",   "place":"Wonder Hills Cafe","price":100,"tags":["sweet","cooling","light","fun"],    "category":"Ice Cream"},
    {"name":"Mango Magic Scoop WH",   "place":"Wonder Hills Cafe","price":100,"tags":["sweet","refreshing","fun","light"], "category":"Ice Cream"},
    {"name":"French Fries WH",        "place":"Wonder Hills Cafe","price":90, "tags":["comfort","quick","snack","fun"],    "category":"Quick Bites"},
    {"name":"Cheesy Loaded Fries WH", "place":"Wonder Hills Cafe","price":110,"tags":["cheesy","indulgent","fun","snack"], "category":"Quick Bites"},
    {"name":"Stuffed Paratha WH",     "place":"Wonder Hills Cafe","price":60, "tags":["comfort","warm","filling","morning"],"category":"Breakfast"},
    {"name":"Pahadi Paneer Paratha",  "place":"Wonder Hills Cafe","price":70, "tags":["comfort","warm","special","filling"],"category":"Breakfast"},
    {"name":"Morning Masti Poha WH",  "place":"Wonder Hills Cafe","price":60, "tags":["light","easy","comfort","morning"], "category":"Breakfast"},
    {"name":"Rajma Rice Combo WH",    "place":"Wonder Hills Cafe","price":70, "tags":["comfort","filling","warm","value"],  "category":"Comfort Combo"},

    # ── ALPINE ESPRESSO ─────────────────────────────────────────────
    {"name":"Espresso AE",            "place":"Alpine Espresso","price":80,  "tags":["energy","strong","quick","warm"],    "category":"Coffee"},
    {"name":"Americano AE",           "place":"Alpine Espresso","price":90,  "tags":["energy","warm","strong","comfort"],  "category":"Coffee"},
    {"name":"Cappuccino AE",          "place":"Alpine Espresso","price":110, "tags":["energy","creamy","warm","comfort"],  "category":"Coffee"},
    {"name":"Cafe Latte AE",          "place":"Alpine Espresso","price":120, "tags":["comfort","creamy","warm","easy"],    "category":"Coffee"},
    {"name":"Mocha AE",               "place":"Alpine Espresso","price":150, "tags":["comfort","sweet","warm","indulgent"],"category":"Coffee"},
    {"name":"Hot Chocolate AE",       "place":"Alpine Espresso","price":150, "tags":["comfort","sweet","warm","soothing"], "category":"Coffee"},
    {"name":"Irish Coffee AE",        "place":"Alpine Espresso","price":150, "tags":["special","warm","comfort","indulgent"],"category":"Coffee"},
    {"name":"Tiramisu Coffee AE",     "place":"Alpine Espresso","price":150, "tags":["special","sweet","warm","indulgent"],"category":"Coffee"},
    {"name":"Iced Americano AE",      "place":"Alpine Espresso","price":85,  "tags":["energy","refreshing","cold","strong"],"category":"Cold Coffee"},
    {"name":"Iced Cappuccino AE",     "place":"Alpine Espresso","price":100, "tags":["energy","refreshing","creamy","fun"], "category":"Cold Coffee"},
    {"name":"Iced Latte AE",          "place":"Alpine Espresso","price":110, "tags":["energy","creamy","refreshing","fun"],"category":"Cold Coffee"},
    {"name":"Frappe AE",              "place":"Alpine Espresso","price":120, "tags":["energy","sweet","refreshing","fun"],  "category":"Cold Coffee"},
    {"name":"Boba Tea Green Apple AE","place":"Alpine Espresso","price":150, "tags":["refreshing","fun","special","sweet"], "category":"Boba Tea"},
    {"name":"Boba Tea Raspberry AE",  "place":"Alpine Espresso","price":130, "tags":["refreshing","fun","special","sweet"], "category":"Boba Tea"},
    {"name":"Redbull AE",             "place":"Alpine Espresso","price":130, "tags":["energy","strong","refreshing","quick"],"category":"Energy Drink"},
    {"name":"Veg Burger AE",          "place":"Alpine Espresso","price":80,  "tags":["quick","comfort","light","easy"],    "category":"Burger"},
    {"name":"Cheese Burger AE",       "place":"Alpine Espresso","price":100, "tags":["fun","cheesy","filling","comfort"],  "category":"Burger"},
    {"name":"Super Veggie Burger AE", "place":"Alpine Espresso","price":130, "tags":["fun","filling","cheesy","indulgent"],"category":"Burger"},
    {"name":"Veg Wrap AE",            "place":"Alpine Espresso","price":99,  "tags":["quick","light","filling","comfort"], "category":"Wrap"},
    {"name":"Paneer Wrap AE",         "place":"Alpine Espresso","price":119, "tags":["filling","comfort","cheesy","quick"],"category":"Wrap"},
    {"name":"Fries AE",               "place":"Alpine Espresso","price":110, "tags":["comfort","quick","snack","fun"],     "category":"Crisps"},
    {"name":"Peri Peri Fries AE",     "place":"Alpine Espresso","price":120, "tags":["spicy","fun","snack","indulgent"],   "category":"Crisps"},
    {"name":"Cheese Fries AE",        "place":"Alpine Espresso","price":130, "tags":["cheesy","indulgent","fun","snack"],  "category":"Crisps"},
    {"name":"Veg Nugget AE",          "place":"Alpine Espresso","price":130, "tags":["crispy","fun","snack","light"],      "category":"Crisps"},
    {"name":"Veg Grilled Sandwich AE","place":"Alpine Espresso","price":120, "tags":["comfort","warm","quick","filling"],  "category":"Sandwich"},
    {"name":"Paneer Sandwich AE",     "place":"Alpine Espresso","price":150, "tags":["filling","comfort","cheesy","warm"], "category":"Sandwich"},
    {"name":"Club Veg Sandwich AE",   "place":"Alpine Espresso","price":200, "tags":["filling","comfort","fresh","special"],"category":"Sandwich"},
    {"name":"Red Sauce Spaghetti AE", "place":"Alpine Espresso","price":170, "tags":["comfort","tangy","filling","warm"],  "category":"Spaghetti"},
    {"name":"White Sauce Spaghetti AE","place":"Alpine Espresso","price":180,"tags":["comfort","creamy","filling","warm"], "category":"Spaghetti"},
    {"name":"Pink Sauce Spaghetti AE","place":"Alpine Espresso","price":200, "tags":["comfort","rich","filling","special"],"category":"Spaghetti"},
    {"name":"Red Sauce Pasta AE",     "place":"Alpine Espresso","price":160, "tags":["comfort","tangy","filling","warm"],  "category":"Pasta"},
    {"name":"White Sauce Pasta AE",   "place":"Alpine Espresso","price":170, "tags":["comfort","creamy","filling","warm"], "category":"Pasta"},
    {"name":"Margherita Pizza S AE",  "place":"Alpine Espresso","price":120, "tags":["fun","cheesy","light","classic"],    "category":"Pizza"},
    {"name":"Farm House Pizza AE",    "place":"Alpine Espresso","price":140, "tags":["fun","cheesy","heavy","filling"],    "category":"Pizza"},
    {"name":"Garlic Loaf S AE",       "place":"Alpine Espresso","price":100, "tags":["comfort","warm","cheesy","snack"],   "category":"Garlic Loaf"},
    {"name":"Chocolate Waffle AE",    "place":"Alpine Espresso","price":160, "tags":["sweet","indulgent","comfort","fun"], "category":"Dessert"},
    {"name":"Brownie AE",             "place":"Alpine Espresso","price":110, "tags":["sweet","comfort","indulgent","quick"],"category":"Dessert"},
    {"name":"Brownie with Ice Cream", "place":"Alpine Espresso","price":170, "tags":["sweet","indulgent","special","fun"], "category":"Dessert"},
    {"name":"Protein Shake AE",       "place":"Alpine Espresso","price":150, "tags":["healthy","energy","protein","fresh"],"category":"Shake"},
    {"name":"Oreo Shake AE",          "place":"Alpine Espresso","price":170, "tags":["sweet","comfort","indulgent","fun"], "category":"Shake"},
    {"name":"Banana Smoothie AE",     "place":"Alpine Espresso","price":200, "tags":["healthy","energy","light","fresh"],  "category":"Smoothie"},
    {"name":"Mango Smoothie AE",      "place":"Alpine Espresso","price":200, "tags":["refreshing","sweet","energy","fresh"],"category":"Smoothie"},
    {"name":"Protein Smoothie AE",    "place":"Alpine Espresso","price":200, "tags":["healthy","energy","protein","special"],"category":"Smoothie"},
    {"name":"Veg Salad AE",           "place":"Alpine Espresso","price":100, "tags":["healthy","fresh","light","cooling"],  "category":"Salad"},
    {"name":"Cornflakes Bowl AE",     "place":"Alpine Espresso","price":80,  "tags":["light","healthy","morning","quick"],  "category":"Breakfast"},

    # ── PIZZA TOWN ──────────────────────────────────────────────────
    {"name":"Aloo Tikki Burger PT",   "place":"Pizza Town","price":39,  "tags":["quick","light","snack","comfort"],      "category":"Burger"},
    {"name":"Veggie Burger PT",       "place":"Pizza Town","price":45,  "tags":["quick","comfort","light","easy"],       "category":"Burger"},
    {"name":"Cheesy Burger PT",       "place":"Pizza Town","price":60,  "tags":["fun","cheesy","filling","indulgent"],   "category":"Burger"},
    {"name":"Paneer Burger PT",       "place":"Pizza Town","price":65,  "tags":["fun","filling","cheesy","comfort"],     "category":"Burger"},
    {"name":"Maharaja Burger PT",     "place":"Pizza Town","price":70,  "tags":["heavy","indulgent","filling","fun"],    "category":"Burger"},
    {"name":"Margherita PT Reg",      "place":"Pizza Town","price":120, "tags":["fun","cheesy","light","classic"],       "category":"Pizza Veg"},
    {"name":"Dbl Cheese Margherita",  "place":"Pizza Town","price":160, "tags":["fun","cheesy","heavy","indulgent"],     "category":"Pizza Veg"},
    {"name":"Farm Fresh PT",          "place":"Pizza Town","price":200, "tags":["fun","fresh","cheesy","heavy"],         "category":"Pizza Veg"},
    {"name":"Achaari Pizza PT",       "place":"Pizza Town","price":200, "tags":["spicy","fun","heavy","indulgent"],      "category":"Pizza Veg"},
    {"name":"Veg Deluxe PT",          "place":"Pizza Town","price":240, "tags":["fun","heavy","cheesy","indulgent"],     "category":"Pizza Veg"},
    {"name":"Mix Veg Pizza PT",       "place":"Pizza Town","price":260, "tags":["fun","heavy","cheesy","indulgent"],     "category":"Pizza Veg"},
    {"name":"Tomato Single Pizza",    "place":"Pizza Town","price":79,  "tags":["fun","cheesy","light","quick"],         "category":"Mini Pizza"},
    {"name":"Onion Single Pizza",     "place":"Pizza Town","price":79,  "tags":["fun","cheesy","light","quick"],         "category":"Mini Pizza"},
    {"name":"Red Sauce Pasta PT",     "place":"Pizza Town","price":100, "tags":["comfort","tangy","filling","warm"],     "category":"Pasta"},
    {"name":"White Sauce Pasta PT",   "place":"Pizza Town","price":100, "tags":["comfort","creamy","filling","warm"],    "category":"Pasta"},
    {"name":"Makhani Pasta PT",       "place":"Pizza Town","price":130, "tags":["rich","comfort","warm","indulgent"],    "category":"Pasta"},
    {"name":"Grilled Sandwich PT",    "place":"Pizza Town","price":60,  "tags":["comfort","warm","quick","light"],       "category":"Sandwich"},
    {"name":"Zingy Parcel PT",        "place":"Pizza Town","price":40,  "tags":["quick","spicy","snack","light"],        "category":"Sides"},
    {"name":"Salted Fries PT",        "place":"Pizza Town","price":60,  "tags":["comfort","quick","snack","light"],      "category":"Fries"},
    {"name":"Masala Fries PT",        "place":"Pizza Town","price":70,  "tags":["spicy","fun","snack","comfort"],        "category":"Fries"},
    {"name":"Peri Peri Fries PT",     "place":"Pizza Town","price":88,  "tags":["spicy","fun","snack","indulgent"],      "category":"Fries"},
    {"name":"Garlic Bread PT",        "place":"Pizza Town","price":80,  "tags":["comfort","warm","snack","quick"],       "category":"Breads"},
    {"name":"Stuff Garlic Bread PT",  "place":"Pizza Town","price":100, "tags":["cheesy","comfort","warm","filling"],    "category":"Breads"},
    {"name":"Aloo Tikki Wrap PT",     "place":"Pizza Town","price":80,  "tags":["quick","comfort","light","filling"],    "category":"Wraps"},
    {"name":"Paneer Wrap PT",         "place":"Pizza Town","price":90,  "tags":["filling","comfort","quick","cheesy"],   "category":"Wraps"},
    {"name":"Strawberry Shake PT",    "place":"Pizza Town","price":70,  "tags":["refreshing","sweet","light","fun"],     "category":"Shake"},
    {"name":"Chocolate Shake PT",     "place":"Pizza Town","price":70,  "tags":["comfort","sweet","indulgent","fun"],    "category":"Shake"},
    {"name":"Cold Coffee PT",         "place":"Pizza Town","price":70,  "tags":["energy","refreshing","quick","fun"],    "category":"Drinks"},
    {"name":"Veg Fried Rice PT",      "place":"Pizza Town","price":90,  "tags":["comfort","filling","quick","fun"],      "category":"Chinese"},
    {"name":"Hakka Noodles PT",       "place":"Pizza Town","price":90,  "tags":["fun","spicy","filling","comfort"],      "category":"Chinese"},

    # ── LAZIZ PIZZA ─────────────────────────────────────────────────
    {"name":"Pizza Mania Classic S",  "place":"Laziz Pizza","price":49,  "tags":["fun","cheesy","light","value"],        "category":"Pizza Mania"},
    {"name":"Pizza Mania Onion",      "place":"Laziz Pizza","price":69,  "tags":["fun","cheesy","light","quick"],        "category":"Pizza Mania"},
    {"name":"Pizza Mania Golden Corn","place":"Laziz Pizza","price":89,  "tags":["fun","cheesy","light","sweet"],        "category":"Pizza Mania"},
    {"name":"Margherita S LZ",        "place":"Laziz Pizza","price":149, "tags":["fun","cheesy","light","classic"],      "category":"Pizza Classic"},
    {"name":"Margherita M LZ",        "place":"Laziz Pizza","price":199, "tags":["fun","cheesy","filling","comfort"],    "category":"Pizza Classic"},
    {"name":"Peri Peri Margherita S", "place":"Laziz Pizza","price":159, "tags":["spicy","fun","cheesy","indulgent"],    "category":"Pizza Classic"},
    {"name":"Vibrant Trio M LZ",      "place":"Laziz Pizza","price":249, "tags":["fun","cheesy","heavy","indulgent"],    "category":"Pizza Premium"},
    {"name":"Mexican Pizza M LZ",     "place":"Laziz Pizza","price":289, "tags":["spicy","fun","heavy","indulgent"],     "category":"Pizza Spicy"},
    {"name":"King of Hell S LZ",      "place":"Laziz Pizza","price":229, "tags":["very spicy","fun","heavy","extreme"],  "category":"Pizza Spicy"},
    {"name":"Unlimited Fri Buffet LZ","place":"Laziz Pizza","price":190, "tags":["value","fun","heavy","special"],      "category":"Special"},
    {"name":"Veg Fusion Burger LZ",   "place":"Laziz Pizza","price":85,  "tags":["fun","filling","quick","comfort"],    "category":"Burger"},
    {"name":"White Sauce Pasta LZ",   "place":"Laziz Pizza","price":149, "tags":["comfort","creamy","filling","warm"],  "category":"Pasta"},
    {"name":"Cheese Burst Garlic LZ", "place":"Laziz Pizza","price":149, "tags":["cheesy","comfort","warm","snack"],    "category":"Garlic Bread"},
    {"name":"Veg Grill Sandwich LZ",  "place":"Laziz Pizza","price":129, "tags":["comfort","warm","quick","filling"],   "category":"Sandwich"},
    {"name":"Laziz Veg Thali",        "place":"Laziz Pizza","price":150, "tags":["filling","comfort","value","complete"],"category":"Thali"},

    # ── DOMINO'S ────────────────────────────────────────────────────
    {"name":"Pizza Mania Classic Dom","place":"Domino's","price":49,  "tags":["fun","cheesy","light","value"],          "category":"Pizza Mania"},
    {"name":"Pizza Mania Onion Dom",  "place":"Domino's","price":69,  "tags":["fun","cheesy","light","quick"],          "category":"Pizza Mania"},
    {"name":"Pizza Mania Capsicum",   "place":"Domino's","price":85,  "tags":["fun","cheesy","light","quick"],          "category":"Pizza Mania"},
    {"name":"Margherita Dom Reg",     "place":"Domino's","price":109, "tags":["fun","cheesy","light","classic"],        "category":"Classic Pizza"},
    {"name":"Farmhouse Dom Med",      "place":"Domino's","price":319, "tags":["fun","cheesy","heavy","indulgent"],      "category":"Classic Pizza"},
    {"name":"Veg Extravaganza Dom",   "place":"Domino's","price":289, "tags":["fun","heavy","cheesy","indulgent"],      "category":"Classic Pizza"},
    {"name":"Cheese Overload Dom",    "place":"Domino's","price":349, "tags":["fun","cheesy","heavy","indulgent"],      "category":"Classic Pizza"},
    {"name":"Garlic Breadsticks Dom", "place":"Domino's","price":105, "tags":["comfort","warm","cheesy","snack"],       "category":"Sides"},
    {"name":"Zingy Parcel Dom",       "place":"Domino's","price":109, "tags":["quick","spicy","snack","light"],         "category":"Sides"},
    {"name":"Choco Lava Cake Dom",    "place":"Domino's","price":109, "tags":["sweet","indulgent","comfort","special"], "category":"Dessert"},
    {"name":"Lunch Feast 99 Dom",     "place":"Domino's","price":99,  "tags":["value","filling","fun","quick"],         "category":"Special"},
    {"name":"Meal for 1 Dom",         "place":"Domino's","price":199, "tags":["value","filling","fun","complete"],      "category":"Combo"},
    {"name":"Spicy Chicken Pops Dom", "place":"Domino's","price":109, "tags":["spicy","fun","quick","snack"],           "category":"Chicken Feast"},
]

# ═══════════════════════════════════════════════════════════
# TASK 2: TEXT PREPARATION
# ═══════════════════════════════════════════════════════════
def food_to_text(food: dict) -> str:
    tags_str = " ".join(food["tags"])
    return (
        f"{food['name']}, available at {food['place']}, "
        f"price Rs {food['price']}, tags: {tags_str}, "
        f"category: {food['category']}"
    )

# ═══════════════════════════════════════════════════════════
# TASK 3 + 4: EMBEDDINGS + CHROMADB
# ═══════════════════════════════════════════════════════════
print("Loading embedding model (all-MiniLM-L6-v2)...")
model      = SentenceTransformer("all-MiniLM-L6-v2")
client     = chromadb.Client()
collection = client.get_or_create_collection("shoolini_food_db")


def build_database():
    if collection.count() > 0:
        print(f"DB ready: {collection.count()} items across {len(RESTAURANTS)} restaurants.")
        return
    print(f"Building DB: {len(foods)} items from {len(RESTAURANTS)} restaurants...")
    texts      = [food_to_text(f) for f in foods]
    embeddings = model.encode(texts).tolist()
    for i, (food, text, emb) in enumerate(zip(foods, texts, embeddings)):
        r = RESTAURANTS.get(food["place"], {})
        collection.add(
            documents  = [text],
            embeddings = [emb],
            metadatas  = [{
                "name"        : food["name"],
                "place"       : food["place"],
                "price"       : food["price"],
                "tags"        : ", ".join(food["tags"]),
                "category"    : food["category"],
                "location"    : r.get("location", "Near Shoolini University"),
                "distance_km" : r.get("distance_km", 0.5),
                "timing"      : r.get("timing", "All day"),
                "delivery"    : str(r.get("delivery", False)),
            }],
            ids = [str(i + 1)]
        )
    print(f"✅ DB ready: {collection.count()} items.")


# ═══════════════════════════════════════════════════════════
# TASK 5 + 6 + 7: SEARCH FUNCTION
# ═══════════════════════════════════════════════════════════
def search_foods(
    food_intent  : list,
    budget       : int  = None,
    cuisine      : str  = None,
    place        : str  = None,
    delivery_only: bool = False,
    n_candidates : int  = 25,
    top_n        : int  = 3,
) -> list:
    """
    Main function called by Person 2 and Person 4.

    Parameters
    ----------
    food_intent   : mood tags e.g. ["comfort","warm","light"]
    budget        : max price in Rs. None = no filter.
    cuisine       : category keyword e.g. "Pizza", "Maggi", "South Indian"
    place         : specific restaurant name filter
    delivery_only : if True, return only places with delivery
    top_n         : how many results to return (default 3)

    Returns
    -------
    list of dicts: name, place, price, tags, category,
                   location, distance_km, timing, delivery, value_score
    """
    query = " ".join(food_intent)
    print(f"\n🔍 '{query}' | Budget:₹{budget} | Cuisine:{cuisine} | Place:{place} | Delivery:{delivery_only}")

    q_emb      = model.encode([query]).tolist()
    results    = collection.query(query_embeddings=q_emb,
                                  n_results=min(n_candidates, collection.count()))
    candidates = results["metadatas"][0]

    if budget is not None:
        candidates = [f for f in candidates if int(f["price"]) <= budget]

    if cuisine:
        filtered = [f for f in candidates
                    if cuisine.lower() in f["category"].lower()
                    or cuisine.lower() in f["tags"].lower()
                    or cuisine.lower() in f["name"].lower()]
        if filtered:
            candidates = filtered

    if place:
        filtered = [f for f in candidates if place.lower() in f["place"].lower()]
        if filtered:
            candidates = filtered

    if delivery_only:
        candidates = [f for f in candidates if f["delivery"] == "True"]

    cap = budget if budget else 300
    for f in candidates:
        f["value_score"] = round((cap - int(f["price"])) / cap * 100, 1) if cap > 0 else 0

    top = candidates[:top_n]
    print(f"✅ Top {len(top)} results:")
    for item in top:
        print(f"   → {item['name']} | ₹{item['price']} | {item['place']} | {item['location']}")
    return top


# ═══════════════════════════════════════════════════════════
# BONUS: PRICE COMPARISON ACROSS RESTAURANTS
# ═══════════════════════════════════════════════════════════
def compare_prices(dish_keyword: str) -> list:
    """Find all places serving a dish, sorted cheapest first."""
    matches = [f for f in foods
               if dish_keyword.lower() in f["name"].lower()
               or dish_keyword.lower() in f["category"].lower()]
    matches.sort(key=lambda x: x["price"])
    print(f"\n💰 Price comparison: '{dish_keyword}' ({len(matches)} options)")
    for m in matches:
        print(f"   ₹{m['price']:>4} | {m['name']:<38} | {m['place']}")
    return matches


def cheapest_in_category(category: str, budget: int = None) -> list:
    """Find cheapest items in a category across all restaurants."""
    matches = [f for f in foods if category.lower() in f["category"].lower()]
    if budget:
        matches = [f for f in matches if f["price"] <= budget]
    matches.sort(key=lambda x: x["price"])
    print(f"\n🏷️  Cheapest '{category}' items:")
    for m in matches[:5]:
        print(f"   ₹{m['price']:>4} | {m['name']:<38} | {m['place']}")
    return matches


# ═══════════════════════════════════════════════════════════
# TASK 10: TESTS
# ═══════════════════════════════════════════════════════════
def run_tests():
    print("\n" + "="*60)
    print("  TASK 10: TEST CASES — All 16 Restaurants")
    print("="*60)

    tests = [
        {"desc":"😴 Tired + tiny budget ≤ ₹30",           "food_intent":["comfort","quick","light","easy"],         "budget":30,  "expected":"Maggi, chai, tea"},
        {"desc":"😰 Stressed + warm comfort ≤ ₹80",        "food_intent":["comfort","warm","soothing","light"],      "budget":80,  "expected":"soup, thupka, chai"},
        {"desc":"🥳 Celebrating + no budget limit",         "food_intent":["indulgent","heavy","cheesy","fun"],       "budget":400, "expected":"pizza, pasta, burger"},
        {"desc":"🌅 Breakfast ≤ ₹50",                       "food_intent":["morning","filling","warm","comfort"],     "budget":50,  "expected":"paratha, poha"},
        {"desc":"😤 Spicy craving ≤ ₹120",                  "food_intent":["spicy","fun","snack"],                    "budget":120, "expected":"momos, chilli potato, fries"},
        {"desc":"💪 Healthy + energy + juices only",        "food_intent":["healthy","fresh","energy","light"],       "budget":100, "place":"Chaudhary Juice Corner", "expected":"juice, shake"},
        {"desc":"🍕 Pizza specifically ≤ ₹150",             "food_intent":["fun","cheesy","indulgent"],               "budget":150, "cuisine":"Pizza", "expected":"pizza options ≤150"},
        {"desc":"☕ Chai craving, best chai places",        "food_intent":["comfort","warm","soothing","quick"],      "budget":50,  "cuisine":"Chai", "expected":"chai from Cheers to Chai, Nescafe, WNR"},
        {"desc":"🏠 Delivery only, late night ≤ ₹150",     "food_intent":["comfort","filling","quick"],              "budget":150, "delivery_only":True, "expected":"Chai Vyanjan, Kiyansh, Dominos"},
        {"desc":"💰 Value thali ≤ ₹100",                   "food_intent":["filling","complete","value","comfort"],   "budget":100, "cuisine":"Thali", "expected":"thali options"},
    ]

    for tc in tests:
        print(f"\n📌 {tc['desc']}")
        print(f"   Expected: {tc['expected']}")
        search_foods(
            food_intent   = tc["food_intent"],
            budget        = tc.get("budget"),
            cuisine       = tc.get("cuisine"),
            place         = tc.get("place"),
            delivery_only = tc.get("delivery_only", False),
        )

    print("\n" + "="*60)
    print("  BONUS: PRICE COMPARISONS")
    print("="*60)
    compare_prices("maggi")
    compare_prices("momos")
    compare_prices("chai")
    cheapest_in_category("Pizza", budget=150)
    cheapest_in_category("Thali", budget=100)


# ═══════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    build_database()
    run_tests()
