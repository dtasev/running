#!/usr/bin/env python3
"""
Dr. Phil Maffetone MAF 180 Formula & Training Zone Calculator
Calculates Maximum Aerobic Function (MAF) heart rate, training zones, and MAF test guidelines.
"""

import sys
import argparse

def calculate_maf_hr(age: int, category: int) -> dict:
    base_hr = 180 - age
    modifiers = {
        1: (-10, "Major illness, surgery, chronic disease, hospital rehabilitation"),
        2: (-5, "Injured, frequent colds/allergies, inconsistent training (< 1 year)"),
        3: (0, "Training consistently for 1-2 years without injury or major illness"),
        4: (+5, "Training consistently for 2+ years without injury, competing and steadily improving")
    }

    if category not in modifiers:
        raise ValueError(f"Category must be 1, 2, 3, or 4. Got {category}")

    adj, desc = modifiers[category]
    maf_hr = base_hr + adj
    zone_low = maf_hr - 10

    return {
        "Age": age,
        "Category": category,
        "Category Description": desc,
        "MAF Heart Rate (Maximum Aerobic Ceiling)": maf_hr,
        "Optimal Aerobic Training Zone": f"{zone_low} - {maf_hr} bpm",
        "Warmup / Recovery Zone": f"{zone_low - 10} - {zone_low} bpm"
    }

def main():
    parser = argparse.ArgumentParser(description="Maffetone MAF 180 Calculator")
    parser.add_argument("--age", "-a", type=int, required=True, help="Athlete age in years")
    parser.add_argument(
        "--category", "-c", type=int, choices=[1, 2, 3, 4], default=3,
        help="Health & training category (1=Recovering/Ill, 2=Injured/Inconsistent, 3=Consistent 1-2yr, 4=Advanced 2yr+ progressing)"
    )

    args = parser.parse_args()
    results = calculate_maf_hr(args.age, args.category)

    print("==================================================")
    print(f"  MAFFETONE 180 FORMULA PROFILE (Age: {args.age})")
    print("==================================================")
    print(f"Category: {results['Category']} ({results['Category Description']})")
    print(f"\n>> MAF Heart Rate (Ceiling): {results['MAF Heart Rate (Maximum Aerobic Ceiling)']} bpm")
    print(f">> Aerobic Base Zone:        {results['Optimal Aerobic Training Zone']}")
    print(f">> Warm-up / Recovery Zone:  {results['Warmup / Recovery Zone']}")
    print("\nTraining Rules:")
    print("  1. NEVER exceed your MAF HR during base building (even when running uphill).")
    print("  2. If your HR touches the MAF ceiling, slow down or walk until it drops 5 bpm.")
    print("  3. Perform a monthly MAF Test (5 miles / 8 km on a track at exact MAF HR) to evaluate speed progress.")

if __name__ == "__main__":
    main()
