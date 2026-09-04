# Jack Daniels VDOT Pace Tables & Mathematical Formulas

This reference provides standard VDOT lookup values, training pace equivalents, and the underlying Daniels & Gilbert mathematical models.

---

## 1. VDOT Quick Reference Table

| VDOT | 5k Race | 10k Race | Half Marathon | Marathon | Easy (E) /km | Easy (E) /mi | Marathon (M) /km | Marathon (M) /mi | Threshold (T) /km | Threshold (T) /mi | Interval (I) /km | Interval (I) /mi | Repetition (R) /400m |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **35** | 27:00 | 56:06 | 2:04:40 | 4:19:00 | 6:40 - 7:22 | 10:44 - 11:51 | 6:08 | 9:53 | 5:44 | 9:14 | 5:16 | 8:28 | 1:57 |
| **40** | 24:08 | 50:03 | 1:50:59 | 3:49:45 | 5:58 - 6:35 | 9:36 - 10:36 | 5:26 | 8:46 | 5:06 | 8:12 | 4:40 | 7:31 | 1:44 |
| **45** | 21:50 | 45:16 | 1:40:20 | 3:28:00 | 5:27 - 6:01 | 8:46 - 9:41 | 4:56 | 7:56 | 4:37 | 7:26 | 4:14 | 6:49 | 1:34 |
| **50** | 19:57 | 41:21 | 1:31:35 | 3:10:49 | 5:02 - 5:33 | 8:06 - 8:56 | 4:31 | 7:17 | 4:14 | 6:49 | 3:53 | 6:15 | 1:26 |
| **55** | 18:22 | 38:06 | 1:24:18 | 2:56:00 | 4:41 - 5:10 | 7:32 - 8:19 | 4:10 | 6:42 | 3:55 | 6:18 | 3:35 | 5:46 | 1:19 |
| **60** | 17:03 | 35:22 | 1:18:07 | 2:43:18 | 4:23 - 4:50 | 7:03 - 7:47 | 3:52 | 6:14 | 3:38 | 5:51 | 3:20 | 5:22 | 1:13 |
| **65** | 15:54 | 32:59 | 1:12:49 | 2:32:15 | 4:08 - 4:33 | 6:39 - 7:20 | 3:37 | 5:49 | 3:24 | 5:28 | 3:07 | 5:01 | 1:08 |
| **70** | 14:55 | 30:53 | 1:08:12 | 2:22:30 | 3:54 - 4:18 | 6:17 - 6:55 | 3:23 | 5:26 | 3:11 | 5:08 | 2:56 | 4:43 | 1:04 |

---

## 2. Mathematical Model (Daniels & Gilbert Equation)

Given distance $d$ in meters and time $t$ in minutes:

### 1. Velocity ($v$)
$$v = \frac{d}{t} \quad (\text{meters/min})$$

### 2. Fractional Utilization ($\% \text{VO}_2\text{max}$)
$$p = 0.8 + 0.1894393 \cdot e^{-0.012778 \cdot t} + 0.2989558 \cdot e^{-0.1932605 \cdot t}$$

### 3. Oxygen Cost of Running ($\text{VO}_2$)
$$\text{VO}_2 = -4.60 + 0.182258 \cdot v + 0.000104 \cdot v^2 \quad (\text{ml/kg/min})$$

### 4. VDOT
$$\text{VDOT} = \frac{\text{VO}_2}{p}$$

---

## 3. Training Pace Derivations

Once $\text{VDOT}$ is established, target $\text{VO}_2$ demands are calculated for each zone:
- **Easy (E)**: $0.62 \cdot \text{VDOT}$ to $0.70 \cdot \text{VDOT}$
- **Marathon (M)**: $0.80 \cdot \text{VDOT}$ to $0.84 \cdot \text{VDOT}$ (or calculated directly from the predicted marathon finish velocity)
- **Threshold (T)**: $0.88 \cdot \text{VDOT}$
- **Interval (I)**: $0.98 \cdot \text{VDOT}$
- **Repetition (R)**: $1.08 \cdot \text{VDOT}$

To solve for the running velocity $v$ (m/min) at a target $\text{VO}_2$:
$$0.000104 \cdot v^2 + 0.182258 \cdot v - (4.60 + \text{VO}_2) = 0$$

Using the quadratic formula:
$$v = \frac{-0.182258 + \sqrt{(0.182258)^2 - 4(0.000104)(-(4.60 + \text{VO}_2))}}{2(0.000104)}$$
