#!/usr/bin/env python3
"""
Coco's Divine Astromantic Throne — Occult Computation Engine
=============================================================
Implements all magical/occult calculations using the databases
from occult_data.py plus swisseph for real-time computation.
"""

import datetime
import swisseph as swe
from occult_data import (
    DAY_RULERS, CHALDEAN, PLANET_SYMBOL, PLANET_NATURE, PLANET_KEYWORDS,
    PLANET_BENEFIC, DOMICILE, DETRIMENT, EXALTATION, FALL,
    SIGN_TRIPLICITY, TERMS_EGYPTIAN, FACES, DIGNITY_SCORES,
    ARABIC_PARTS, LUNAR_MANSIONS, BEHENIAN_STARS,
    PLANETARY_BEINGS, OLYMPIC_SPIRITS, ASPECT_MEANINGS,
    election_score, get_essential_dignities_simple,
)

TZ_OFFSET = 2.0 / 24.0  # SAST = UTC+2


# ===========================================================================
# PLANETARY HOURS — Fixed implementation
# ===========================================================================

def compute_planetary_hours(jd, lat, lon):
    """
    Compute 24 planetary hours starting at sunrise.
    The planetary day starts at sunrise, not midnight.
    Before sunrise = previous day's ruler.
    Hour 1 (sunrise) = day ruler. Chaldean sequence continues through all 24 hours.
    Each hour = (next_sunrise - sunrise) / 24.
    """
    now = datetime.datetime.utcnow()
    now_local = now + datetime.timedelta(hours=2)

    jd_today_start = swe.julday(now_local.year, now_local.month, now_local.day, 0.0)
    jd_now = swe.julday(now.year, now.month, now.day,
                        now.hour + now.minute / 60 + now.second / 3600)

    geopos = [lon, lat, 0]
    rise_flags = swe.CALC_RISE | swe.BIT_DISC_CENTER
    set_flags = swe.CALC_SET | swe.BIT_DISC_CENTER

    # Get today's sunrise
    res_rise, tret_rise = swe.rise_trans(jd_today_start, swe.SUN, rise_flags, geopos, 1013.25, 0.0)
    jd_rise_today = tret_rise[0]

    # Determine the current planetary day ruler
    # Before sunrise = previous day's ruler; after sunrise = today's ruler
    if jd_now < jd_rise_today:
        prev_day = now_local - datetime.timedelta(days=1)
        weekday = prev_day.weekday()
        # Use yesterday's sunrise as cycle start
        jd_yesterday = jd_today_start - 1.0
        res_yrise, tret_yrise = swe.rise_trans(jd_yesterday, swe.SUN, rise_flags, geopos, 1013.25, 0.0)
        jd_rise = tret_yrise[0]
    else:
        weekday = now_local.weekday()
        jd_rise = jd_rise_today

    day_ruler = DAY_RULERS[weekday]
    day_ruler_idx = CHALDEAN.index(day_ruler)

    # Get sunset and next sunrise for the cycle
    res_set, tret_set = swe.rise_trans(jd_today_start, swe.SUN, set_flags, geopos, 1013.25, 0.0)
    jd_set = tret_set[0]

    jd_tomorrow = jd_today_start + 1.0
    res_rise2, tret_rise2 = swe.rise_trans(jd_tomorrow, swe.SUN, rise_flags, geopos, 1013.25, 0.0)
    jd_rise_next = tret_rise2[0]

    # 24-hour period from sunrise to next sunrise
    full_cycle_jd = jd_rise_next - jd_rise
    hour_len = full_cycle_jd / 24

    # Determine current hour (1-24)
    elapsed = jd_now - jd_rise
    if elapsed < 0:
        elapsed += 24.0 / 24.0
    hour_num = int(elapsed / hour_len) + 1
    if hour_num > 24:
        hour_num = 24

    # Build all 24 hours
    def jd_to_local_str(jd_val):
        yr, mo, d, h = swe.revjul(jd_val + TZ_OFFSET)
        hr = int(h)
        mi = int((h - hr) * 60)
        se = int(((h - hr) * 60 - mi) * 60)
        return f"{yr:04d}-{mo:02d}-{d:02d} {hr:02d}:{mi:02d}:{se:02d}"

    def jd_to_time_str(jd_val):
        yr, mo, d, h = swe.revjul(jd_val + TZ_OFFSET)
        hr = int(h)
        mi = int((h - hr) * 60)
        return f"{hr:02d}:{mi:02d}"

    all_hours = []
    for h in range(1, 25):
        ruler_idx = (day_ruler_idx + (h - 1)) % 7
        ruler = CHALDEAN[ruler_idx]
        st = jd_rise + (h - 1) * hour_len
        et = st + hour_len
        all_hours.append({
            "hour_number": h,
            "ruler": ruler,
            "symbol": PLANET_SYMBOL.get(ruler, ""),
            "benefic": PLANET_BENEFIC.get(ruler, "neutral"),
            "start": jd_to_time_str(st),
            "end": jd_to_time_str(et),
            "start_full": jd_to_local_str(st),
            "end_full": jd_to_local_str(et),
            "active": (h == hour_num),
        })

    # Current hour details
    current_ruler_idx = (day_ruler_idx + (hour_num - 1)) % 7
    current_ruler = CHALDEAN[current_ruler_idx]

    return {
        "timestamp": now_local.strftime("%Y-%m-%d %H:%M:%S") + " SAST",
        "julian_day": round(jd_now, 6),
        "location": {"lat": lat, "lon": lon},
        "day_of_week": now_local.strftime("%A"),
        "day_ruler": day_ruler,
        "sunrise": jd_to_time_str(jd_rise),
        "sunset": jd_to_time_str(jd_set),
        "next_sunrise": jd_to_time_str(jd_rise_next),
        "cycle_hours": 24,
        "current": {
            "hour_number": hour_num,
            "ruler": current_ruler,
            "symbol": PLANET_SYMBOL.get(current_ruler, ""),
            "day_ruler": day_ruler,
            "benefic": PLANET_BENEFIC.get(current_ruler, ""),
            "nature": PLANET_NATURE.get(current_ruler, {}),
            "keywords": PLANET_KEYWORDS.get(current_ruler, []),
            "start": jd_to_time_str(jd_rise + (hour_num - 1) * hour_len),
            "end": jd_to_time_str(jd_rise + hour_num * hour_len),
            "angel": PLANETARY_BEINGS.get(current_ruler, {}).get("angel", ""),
            "intelligence": PLANETARY_BEINGS.get(current_ruler, {}).get("intelligence", ""),
            "spirit": PLANETARY_BEINGS.get(current_ruler, {}).get("spirit", ""),
        },
        "hours": all_hours,
    }


# ===========================================================================
# ESSENTIAL DIGNITIES
# ===========================================================================

def compute_essential_dignities(planets):
    """
    Given planets data (list of dicts with name, longitude, sign),
    compute essential dignities for each planet.

    Returns per-planet dignity breakdown + total scores.
    """
    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    results = {}

    for planet in planets:
        name = planet["name"]
        sign = planet["sign"]
        lon = planet["longitude"]
        degree_in_sign = lon % 30
        
        dignities = {
            "domicile": False,
            "detriment": False,
            "exaltation": False,
            "exaltation_distance": None,
            "fall": False,
            "fall_distance": None,
            "triplicity": False,
            "term": None,
            "face": None,
            "score": 0,
        }
        detail = []

        # Domicile
        if name in DOMICILE and sign in DOMICILE[name]:
            dignities["domicile"] = True
            dignities["score"] += DIGNITY_SCORES["domicile"]
            detail.append(f"Domicile (+{DIGNITY_SCORES['domicile']})")

        # Detriment
        if name in DETRIMENT and sign in DETRIMENT[name]:
            dignities["detriment"] = True
            dignities["score"] += DIGNITY_SCORES["detriment"]
            detail.append(f"Detriment ({DIGNITY_SCORES['detriment']})")

        # Exaltation
        if name in EXALTATION:
            ex_sign, ex_deg = EXALTATION[name]
            if sign == ex_sign:
                dignities["exaltation"] = True
                dist = abs(degree_in_sign - ex_deg)
                dignities["exaltation_distance"] = round(dist, 2)
                dignities["score"] += DIGNITY_SCORES["exaltation"]
                detail.append(f"Exaltation ({ex_deg}°{ex_sign}, {round(dist,1)}° away, +{DIGNITY_SCORES['exaltation']})")

        # Fall
        if name in FALL:
            fl_sign, fl_deg = FALL[name]
            if sign == fl_sign:
                dignities["fall"] = True
                dist = abs(degree_in_sign - fl_deg)
                dignities["fall_distance"] = round(dist, 2)
                dignities["score"] += DIGNITY_SCORES["fall"]
                detail.append(f"Fall ({fl_deg}°{fl_sign}, {round(dist,1)}° away, {DIGNITY_SCORES['fall']})")

        # Triplicity
        if sign in SIGN_TRIPLICITY:
            tri = SIGN_TRIPLICITY[sign]
            # Use Sun's position to determine day/night (above/below horizon)
            dignities["triplicity"] = tri.get("day")
            dignities["score"] += DIGNITY_SCORES["triplicity"]
            detail.append(f"Triplicity ({tri.get('day')}, +{DIGNITY_SCORES['triplicity']})")

        # Term
        if sign in TERMS_EGYPTIAN:
            for end_deg, term_planet in TERMS_EGYPTIAN[sign]:
                if degree_in_sign < end_deg:
                    dignities["term"] = term_planet
                    if term_planet == name:
                        dignities["score"] += DIGNITY_SCORES["term"]
                        detail.append(f"Term (+{DIGNITY_SCORES['term']})")
                    break

        # Face (decan)
        if sign in FACES:
            face_idx = int(degree_in_sign // 10)
            if face_idx < 3:
                face_ruler = FACES[sign][face_idx]
                dignities["face"] = face_ruler
                if face_ruler == name:
                    dignities["score"] += DIGNITY_SCORES["face"]
                    detail.append(f"Face (+{DIGNITY_SCORES['face']})")

        # Determine overall condition
        score = dignities["score"]
        if score >= 12:
            condition = "very_strong"
        elif score >= 7:
            condition = "strong"
        elif score >= 3:
            condition = "moderate"
        elif score >= 0:
            condition = "weak"
        elif score >= -5:
            condition = "debilitated"
        else:
            condition = "peregrine"

        dignities["condition"] = condition
        dignities["detail"] = detail
        results[name] = dignities

    return results


# ===========================================================================
# ARABIC PARTS — Computation
# ===========================================================================

def compute_arabic_parts(planets, asc_lon, houses_data=None):
    """
    Compute Arabic Parts/Lots from planetary positions.
    Parts computed: Fortune, Spirit, Marriage, Father, Mother, Children, Travel, Sickness, Death, Honor.
    """
    # Build a quick lookup: planet_name -> longitude
    plon = {p["name"]: p["longitude"] for p in planets}

    sun_lon = plon.get("Sun", 0)
    moon_lon = plon.get("Moon", 0)
    venus_lon = plon.get("Venus", 0)
    mars_lon = plon.get("Mars", 0)
    jupiter_lon = plon.get("Jupiter", 0)
    saturn_lon = plon.get("Saturn", 0)
    asc = asc_lon

    # Determine sect: Sun above horizon = day chart
    # Simplified: use MC
    is_day_chart = True  # Would need houses_data for this; defaulting

    def norm(lon):
        return lon % 360

    parts = {}

    # Part of Fortune
    if is_day_chart:
        fortune = norm(asc + moon_lon - sun_lon)
    else:
        fortune = norm(asc + sun_lon - moon_lon)
    parts["Part_of_Fortune"] = {
        "longitude": round(fortune, 4),
        "sign": sign_of(fortune),
        "degree": round(fortune % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Fortune", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Spirit
    if is_day_chart:
        spirit = norm(asc + sun_lon - moon_lon)
    else:
        spirit = norm(asc + moon_lon - sun_lon)
    parts["Part_of_Spirit"] = {
        "longitude": round(spirit, 4),
        "sign": sign_of(spirit),
        "degree": round(spirit % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Spirit", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Marriage (using DC = ASC + 180)
    dc = norm(asc + 180)
    marriage = norm(asc + dc - venus_lon)
    parts["Part_of_Marriage"] = {
        "longitude": round(marriage, 4),
        "sign": sign_of(marriage),
        "degree": round(marriage % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Marriage", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Father
    if is_day_chart:
        father = norm(asc + saturn_lon - sun_lon)
    else:
        father = norm(asc + sun_lon - saturn_lon)
    parts["Part_of_Father"] = {
        "longitude": round(father, 4),
        "sign": sign_of(father),
        "degree": round(father % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Father", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Mother
    if is_day_chart:
        mother = norm(asc + moon_lon - venus_lon)
    else:
        mother = norm(asc + venus_lon - moon_lon)
    parts["Part_of_Mother"] = {
        "longitude": round(mother, 4),
        "sign": sign_of(mother),
        "degree": round(mother % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Mother", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Children
    if is_day_chart:
        children = norm(asc + jupiter_lon - saturn_lon)
    else:
        children = norm(asc + saturn_lon - jupiter_lon)
    parts["Part_of_Children"] = {
        "longitude": round(children, 4),
        "sign": sign_of(children),
        "degree": round(children % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Children", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Sickness
    if is_day_chart:
        sickness = norm(asc + mars_lon - saturn_lon)
    else:
        sickness = norm(asc + saturn_lon - mars_lon)
    parts["Part_of_Sickness"] = {
        "longitude": round(sickness, 4),
        "sign": sign_of(sickness),
        "degree": round(sickness % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Sickness", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Death (from 8th house cusp if available)
    eighth_cusp = houses_data.get("cusps", {}).get("8th", norm(asc + 210)) if houses_data else norm(asc + 210)
    if is_day_chart:
        death = norm(asc + eighth_cusp - moon_lon)
    else:
        death = norm(asc + moon_lon - eighth_cusp)
    parts["Part_of_Death"] = {
        "longitude": round(death, 4),
        "sign": sign_of(death),
        "degree": round(death % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Death", {}).items() if k not in ("formula_day", "formula_night")},
    }

    # Part of Honor
    if is_day_chart:
        mc = houses_data.get("mc", norm(asc + 270)) if houses_data else norm(asc + 270)
        honor = norm(asc + sun_lon - saturn_lon)
    else:
        honor = norm(asc + saturn_lon - sun_lon)
    parts["Part_of_Honor"] = {
        "longitude": round(honor, 4),
        "sign": sign_of(honor),
        "degree": round(honor % 30, 2),
        **{k: v for k, v in ARABIC_PARTS.get("Part_of_Honor", {}).items() if k not in ("formula_day", "formula_night")},
    }

    return parts


def sign_of(lon):
    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return SIGNS[int(lon // 30) % 12]


# ===========================================================================
# LUNAR MANSIONS — Current mansion + next
# ===========================================================================

def get_lunar_mansion(moon_lon):
    """
    Given Moon's ecliptic longitude, determine the current lunar mansion.
    Returns current mansion info + adjacent mansions.
    """
    mansion_size = 360.0 / 28  # = 12.857... degrees per mansion

    # Mansion number (1-indexed)
    mansion_idx = int(moon_lon / mansion_size)
    if mansion_idx >= 28:
        mansion_idx = 27

    mansion = LUNAR_MANSIONS[mansion_idx]
    next_mansion = LUNAR_MANSIONS[(mansion_idx + 1) % 28]
    prev_mansion = LUNAR_MANSIONS[(mansion_idx - 1) % 28]

    # How far through this mansion (0-100%)
    mansion_start = mansion_idx * mansion_size
    mansion_end = mansion_start + mansion_size
    progress_pct = ((moon_lon - mansion_start) / mansion_size) * 100

    # Degrees remaining in this mansion
    degrees_remaining = mansion_end - moon_lon

    return {
        "current": {
            "number": mansion["number"],
            "name": mansion["name"],
            "ruled_by": mansion["ruled_by"],
            "nature": mansion["nature"],
            "keywords": mansion["keywords"],
            "magical": mansion["magical"],
            "picatrix": mansion["picatrix"],
            "progress_percent": round(progress_pct, 1),
            "degrees_remaining": round(degrees_remaining, 2),
            "mansion_symbol": PLANET_SYMBOL.get(mansion["ruled_by"], ""),
            "planetary_being": PLANETARY_BEINGS.get(mansion["ruled_by"], {}),
        },
        "next": {
            "number": next_mansion["number"],
            "name": next_mansion["name"],
            "ruled_by": next_mansion["ruled_by"],
            "degrees_until": round(mansion_end - moon_lon, 2),
        },
        "previous": {
            "number": prev_mansion["number"],
            "name": prev_mansion["name"],
            "ruled_by": prev_mansion["ruled_by"],
        },
    }


# ===========================================================================
# FIXED STARS — Conjunction detection
# ===========================================================================

def get_fixed_star_conjunctions(planets, orb=1.0):
    """
    Check if any planet is conjunct a Behenian star (within orb degrees).
    Uses J2000 positions — for precise work would need precession.
    """
    conjunctions = []
    for planet in planets:
        for star in BEHENIAN_STARS:
            planet_lon = planet["longitude"]
            star_lon = star["ecliptic_lon_j2000"]
            diff = abs(planet_lon - star_lon)
            diff = min(diff, 360 - diff)
            if diff <= orb:
                conjunctions.append({
                    "planet": planet["name"],
                    "star": star["name"],
                    "star_constellation": star["constellation"],
                    "orb": round(diff, 3),
                    "star_nature": star["nature"],
                    "star_keywords": star["keywords"],
                    "magical": star["magical"],
                    "planet_sign": planet["sign"],
                    "planet_degree": planet["degree"],
                })
    return conjunctions


# ===========================================================================
# PLANETARY BEINGS — Angelic / Intelligence / Spirit
# ===========================================================================

def get_planetary_beings(planet_name):
    """Return full angelic/spiritual data for a planet."""
    return PLANETARY_BEINGS.get(planet_name, {})


def get_olympic_spirit(planet_name):
    """Return the Olympic Spirit associated with a planet."""
    for name, data in OLYMPIC_SPIRITS.items():
        if data["planet"] == planet_name:
            return {"name": name, **data}
    return {}


# ===========================================================================
# ELECTIONAL SCORING
# ===========================================================================

def recommend_election(planets, moon_phase, purpose="general"):
    """
    Given current chart conditions, provide an electional assessment.
    purpose: one of "love", "wealth", "protection", "destruction", "binding",
             "travel", "healing", "career", "general"
    """
    purpose_keywords_map = {
        "love": ["love", "art", "music", "friendship", "pleasure", "harmony", "beauty", "social"],
        "wealth": ["wealth", "law", "religion", "expansion", "luck", "mercy", "healing", "diplomacy"],
        "protection": ["binding", "limitation", "time", "structures", "discipline"],
        "destruction": ["war", "courage", "conflict", "fire", "competition"],
        "binding": ["binding", "limitation", "death", "time", "structures", "discipline"],
        "travel": ["travel", "messages", "communication", "study"],
        "healing": ["healing", "mercy", "health", "luck", "medicine"],
        "career": ["authority", "success", "promotion", "illumination", "honor", "wealth"],
        "general": [],
    }

    keywords = purpose_keywords_map.get(purpose, [])

    # Get Moon details
    moon_data = next((p for p in planets if p["name"] == "Moon"), None)
    if not moon_data:
        return {"error": "Moon data not available"}

    moon_sign = moon_data["sign"]
    moon_aspects = []  # Would need aspect calculation

    # Hour ruler score placeholder (would integrate with planetary hours)
    score_info = {
        "purpose": purpose,
        "purpose_keywords": keywords,
        "moon_sign": moon_sign,
        "moon_phase": moon_phase,
        "moon_dignities": {},  # Would fill from essential dignities
        "recommendation": "",
        "score": 0,
        "verdict": "unknown",
    }

    # Simple rule-based assessment
    moon_nature = PLANET_NATURE.get("Moon", {})
    is_benefic_moon = moon_sign in ("Cancer", "Taurus", "Pisces", "Libra", "Sagittarius")

    if is_benefic_moon and purpose in ("love", "healing", "wealth"):
        score_info["score"] += 3
        score_info["recommendation"] = f"Moon in {moon_sign} is well-placed for {purpose} workings."
    elif moon_sign in ("Scorpio", "Capricorn", "Aries") and purpose in ("destruction", "binding"):
        score_info["score"] += 2
        score_info["recommendation"] = f"Moon in {moon_sign} supports {purpose} operations."
    elif moon_sign in ("Scorpio", "Capricorn") and purpose in ("love", "healing"):
        score_info["score"] -= 2
        score_info["recommendation"] = f"Moon in {moon_sign} is challenging for {purpose}."

    # Phase check
    if "waxing" in moon_phase.lower() and purpose in ("love", "wealth", "healing"):
        score_info["score"] += 2
        score_info["recommendation"] += " Waxing moon supports growth workings."
    elif "waning" in moon_phase.lower() and purpose in ("destruction", "binding"):
        score_info["score"] += 1
        score_info["recommendation"] += " Waning moon supports decrease workings."
    elif "full" in moon_phase.lower():
        score_info["score"] += 2
        score_info["recommendation"] += " Full moon amplifies all workings."
    elif "new" in moon_phase.lower() and purpose in ("protection", "general"):
        score_info["score"] += 1
        score_info["recommendation"] += " New moon is good for new beginnings."

    score_info["score"] = max(-10, min(10, score_info["score"]))

    if score_info["score"] >= 5:
        score_info["verdict"] = "excellent"
    elif score_info["score"] >= 2:
        score_info["verdict"] = "good"
    elif score_info["score"] >= -1:
        score_info["verdict"] = "fair"
    elif score_info["score"] >= -5:
        score_info["verdict"] = "poor"
    else:
        score_info["verdict"] = "inauspicious"

    return score_info
