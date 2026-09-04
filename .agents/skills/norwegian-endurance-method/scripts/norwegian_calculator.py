#!/usr/bin/env python3
"""
Norwegian Endurance Method Calculator
Calculates lactate-guided sub-threshold paces, interval workouts, and heart rate boundaries
based on the Marius Bakken & Ingebrigtsen training models adapted for Half Marathon & Marathon.
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

def sec_to_pace_str(sec_per_km: float) -> str:
    m = int(sec_per_km // 60)
    s = int(round(sec_per_km % 60))
    if s == 60:
        m += 1
        s = 0
    return f"{m}:{s:02d}"

def calculate_norwegian_zones(race_distance: str, race_time_sec: float, max_hr: int = None) -> dict:
    # Estimate 10k pace in sec/km
    if race_distance in ["5k", "5000m"]:
        v_5k_km = race_time_sec / 5.0
        sec_10k_km = v_5k_km * 1.06
    elif race_distance in ["10k", "10000m"]:
        sec_10k_km = race_time_sec / 10.0
    elif race_distance in ["hm", "half_marathon"]:
        v_hm_km = race_time_sec / 21.0975
        sec_10k_km = v_hm_km / 1.05
    elif race_distance in ["marathon", "fm"]:
        v_m_km = race_time_sec / 42.195
        sec_10k_km = v_m_km / 1.12
    else:
        raise ValueError(f"Unsupported race distance: {race_distance}")

    sec_5k_km = sec_10k_km / 1.06
    sec_hm_km = sec_10k_km * 1.05
    sec_m_km = sec_10k_km * 1.12
    sec_easy_km = sec_10k_km * 1.30

    # Norwegian Sub-threshold Paces
    # Lower Threshold (AM): ~2.0 - 2.8 mmol/L (between HM and 15k pace)
    lt1_lower_km = sec_hm_km
    lt1_upper_km = sec_10k_km * 1.03

    # Upper Threshold (PM): ~3.0 - 3.8 mmol/L (between 10k and 15k pace)
    lt2_lower_km = sec_10k_km * 1.02
    lt2_upper_km = sec_10k_km * 0.98

    zones = {
        "Zone 1 (Easy Aerobic / Volume)": {
            "lactate": "< 1.5 mmol/L",
            "pace_km": f"{sec_to_pace_str(sec_easy_km)} - {sec_to_pace_str(sec_easy_km + 30)}",
            "pace_mile": f"{sec_to_pace_str(sec_easy_km * 1.60934)} - {sec_to_pace_str((sec_easy_km + 30) * 1.60934)}",
            "hr": f"< {round(max_hr * 0.75)} bpm (< 75% Max HR)" if max_hr else "65-75% Max HR",
            "workouts": "Daily easy recovery runs, high volume without autonomic strain"
        },
        "Sub-Threshold AM (Lower Threshold / Long Reps)": {
            "lactate": "2.0 - 2.8 mmol/L",
            "pace_km": f"{sec_to_pace_str(lt1_lower_km)} - {sec_to_pace_str(lt1_upper_km)}",
            "pace_mile": f"{sec_to_pace_str(lt1_lower_km * 1.60934)} - {sec_to_pace_str(lt1_upper_km * 1.60934)}",
            "hr": f"{round(max_hr * 0.82)} - {round(max_hr * 0.86)} bpm" if max_hr else "82-86% Max HR",
            "workouts": "5-6 x 6 min (60s rest), 4-5 x 2 km (60s rest), or 3 x 3 km (90s rest)"
        },
        "Sub-Threshold PM (Upper Threshold / Short Reps)": {
            "lactate": "3.0 - 3.8 mmol/L",
            "pace_km": f"{sec_to_pace_str(lt2_lower_km)} - {sec_to_pace_str(lt2_upper_km)}",
            "pace_mile": f"{sec_to_pace_str(lt2_lower_km * 1.60934)} - {sec_to_pace_str(lt2_upper_km * 1.60934)}",
            "hr": f"{round(max_hr * 0.86)} - {round(max_hr * 0.90)} bpm" if max_hr else "86-90% Max HR",
            "workouts": "20-25 x 400m (30s rest), 10-12 x 1 km (45-60s rest), or 6-8 x 1500m (60s rest)"
        },
        "Marathon Specific Threshold Block (Weekend)": {
            "lactate": "1.8 - 2.5 mmol/L",
            "pace_km": sec_to_pace_str(sec_m_km),
            "pace_mile": sec_to_pace_str(sec_m_km * 1.60934),
            "hr": f"{round(max_hr * 0.80)} - {round(max_hr * 0.85)} bpm" if max_hr else "80-85% Max HR",
            "workouts": "30-35km Long run with 2 x 8km or 3 x 5km @ Marathon Specific Pace"
        }
    }
    return zones

def main():
    parser = argparse.ArgumentParser(description="Norwegian Sub-Threshold Endurance Calculator")
    parser.add_argument("--distance", "-d", choices=["5k", "10k", "hm", "marathon"], required=True, help="Baseline race distance")
    parser.add_argument("--time", "-t", required=True, help="Baseline race time in MM:SS or HH:MM:SS")
    parser.add_argument("--max-hr", type=int, help="Athlete Max Heart Rate (optional)")

    args = parser.parse_args()
    t_sec = parse_time(args.time)
    zones = calculate_norwegian_zones(args.distance, t_sec, args.max_hr)

    print("==================================================")
    print("  NORWEGIAN SUB-THRESHOLD TRAINING TARGETS")
    print("==================================================")
    for name, data in zones.items():
        print(f"\n[{name}]")
        print(f"  Target Lactate: {data['lactate']}")
        print(f"  Pace/km:        {data['pace_km']}")
        print(f"  Pace/mile:      {data['pace_mile']}")
        print(f"  Heart Rate:     {data['hr']}")
        print(f"  Workouts:       {data['workouts']}")

if __name__ == "__main__":
    main()
