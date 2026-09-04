# RunningCoach: Comprehensive Marathon & Half-Marathon Coaching Skills Suite

An evidence-based knowledge base and operational skills suite for **Antigravity AI Running Coach Agents**, featuring major running methodologies, physiological pacing calculators, and periodized training templates for **Marathon** and **Half Marathon** preparation.

---

## 🧭 Skills Suite Directory

All skills are structured in `.agents/skills/` following the Antigravity skill architecture:

```text
.agents/skills/
├── running-coach-orchestrator/       # Master Intake, Methodology Decision Matrix & CLI
├── daniels-running-formula/          # Jack Daniels VDOT, E/M/T/I/R Zones, 2Q Marathon Plans
├── pfitzinger-marathoning/           # Pete Pfitzinger LT Focus, Midweek MLRs, 18/55 & 18/70 Plans
├── hansons-marathon-method/          # Cumulative Fatigue, 16-mi Long Run Cap, SOS Workouts
├── norwegian-endurance-method/       # Double Threshold & Sub-Threshold Lactate Control
├── canova-marathon-method/           # Renato Canova Funnel Periodization & Specific Endurance
├── maffetone-low-hr-method/          # Dr. Phil Maffetone MAF 180 Low-HR Base & MAF Track Tests
└── galloway-run-walk-method/         # Jeff Galloway Run-Walk-Run & Magic Mile Strategy
```

---

## 📊 Methodology Comparison Matrix

| Methodology | Core Philosophy | Signature Workout | Long Run Limit | Frequency | Ideal Athlete |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Jack Daniels (VDOT)** | Mathematical pacing by physiological zone (E/M/T/I/R) | Cruise Intervals ($5 \times 1\text{ mi @ T}$) & 2Q blocks | 18–20 mi (or 2.5 hrs) | 4–6 days/wk | Data-driven, flexible schedule |
| **Pete Pfitzinger (Pfitz)** | High endurance base, lactate threshold, fatigue resistance | Midweek Medium-Long Run (11–15 mi) & LT Tempos | 20–22 mi (Progressive) | 5–6 days/wk | Ambitious runners targeting BQ/PR |
| **Hansons Marathon** | Cumulative fatigue; training on tired legs without muscle breakdown | Something of Substance (SOS) Triad (Speed/Strength, Tempo, Long) | **16 miles max** (25-33% weekly volume) | **Strictly 6 days/wk** | Runners avoiding 20+ miler breakdown |
| **Norwegian Method** | Sub-threshold volume with blood lactate clamping ($< 3.8\text{ mmol/L}$) | Double Threshold days ($20 \times 400\text{m} + 5 \times 6\text{ min}$) | Specific MP long blocks (30–34 km) | 5–7 days/wk | Athletes with HR/lactate meters |
| **Renato Canova** | Funnel periodization toward Specific Race Endurance (95–102% MP) | Special Blocks (AM/PM double hard sessions) | Long Fast Runs (28–35 km @ 92–95% MP) | 6–7 days/wk | Competitive, sub-elite, and elite |
| **Phil Maffetone (MAF)** | Pure aerobic fat burning capped at $(180 - \text{age})$ HR | Monthly MAF 5-mile track time trial | 16–20 mi at MAF HR | 4–6 days/wk | Overtrained, injury recovery, base |
| **Jeff Galloway (RWR)** | Strategic Run-Walk-Run intervals to eliminate the wall | Magic Mile time trial & Over-distance runs | Over-distance (26–29 mi) | 3–4 days/wk | First-time marathoners, injury-prone |

---

## 🛠️ Python CLI Calculation Tools

Each skill includes an executable script to calculate exact training paces, heart-rate zones, and workouts:

1. **Master Athlete Diagnostic & Selector**:
   ```bash
   python .agents/skills/running-coach-orchestrator/scripts/coach_assessment.py --race marathon --mileage 45 --days 5 --goal pr --hr-monitor
   ```
2. **Jack Daniels VDOT Calculator**:
   ```bash
   python .agents/skills/daniels-running-formula/scripts/vdot_calculator.py --distance 5k --time 19:45
   ```
3. **Pete Pfitzinger Heart Rate Zone & Plan Tool**:
   ```bash
   python .agents/skills/pfitzinger-marathoning/scripts/pfitz_planner.py --max-hr 185 --rest-hr 50 --plan marathon_18_70
   ```
4. **Hansons Marathon Method Pace Calculator**:
   ```bash
   python .agents/skills/hansons-marathon-method/scripts/hansons_calculator.py --goal-time 3:30:00
   ```
5. **Norwegian Sub-Threshold Calculator**:
   ```bash
   python .agents/skills/norwegian-endurance-method/scripts/norwegian_calculator.py --distance 10k --time 38:30 --max-hr 188
   ```
6. **Maffetone MAF 180 Formula Calculator**:
   ```bash
   python .agents/skills/maffetone-low-hr-method/scripts/maf_calculator.py --age 35 --category 3
   ```
7. **Jeff Galloway Magic Mile & Run-Walk-Run Ratio Tool**:
   ```bash
   python .agents/skills/galloway-run-walk-method/scripts/galloway_calculator.py --magic-mile 7:45
   ```

---

## 📖 Training Plan Catalog

Each skill includes ready-to-run 12-to-24-week periodized plans:
- [Daniels 18-Week 2Q Marathon Plan](.agents/skills/daniels-running-formula/examples/marathon_2q_18_week.md)
- [Daniels 16-Week Half Marathon Plan](.agents/skills/daniels-running-formula/examples/half_marathon_16_week.md)
- [Pfitzinger Marathon 18/55 Plan](.agents/skills/pfitzinger-marathoning/examples/marathon_18_55.md)
- [Pfitzinger Marathon 18/70 Plan](.agents/skills/pfitzinger-marathoning/examples/marathon_18_70.md)
- [Pfitzinger Half Marathon 12/63 Plan](.agents/skills/pfitzinger-marathoning/examples/half_marathon_12_63.md)
- [Hansons Advanced Marathon 18-Week Plan](.agents/skills/hansons-marathon-method/examples/marathon_advanced_18_week.md)
- [Hansons Half Marathon 18-Week Plan](.agents/skills/hansons-marathon-method/examples/half_marathon_18_week.md)
- [Norwegian Marathon 16-Week Threshold Plan](.agents/skills/norwegian-endurance-method/examples/marathon_threshold_block.md)
- [Norwegian Half Marathon 12-Week Threshold Plan](.agents/skills/norwegian-endurance-method/examples/half_marathon_threshold_plan.md)
- [Canova Elite Marathon 8-Week Specific Period](.agents/skills/canova-marathon-method/examples/elite_marathon_specific_period.md)
- [Maffetone Marathon 16-Week Base & Build Plan](.agents/skills/maffetone-low-hr-method/examples/maf_marathon_16_week.md)
- [Galloway First-Time Marathon 24-Week Plan](.agents/skills/galloway-run-walk-method/examples/first_time_marathon_plan.md)
- [Galloway Half Marathon 16-Week Plan](.agents/skills/galloway-run-walk-method/examples/half_marathon_run_walk_plan.md)
