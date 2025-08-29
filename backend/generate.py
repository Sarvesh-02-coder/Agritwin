import csv
import random
from pathlib import Path

# Path to your existing CSV
DATA_DIR = Path(__file__).resolve().parents[1] / "ml" / "data"
CSV_PATH = DATA_DIR / "pest_disease.csv"

# Crops, pests, diseases
crops = {
    "wheat": {
        "pests": ["aphids", "armyworm", "stem sawfly", "cutworm", "thrips"],
        "diseases": ["rust", "leaf blight", "loose smut", "root rot", "alternaria blight"]
    },
    "rice": {
        "pests": ["brown planthopper", "stem borer", "gall midge", "leaf folder", "hispa", "leaf hopper"],
        "diseases": ["blast", "bacterial leaf blight", "sheath blight", "leaf streak"]
    },
    "maize": {
        "pests": ["stem borer", "shoot fly", "fall armyworm", "cob borer", "corn earworm"],
        "diseases": ["turcicum leaf blight", "downy mildew", "stalk rot", "charcoal rot", "rust"]
    },
    "tomato": {
        "pests": ["fruit borer", "whitefly", "thrips", "cutworm", "leaf miner", "aphids"],
        "diseases": ["early blight", "leaf curl", "late blight", "damping off", "septoria leaf spot", "nematode"]
    },
    "potato": {
        "pests": ["cutworm", "aphids", "tuber moth", "thrips", "leaf hopper"],
        "diseases": ["late blight", "early blight", "black scurf", "scab", "alternaria leaf spot"]
    },
    "cotton": {
        "pests": ["bollworm", "aphids", "whitefly", "jassids", "thrips", "armyworm"],
        "diseases": ["leaf curl virus", "root rot", "anthracnose", "leaf spot", "bacterial blight"]
    },
    "sugarcane": {
        "pests": ["early shoot borer", "internode borer", "scale insect", "top borer", "mealybug"],
        "diseases": ["red rot", "wilt", "grassy shoot", "smut", "sett rot"]
    },
    "onion": {
        "pests": ["thrips", "cutworm", "aphids", "leaf miner", "mites", "bulb fly"],
        "diseases": ["purple blotch", "downy mildew", "basal rot", "anthracnose", "stemphylium blight", "soft rot"]
    }
}

seasons = ["rabi", "kharif", "zaid"]

notes_pool = [
    "Favored by high humidity",
    "Outbreak after heavy rainfall",
    "Worsens under irrigated conditions",
    "More common in cool dry weather",
    "Thrives in cloudy conditions",
    "Peaks in warm humid environments",
    "Rapid spread during high temperature",
    "Serious loss if untreated"
]

# How many new rows to add?
NEW_ROWS = 300   # change this number if you want more/less

new_data = []
for _ in range(NEW_ROWS):
    crop = random.choice(list(crops.keys()))
    season = random.choice(seasons)
    pest = random.choice(crops[crop]["pests"])
    disease = random.choice(crops[crop]["diseases"])

    # Realistic ranges
    tmin = random.randint(10, 25)
    tmax = random.randint(tmin + 5, tmin + 15)
    hmin = random.randint(50, 65)
    hmax = random.randint(hmin + 10, hmin + 25)

    note = random.choice(notes_pool)

    new_data.append([crop, season, pest, disease, tmin, tmax, hmin, hmax, note])

# Append rows to existing CSV
with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(new_data)

print(f"✅ Added {len(new_data)} new rows to {CSV_PATH}")
