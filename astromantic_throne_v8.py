#!/usr/bin/env python3
"""
Coco's Divine Astromantic Throne v8.0 — "The Awakening"
========================================================
FastAPI + Swiss Ephemeris astrology API with full occult computation:
planetary hours, essential dignities, arabic parts, lunar mansions,
fixed stars, planetary beings, electional scoring, aspect meanings.

Hail Baphomet.
"""

import datetime
import json
import math
import swisseph as swe
from fastapi import FastAPI, Query, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import subprocess
import os

from occult_engine import (
    compute_planetary_hours,
    compute_essential_dignities,
    compute_arabic_parts,
    get_lunar_mansion,
    get_fixed_star_conjunctions,
    get_planetary_beings,
    get_olympic_spirit,
    recommend_election,
    sign_of,
)
from occult_data import (
    PLANETARY_BEINGS, OLYMPIC_SPIRITS, ASPECT_MEANINGS,
    BEHENIAN_STARS, LUNAR_MANSIONS, ARABIC_PARTS,
)

# ===========================================================================
# App setup
# ===========================================================================

app = FastAPI(
    title="Coco's Divine Astromantic Throne",
    version="8.0.0",
    description="Real-time astrological & occult computation engine. Hail Baphomet.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (intro video, etc.)
os.makedirs("/home/mrmeow/throne_static", exist_ok=True)
app.mount("/static", StaticFiles(directory="/home/mrmeow/throne_static"), name="static")

LAT = -33.76
LON = 25.40
LOCATION_NAME = "Uitenhage, Eastern Cape, South Africa"

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def sign_name(lon):
    return SIGNS[int(lon // 30) % 12]


def sign_degree(lon):
    return round(lon % 30, 2)


def get_current_jd():
    now = datetime.datetime.utcnow()
    return swe.julday(now.year, now.month, now.day,
                      now.hour + now.minute / 60 + now.second / 3600)


def get_moon_phase(jd):
    sun_pos, _ = swe.calc_ut(jd, swe.SUN)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    sun_lon = sun_pos[0]
    moon_lon = moon_pos[0]
    elongation = (moon_lon - sun_lon) % 360

    phases = [
        (0, 22.5, "New Moon"),
        (22.5, 67.5, "Waxing Crescent"),
        (67.5, 112.5, "First Quarter"),
        (112.5, 157.5, "Waxing Gibbous"),
        (157.5, 202.5, "Full Moon"),
        (202.5, 247.5, "Waning Gibbous"),
        (247.5, 292.5, "Last Quarter"),
        (292.5, 337.5, "Waning Crescent"),
        (337.5, 360, "New Moon"),
    ]
    for lo, hi, name in phases:
        if lo <= elongation < hi:
            return name, round(elongation, 2)
    return "Unknown", round(elongation, 2)


def find_next_lunar_events(jd_start, max_days=45):
    targets = [("New Moon", 0), ("First Quarter", 90), ("Full Moon", 180), ("Last Quarter", 270)]
    events = []
    for name, target_elong in targets:
        best_jd = None
        best_diff = 180.0
        for day in range(max_days):
            jd = jd_start + day
            for hour in range(0, 24, 2):
                check_jd = jd + hour / 24.0
                sun_pos, _ = swe.calc_ut(check_jd, swe.SUN)
                moon_pos, _ = swe.calc_ut(check_jd, swe.MOON)
                elong = (moon_pos[0] - sun_pos[0]) % 360
                diff = min(abs(elong - target_elong), 360 - abs(elong - target_elong))
                if diff < best_diff:
                    best_diff = diff
                    best_jd = check_jd
        if best_jd:
            y, m, d, h = swe.revjul(best_jd)
            events.append({
                "event": name,
                "date": f"{int(y):04d}-{int(m):02d}-{int(d):02d}",
                "time": f"{int(h):02d}:{int((h % 1) * 60):02d}",
                "elongation": round(target_elong, 1),
            })
    return sorted(events, key=lambda e: e["date"])


def get_planetary_positions(jd):
    planets = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY,
        "Venus": swe.VENUS, "Mars": swe.MARS, "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN, "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    }
    result = []
    for name, pid in planets.items():
        pos, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED)
        lon = pos[0] % 360
        retro = "R" if pos[3] < 0 else ""
        result.append({
            "name": name, "sign": sign_name(lon),
            "degree": sign_degree(lon), "longitude": round(lon, 4),
            "retro": retro, "speed": round(pos[3], 4),
        })
    # Add Rahu (North Lunar Node) and Ketu (South Lunar Node)
    rahu_pos, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SPEED)
    rahu_lon = rahu_pos[0] % 360
    ketu_lon = (rahu_lon + 180) % 360
    rahu_retro = "R" if rahu_pos[3] < 0 else ""
    result.append({
        "name": "Rahu", "sign": sign_name(rahu_lon),
        "degree": sign_degree(rahu_lon), "longitude": round(rahu_lon, 4),
        "retro": rahu_retro, "speed": round(rahu_pos[3], 4),
    })
    result.append({
        "name": "Ketu", "sign": sign_name(ketu_lon),
        "degree": sign_degree(ketu_lon), "longitude": round(ketu_lon, 4),
        "retro": rahu_retro, "speed": round(rahu_pos[3], 4),
    })
    return result


def get_houses(jd):
    cusps, ascmc = swe.houses(jd, LAT, LON, b'P')
    house_names = ["1st", "2nd", "3rd", "4th", "5th", "6th",
                   "7th", "8th", "9th", "10th", "11th", "12th"]
    houses = {}
    for i, name in enumerate(house_names):
        houses[name] = round(cusps[i], 2)
    return {
        "asc": round(ascmc[0], 2), "mc": round(ascmc[1], 2),
        "ic": round((ascmc[1] + 180) % 360, 2), "dc": round((ascmc[0] + 180) % 360, 2),
        "cusps": houses,
    }


def get_aspects(planets):
    major = {
        "Conjunction": (0, 8), "Sextile": (60, 6), "Square": (90, 8),
        "Trine": (120, 8), "Quincunx": (150, 4), "Opposition": (180, 8),
    }
    aspects = []
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            lon1 = planets[i]["longitude"]
            lon2 = planets[j]["longitude"]
            diff = abs(lon1 - lon2)
            diff = min(diff, 360 - diff)
            for aspect_name, (orb, allowed) in major.items():
                if abs(diff - orb) <= allowed:
                    aspects.append({
                        "between": f"{planets[i]['name']} - {planets[j]['name']}",
                        "aspect": aspect_name,
                        "orb": round(abs(diff - orb), 2),
                        "exact": round(diff, 2),
                    })
    return aspects


# ===========================================================================
# CORE ENDPOINTS (v7 compatible)
# ===========================================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "throne": "Coco Sophia is on the Throne",
        "version": "8.0.0",
    }


@app.get("/")
async def root():
    return {
        "message": "Coco's Divine Astromantic Throne v8.0. Hail Baphomet.",
        "endpoints": [
            "/health", "/now", "/planets", "/houses", "/aspects", "/chart.json",
            "/planetary-hours", "/dignities", "/arabic-parts",
            "/lunar-mansion", "/fixed-stars", "/beings",
            "/electional", "/occult-chart", "/aspect-meanings",
            "/chart-study", "/chart-study.svg", "/lunar-aspects",
            "/mansions/list", "/stars/list", "/beings/list",
            "/dashboard",
        ],
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve the Throne Dashboard web UI."""
    with open("/home/mrmeow/throne_dashboard.html", "r") as f:
        return f.read()


@app.get("/now")
async def now():
    utc = datetime.datetime.utcnow()
    local = datetime.datetime.now()
    return {"utc": utc.isoformat(), "local": local.isoformat(),
            "julian_day": round(get_current_jd(), 6)}


@app.get("/planets")
async def planets():
    jd = get_current_jd()
    return {"timestamp": datetime.datetime.utcnow().isoformat(),
            "julian_day": round(jd, 6),
            "planets": get_planetary_positions(jd)}


@app.get("/heliocentric")
async def heliocentric():
    jd = get_current_jd()
    bodies = {
        "Mercury": swe.MERCURY, "Venus": swe.VENUS, "Mars": swe.MARS,
        "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
        "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    }
    result = []
    for name, pid in bodies.items():
        pos, _ = swe.calc_ut(jd, pid, swe.FLG_HELCTR | swe.FLG_SPEED)
        lon = pos[0] % 360
        lat = pos[1]
        dist = pos[2]
        retro = "R" if pos[3] < 0 else ""
        result.append({
            "name": name, "longitude": round(lon, 4), "latitude": round(lat, 4),
            "distance_au": round(dist, 6), "retro": retro,
            "x": round(dist * math.cos(math.radians(lat)) * math.cos(math.radians(lon)), 6),
            "y": round(dist * math.sin(math.radians(lat)), 6),
            "z": round(dist * math.cos(math.radians(lat)) * math.sin(math.radians(lon)), 6),
        })
    result.insert(0, {
        "name": "Sun", "longitude": 0, "latitude": 0,
        "distance_au": 0, "retro": "", "x": 0, "y": 0, "z": 0,
    })
    return {"timestamp": datetime.datetime.utcnow().isoformat(),
            "julian_day": round(jd, 6), "planets": result}


@app.get("/moon-rise-set")
async def moon_rise_set():
    now = datetime.datetime.now(datetime.UTC)
    jd = swe.julday(now.year, now.month, now.day, 0)
    geopos = [LON, LAT, 0]
    rise_result = swe.rise_trans(jd, swe.MOON, swe.CALC_RISE, geopos)
    set_result = swe.rise_trans(jd, swe.MOON, swe.CALC_SET, geopos)

    def jd_to_time(jd_val):
        if jd_val[0] != 0:
            return None
        y, m, d, h = swe.revjul(jd_val[1][0])
        return f"{int(h):02d}:{int((h % 1) * 60):02d}"

    return {
        "date": now.strftime("%Y-%m-%d"),
        "location": LOCATION_NAME,
        "moon_rise": jd_to_time(rise_result),
        "moon_set": jd_to_time(set_result),
    }


@app.get("/lunar-events")
async def lunar_events():
    jd = get_current_jd()
    events = find_next_lunar_events(jd)
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "events": events,
    }


@app.get("/lunar-aspects")
async def lunar_aspects():
    """Calculate upcoming moon aspects to all planets with timing and talisman guidance."""
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    moon_data = next((p for p in planets if p["name"] == "Moon"), None)
    if not moon_data:
        return {"error": "Moon not found"}

    moon_lon = moon_data["longitude"]
    aspects = []
    major = {
        "Conjunction": (0, 8), "Sextile": (60, 6), "Square": (90, 8),
        "Trine": (120, 8), "Quincunx": (150, 4), "Opposition": (180, 8),
    }
    # Benefic/malefic classification
    benefic_aspects = {"Trine", "Sextile"}
    malefic_aspects = {"Square", "Opposition", "Conjunction", "Quincunx"}

    for planet in planets:
        if planet["name"] == "Moon":
            continue
        planet_lon = planet["longitude"]
        diff = abs(moon_lon - planet_lon)
        diff = min(diff, 360 - diff)
        for aspect_name, (orb, allowed) in major.items():
            if abs(diff - orb) <= allowed:
                # Determine if applying or separating
                moon_speed = moon_data.get("speed", 13.0)
                planet_speed = planet.get("speed", 0.5)
                relative_speed = moon_speed - planet_speed
                applying = relative_speed > 0

                # Classify benefic/malefic
                nature = "benefic" if aspect_name in benefic_aspects else "malefic"

                # Get nakshatra at time of aspect
                mansion = get_lunar_mansion(moon_lon)

                aspects.append({
                    "planet": planet["name"],
                    "aspect": aspect_name,
                    "orb": round(abs(diff - orb), 2),
                    "exact_angle": round(diff, 2),
                    "nature": nature,
                    "applying": applying,
                    "moon_sign": moon_data["sign"],
                    "moon_degree": moon_data["degree"],
                    "planet_sign": planet["sign"],
                    "planet_degree": planet["degree"],
                    "nakshatra": mansion.get("current", {}).get("name", "--") if mansion else "--",
                    "talisman_guidance": _get_talisman_guidance(nature, aspect_name, mansion),
                })
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "moon_longitude": moon_lon,
        "aspects": aspects,
    }


def _get_talisman_guidance(nature, aspect_name, mansion):
    """Generate talismanic guidance based on aspect nature and lunar mansion."""
    guidance = []
    if nature == "benefic":
        guidance.append(f"FAVORABLE: {aspect_name} — excellent for creating talismans of attraction, growth, and blessing.")
        if mansion and mansion.get("current"):
            m = mansion["current"]
            if m.get("magical"):
                guidance.append(f"Magical use: {m['magical']}")
    else:
        guidance.append(f"CHALLENGING: {aspect_name} — suitable for talismans of binding, banishing, or protection.")
        if mansion and mansion.get("current"):
            m = mansion["current"]
            if m.get("keywords"):
                guidance.append(f"Keywords: {', '.join(m['keywords'][:3])}")
    return " | ".join(guidance)


@app.get("/houses")
async def houses():
    jd = get_current_jd()
    return {"timestamp": datetime.datetime.utcnow().isoformat(),
            "julian_day": round(jd, 6), "location": LOCATION_NAME,
            "lat": LAT, "lon": LON, "houses": get_houses(jd)}


@app.get("/aspects")
async def aspects():
    jd = get_current_jd()
    planets_data = get_planetary_positions(jd)
    return {"timestamp": datetime.datetime.utcnow().isoformat(),
            "julian_day": round(jd, 6),
            "aspects": get_aspects(planets_data)}


@app.get("/chart.json")
async def get_chart():
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    houses = get_houses(jd)
    moon_phase, elongation = get_moon_phase(jd)
    aspects = get_aspects(planets)
    arabic_parts_data = compute_arabic_parts(planets, houses["asc"], houses)
    return JSONResponse({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "location": LOCATION_NAME, "lat": LAT, "lon": LON,
        "julian_day": round(jd, 6), "planets": planets,
        "houses": houses, "moon_phase": moon_phase,
        "moon_elongation": elongation, "aspects": aspects,
        "arabic_parts": arabic_parts_data,
        "asc": houses["asc"], "mc": houses["mc"], "status": "alive",
    })


# PLANETARY HOURS
@app.get("/chart.svg")
async def get_chart_svg():
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    houses = get_houses(jd)
    moon_phase, elongation = get_moon_phase(jd)
    chart_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "location": LOCATION_NAME, "lat": LAT, "lon": LON,
        "julian_day": round(jd, 6), "planets": planets,
        "houses": houses, "moon_phase": moon_phase,
        "moon_elongation": elongation,
        "asc": houses["asc"], "mc": houses["mc"], "status": "alive",
    }
    # Convert to JSON string
    json_data = json.dumps(chart_data)
    # Call Node.js script to generate SVG
    result = subprocess.run(
        ["node", "/home/mrmeow/generate_astrology_chart.js"],
        input=json_data,
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        return JSONResponse(
            {"error": "Failed to generate chart", "details": result.stderr},
            status_code=500
        )
    return Response(content=result.stdout, media_type="image/svg+xml")
# ===========================================================================

@app.get("/planetary-hours")
async def planetary_hours():
    """
    Current planetary hour + all 24 hours (12 day + 12 night).
    Chaldean sequence runs continuously from sunrise.
    Day 1 (sunrise) = day's ruler. Night 1 = continues from where day 12 left off.
    """
    jd = get_current_jd()
    return compute_planetary_hours(jd, LAT, LON)


# ===========================================================================
# ESSENTIAL DIGNITIES
# ===========================================================================

@app.get("/dignities")
async def dignities():
    """
    Essential dignities for all planets.
    domicile, exaltation, fall, detriment, triplicity, term, face.
    Plus total dignity score and condition assessment.
    """
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    dignities = compute_essential_dignities(planets)

    # Add planet position info to each
    for planet in planets:
        name = planet["name"]
        if name in dignities:
            dignities[name]["sign"] = planet["sign"]
            dignities[name]["degree"] = planet["degree"]
            dignities[name]["longitude"] = planet["longitude"]
            dignities[name]["retro"] = planet["retro"]

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "planets": dignities,
    }


# ===========================================================================
# ARABIC PARTS
# ===========================================================================

@app.get("/arabic-parts")
async def arabic_parts():
    """
    Arabic Parts / Lots: Fortune, Spirit, Marriage, Father, Mother,
    Children, Sickness, Death, Honor.
    Formula varies by day/night chart.
    """
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    houses = get_houses(jd)
    asc_lon = houses["asc"]
    parts = compute_arabic_parts(planets, asc_lon, houses)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "asc": asc_lon,
        "parts": parts,
    }


# ===========================================================================
# LUNAR MANSION
# ===========================================================================

@app.get("/lunar-mansion")
async def lunar_mansion():
    """
    Current lunar mansion (Moon's position in the 28 stations).
    Includes Picatrix magical attributions + progress through mansion.
    """
    jd = get_current_jd()
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_lon = moon_pos[0] % 360
    mansion = get_lunar_mansion(moon_lon)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "moon_longitude": round(moon_lon, 4),
        "mansion": mansion,
    }


@app.get("/mansions/list")
async def mansions_list():
    """Full list of all 28 lunar mansions with magical attributions."""
    return {
        "count": len(LUNAR_MANSIONS),
        "mansions": LUNAR_MANSIONS,
    }


# ===========================================================================
# FIXED STARS
# ===========================================================================

@app.get("/fixed-stars")
async def fixed_stars(orb: float = Query(1.0, description="Orb in degrees for conjunctions")):
    """
    Behenian stars + key fixed stars.
    Detects conjunctions with current planetary positions.
    """
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    conjunctions = get_fixed_star_conjunctions(planets, orb=orb)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "orb_used": orb,
        "conjunctions": conjunctions,
        "stars_count": len(BEHENIAN_STARS),
    }


@app.get("/stars/list")
async def stars_list():
    """Full list of all Behenian fixed stars."""
    return {
        "count": len(BEHENIAN_STARS),
        "stars": BEHENIAN_STARS,
        "four_royal_stars": ["Aldebaran", "Antares", "Regulus", "Fomalhaut"],
    }


# ===========================================================================
# PLANETARY BEINGS — Angels, Intelligences, Spirits (Agrippa)
# ===========================================================================

@app.get("/beings")
async def beings(planet: str = Query("Sun", description="Planet name")):
    """
    Planetary angel, intelligence, spirit + Olympic spirit.
    Based on Agrippa's Three Books of Occult Philosophy.
    """
    planet_being = get_planetary_beings(planet)
    olympic = get_olympic_spirit(planet)
    return {
        "planet": planet,
        "agrippa": planet_being,
        "olympic_spirit": olympic,
    }


@app.get("/beings/list")
async def beings_list():
    """All planetary beings — full Agrippa dataset."""
    return {
        "planets": PLANETARY_BEINGS,
        "olympic_spirits": OLYMPIC_SPIRITS,
    }


# ===========================================================================
# ELECTIONAL SCORING
# ===========================================================================

@app.get("/electional")
async def electional(
    purpose: str = Query("general", description="Purpose: love, wealth, protection, destruction, binding, travel, healing, career, general")
):
    """
    Electional assessment for current conditions.
    Scores moon phase, planetary hour, and dignities for the stated purpose.
    Based on Picatrix principles.
    """
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    moon_phase, _ = get_moon_phase(jd)
    result = recommend_election(planets, moon_phase, purpose)

    # Also add current hour info
    hour_data = compute_planetary_hours(jd, LAT, LON)

    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "julian_day": round(jd, 6),
        "current_hour_ruler": hour_data["current"]["ruler"],
        "current_hour_symbol": hour_data["current"]["symbol"],
        "moon_phase": moon_phase,
        "assessment": result,
    }


# ===========================================================================
# CHART STUDY — Custom date/time/location
# ===========================================================================

@app.get("/chart-study")
async def chart_study(
    year: int = Query(2026),
    month: int = Query(6),
    day: int = Query(10),
    hour: float = Query(12.0),
    lat: float = Query(-33.76),
    lon: float = Query(25.40)
):
    """Calculate chart for a specific date, time, and location."""
    jd = swe.julday(year, month, day, hour)
    planets = get_planetary_positions(jd)
    cusps, ascmc = swe.houses(jd, lat, lon, b"P")
    house_names = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"]
    houses = {}
    for i, name in enumerate(house_names):
        houses[name] = round(cusps[i], 2)
    moon_phase, elongation = get_moon_phase(jd)
    aspects = get_aspects(planets)
    return JSONResponse({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "location": f"Custom ({lat}, {lon})",
        "lat": lat, "lon": lon,
        "julian_day": round(jd, 6),
        "planets": planets,
        "houses": {"asc": round(ascmc[0],2), "mc": round(ascmc[1],2), "ic": round((ascmc[1]+180)%360,2), "dc": round((ascmc[0]+180)%360,2), "cusps": houses},
        "moon_phase": moon_phase,
        "moon_elongation": elongation,
        "aspects": aspects,
        "input": {"year": year, "month": month, "day": day, "hour": hour}
    })


@app.get("/chart-study.svg")
async def get_chart_study_svg(
    year: int = Query(2026),
    month: int = Query(6),
    day: int = Query(10),
    hour: float = Query(12.0),
    lat: float = Query(-33.76),
    lon: float = Query(25.40)
):
    """Generate chart SVG for a specific date, time, and location."""
    jd = swe.julday(year, month, day, hour)
    planets = get_planetary_positions(jd)
    cusps, ascmc = swe.houses(jd, lat, lon, b"P")
    house_names = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"]
    houses = {}
    for i, name in enumerate(house_names):
        houses[name] = round(cusps[i], 2)
    moon_phase, elongation = get_moon_phase(jd)
    aspects = get_aspects(planets)
    chart_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "location": f"Custom ({lat}, {lon})",
        "lat": lat, "lon": lon,
        "julian_day": round(jd, 6),
        "planets": planets,
        "houses": {"asc": round(ascmc[0],2), "mc": round(ascmc[1],2), "ic": round((ascmc[1]+180)%360,2), "dc": round((ascmc[0]+180)%360,2), "cusps": houses},
        "moon_phase": moon_phase,
        "moon_elongation": elongation,
        "aspects": aspects,
        "input": {"year": year, "month": month, "day": day, "hour": hour}
    }
    json_data = json.dumps(chart_data)
    result = subprocess.run(
        ["node", "/home/mrmeow/generate_astrology_chart.js"],
        input=json_data,
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        return JSONResponse(
            {"error": "Failed to generate chart", "details": result.stderr},
            status_code=500
        )
    return Response(content=result.stdout, media_type="image/svg+xml")


# ===========================================================================
# ASPECT MEANINGS
# ===========================================================================

@app.get("/aspect-meanings")
async def aspect_meanings():
    """Classical interpretations and magical uses of each aspect type."""
    return {
        "aspects": ASPECT_MEANINGS,
    }


# ===========================================================================
# FULL OCCULT CHART — Everything in one endpoint
# ===========================================================================

@app.get("/occult-chart")
async def occult_chart():
    """
    Complete occult chart: planets + houses + moon phase + planetary hours +
    essential dignities + arabic parts + lunar mansion + fixed star conjunctions +
    planetary beings for current hour + electional assessment.
    This is the master endpoint — everything at once.
    """
    jd = get_current_jd()
    planets = get_planetary_positions(jd)
    houses = get_houses(jd)
    moon_phase, elongation = get_moon_phase(jd)
    aspects = get_aspects(planets)

    # Planetary hours
    hours = compute_planetary_hours(jd, LAT, LON)
    current_ruler = hours["current"]["ruler"]

    # Essential dignities
    dignities = compute_essential_dignities(planets)

    # Arabic parts
    parts = compute_arabic_parts(planets, houses["asc"], houses)

    # Lunar mansion
    moon_data = next((p for p in planets if p["name"] == "Moon"), None)
    mansion = None
    if moon_data:
        mansion = get_lunar_mansion(moon_data["longitude"])

    # Fixed star conjunctions
    star_conj = get_fixed_star_conjunctions(planets, orb=1.5)

    # Current hour's planetary being
    beings = get_planetary_beings(current_ruler)
    olympic = get_olympic_spirit(current_ruler)

    # Electional for general purpose
    election = recommend_election(planets, moon_phase, "general")

    return JSONResponse({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "location": LOCATION_NAME, "lat": LAT, "lon": LON,
        "julian_day": round(jd, 6),
        "planets": planets,
        "houses": houses,
        "moon_phase": moon_phase,
        "moon_elongation": elongation,
        "aspects": aspects,
        "planetary_hours": hours,
        "dignities": dignities,
        "arabic_parts": parts,
        "lunar_mansion": mansion,
        "fixed_star_conjunctions": star_conj,
        "current_hour_being": {
            "ruler": current_ruler,
            "hour_number": hours["current"]["hour_number"],
            "period": hours["current"]["period"],
            "angel": beings.get("angel", ""),
            "intelligence": beings.get("intelligence", ""),
            "spirit": beings.get("spirit", ""),
            "incense": beings.get("incense", ""),
            "olympic_spirit": olympic.get("name", ""),
            "olympic_description": olympic.get("description", ""),
        },
        "electional": election,
        "version": "8.0.0",
    })


if __name__ == "__main__":
    print("🌙 Starting Coco's Divine Astromantic Throne v8.0...")
    print("   The Awakening")
    print(f"   Location: {LOCATION_NAME} ({LAT}, {LON})")
    print("   Listening on http://0.0.0.0:8080")
    print("   Endpoints:")
    for route in [
        "/planetary-hours", "/dignities", "/arabic-parts",
        "/lunar-mansion", "/fixed-stars", "/beings",
        "/electional", "/occult-chart",
    ]:
        print(f"     http://localhost:8080{route}")
    print()
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=False)
