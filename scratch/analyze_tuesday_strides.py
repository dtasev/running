import csv

csv_path = r'c:\Users\Dimitar\RunningCoach\completed\w02\2026-09-08-i184641656_intervals.csv'
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

def parse_dist(d_str):
    if 'km' in d_str:
        return float(d_str.replace('km','')) * 1000
    return float(d_str.replace('m',''))

def parse_pace(p_str):
    parts = p_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])

# Overall totals
tot_d = 0
tot_mov_t = 0
tot_elap_t = 0
tot_gain = 0
hr_weighted = 0
pwr_weighted = 0
cad_weighted = 0
vo_weighted = 0
vr_weighted = 0
sl_weighted = 0
gap_dist_weighted = 0
max_hr_seen = 0

for r in rows:
    d = parse_dist(r['Distance'])
    el = float(r['Elapsed Time'])
    p_sec = parse_pace(r['Pace'])
    mov_t = (d / 1000.0) * p_sec
    gain = float(r['Altitude Gain'].replace('m',''))
    gap_sec = parse_pace(r['GAP'])
    hr = float(r['Avg HR'])
    mhr = float(r['Max HR'])
    pwr = float(r['Avg Power'])
    vo = float(r['Avg Vertical Oscillation'])
    vr = float(r['Avg Vertical Ratio'])
    sl = float(r['Stride'])
    cad = (d / mov_t / sl) * 60 if (sl > 0 and mov_t > 0) else 0

    tot_d += d
    tot_mov_t += mov_t
    tot_elap_t += el
    tot_gain += gain
    hr_weighted += hr * mov_t
    pwr_weighted += pwr * mov_t
    cad_weighted += cad * mov_t
    vo_weighted += vo * mov_t
    vr_weighted += vr * mov_t
    sl_weighted += sl * mov_t
    gap_dist_weighted += gap_sec * d
    if mhr > max_hr_seen:
        max_hr_seen = mhr

avg_mov_pace = tot_mov_t / (tot_d / 1000.0)
avg_gap = gap_dist_weighted / tot_d
avg_hr = hr_weighted / tot_mov_t
avg_pwr = pwr_weighted / tot_mov_t
avg_cad = cad_weighted / tot_mov_t
avg_vo = vo_weighted / tot_mov_t
avg_vr = vr_weighted / tot_mov_t
avg_sl = sl_weighted / tot_mov_t

print(f"=== TOTAL WORKOUT ===")
print(f"Distance: {tot_d/1000:.2f} km")
print(f"Moving Time: {int(tot_mov_t//60)}:{int(tot_mov_t%60):02d} | Elapsed: {int(tot_elap_t//60)}:{int(tot_elap_t%60):02d}")
print(f"Avg Moving Pace: {int(avg_mov_pace//60)}:{int(round(avg_mov_pace%60)):02d} /km | GAP: {int(avg_gap//60)}:{int(round(avg_gap%60)):02d} /km")
print(f"Avg HR: {avg_hr:.1f} bpm | Peak HR: {max_hr_seen:.0f} bpm")
print(f"Avg Cadence: {avg_cad:.1f} spm | Stride: {avg_sl:.2f} m")
print(f"Avg Power: {avg_pwr:.1f} W | Elev Gain: {tot_gain:.0f} m")
print(f"VO: {avg_vo:.1f} mm | VR: {avg_vr:.2f} %")
print()

# Breakdown of the 6 strides and walks:
# Stride 1: rows 1 to 5 (indices 2 to 6 in rows, 0-indexed: rows[1:6])
# Walk 1: rows[6:9]
# Stride 2: rows[9:14]
# Walk 2: rows[14:17]
# Stride 3: rows[17:23]
# Walk 3: rows[23:26]
# Stride 4: rows[26:32]
# Walk 4: rows[32:35]
# Stride 5: rows[35:41]
# Walk 5: rows[41:44]
# Stride 6: rows[44:50]
# Walk 6: rows[50:53]
# Cooldown: rows[53] (last row)

strides_data = [
    ("Stride 1", rows[1:6], rows[6:9]),
    ("Stride 2", rows[9:14], rows[14:17]),
    ("Stride 3", rows[17:23], rows[23:26]),
    ("Stride 4", rows[26:32], rows[32:35]),
    ("Stride 5", rows[35:41], rows[41:44]),
    ("Stride 6", rows[44:50], rows[50:53]),
]

for name, s_rows, w_rows in strides_data:
    s_d = sum(parse_dist(r['Distance']) for r in s_rows)
    s_t = sum((parse_dist(r['Distance'])/1000.0)*parse_pace(r['Pace']) for r in s_rows)
    s_p = s_t / (s_d / 1000.0)
    best_pace = min(parse_pace(r['Pace']) for r in s_rows)
    max_hr = max(float(r['Max HR']) for r in s_rows)
    max_pwr = max(float(r['Avg Power']) for r in s_rows)
    max_sl = max(float(r['Stride']) for r in s_rows)
    
    w_d = sum(parse_dist(r['Distance']) for r in w_rows)
    w_t = sum(float(r['Elapsed Time']) for r in w_rows)
    w_min_hr = min(float(r['Avg HR']) for r in w_rows)
    
    print(f"{name}: {s_d:.0f}m in {s_t:.1f}s | Avg Pace: {int(s_p//60)}:{int(round(s_p%60)):02d}/km | Fast Split: {int(best_pace//60)}:{int(best_pace%60):02d}/km | Max HR: {max_hr:.0f} | Peak Pwr: {max_pwr:.0f}W | Stride: {max_sl:.2f}m")
    print(f"  Recovery Walk: {w_d:.0f}m in {w_t:.0f}s | HR dropped to: {w_min_hr:.0f} bpm")
