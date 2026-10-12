---
name: intervals-icu-workout-format
description: >-
  Intervals.icu plain-text workout builder syntax reference and code generator for running,
  cycling, and swimming structured workouts. Covers duration/distance definitions, pace/HR/power
  targets, repeats, ramps, cadence, prompts, and markdown metadata.
---

# Intervals.icu Workout Builder Syntax Guide & Generator

Intervals.icu allows athletes and coaches to build structured workouts using human-readable plain text. The platform automatically parses each line to determine workout structure, steps, target ranges, duration, training load (TSS/HRSS), and Garmin/Wahoo/Suunto/Zwift export instructions.

---

## 1. Core Step Syntax & Rules

Every executable workout step **must begin with a hyphen and a space (`- `)**:

```text
- [Step Cue / Prompt] [Duration OR Distance] [Target] [Optional Cadence / Notes]
```

### Essential Parsing Rules:
1. **Hyphen (`- `)** defines an active step. Lines without a leading `- ` (such as markdown headers, notes, or blank lines) are treated as athlete instructions/notes and ignored by the workout parser.
2. **`m` means MINUTES, never meters!**
   - `5m` = 5 minutes.
   - For meters, you **must use `mtr`** (e.g., `400mtr`, `1000mtr`).
3. **Step Cue / Label**: Any text placed *before* the duration or distance becomes the display label/cue on watches and head units (e.g., `- Warmup 15m ...`, `- Easy Jog 500mtr ...`).
4. **Blank Lines**: Always place a blank line before and after repeat blocks (`5x` or `Main Set 4x`).

---

## 2. Duration & Distance Specifications

### Time / Duration
- **Minutes**: `10m`, `5m`, `30m`
- **Seconds**: `30s`, `45s`, `90s`
- **Hours**: `1h`, `1.5h`, `2h`
- **Combined**: `1h15m`, `5m30s`, `1h2m30s`
- **Shorthand / Quotes**: `5'`, `30"`, `1'30"`

### Distance
- **Meters**: `100mtr`, `400mtr`, `800mtr`, `1200mtr` (*Never use `m`*)
- **Kilometers**: `1km`, `2.5km`, `10km`, `15km`
- **Miles**: `1mi`, `4.5mi`, `10mi`

### Open Duration (Lap Button Press)
- Include `Press lap` to make a step indefinite until the athlete manually presses the watch lap key (ideal for open warmups, cooldowns, or crossing intersections):
  ```text
  - Warmup Press lap 65% HR
  - Cooldown Press lap 5:45/km Pace
  ```

---

## 3. Targets (Pace, Heart Rate, Power)

### Running Pace Targets
Pace can be specified as absolute pace (`mm:ss/km Pace` or `mm:ss/mi Pace`), percentage of threshold pace, or pace zones:

| Target Syntax | Description | Example |
| :--- | :--- | :--- |
| `mm:ss/km Pace` | Absolute pace per kilometer | `5:25/km Pace` |
| `mm:ss-mm:ss/km Pace` | Pace range per kilometer | `5:25-5:30/km Pace` |
| `mm:ss/mi Pace` | Absolute pace per mile | `8:00/mi Pace` |
| `mm:ss-mm:ss/mi Pace` | Pace range per mile | `7:55-8:05/mi Pace` |
| `% Pace` | Percent of Threshold Pace | `80% Pace`, `75-82% Pace` |
| `Z# Pace` | Structured Pace Zone | `Z2 Pace`, `Z2-Z3 Pace` |

> [!NOTE]
> When defining pace, adding the explicit unit `/km Pace` or `/mi Pace` ensures unambiguous cross-platform syncing to Garmin Connect and watch screens.

### Heart Rate Targets
Heart rate can be specified as % of Max Heart Rate, % of Lactate Threshold Heart Rate (LTHR), or HR zones:

| Target Syntax | Description | Example |
| :--- | :--- | :--- |
| `% HR` | Percent of Maximum Heart Rate | `70% HR`, `70-75% HR` |
| `% LTHR` | Percent of Threshold Heart Rate | `85% LTHR`, `90-95% LTHR` |
| `Z# HR` | Structured Heart Rate Zone | `Z2 HR`, `Z1-Z2 HR` |
| `bpm HR` | Absolute beats per minute (where supported) | `140-150bpm HR` |

### Power Targets (Running Stryd / Cycling)
| Target Syntax | Description | Example |
| :--- | :--- | :--- |
| `%` | Percent of FTP | `75%`, `90-95%` |
| `w` | Absolute Watts | `350w`, `330-350w` |
| `Z#` | Power Zone | `Z2`, `Z3-Z4` |
| `% MMP 5m` | Percent of Mean Maximal Power | `85% MMP 5m` |

---

## 4. Cadence & Dynamic Modifiers

### Cadence
Append cadence to the end of any step:
- `180spm` or `175-185spm` (Running strides per minute)
- `90rpm` or `85-95rpm` (Cycling revolutions per minute)

```text
- 5km 5:25/km Pace 180spm
- 10m 75% 90rpm
```

### Ramps (Gradual Progression)
Use `ramp` for progressive steps:
```text
- Progression 10km ramp 5:40-5:15/km Pace
- 15m ramp 60-80% HR
- 10m ramp 50%-75%
```

### Freeride
Disables trainer ERG mode for open sprints or drills:
```text
- 20m freeride
```

---

## 5. Repeats & Interval Sets

Repeats can be defined either as a named block header or a simple repeat count:

### Format A: Named Header with Repeat Count
```text
Warmup
- 2km 5:45/km Pace

Intervals 6x
- Fast 800mtr 4:10-4:15/km Pace
- Recovery 400mtr 6:00/km Pace

Cooldown
- 2km 5:50/km Pace
```

### Format B: Simple Repeat Count Line
```text
5x
- 3m 105%
- 2m 50%
```

> [!IMPORTANT]
> - Always leave an empty blank line before and after each repeat block.
> - Nested repeats (a repeat block inside another repeat block) are **not supported**.

---

## 6. Text Prompts & In-Step Timed Cues

### Basic Step Prompt
Any text before the duration/distance is displayed on the athlete's screen:
```text
- Easy Aerobic 10km 5:30/km Pace
- Strides 100mtr 3:30/km Pace
```

### Timed Cues Inside a Single Step
Use `[sec]^[cue text] <!> [duration] [target]` for midpoint reminders (e.g. nutrition, form checks):
```text
- Drink fluid    1800^Take energy gel    <!> 1h 5:25/km Pace
```

---

## 7. Markdown Notes & Metadata Wrapping (Using `>`)

Intervals.icu allows notes and metadata, but the parser is sensitive:
> [!CRITICAL]
> 1. **Any line starting with `- ` is treated as a workout step!** Never use standard Markdown bullet points (`- Item`) in your notes, as they will pollute the parsed workout.
> 2. **Always prefix workout notes and descriptions with `>` (Markdown blockquote)**. When lines start with `>`, Intervals.icu's workout parser completely ignores them when constructing steps, but displays them cleanly as styled callout notes in the UI.
> 3. Separate the blockquote notes from the executable steps with `---`.

### Correct Syntax Example:
```text
> # Pfitzinger W06 - Rebalanced Long Run (15 km)
>
> Focus: Controlled progressive endurance run. Keep the opening 3 km relaxed to let Friday's recovery fatigue wash out.
>
> • Distance: 15.0 km
> • Target Pace: 5:25 – 5:35 min/km (Progressive)
> • Heart Rate Ceiling: < 155 bpm (Endurance Zone)
> • Nutrition: Sip fluids every 20 min; take 1 energy gel at KM 10.

---

- Warmup Easy 3km 5:35-5:45/km Pace 176-180spm
- Steady Endurance 10km 5:25-5:30/km Pace 178-182spm
- Strong Finish 2km 5:20-5:25/km Pace 180-184spm
```

---

## 8. Common Syntax Pitfalls Checklist

| Error | Cause | Correct Syntax |
| :--- | :--- | :--- |
| Notes polluted as steps | Used `- Bullet` in notes above steps | Prefix all notes with `>` and avoid `- ` bullets |
| `- 400m 4:15/km` | `m` is parsed as 400 **minutes**! | `- 400mtr 4:15/km Pace` |
| `Warmup 10m 5:30/km` | Missing leading `- ` (ignored as a note) | `- Warmup 10m 5:30/km Pace` |
| `5:30 Pace` without unit | May default to watch or account preference | `5:30/km Pace` or `8:50/mi Pace` |
| `Main Set 4x` without blank lines | Repeats bleed into surrounding steps | Keep blank line above and below |
| `- 5km 145-155 HR` | Unspecified HR metric | `- 5km 75-80% HR` or `- 5km Z2 HR` |

