#!/usr/bin/env python3
"""
Jack Daniels VDOT and Training Pace Calculator
Based on the mathematical models developed by Jack Daniels and Jimmy Gilbert.
"""

import math
import sys
import argparse

DISTANCE_MAP = {
    "1500m": 1500,
    "mile": 1609.34,
    "3k": 3000,
    "5k": 5000,
    "8k": 8000,
    "10k": 10000,
    "15k": 15000,
    "10mile": 16093.4,
    "half_marathon": 21097.5,
    "hm": 21097.5,
    "marathon": 42195.0,
    "fm": 42195.0,
}

def parse_time_to_seconds(time_str: str) -> float:
    """Parses HH:MM:SS or MM:SS to seconds."""
    parts = [float(p) for p in time_str.strip().split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:
        return parts[0]
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def format_seconds_to_time(total_seconds: float) -> str:
    """Formats seconds to HH:MM:SS or MM:SS."""
    total_seconds = round(total_seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"

def format_pace(seconds_per_unit: float) -> str:
    """Formats seconds per km/mile to M:SS/unit."""
    minutes = int(seconds_per_unit // 60)
    seconds = int(round(seconds_per_unit % 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"

def calculate_vdot(distance_meters: float, time_seconds: float) -> float:
    """Calculates VDOT from race distance in meters and race time in seconds."""
    t_min = time_seconds / 60.0
    v = distance_meters / t_min  # meters per minute

    # Percent of VO2max (Daniels & Gilbert formula)
    percent_vo2max = (
        0.8
        + 0.1894393 * math.exp(-0.012778 * t_min)
        + 0.2989558 * math.exp(-0.1932605 * t_min)
    )

    # VO2 cost for velocity v (ml/kg/min)
    vo2 = -4.60 + 0.182258 * v + 0.000104 * (v**2)

    vdot = vo2 / percent_vo2max
    return round(vdot, 2)

def calculate_time_for_vdot_and_distance(vdot: float, distance_meters: float) -> float:
    """Finds time in seconds for given VDOT and distance using binary search."""
    low_t = 60.0  # 1 min
    high_t = 86400.0  # 24 hours

    for _ in range(50):
        mid_t = (low_t + high_t) / 2.0
        est_vdot = calculate_vdot(distance_meters, mid_t)
        if est_vdot < vdot:
            # Faster needed, so time should be smaller
            high_t = mid_t
        else:
            low_t = mid_t

    return (low_t + high_t) / 2.0

def velocity_from_vo2(vo2: float) -> float:
    """Inverts the VO2 formula to find velocity v (m/min) given VO2."""
    # vo2 = -4.60 + 0.182258 * v + 0.000104 * v^2
    # 0.000104 * v^2 + 0.182258 * v - (4.60 + vo2) = 0
    a = 0.000104
    b = 0.182258
    c = -(4.60 + vo2)
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return 0.0
    v = (-b + math.sqrt(discriminant)) / (2 * a)
    return v

def get_training_paces(vdot: float) -> dict:
    """
    Calculates Jack Daniels training paces based on % of VDOT / VO2max.
    E (Easy): 62% - 70% VDOT
    M (Marathon): ~80% - 84% VDOT (or derived from marathon race time)
    T (Threshold): ~86% - 88% VDOT (~1 hour race pace)
    I (Interval): ~95% - 100% VDOT (VO2max pace, ~3k-5k pace)
    R (Repetition): ~105% - 110% VDOT (Economy pace, ~800m-1500m pace)
    """
    # Easy pace range (62% to 70% of VDOT)
    v_e_slow = velocity_from_vo2(vdot * 0.62)
    v_e_fast = velocity_from_vo2(vdot * 0.70)
    
    # Marathon pace (calculated directly from marathon distance time)
    m_time_sec = calculate_time_for_vdot_and_distance(vdot, 42195.0)
    v_m = 42195.0 / (m_time_sec / 60.0)

    # Threshold pace (88% of VDOT)
    v_t = velocity_from_vo2(vdot * 0.88)

    # Interval pace (98% of VDOT)
    v_i = velocity_from_vo2(vdot * 0.98)

    # Repetition pace (108% of VDOT)
    v_r = velocity_from_vo2(vdot * 1.08)

    def v_to_paces(v_m_per_min):
        if v_m_per_min <= 0:
            return {"km": "0:00", "mile": "0:00", "sec_km": 0}
        sec_per_km = 1000.0 / (v_m_per_min / 60.0)
        sec_per_mile = 1609.34 / (v_m_per_min / 60.0)
        return {
            "km": format_pace(sec_per_km),
            "mile": format_pace(sec_per_mile),
            "sec_km": sec_per_km,
            "sec_mile": sec_per_mile
        }

    return {
        "VDOT": vdot,
        "Easy (E)": {
            "km": f"{v_to_paces(v_e_fast)['km']} - {v_to_paces(v_e_slow)['km']}",
            "mile": f"{v_to_paces(v_e_fast)['mile']} - {v_to_paces(v_e_slow)['mile']}",
            "description": "Aerobic foundation, active recovery, warmups/cooldowns (62-70% VO2max)"
        },
        "Marathon (M)": {
            "km": v_to_paces(v_m)["km"],
            "mile": v_to_paces(v_m)["mile"],
            "description": "Marathon race pace, specific endurance (80-84% VO2max)"
        },
        "Threshold (T)": {
            "km": v_to_paces(v_t)["km"],
            "mile": v_to_paces(v_t)["mile"],
            "description": "Lactate threshold, comfortably hard, ~1 hour race pace (86-88% VO2max)"
        },
        "Interval (I)": {
            "km": v_to_paces(v_i)["km"],
            "mile": v_to_paces(v_i)["mile"],
            "400m": format_seconds_to_time(v_to_paces(v_i)["sec_km"] * 0.4),
            "1000m": format_seconds_to_time(v_to_paces(v_i)["sec_km"] * 1.0),
            "1200m": format_seconds_to_time(v_to_paces(v_i)["sec_km"] * 1.2),
            "description": "VO2max stimulus, 3-5 minute bouts, ~3k-5k pace (95-100% VO2max)"
        },
        "Repetition (R)": {
            "km": v_to_paces(v_r)["km"],
            "mile": v_to_paces(v_r)["mile"],
            "200m": format_seconds_to_time(v_to_paces(v_r)["sec_km"] * 0.2),
            "400m": format_seconds_to_time(v_to_paces(v_r)["sec_km"] * 0.4),
            "description": "Running economy, neuromuscular speed, full recovery (105-110% VO2max)"
        }
    }

def get_equivalent_race_times(vdot: float) -> dict:
    """Calculates equivalent race times across standard distances for a given VDOT."""
    standard_distances = [
        ("5k", 5000),
        ("10k", 10000),
        ("Half Marathon", 21097.5),
        ("Marathon", 42195.0)
    ]
    results = {}
    for name, dist in standard_distances:
        t_sec = calculate_time_for_vdot_and_distance(vdot, dist)
        results[name] = format_seconds_to_time(t_sec)
    return results

def main():
    parser = argparse.ArgumentParser(description="Jack Daniels VDOT & Training Pace Calculator")
    parser.add_argument("--distance", "-d", choices=list(DISTANCE_MAP.keys()), help="Recent race distance (e.g. 5k, 10k, hm, marathon)")
    parser.add_argument("--time", "-t", help="Recent race time in HH:MM:SS or MM:SS (e.g. 19:45 or 1:35:20)")
    parser.add_argument("--vdot", "-v", type=float, help="Directly provide VDOT value (e.g. 48.5)")

    args = parser.parse_args()

    if args.vdot:
        vdot = args.vdot
    elif args.distance and args.time:
        dist_m = DISTANCE_MAP[args.distance.lower()]
        time_sec = parse_time_to_seconds(args.time)
        vdot = calculate_vdot(dist_m, time_sec)
    else:
        print("Error: Must provide either --vdot or both --distance and --time.")
        sys.exit(1)

    print(f"==================================================")
    print(f"  JACK DANIELS VDOT TRAINING PROFILE (VDOT: {vdot})")
    print(f"==================================================")
    
    print("\n--- Equivalent Race Performances ---")
    equiv = get_equivalent_race_times(vdot)
    for race, t_str in equiv.items():
        print(f"  {race:15s}: {t_str}")

    print("\n--- Training Paces ---")
    paces = get_training_paces(vdot)
    for pace_type, data in paces.items():
        if pace_type == "VDOT":
            continue
        print(f"\n[{pace_type}] - {data['description']}")
        print(f"  Pace/km:   {data['km']}")
        print(f"  Pace/mile: {data['mile']}")
        if "400m" in data:
            print(f"  400m split: {data['400m']}")
        if "1000m" in data:
            print(f"  1000m split: {data['1000m']}")
        if "200m" in data:
            print(f"  200m split: {data['200m']}")

if __name__ == "__main__":
    main()
