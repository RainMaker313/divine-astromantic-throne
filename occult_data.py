#!/usr/bin/env python3
"""
Coco's Divine Astromantic Throne — Occult & Magical Databases
=============================================================
Planetary Hours (fixed), Essential Dignities, Arabic Parts,
Lunar Mansions, Fixed Stars, Planetary Intelligences & Spirits,
Electional Scoring, Aspect Interpretations.

Data sourced from: Ptolemy, Lilly, Agrippa, Picatrix, Bonatti,
al-Biruni, William Ramesey, and the Hermetic tradition.
"""

# ===========================================================================
# PLANETARY HOURS — Chaldean order, continuous 24-hour sequence
# ===========================================================================

# Day rulers: Sunday=Sun, Monday=Moon, Tuesday=Mars, Wednesday=Mercury,
#             Thursday=Jupiter, Friday=Venus, Saturn=Saturday
DAY_RULERS = {
    6: "Sun",
    0: "Moon",
    1: "Mars",
    2: "Mercury",
    3: "Jupiter",
    4: "Venus",
    5: "Saturn",
}

# Chaldean order — the eternal sequence of planetary hours
CHALDEAN = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

# Planet emojis/symbols
PLANET_SYMBOL = {
    "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀",
    "Mars": "♂", "Jupiter": "♃", "Saturn": "♄",
    "Uranus": "⛢", "Neptune": "♆", "Pluto": "♇",
}

# Planet nature / temperament
PLANET_NATURE = {
    "Sun":     {"nature": "diurnal",  "temperament": "hot_moist",  "element": "fire"},
    "Moon":    {"nature": "nocturnal", "temperament": "cold_moist", "element": "water"},
    "Mercury": {"nature": "neutral",  "temperament": "variable",   "element": "air"},
    "Venus":   {"nature": "nocturnal", "temperament": "cold_moist", "element": "water"},
    "Mars":    {"nature": "nocturnal", "temperament": "hot_dry",    "element": "fire"},
    "Jupiter": {"nature": "diurnal",  "temperament": "hot_moist",  "element": "air"},
    "Saturn":  {"nature": "diurnal",  "temperament": "cold_dry",   "element": "earth"},
}

PLANET_KEYWORDS = {
    "Sun":     ["authority", "success", "promotion", "illumination", "crown", "gold"],
    "Moon":    ["travel", "messages", "fluids", "cycles", "public", "dreams", "memory"],
    "Mercury": ["communication", "trade", "study", "writing", "contracts", "trickery", "theft"],
    "Venus":   ["love", "art", "music", "friendship", "pleasure", "harmony", "beauty", "social"],
    "Mars":    ["war", "courage", "conflict", "surgery", "iron", "fire", "competition", "victory"],
    "Jupiter": ["wealth", "law", "religion", "expansion", "luck", "mercy", "healing", "diplomacy"],
    "Saturn":  ["binding", "limitation", "death", "time", "structures", "real_estate", "old_age", "discipline"],
}

PLANET_BENEFIC = {
    "Sun": "neutral", "Moon": "benefic", "Mercury": "neutral",
    "Venus": "benefic", "Mars": "malefic", "Jupiter": "benefic", "Saturn": "malefic",
}


# ===========================================================================
# ESSENTIAL DIGNITIES — Ptolemy's system (domicile, exaltation, triplicity, term, face)
# ===========================================================================

DOMICILE = {
    "Sun":     ["Leo"],
    "Moon":    ["Cancer"],
    "Mercury": ["Gemini", "Virgo"],
    "Venus":   ["Taurus", "Libra"],
    "Mars":    ["Aries", "Scorpio"],
    "Jupiter": ["Sagittarius", "Pisces"],
    "Saturn":  ["Capricorn", "Aquarius"],
    "Uranus":  ["Aquarius"],
    "Neptune": ["Pisces"],
    "Pluto":   ["Scorpio"],
}

DETRIMENT = {
    "Sun":     ["Aquarius"],
    "Moon":    ["Capricorn"],
    "Mercury": ["Sagittarius", "Pisces"],
    "Venus":   ["Scorpio", "Aries"],
    "Mars":    ["Libra", "Taurus"],
    "Jupiter": ["Gemini", "Virgo"],
    "Saturn":  ["Cancer", "Leo"],
}

EXALTATION = {
    "Sun":     ("Aries", 19),
    "Moon":    ("Taurus", 3),
    "Mercury": ("Virgo", 15),
    "Venus":   ("Pisces", 27),
    "Mars":    ("Capricorn", 28),
    "Jupiter": ("Cancer", 15),
    "Saturn":  ("Libra", 21),
}

FALL = {
    "Sun":     ("Libra", 19),
    "Moon":    ("Scorpio", 3),
    "Mercury": ("Pisces", 15),
    "Venus":   ("Virgo", 27),
    "Mars":    ("Cancer", 28),
    "Jupiter": ("Capricorn", 15),
    "Saturn":  ("Aries", 21),
}

SIGN_TRIPLICITY = {
    "Aries":       {"day": "Sun",   "night": "Jupiter"},
    "Leo":         {"day": "Sun",   "night": "Jupiter"},
    "Sagittarius": {"day": "Sun",   "night": "Jupiter"},
    "Taurus":      {"day": "Venus", "night": "Moon"},
    "Virgo":       {"day": "Venus", "night": "Moon"},
    "Capricorn":   {"day": "Venus", "night": "Moon"},
    "Gemini":      {"day": "Saturn","night": "Mercury"},
    "Libra":       {"day": "Saturn","night": "Mercury"},
    "Aquarius":    {"day": "Saturn","night": "Mercury"},
    "Cancer":      {"day": "Venus", "night": "Mars"},
    "Scorpio":     {"day": "Venus", "night": "Mars"},
    "Pisces":      {"day": "Venus", "night": "Mars"},
}

# Terms (Egyptian boundaries) — per sign: list of (end_degree, planet)
TERMS_EGYPTIAN = {
    "Aries":       [(6, "Jupiter"), (8, "Venus"), (14, "Mercury"), (21, "Mars"), (26, "Saturn"), (30, "Jupiter")],
    "Taurus":      [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")],
    "Gemini":      [(6, "Mercury"), (12, "Jupiter"), (17, "Venus"), (24, "Mars"), (30, "Saturn")],
    "Cancer":      [(7, "Mars"), (13, "Jupiter"), (20, "Mercury"), (27, "Venus"), (30, "Saturn")],
    "Leo":         [(6, "Saturn"), (11, "Mercury"), (18, "Jupiter"), (24, "Venus"), (30, "Mars")],
    "Virgo":       [(7, "Mercury"), (13, "Venus"), (18, "Jupiter"), (25, "Saturn"), (30, "Mars")],
    "Libra":       [(6, "Venus"), (10, "Jupiter"), (19, "Mercury"), (24, "Mars"), (30, "Saturn")],
    "Scorpio":     [(7, "Mars"), (14, "Jupiter"), (21, "Venus"), (27, "Mercury"), (30, "Saturn")],
    "Sagittarius": [(12, "Jupiter"), (17, "Venus"), (24, "Mercury"), (29, "Saturn"), (30, "Mars")],
    "Capricorn":   [(7, "Jupiter"), (14, "Venus"), (22, "Mercury"), (26, "Mars"), (30, "Saturn")],
    "Aquarius":    [(7, "Jupiter"), (13, "Mercury"), (20, "Venus"), (26, "Saturn"), (30, "Mars")],
    "Pisces":      [(12, "Venus"), (16, "Jupiter"), (21, "Mercury"), (25, "Mars"), (30, "Saturn")],
}

# Faces (Decans) — 3 per sign of 10 degrees each
FACES = {
    "Aries":       ["Mars",    "Sun",     "Venus"],
    "Taurus":      ["Mercury", "Moon",    "Saturn"],
    "Gemini":      ["Jupiter", "Mars",    "Sun"],
    "Cancer":      ["Venus",   "Mercury", "Moon"],
    "Leo":         ["Saturn",  "Jupiter", "Mars"],
    "Virgo":       ["Sun",     "Venus",   "Mercury"],
    "Libra":       ["Moon",    "Saturn",  "Jupiter"],
    "Scorpio":     ["Mars",    "Sun",     "Venus"],
    "Sagittarius": ["Mercury", "Moon",    "Saturn"],
    "Capricorn":   ["Jupiter", "Mars",    "Sun"],
    "Aquarius":    ["Venus",   "Mercury", "Moon"],
    "Pisces":      ["Saturn",  "Jupiter", "Mars"],
}

DIGNITY_SCORES = {
    "domicile":   5,
    "exaltation": 4,
    "triplicity": 3,
    "term":       2,
    "face":       1,
    "detriment": -5,
    "fall":      -4,
}


# ===========================================================================
# ARABIC PARTS (Lots)
# ===========================================================================

ARABIC_PARTS = {
    "Part_of_Fortune": {
        "name": "Part of Fortune",
        "symbol": "⊗",
        "formula_day": "Asc + Moon - Sun",
        "formula_night": "Asc + Sun - Moon",
        "keywords": ["fortune", "health", "wealth", "material_success", "luck"],
        "description": "The most important lot. Material fortune and physical well-being.",
    },
    "Part_of_Spirit": {
        "name": "Part of Spirit",
        "symbol": "⊕",
        "formula_day": "Asc + Sun - Moon",
        "formula_night": "Asc + Moon - Sun",
        "keywords": ["spirit", "soul", "purpose", "will", "consciousness"],
        "description": "The converse of Fortune. Spirit's intention, chosen path.",
    },
    "Part_of_Marriage": {
        "name": "Part of Marriage",
        "symbol": "",
        "formula_day": "Asc + DC7 - Venus",
        "formula_night": "Asc + DC7 - Venus",
        "keywords": ["marriage", "partnership", "contracts", "union"],
        "description": "Lilly's part for marriage and partnerships.",
    },
    "Part_of_Father": {
        "name": "Part of Father",
        "symbol": "",
        "formula_day": "Asc + Saturn - Sun",
        "formula_night": "Asc + Sun - Saturn",
        "keywords": ["father", "authority", "inheritance", "elders"],
        "description": "Shows the father and authority figures.",
    },
    "Part_of_Mother": {
        "name": "Part of Mother",
        "symbol": "",
        "formula_day": "Asc + Moon - Venus",
        "formula_night": "Asc + Venus - Moon",
        "keywords": ["mother", "family", "property", "nurturing"],
        "description": "Shows the mother and maternal influences.",
    },
    "Part_of_Children": {
        "name": "Part of Children",
        "symbol": "",
        "formula_day": "Asc + Jupiter - Saturn",
        "formula_night": "Asc + Saturn - Jupiter",
        "keywords": ["children", "offspring", "creativity", "legacy"],
        "description": "Indicates children and creative output.",
    },
    "Part_of_Brothers": {
        "name": "Part of Brothers",
        "symbol": "",
        "formula_day": "Asc + Saturn - Jupiter",
        "formula_night": "Asc + Jupiter - Saturn",
        "keywords": ["siblings", "relatives", "neighbors"],
        "description": "Shows siblings and close relatives.",
    },
    "Part_of_Travel": {
        "name": "Part of Travel",
        "symbol": "",
        "formula_day": "Asc + 12th_cusp - Moon",
        "formula_night": "Asc + Moon - 12th_cusp",
        "keywords": ["travel", "journeys", "foreign", "migration"],
        "description": "Long-distance travel and foreign affairs.",
    },
    "Part_of_Sickness": {
        "name": "Part of Sickness",
        "symbol": "",
        "formula_day": "Asc + Mars - Saturn",
        "formula_night": "Asc + Saturn - Mars",
        "keywords": ["illness", "disease", "weakness", "chronic"],
        "description": "Illness and chronic conditions.",
    },
    "Part_of_Death": {
        "name": "Part of Death",
        "symbol": "",
        "formula_day": "Asc + 8th_cusp - Moon",
        "formula_night": "Asc + Moon - 8th_cusp",
        "keywords": ["death", "transformation", "fear", "crisis"],
        "description": "A dark lot. Transformation through crisis.",
    },
    "Part_of_Honor": {
        "name": "Part of Honor",
        "symbol": "",
        "formula_day": "Asc + Sun - Saturn",
        "formula_night": "Asc + Saturn - Sun",
        "keywords": ["honor", "reputation", "status", "recognition"],
        "description": "Worldly honor and reputation.",
    },
    "Part_of_Profit": {
        "name": "Part of Profit",
        "symbol": "",
        "formula_day": "Asc + Jupiter - Part_of_Fortune",
        "formula_night": "Asc + Part_of_Fortune - Jupiter",
        "keywords": ["profit", "success", "gain", "advancement"],
        "description": "Material success and gain.",
    },
}


# ===========================================================================
# LUNAR MANSIONS — 28 Stations of the Moon (Arabic Manzil)
# ===========================================================================

# Based on classical Arabic system with Picatrix attributions
# Starting from 0 Aries = Al-Sharatain (beta-gamma Arietis)
LUNAR_MANSIONS = [
    {
        "number": 1, "name": "Al-Sharatain", "start_sign": "Aries", "start_deg": 0.0,
        "ruled_by": "Mars", "nature": "malefic",
        "keywords": ["destruction", "division", "beginnings", "separation"],
        "magical": "Destroying enemies, dividing lovers, beginning ventures.",
        "picatrix": "For destroying and for separation. Good for journeys.",
    },
    {
        "number": 2, "name": "Al-Butain", "start_sign": "Taurus", "start_deg": 12.857,
        "ruled_by": "Venus", "nature": "benefic",
        "keywords": ["love", "union", "hidden_treasures", "digging"],
        "magical": "Love, friendship, finding hidden things, excavation.",
        "picatrix": "For love and friendship, finding what is hidden.",
    },
    {
        "number": 3, "name": "Al-Thurayya", "start_sign": "Gemini", "start_deg": 25.714,
        "ruled_by": "Sun", "nature": "benefic",
        "keywords": ["abundance", "profit", "fire", "messengers"],
        "magical": "Trade profit, fire-working, aiding messengers.",
        "picatrix": "For making a thing to grow, for profit and fire.",
    },
    {
        "number": 4, "name": "Al-Dabaran", "start_sign": "Cancer", "start_deg": 38.571,
        "ruled_by": "Mercury", "nature": "malefic",
        "keywords": ["hatred", "strife", "discord", "poison"],
        "magical": "Creating enmity, planting discord between people.",
        "picatrix": "For causing hatred and discord between people.",
    },
    {
        "number": 5, "name": "Al-Haqa", "start_sign": "Leo", "start_deg": 51.429,
        "ruled_by": "Mars", "nature": "benefic",
        "keywords": ["honor", "learning", "virtue", "teaching"],
        "magical": "Acquiring knowledge, gaining respect, scholarship.",
        "picatrix": "For learning the sciences and for knowledge and virtue.",
    },
    {
        "number": 6, "name": "Al-Hana", "start_sign": "Virgo", "start_deg": 64.286,
        "ruled_by": "Jupiter", "nature": "malefic",
        "keywords": ["harm", "love_reverse", "destruction_of_enemies"],
        "magical": "Destroying enemies.",
        "picatrix": "For the destruction of enemies.",
    },
    {
        "number": 7, "name": "Al-Dhira", "start_sign": "Libra", "start_deg": 77.143,
        "ruled_by": "Venus", "nature": "benefic",
        "keywords": ["love", "friendship", "good_desire", "union"],
        "magical": "Drawing people together, ensuring good outcomes.",
        "picatrix": "For love and friendship, for all good desires.",
    },
    {
        "number": 8, "name": "Al-Nathrah", "start_sign": "Scorpio", "start_deg": 90.0,
        "ruled_by": "Mercury", "nature": "malefic",
        "keywords": ["birds", "hunting", "binding", "capturing"],
        "magical": "Catching birds, binding secrets.",
        "picatrix": "For causing birds to gather, for love.",
    },
    {
        "number": 9, "name": "Al-Tarf", "start_sign": "Sagittarius", "start_deg": 102.857,
        "ruled_by": "Moon", "nature": "malefic",
        "keywords": ["sickness", "infirmity", "destruction", "weakness"],
        "magical": "Causing weakness, delaying things.",
        "picatrix": "For infirmity and destruction of anything.",
    },
    {
        "number": 10, "name": "Al-Jabhah", "start_sign": "Capricorn", "start_deg": 115.714,
        "ruled_by": "Sun", "nature": "malefic",
        "keywords": ["desired_things", "love", "healing", "travel"],
        "magical": "Obtaining desired things, healing, safe travel.",
        "picatrix": "For obtaining whatever is desired, for healing.",
    },
    {
        "number": 11, "name": "Al-Zubrah", "start_sign": "Aquarius", "start_deg": 128.571,
        "ruled_by": "Jupiter", "nature": "benefic",
        "keywords": ["liberation", "prison", "trade", "profit"],
        "magical": "Freeing prisoners, trade profit.",
        "picatrix": "For freeing captives, for profit in trade.",
    },
    {
        "number": 12, "name": "Al-Sarfah", "start_sign": "Pisces", "start_deg": 141.429,
        "ruled_by": "Saturn", "nature": "malefic",
        "keywords": ["marriage_pregnancy", "separation", "animals"],
        "magical": "Benefic for marriage/pregnancy, malefic for separation.",
        "picatrix": "For marriage and pregnancy. For separation of lovers.",
    },
    {
        "number": 13, "name": "Al-Awwa", "start_sign": "Aries", "start_deg": 154.286,
        "ruled_by": "Jupiter", "nature": "benefic",
        "keywords": ["love", "union", "trade", "travel", "healing"],
        "magical": "Love, trade, safe journeys, healing. Very benefic.",
        "picatrix": "For love, good will, trade, safe travel, healing.",
    },
    {
        "number": 14, "name": "Al-Simak", "start_sign": "Taurus", "start_deg": 167.143,
        "ruled_by": "Venus", "nature": "benefic",
        "keywords": ["love", "friendship", "reconciliation", "abandoned"],
        "magical": "Love, reconciliation, helping abandoned people.",
        "picatrix": "For love and friendship, calling the abandoned back.",
    },
    {
        "number": 15, "name": "Al-Ghafr", "start_sign": "Gemini", "start_deg": 180.0,
        "ruled_by": "Mercury", "nature": "malefic",
        "keywords": ["love_reverse", "destruction", "separation", "poison"],
        "magical": "Destroying things, creating enmity.",
        "picatrix": "For destruction of anything, for causing hatred.",
    },
    {
        "number": 16, "name": "Al-Zubana", "start_sign": "Cancer", "start_deg": 192.857,
        "ruled_by": "Mars", "nature": "benefic",
        "keywords": ["purchase", "selling", "profit", "captives"],
        "magical": "Trade, buying/selling, freeing captives.",
        "picatrix": "For buying and selling and for freeing captives.",
    },
    {
        "number": 17, "name": "Al-Iklil", "start_sign": "Leo", "start_deg": 205.714,
        "ruled_by": "Jupiter", "nature": "malefic",
        "keywords": ["safety", "prisoners", "union", "friendship"],
        "magical": "Friendship, love, freeing prisoners.",
        "picatrix": "For friendship and good union, for safety of prisoners.",
    },
    {
        "number": 18, "name": "Al-Qalb", "start_sign": "Virgo", "start_deg": 218.571,
        "ruled_by": "Mars", "nature": "malefic",
        "keywords": ["enmity", "destruction", "poison", "buildings"],
        "magical": "Enmity, destroying buildings.",
        "picatrix": "For causing enmity, for destroying buildings.",
    },
    {
        "number": 19, "name": "Al-Shaulah", "start_sign": "Libra", "start_deg": 231.429,
        "ruled_by": "Mercury", "nature": "benefic",
        "keywords": ["travel", "captives", "victory", "profit"],
        "magical": "Safe journeys, freeing captives, victory.",
        "picatrix": "For safe travel, for freeing captives, for victory.",
    },
    {
        "number": 20, "name": "Al-Balda", "start_sign": "Scorpio", "start_deg": 244.286,
        "ruled_by": "Moon", "nature": "benefic",
        "keywords": ["healing", "buildings", "wells", "wives"],
        "magical": "Healing, building, digging wells.",
        "picatrix": "For healing, for building, for digging wells.",
    },
    {
        "number": 21, "name": "Al-Sa'd al-Dhabih", "start_sign": "Sagittarius", "start_deg": 257.143,
        "ruled_by": "Jupiter", "nature": "malefic",
        "keywords": ["union", "enmity", "escape", "flight"],
        "magical": "Union, discord, escaping from danger.",
        "picatrix": "For union, for causing enmity, for escape.",
    },
    {
        "number": 22, "name": "Al-Sa'd al-Bula", "start_sign": "Capricorn", "start_deg": 270.0,
        "ruled_by": "Venus", "nature": "benefic",
        "keywords": ["healing", "destruction", "prisoners"],
        "magical": "Healing, destroying cities, freeing captives.",
        "picatrix": "For healing, for destruction of enemies.",
    },
    {
        "number": 23, "name": "Al-Sa'd al-Su'ud", "start_sign": "Aquarius", "start_deg": 282.857,
        "ruled_by": "Moon", "nature": "malefic",
        "keywords": ["pregnancy", "fruitfulness", "destruction"],
        "magical": "Fertility, pregnancy, but also destruction.",
        "picatrix": "For pregnancy and fruitfulness, for destruction.",
    },
    {
        "number": 24, "name": "Al-Sa'd al-Akhbiya", "start_sign": "Pisces", "start_deg": 295.714,
        "ruled_by": "Saturn", "nature": "malefic",
        "keywords": ["hunting", "destruction", "agriculture", "works"],
        "magical": "Hunting, destruction, agriculture, planned endeavors.",
        "picatrix": "For hunting, for destruction, for planting and works.",
    },
    {
        "number": 25, "name": "Al-Fargh al-Awwal", "start_sign": "Aries", "start_deg": 308.571,
        "ruled_by": "Jupiter", "nature": "benefic",
        "keywords": ["love", "friendship", "safety", "profit", "travel"],
        "magical": "Love, friendship, safety, profit, travel. Highly benefic.",
        "picatrix": "For love and friendship and all good works and profit.",
    },
    {
        "number": 26, "name": "Al-Fargh al-Thani", "start_sign": "Taurus", "start_deg": 321.429,
        "ruled_by": "Venus", "nature": "malefic",
        "keywords": ["enmity", "strength", "buildings", "wells"],
        "magical": "Enmity, strengthening buildings, digging wells.",
        "picatrix": "For causing hatred, for strengthening buildings.",
    },
    {
        "number": 27, "name": "Al-Batn al-Hut", "start_sign": "Gemini", "start_deg": 334.286,
        "ruled_by": "Mercury", "nature": "benefic",
        "keywords": ["plants", "cities", "union", "trade"],
        "magical": "Agriculture, building cities, union, trade.",
        "picatrix": "For planting and for building cities and for union.",
    },
    {
        "number": 28, "name": "Al-Ras al-Hut", "start_sign": "Cancer", "start_deg": 347.143,
        "ruled_by": "Mars", "nature": "malefic",
        "keywords": ["completion", "endings", "binding", "talismans"],
        "magical": "Endings, talismanic completion, binding.",
        "picatrix": "The end of the cycle. For completion and binding.",
    },
]


# ===========================================================================
# FIXED STARS — Behenian Stars + Key Stars
# ===========================================================================

BEHENIAN_STARS = [
    {"name": "Alcyone", "constellation": "Tauri (Pleiades)", "ecliptic_lon_j2000": 0.30,
     "nature": "Moon/Venus", "keywords": ["love", "piercing", "vision"],
     "magical": "Love, obtaining visions, piercing light."},
    {"name": "Algol", "constellation": "Persei", "ecliptic_lon_j2000": 26.30,
     "nature": "Saturn/Jupiter", "keywords": ["violence", "head_loss", "power_through_destruction"],
     "magical": "Honors, will, victory. Infamous for violence and madness."},
    {"name": "Procyon", "constellation": "Canis Minoris", "ecliptic_lon_j2000": 25.83,
     "nature": "Mercury/Mars", "keywords": ["violence", "sudden_rise_and_fall", "success_then_disaster"],
     "magical": "Sudden success but also sudden fall. Quick but unstable."},
    {"name": "Sirius", "constellation": "Canis Majoris", "ecliptic_lon_j2000": 14.17,
     "nature": "Venus/Jupiter", "keywords": ["communication", "ambition", "loyalty", "fame"],
     "magical": "Communication, ambition, loyalty, good will, diplomatic arts."},
    {"name": "Aldebaran", "constellation": "Tauri", "ecliptic_lon_j2000": 9.83,
     "nature": "Mars/Venus", "keywords": ["honor", "wisdom", "riches", "integrity", "faith"],
     "magical": "Honor, wisdom, eloquence, lasting riches. One of four Royal Stars."},
    {"name": "Antares", "constellation": "Scorpii", "ecliptic_lon_j2000": 9.93,
     "nature": "Mars/Jupiter", "keywords": ["endurance", "fortitude", "destruction", "defense"],
     "magical": "Mental alertness, endurance, defense, destruction of enemies."},
    {"name": "Regulus", "constellation": "Leonis", "ecliptic_lon_j2000": 29.83,
     "nature": "Jupiter/Mars", "keywords": ["royalty", "power", "success", "authority", "greatness"],
     "magical": "Honors, victory, royal favor. Heart of the Lion. Four Royal Stars."},
    {"name": "Vega", "constellation": "Lyrae", "ecliptic_lon_j2000": 15.35,
     "nature": "Venus/Mercury", "keywords": ["protection", "art", "creativity", "mysticism"],
     "magical": "Protection against poison, arts, mathematics, mystical knowledge."},
    {"name": "Capella", "constellation": "Aurigae", "ecliptic_lon_j2000": 22.07,
     "nature": "Jupiter/Mercury", "keywords": ["ambition", "honor", "wealth", "research"],
     "magical": "Ambition, public honor, research. Protects against wounds."},
    {"name": "Betelgeuse", "constellation": "Orionis", "ecliptic_lon_j2000": 28.67,
     "nature": "Mars/Jupiter", "keywords": ["hunting", "militarism", "success", "honor"],
     "magical": "Military success, martial honor, hunting prowess."},
    {"name": "Fomalhaut", "constellation": "Piscis Austrini", "ecliptic_lon_j2000": 3.88,
     "nature": "Venus/Mercury", "keywords": ["dreams", "occult", "poison_immunity", "fame"],
     "magical": "Dreams, occult knowledge, immunity to poison. Great fame."},
    {"name": "Rigel", "constellation": "Orionis", "ecliptic_lon_j2000": 16.92,
     "nature": "Jupiter/Saturn", "keywords": ["technical_skill", "architecture", "invention"],
     "magical": "Technical architecture, invention, mechanical arts."},
    {"name": "Spica", "constellation": "Virginis", "ecliptic_lon_j2000": 23.93,
     "nature": "Venus/Mercury", "keywords": ["profit", "protection", "wisdom", "arts"],
     "magical": "Profit, protection, wisdom, the arts."},
    {"name": "Arcturus", "constellation": "Bootis", "ecliptic_lon_j2000": 24.28,
     "nature": "Mars/Jupiter", "keywords": ["navigation", "guidance", "protection", "prosperity"],
     "magical": "Navigation, guidance, protection, prosperity."},
    {"name": "Alkaid", "constellation": "Ursae Majoris", "ecliptic_lon_j2000": 26.92,
     "nature": "Venus/Moon", "keywords": ["death_transformation", "endings", "healing"],
     "magical": "Healing through transformation, endings that bring renewal."},
]

FOUR_ROYAL_STARS = ["Aldebaran", "Antares", "Regulus", "Fomalhaut"]
# Aldebaran = Watcher of the East, Antares = Watcher of the West
# Regulus = Watcher of the North, Fomalhaut = Watcher of the South


# ===========================================================================
# PLANETARY ANGELS, INTELLIGENCES & SPIRITS (Agrippa's Three Books)
# ===========================================================================

PLANETARY_BEINGS = {
    "Sun": {
        "angel": "Michael", "intelligence": "Nakhiel", "spirit": "Sorath",
        "incense": "Frankincense", "color": "Gold/Yellow",
        "metal": "Gold", "day": "Sunday",
        "psalm": "Psalm 6",
        "koranic": "Surah 91 (Ash-Shams)",
        "description": "Michael is the solar angel, prince of the Archangels. Nakhiel is the intelligence of the Sun, governing illumination. Sorath is the spirit of the Sun.",
    },
    "Moon": {
        "angel": "Gabriel", "intelligence": "Chasmodai", "spirit": "Hasmodai",
        "incense": "Camphor / Jasmine", "color": "Silver/White",
        "metal": "Silver", "day": "Monday",
        "psalm": "Psalm 74",
        "koranic": "Surah 74 (Al-Muddathir)",
        "description": "Gabriel is the lunar angel of revelation. Chasmodai governs dreams and visions. Hasmodai is the spirit of the Moon.",
    },
    "Mercury": {
        "angel": "Raphael", "intelligence": "Tiriel", "spirit": "Taphthartharath",
        "incense": "Mastic / Cinnamon", "color": "Orange/Blue",
        "metal": "Mercury (Quicksilver)", "day": "Wednesday",
        "psalm": "Psalm 57",
        "koranic": "Surah 20 (Taha)",
        "description": "Raphael is the angel of communication and travel. Tiriel governs knowledge and eloquence.",
    },
    "Venus": {
        "angel": "Anael", "intelligence": "Hagiel", "spirit": "Kedemel",
        "incense": "Sandalwood / Rose", "color": "Green/Pink",
        "metal": "Copper", "day": "Friday",
        "psalm": "Psalm 22",
        "koranic": "Surah 55 (Ar-Rahman)",
        "description": "Anael is the angel of love and beauty. Hagiel governs pleasure and the arts.",
    },
    "Mars": {
        "angel": "Samael", "intelligence": "Graphiel", "spirit": "Barzabel",
        "incense": "Dragon's Blood / Pepper", "color": "Red",
        "metal": "Iron/Steel", "day": "Tuesday",
        "psalm": "Psalm 140",
        "koranic": "Surah 2 (Al-Baqarah, sword-verses)",
        "description": "Samael is the angel of severity and war. Graphiel governs courage and victory.",
    },
    "Jupiter": {
        "angel": "Sachiel", "intelligence": "Iophiel", "spirit": "Hismael",
        "incense": "Saffron / Civet", "color": "Blue/Purple",
        "metal": "Tin", "day": "Thursday",
        "psalm": "Psalm 87",
        "koranic": "Surah 55 (wider mercy)",
        "description": "Sachiel is the angel of expansion and wealth. Iophiel governs wisdom and learning.",
    },
    "Saturn": {
        "angel": "Cassiel", "intelligence": "Agiel", "spirit": "Zazel",
        "incense": "Myrrh / Storax", "color": "Black/Indigo",
        "metal": "Lead", "day": "Saturday",
        "psalm": "Psalm 109",
        "koranic": "Surah 66 (At-Tahrim)",
        "description": "Cassiel is the angel of stillness and time. Agiel governs solitude and discipline.",
    },
}

# Also: the Olympic Spirits (from Arbatel)
OLYMPIC_SPIRITS = {
    "Aratron":  {"planet": "Saturn", "description": "Governs all things Saturnine, invisibility, longevity."},
    "Bethor":   {"planet": "Jupiter", "description": "Governs all things Jove, honors, wealth, friendship."},
    "Phaleg":   {"planet": "Mars", "description": "Governs war, victory, courage, martial affairs."},
    "Och":      {"planet": "Sun", "description": "Governs solar things, health, gold, invisibility, prophecy."},
    "Hagith":   {"planet": "Venus", "description": "Governs love, beauty, transmutation of metals."},
    "Ophiel":   {"planet": "Mercury", "description": "Governs knowledge, eloquence, invisibility, philosophy."},
    "Phul":     {"planet": "Moon", "description": "Governs lunar things, water, healing, transformation."},
}


# ===========================================================================
# ASPECT INTERPRETATIONS — Classical meanings
# ===========================================================================

ASPECT_MEANINGS = {
    "Conjunction": {
        "nature": "neutral (depends on planets)", "harmony": "variable",
        "keywords": ["fusion", "unity", "intensity", "focus", "blending"],
        "description": "Planets fuse their energies. The effect depends entirely on the nature of the planets involved. Benefics conjunction is very powerful. Malefics together amplify suffering.",
        "magical": "The most focused and intense combination. Used to bind planetary forces together.",
    },
    "Sextile": {
        "nature": "benefic", "harmony": "harmonious",
        "keywords": ["opportunity", "ease", "talent", "cooperation", "flow"],
        "description": "A harmonious aspect indicating natural talent and opportunity. The native must act to realize its potential.",
        "magical": "Good for all operations requiring ease and cooperation between forces.",
    },
    "Square": {
        "nature": "malefic", "harmony": "disharmonious",
        "keywords": ["tension", "challenge", "crisis", "growth", "friction", "obstacle"],
        "description": "A challenging aspect creating tension and obstacles. Forces growth through difficulty. The native must work against resistance.",
        "magical": "Used in malefic workings. Breaks down barriers but creates instability.",
    },
    "Trine": {
        "nature": "benefic", "harmony": "harmonious",
        "keywords": ["harmony", "gift", "ease", "flow", "talent", "natural_ability"],
        "description": "The most benefic aspect. Indicates natural talent, ease of expression, and flowing harmony.",
        "magical": "The best aspect for all benefic workings. Represents natural flowing power.",
    },
    "Quincunx": {
        "nature": "malefic", "harmony": "disharmonious",
        "keywords": ["adjustment", "incompatibility", "awkwardness", "malaise", "karma"],
        "description": "An aspect of incompatibility. The planets involved have nothing in common. Requires constant adjustment.",
        "magical": "Difficult to use magically. Represents misalignment of forces.",
    },
    "Opposition": {
        "nature": "malefic", "harmony": "disharmonious",
        "keywords": ["polarity", "projection", "separation", "awareness", "tension", "balance"],
        "description": "Creates awareness through polarity and projection. A relationship aspect. Forces confrontation with the other.",
        "magical": "Used in workings of separation and opposition. Creates a clear axis of tension.",
    },
}


# ===========================================================================
# ELECTIONAL SCORING — Picatrix-influenced system
# ===========================================================================

def election_score(hour_ruler, moon_sign, moon_phase, aspects_to_moon, purpose_keywords):
    """
    Score the quality of an election based on multiple factors.
    Returns a dict with score (-10 to +10) and evaluation.
    """
    score = 0
    reasons = []

    # 1. Planetary hour matches purpose
    hour_keywords = PLANET_KEYWORDS.get(hour_ruler, [])
    purpose_match = set(hour_keywords) & set(purpose_keywords)
    if purpose_match:
        score += 3
        reasons.append(f"Hour ruler {hour_ruler} matches purpose: {', '.join(purpose_match)}")
    else:
        score -= 1
        reasons.append(f"Hour ruler {hour_ruler} not ideal for this purpose")

    # 2. Moon phase appropriateness
    if "waxing" in moon_phase.lower() and any(k in ["growth", "increase", "attract", "build", "profit"] for k in purpose_keywords):
        score += 2
        reasons.append("Waxing moon appropriate for growth/increase workings")
    elif "waning" in moon_phase.lower() and any(k in ["decrease", "destroy", "banishing", "end"] for k in purpose_keywords):
        score += 2
        reasons.append("Waning moon appropriate for decrease/banish workings")
    elif "full" in moon_phase.lower():
        score += 2
        reasons.append("Full moon - peak power")
    elif "new" in moon_phase.lower() and any(k in ["beginnings", "secrets", "hidden"] for k in purpose_keywords):
        score += 2
        reasons.append("New moon - good for hidden beginnings")

    # 3. Moon essential dignity
    sign_dignities = get_essential_dignities_simple(moon_sign)
    if sign_dignities.get("domicile"):
        score += 3
        reasons.append(f"Moon in domicile ({moon_sign}) - very strong")
    elif sign_dignities.get("exaltation"):
        score += 3
        reasons.append(f"Moon in exaltation ({moon_sign}) - very strong")
    elif sign_dignities.get("triplicity"):
        score += 2
        reasons.append(f"Moon in triplicity ({moon_sign}) - strong")
    elif sign_dignities.get("fall") or sign_dignities.get("detriment"):
        score -= 3
        reasons.append(f"Moon weak ({sign_dignities.get('fall', sign_dignities.get('detriment'))})")

    # 4. Moon aspects
    for asp in aspects_to_moon:
        if asp["aspect"] in ("Trine", "Sextile"):
            score += 2
            reasons.append(f"Moon {asp['aspect']} {asp['between']} - beneficial")
        elif asp["aspect"] in ("Square", "Opposition"):
            score -= 2
            reasons.append(f"Moon {asp['aspect']} {asp['between']} - challenging")
        elif asp["aspect"] == "Conjunction":
            if "Jupiter" in asp["between"] or "Venus" in asp["between"]:
                score += 2
                reasons.append(f"Moon conjunct benefic")
            elif "Saturn" in asp["between"] or "Mars" in asp["between"]:
                score -= 2
                reasons.append(f"Moon conjunct malefic")

    # Normalize to -10 to +10
    score = max(-10, min(10, score))

    if score >= 7:
        verdict = "excellent"
    elif score >= 4:
        verdict = "good"
    elif score >= 1:
        verdict = "fair"
    elif score >= -3:
        verdict = "poor"
    else:
        verdict = "inauspicious"

    return {"score": score, "verdict": verdict, "reasons": reasons}


def get_essential_dignities_simple(planet_sign_map, sign):
    """
    Given a dict of planet->sign, evaluate essential dignities for a planet in that sign.
    Returns dict of dignity types found.
    """
    dignities = {}
    for planet, psign in planet_sign_map.items():
        if psign == sign:
            # Check each dignity type
            if planet in DOMICILE and sign in DOMICILE[planet]:
                dignities.setdefault("domicile", []).append(planet)
            if planet in DETRIMENT and sign in DETRIMENT[planet]:
                dignities.setdefault("detriment", []).append(planet)
            ex = EXALTATION.get(planet)
            if ex and ex[0] == sign:
                dignities.setdefault("exaltation", []).append(planet)
            fl = FALL.get(planet)
            if fl and fl[0] == sign:
                dignities.setdefault("fall", []).append(planet)
            dignities.setdefault("triplicity", []).append(planet)
            dignities.setdefault("term", []).append(planet)
            dignities.setdefault("face", []).append(planet)
    return dignities
