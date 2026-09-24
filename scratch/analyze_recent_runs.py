import csv

def parse_dist(d_str):
    if 'km' in d_str:
        return float(d_str.replace('km','')) * 1000
    return float(d_str.replace('m',''))

def parse_pace(p_str):
    parts = p_str.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def analyze_file(csv_path, title):
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

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

    time_rec = 0
    time_ga = 0
    time_mp = 0
    time_lt = 0
    time_vo2 = 0

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

        if hr < 142:
            time_rec += mov_t
        elif hr <= 152:
            time_ga += mov_t
        elif hr <= 165:
            time_mp += mov_t
        elif hr <= 175:
            time_lt += mov_t
        else:
            time_vo2 += mov_t

    avg_mov_pace = tot_mov_t / (tot_d / 1000.0)
    avg_gap = gap_dist_weighted / tot_d
    avg_hr = hr_weighted / tot_mov_t
    avg_pwr = pwr_weighted / tot_mov_t
    avg_cad = cad_weighted / tot_mov_t
    avg_vo = vo_weighted / tot_mov_t
    avg_vr = vr_weighted / tot_mov_t
    avg_sl = sl_weighted / tot_mov_t

    print(f"=== {title} ===")
    print(f"Intervals count: {len(rows)}")
    print(f"Distance: {tot_d/1000:.2f} km ({tot_d:.0f} m)")
    print(f"Moving Time: {int(tot_mov_t//60)}:{int(tot_mov_t%60):02d} | Elapsed: {int(tot_elap_t//60)}:{int(tot_elap_t%60):02d} (Pause: {int((tot_elap_t-tot_mov_t)//60)}:{int((tot_elap_t-tot_mov_t)%60):02d})")
    print(f"Moving Pace: {int(avg_mov_pace//60)}:{int(round(avg_mov_pace%60)):02d} /km | GAP: {int(avg_gap//60)}:{int(round(avg_gap%60)):02d} /km")
    print(f"Avg HR: {avg_hr:.1f} bpm | Peak HR: {max_hr_seen:.0f} bpm")
    print(f"Avg Cadence: {avg_cad:.1f} spm | Stride: {avg_sl:.2f} m")
    print(f"Avg Power: {avg_pwr:.1f} W | Elev Gain: {tot_gain:.0f} m")
    print(f"VO: {avg_vo:.1f} mm | VR: {avg_vr:.2f} %")
    print(f"Zones: Rec (<142): {time_rec/tot_mov_t*100:.1f}% ({time_rec/60:.1f}m) | GA (142-152): {time_ga/tot_mov_t*100:.1f}% ({time_ga/60:.1f}m) | MP (153-165): {time_mp/tot_mov_t*100:.1f}% ({time_mp/60:.1f}m) | LT (166-175): {time_lt/tot_mov_t*100:.1f}% ({time_lt/60:.1f}m) | VO2 (>175): {time_vo2/tot_mov_t*100:.1f}% ({time_vo2/60:.1f}m)")
    print()

analyze_file(r'C:\Users\Dimitar\RunningCoach\completed\w03\2026-09-20-i188568187_intervals.csv', "W03 Sunday: 5km (Illness Diagnostic)")
analyze_file(r'C:\Users\Dimitar\RunningCoach\completed\w04\2026-09-24-1-i189909225_intervals.csv', "W04 Thursday: Run 1 (10km)")
analyze_file(r'C:\Users\Dimitar\RunningCoach\completed\w04\2026-09-24-2-i189997786_intervals.csv', "W04 Thursday: Run 2 (5km)")
