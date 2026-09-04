#!/usr/bin/env python3
"""
Master Running Coach Athlete Assessment & Methodology Selector Engine
Analyzes athlete experience, current weekly volume, injury risk, schedule availability,
and racing goals to recommend the optimal Half Marathon or Marathon training methodology.
"""

import sys
import argparse

def evaluate_runner(
    race_type: str,
    weekly_mileage: int,
    days_per_week: int,
    goal: str,
    injury_prone: bool,
    has_hr_or_lactate: bool
) -> dict:
    scores = {
        "daniels-running-formula": 0,
        "pfitzinger-marathoning": 0,
        "hansons-marathon-method": 0,
        "norwegian-endurance-method": 0,
        "canova-marathon-method": 0,
        "maffetone-low-hr-method": 0,
        "galloway-run-walk-method": 0
    }

    reasons = {k: [] for k in scores}

    # 1. Injury Status
    if injury_prone:
        scores["galloway-run-walk-method"] += 40
        reasons["galloway-run-walk-method"].append("Run-Walk-Run intervals virtually eliminate impact stress and soft-tissue injury risk.")
        scores["maffetone-low-hr-method"] += 35
        reasons["maffetone-low-hr-method"].append("Low heart rate training minimizes cortisol and inflammatory damage.")
        scores["pfitzinger-marathoning"] -= 25
        reasons["pfitzinger-marathoning"].append("High weekly volume and hard midweek MLRs may exacerbate existing injuries.")
        scores["canova-marathon-method"] -= 30
    else:
        scores["daniels-running-formula"] += 15
        scores["pfitzinger-marathoning"] += 20
        scores["hansons-marathon-method"] += 20
        scores["norwegian-endurance-method"] += 20

    # 2. Weekly Mileage Baseline
    if weekly_mileage < 25:
        scores["galloway-run-walk-method"] += 30
        scores["maffetone-low-hr-method"] += 25
        scores["pfitzinger-marathoning"] -= 30
        scores["canova-marathon-method"] -= 40
        scores["norwegian-endurance-method"] -= 20
    elif 25 <= weekly_mileage < 45:
        scores["daniels-running-formula"] += 25
        scores["hansons-marathon-method"] += 25
        scores["maffetone-low-hr-method"] += 20
        scores["pfitzinger-marathoning"] += 10
    elif 45 <= weekly_mileage < 65:
        scores["pfitzinger-marathoning"] += 35
        reasons["pfitzinger-marathoning"].append("Current volume (45-65 mpw) is ideal for Pfitz 18/55 or 18/70 mesocycles.")
        scores["daniels-running-formula"] += 30
        scores["hansons-marathon-method"] += 30
        scores["norwegian-endurance-method"] += 25
    else:  # 65+ mpw
        scores["pfitzinger-marathoning"] += 35
        scores["canova-marathon-method"] += 40
        reasons["canova-marathon-method"].append("High baseline volume (65+ mpw) enables elite-level specific endurance extensions.")
        scores["norwegian-endurance-method"] += 35
        reasons["norwegian-endurance-method"].append("High volume runner capable of absorbing single or double threshold sessions.")

    # 3. Days per week available
    if days_per_week <= 4:
        scores["daniels-running-formula"] += 35
        reasons["daniels-running-formula"].append("Daniels 2Q program concentrates quality into 2 key days, fitting busy schedules.")
        scores["galloway-run-walk-method"] += 25
        scores["hansons-marathon-method"] -= 30
        reasons["hansons-marathon-method"].append("Hansons requires a 6-day weekly commitment to distribute cumulative fatigue.")
    elif days_per_week == 5:
        scores["pfitzinger-marathoning"] += 20
        scores["daniels-running-formula"] += 25
        scores["hansons-marathon-method"] += 15
    elif days_per_week >= 6:
        scores["hansons-marathon-method"] += 35
        reasons["hansons-marathon-method"].append("6 days/week availability allows the 16-mile long run cap to work optimally.")
        scores["norwegian-endurance-method"] += 30
        scores["pfitzinger-marathoning"] += 30

    # 4. Primary Goal
    if goal in ["finish", "first_time", "completion"]:
        scores["galloway-run-walk-method"] += 40
        scores["maffetone-low-hr-method"] += 25
        scores["canova-marathon-method"] -= 50
    elif goal in ["pr", "pb", "time_goal", "bq"]:
        scores["pfitzinger-marathoning"] += 30
        scores["daniels-running-formula"] += 30
        scores["hansons-marathon-method"] += 25
        scores["norwegian-endurance-method"] += 30
    elif goal in ["elite", "sub_elite", "breakthrough"]:
        scores["canova-marathon-method"] += 45
        scores["norwegian-endurance-method"] += 40
        scores["pfitzinger-marathoning"] += 30

    # 5. Heart rate or lactate meter usage
    if has_hr_or_lactate:
        scores["norwegian-endurance-method"] += 25
        reasons["norwegian-endurance-method"].append("Athlete has HR / lactate monitoring for precise threshold intensity clamping.")
        scores["maffetone-low-hr-method"] += 25
        reasons["maffetone-low-hr-method"].append("Athlete has HR monitor to strictly enforce MAF ceiling.")

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_method, top_score = sorted_scores[0]
    runner_up, runner_up_score = sorted_scores[1]

    method_display_names = {
        "daniels-running-formula": "Jack Daniels' Running Formula (VDOT / 2Q)",
        "pfitzinger-marathoning": "Pete Pfitzinger (Advanced Marathoning / Faster Road Racing)",
        "hansons-marathon-method": "Hansons Marathon Method (Cumulative Fatigue & 16-mi Cap)",
        "norwegian-endurance-method": "Norwegian Sub-Threshold Method (Controlled Lactate / DT)",
        "canova-marathon-method": "Renato Canova Method (Specific Endurance & Funnel)",
        "maffetone-low-hr-method": "Phil Maffetone MAF 180 (Low-HR Aerobic Base)",
        "galloway-run-walk-method": "Jeff Galloway (Run-Walk-Run Method)"
    }

    return {
        "Top Method": top_method,
        "Top Method Name": method_display_names[top_method],
        "Top Score": top_score,
        "Rationale": reasons[top_method],
        "Runner Up": runner_up,
        "Runner Up Name": method_display_names[runner_up],
        "Runner Up Score": runner_up_score,
        "All Rankings": [(method_display_names[m], s) for m, s in sorted_scores]
    }

def main():
    parser = argparse.ArgumentParser(description="Master Running Coach Athlete Assessment Engine")
    parser.add_argument("--race", choices=["marathon", "half_marathon"], default="marathon", help="Target race distance")
    parser.add_argument("--mileage", type=int, required=True, help="Current weekly mileage in miles")
    parser.add_argument("--days", type=int, default=5, help="Days per week athlete is willing/able to run (3-7)")
    parser.add_argument("--goal", choices=["finish", "pr", "bq", "elite"], default="pr", help="Primary athletic goal")
    parser.add_argument("--injury-prone", action="store_true", help="Set flag if athlete is injury-prone or recovering")
    parser.add_argument("--hr-monitor", action="store_true", help="Set flag if athlete uses heart rate monitor / lactate meter")

    args = parser.parse_args()
    assessment = evaluate_runner(
        race_type=args.race,
        weekly_mileage=args.mileage,
        days_per_week=args.days,
        goal=args.goal,
        injury_prone=args.injury_prone,
        has_hr_or_lactate=args.hr_monitor
    )

    print("==================================================")
    print(f"  MASTER COACH RUNNER ASSESSMENT & METHOD SELECTION")
    print("==================================================")
    print(f"Athlete Profile: {args.race.upper()} | {args.mileage} MPW | {args.days} Days/Wk | Goal: {args.goal.upper()}")
    print(f"Injury Prone: {args.injury_prone} | HR Monitor / Sensor: {args.hr_monitor}")
    print("\n--------------------------------------------------")
    print(f">> #1 RECOMMENDED METHODOLOGY: {assessment['Top Method Name']}")
    print(f"   Skill Name: .agents/skills/{assessment['Top Method']}/SKILL.md")
    print("--------------------------------------------------")
    print("Match Rationale:")
    for r in assessment["Rationale"]:
        print(f"  - {r}")

    print(f"\n>> #2 ALTERNATIVE METHODOLOGY: {assessment['Runner Up Name']}")
    print(f"   Skill Name: .agents/skills/{assessment['Runner Up']}/SKILL.md")

    print("\n--- Complete Methodology Match Ranking ---")
    for name, sc in assessment["All Rankings"]:
        print(f"  [{sc:3d} pts] {name}")

if __name__ == "__main__":
    main()
