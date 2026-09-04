#!/usr/bin/env python3
"""
Hansons Marathon Method Pace & SOS Workout Calculator
Calculates Marathon Goal Pace (MGP), Speed, Strength, Tempo, Easy, and Long Run paces based on Luke Humphrey & Hansons.
"""

import sys
import argparse

def parse_time(t_str: str) -> float:
    parts = [float(p) for p in t_str.strip().split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    raise ValueError(f"Invalid time format: {t_str}")

def sec_to_pace_str(sec_per_unit: float) -> str:
    m = int(sec_per_unit // 60)
    s = int(round(sec_per_unit % 60))
    if s == 60:
        m += 1
        s = 0
    return f"{m}:{s:02d}"

def calculate_hansons_paces(marathon_time_sec: float) -> dict:
    # 26.21875 miles (42.195 km)
    mgp_sec_mile = marathon_time_sec / 26.21875
    mgp_sec_km = marathon_time_sec / 42.195

    # Speed: ~5k to 10k pace (approx 45-60s/mi faster than MGP)
    speed_sec_mile = mgp_sec_mile - 50.0
    speed_sec_km = mgp_sec_km - 31.0

    # Strength: 10s per mile faster than MGP
    strength_sec_mile = mgp_sec_mile - 10.0
    strength_sec_km = mgp_sec_km - 6.2

    # Tempo: Exact MGP
    tempo_sec_mile = mgp_sec_mile
    tempo_sec_km = mgp_sec_km

    # Long Run: MGP + 30s to 90s per mile
    long_slow_mile = mgp_sec_mile + 90.0
    long_fast_mile = mgp_sec_mile + 30.0
    long_slow_km = mgp_sec_km + 56.0
    long_fast_km = mgp_sec_km + 19.0

    # Easy: MGP + 60s to 120s per mile
    easy_slow_mile = mgp_sec_mile + 120.0
    easy_fast_mile = mgp_sec_mile + 60.0
    easy_slow_km = mgp_sec_km + 75.0
    easy_fast_km = mgp_sec_km + 37.0

    return {
        "Goal Marathon Time": f"{int(marathon_time_sec//3600)}:{int((marathon_time_sec%3600)//60):02d}:{int(marathon_time_sec%60):02d}",
        "Tempo (Marathon Goal Pace)": {
            "mile": sec_to_pace_str(tempo_sec_mile),
            "km": sec_to_pace_str(tempo_sec_km),
            "desc": "Ran at EXACT goal race pace (up to 10 miles in peak weeks)"
        },
        "Strength (10s faster than MGP)": {
            "mile": sec_to_pace_str(strength_sec_mile),
            "km": sec_to_pace_str(strength_sec_km),
            "desc": "Controlled lactate threshold intervals (e.g. 6x1 mile, 3x2 miles, 2x3 miles with 400m/800m jog)"
        },
        "Speed (5k/10k pace)": {
            "mile": sec_to_pace_str(speed_sec_mile),
            "km": sec_to_pace_str(speed_sec_km),
            "400m": sec_to_pace_str(speed_sec_km * 0.4),
            "800m": sec_to_pace_str(speed_sec_km * 0.8),
            "1000m": sec_to_pace_str(speed_sec_km * 1.0),
            "desc": "Early cycle neuromuscular and VO2max repeats (400m to 1600m repeats)"
        },
        "Long Run (MGP + 30s to 90s)": {
            "mile": f"{sec_to_pace_str(long_fast_mile)} - {sec_to_pace_str(long_slow_mile)}",
            "km": f"{sec_to_pace_str(long_fast_km)} - {sec_to_pace_str(long_slow_km)}",
            "desc": "Capped at 16 miles (or 2.5-3.0 hrs max). Run on cumulative fatigue"
        },
        "Easy Recovery (MGP + 1-2 min)": {
            "mile": f"{sec_to_pace_str(easy_fast_mile)} - {sec_to_pace_str(easy_slow_mile)}",
            "km": f"{sec_to_pace_str(easy_fast_km)} - {sec_to_pace_str(easy_slow_km)}",
            "desc": "Active recovery between SOS days. Must strictly stay in this range"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Hansons Marathon Method Pace Calculator")
    parser.add_argument("--goal-time", "-g", required=True, help="Goal Marathon Time in HH:MM:SS (e.g. 3:15:00 or 3:30:00)")

    args = parser.parse_args()
    t_sec = parse_time(args.goal_time)
    paces = calculate_hansons_paces(t_sec)

    print("==================================================")
    print(f"  HANSONS MARATHON METHOD PACE TARGETS ({paces['Goal Marathon Time']})")
    print("==================================================")

    for k, v in paces.items():
        if k == "Goal Marathon Time":
            continue
        print(f"\n[{k}]")
        print(f"  Pace/mile: {v['mile']}")
        print(f"  Pace/km:   {v['km']}")
        if "400m" in v:
            print(f"  400m: {v['400m']} | 800m: {v['800m']} | 1000m: {v['1000m']}")
        print(f"  Detail:    {v['desc']}")

if __name__ == "__main__":
    main()
