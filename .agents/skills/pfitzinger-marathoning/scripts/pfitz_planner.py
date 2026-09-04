#!/usr/bin/env python3
"""
Pete Pfitzinger (Advanced Marathoning) Training Zone and Plan Generator
Calculates heart rate reserve (HRR), pace targets, and plan structures based on Pfitzinger & Douglas.
"""

import sys
import argparse

PLANS = {
    "marathon_18_55": {
        "name": "Marathon 18 Weeks / Up to 55 Miles (88 km)",
        "peak_mileage": 55,
        "weeks": 18,
        "target_level": "Intermediate marathoner stepping up volume",
        "key_workouts": ["LT runs up to 7 miles", "MLRs up to 12 miles", "Long runs up to 20 miles with MP blocks"]
    },
    "marathon_18_70": {
        "name": "Marathon 18 Weeks / Up to 70 Miles (112 km)",
        "peak_mileage": 70,
        "weeks": 18,
        "target_level": "Advanced marathoner targeting BQ or PR",
        "key_workouts": ["Midweek MLRs (14-15 mi)", "LT tempos up to 7-8 miles", "Long runs up to 21-22 miles", "Tune-up 8k-15k races"]
    },
    "marathon_18_85": {
        "name": "Marathon 18 Weeks / Up to 85 Miles (137 km)",
        "peak_mileage": 85,
        "weeks": 18,
        "target_level": "High-volume competitive marathoner",
        "key_workouts": ["Two MLRs per week", "Multiple 20+ milers", "High cumulative fatigue"]
    },
    "hm_12_63": {
        "name": "Half Marathon 12 Weeks / Up to 63 Miles (101 km)",
        "peak_mileage": 63,
        "weeks": 12,
        "target_level": "Intermediate-to-advanced half marathoner",
        "key_workouts": ["LT intervals and steady tempos (up to 38-42 min)", "Midweek MLRs (11-12 mi)", "Progression long runs (14-16 mi)"]
    }
}

def calculate_hr_zones(max_hr: int, rest_hr: int = None) -> dict:
    """Calculates Pfitzinger HR zones via % Max HR and optionally % Heart Rate Reserve (Karvonen)."""
    zones = {}
    
    # % Max HR standard ranges
    zones["Recovery"] = {
        "max_hr_range": f"< {round(max_hr * 0.76)} bpm (< 76% Max HR)",
        "desc": "Active recovery, strictly easy effort"
    }
    zones["General Aerobic (GA)"] = {
        "max_hr_range": f"{round(max_hr * 0.70)} - {round(max_hr * 0.81)} bpm (70-81% Max HR)",
        "desc": "Standard aerobic conditioning runs"
    }
    zones["Endurance (Long / MLR)"] = {
        "max_hr_range": f"{round(max_hr * 0.73)} - {round(max_hr * 0.84)} bpm (73-84% Max HR)",
        "desc": "Starts at ~73-74% and gradually progresses up to 84% in final miles"
    }
    zones["Marathon Pace (MP)"] = {
        "max_hr_range": f"{round(max_hr * 0.82)} - {round(max_hr * 0.88)} bpm (82-88% Max HR)",
        "desc": "Specific marathon pace rhythm and fuel utilization"
    }
    zones["Lactate Threshold (LT)"] = {
        "max_hr_range": f"{round(max_hr * 0.85)} - {round(max_hr * 0.91)} bpm (85-91% Max HR)",
        "desc": "15k to Half Marathon race pace (comfortably hard)"
    }
    zones["VO2max (Speed Intervals)"] = {
        "max_hr_range": f"{round(max_hr * 0.93)} - {round(max_hr * 0.98)} bpm (93-98% Max HR)",
        "desc": "3k to 5k race pace, 600m-1600m repeats"
    }

    if rest_hr:
        hrr = max_hr - rest_hr
        zones["Recovery"]["hrr_range"] = f"< {round(rest_hr + hrr * 0.70)} bpm (< 70% HRR)"
        zones["General Aerobic (GA)"]["hrr_range"] = f"{round(rest_hr + hrr * 0.62)} - {round(rest_hr + hrr * 0.75)} bpm (62-75% HRR)"
        zones["Endurance (Long / MLR)"]["hrr_range"] = f"{round(rest_hr + hrr * 0.65)} - {round(rest_hr + hrr * 0.78)} bpm (65-78% HRR)"
        zones["Marathon Pace (MP)"]["hrr_range"] = f"{round(rest_hr + hrr * 0.73)} - {round(rest_hr + hrr * 0.84)} bpm (73-84% HRR)"
        zones["Lactate Threshold (LT)"]["hrr_range"] = f"{round(rest_hr + hrr * 0.77)} - {round(rest_hr + hrr * 0.88)} bpm (77-88% HRR)"
        zones["VO2max (Speed Intervals)"]["hrr_range"] = f"{round(rest_hr + hrr * 0.90)} - {round(rest_hr + hrr * 0.95)} bpm (90-95% HRR)"

    return zones

def main():
    parser = argparse.ArgumentParser(description="Pete Pfitzinger Training Zone & Plan Generator")
    parser.add_argument("--max-hr", type=int, required=True, help="Maximum Heart Rate (bpm)")
    parser.add_argument("--rest-hr", type=int, help="Resting Heart Rate (bpm, optional for HRR calculation)")
    parser.add_argument("--plan", choices=list(PLANS.keys()), help="Display overview of a Pfitzinger plan template")

    args = parser.parse_args()

    print("==================================================")
    print("  PFITZINGER TRAINING ZONES & PHYSIOLOGICAL TARGETS")
    print("==================================================")
    print(f"Max Heart Rate: {args.max_hr} bpm" + (f" | Resting Heart Rate: {args.rest_hr} bpm" if args.rest_hr else ""))

    zones = calculate_hr_zones(args.max_hr, args.rest_hr)
    for name, data in zones.items():
        print(f"\n[{name}]")
        print(f"  Max HR Target: {data['max_hr_range']}")
        if "hrr_range" in data:
            print(f"  HRR Target:    {data['hrr_range']}")
        print(f"  Purpose:       {data['desc']}")

    if args.plan:
        plan_info = PLANS[args.plan]
        print(f"\n==================================================")
        print(f"  PLAN TEMPLATE: {plan_info['name']}")
        print(f"==================================================")
        print(f"Target Runner: {plan_info['target_level']}")
        print(f"Duration:      {plan_info['weeks']} weeks")
        print(f"Peak Mileage:  {plan_info['peak_mileage']} miles / week")
        print("Signature Elements:")
        for w in plan_info["key_workouts"]:
            print(f"  - {w}")

if __name__ == "__main__":
    main()
