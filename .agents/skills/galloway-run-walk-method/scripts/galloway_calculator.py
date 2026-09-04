#!/usr/bin/env python3
"""
Jeff Galloway Run-Walk-Run & Magic Mile Calculator
Calculates race predictions from Magic Mile time trials and recommends optimal Run-Walk-Run ratios.
"""

import sys
import argparse

def parse_time(t_str: str) -> float:
    parts = [float(p) for p in t_str.strip().split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:
        return parts[0]
    raise ValueError(f"Invalid time format: {t_str}")

def format_sec(sec: float) -> str:
    sec = round(sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def get_run_walk_ratio(pace_min_mile: float) -> list:
    if pace_min_mile <= 7.0:
        return ["Run 4 min / Walk 30 sec", "Run 2 min / Walk 15 sec", "Run 90 sec / Walk 15 sec"]
    elif pace_min_mile <= 7.5:
        return ["Run 3 min / Walk 30 sec", "Run 2 min / Walk 20 sec", "Run 90 sec / Walk 15 sec"]
    elif pace_min_mile <= 8.0:
        return ["Run 2 min / Walk 30 sec", "Run 90 sec / Walk 30 sec", "Run 60 sec / Walk 20 sec"]
    elif pace_min_mile <= 8.5:
        return ["Run 90 sec / Walk 30 sec", "Run 60 sec / Walk 30 sec", "Run 45 sec / Walk 20 sec"]
    elif pace_min_mile <= 9.0:
        return ["Run 60 sec / Walk 30 sec", "Run 45 sec / Walk 30 sec", "Run 30 sec / Walk 20 sec"]
    elif pace_min_mile <= 10.5:
        return ["Run 45 sec / Walk 30 sec", "Run 30 sec / Walk 30 sec", "Run 20 sec / Walk 20 sec"]
    elif pace_min_mile <= 11.5:
        return ["Run 30 sec / Walk 30 sec", "Run 20 sec / Walk 20 sec", "Run 15 sec / Walk 15 sec"]
    elif pace_min_mile <= 12.5:
        return ["Run 20 sec / Walk 20 sec", "Run 15 sec / Walk 15 sec", "Run 10 sec / Walk 10 sec"]
    elif pace_min_mile <= 13.5:
        return ["Run 15 sec / Walk 15 sec", "Run 10 sec / Walk 10 sec", "Run 10 sec / Walk 20 sec"]
    else:
        return ["Run 10 sec / Walk 10 sec", "Run 10 sec / Walk 20 sec", "Run 10 sec / Walk 30 sec"]

def calculate_galloway_profile(mm_sec: float) -> dict:
    # Galloway Magic Mile Predictions:
    # 5k pace = MM + 33s/mi
    # 10k pace = MM * 1.15
    # Half Marathon pace = MM * 1.20
    # Marathon pace = MM * 1.30

    pace_5k = mm_sec + 33.0
    time_5k = pace_5k * 3.10686

    pace_10k = mm_sec * 1.15
    time_10k = pace_10k * 6.21371

    pace_hm = mm_sec * 1.20
    time_hm = pace_hm * 13.109375

    pace_m = mm_sec * 1.30
    time_m = pace_m * 26.21875

    long_run_pace = pace_m + 120.0  # 2 min/mile slower

    return {
        "Magic Mile Time": format_sec(mm_sec),
        "Predictions": {
            "5k": {"Time": format_sec(time_5k), "Pace/mi": format_sec(pace_5k)},
            "10k": {"Time": format_sec(time_10k), "Pace/mi": format_sec(pace_10k)},
            "Half Marathon": {"Time": format_sec(time_hm), "Pace/mi": format_sec(pace_hm)},
            "Marathon": {"Time": format_sec(time_m), "Pace/mi": format_sec(pace_m)}
        },
        "Marathon Run-Walk Options": get_run_walk_ratio(pace_m / 60.0),
        "Half Marathon Run-Walk Options": get_run_walk_ratio(pace_hm / 60.0),
        "Training Long Run Pace": f"{format_sec(long_run_pace)}/mile (Run 2 min/mile slower than goal marathon pace)"
    }

def main():
    parser = argparse.ArgumentParser(description="Jeff Galloway Run-Walk-Run & Magic Mile Calculator")
    parser.add_argument("--magic-mile", "-m", help="Magic Mile time trial in MM:SS (e.g. 7:30 or 8:15)")
    parser.add_argument("--goal-pace", "-p", help="Target pace in MM:SS per mile to get Run-Walk-Run ratio directly")

    args = parser.parse_args()

    if args.goal_pace:
        pace_sec = parse_time(args.goal_pace)
        ratios = get_run_walk_ratio(pace_sec / 60.0)
        print("==================================================")
        print(f"  GALLOWAY RUN-WALK-RUN RATIOS ({args.goal_pace}/mile)")
        print("==================================================")
        for i, r in enumerate(ratios, 1):
            print(f"  Option {i}: {r}")
    elif args.magic_mile:
        mm_sec = parse_time(args.magic_mile)
        profile = calculate_galloway_profile(mm_sec)
        print("==================================================")
        print(f"  GALLOWAY MAGIC MILE RACE PREDICTIONS (MM: {profile['Magic Mile Time']})")
        print("==================================================")
        for dist, data in profile["Predictions"].items():
            print(f"  {dist:15s}: {data['Time']} (Pace: {data['Pace/mi']}/mile)")
        
        print("\n--- Recommended Marathon Run-Walk-Run Ratios ---")
        for i, r in enumerate(profile["Marathon Run-Walk Options"], 1):
            print(f"  Option {i}: {r}")

        print("\n--- Training Long Run Pacing ---")
        print(f"  {profile['Training Long Run Pace']}")
    else:
        print("Error: Must provide either --magic-mile or --goal-pace.")
        sys.exit(1)

if __name__ == "__main__":
    main()
