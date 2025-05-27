# Feature Documentation

This document provides detailed explanations for each feature used in the Mental Health Burnout Detection System. These features are derived from daily user logs and engineered metrics, designed to capture the behavioral and physiological patterns most relevant to burnout risk.

---

## 1. sleep_hours

**Description:**  
Total hours of sleep the user got each night.

**Rationale:**  
Sustained lack of sleep is a strong indicator of increased stress and reduced recovery. Consistently short sleep is a known early warning sign for both mental and physical burnout.

---

## 2. work_sleep_ratio

**Description:**  
The ratio of daily work hours to sleep hours.

**Rationale:**  
This feature highlights the balance between work and rest. A high ratio suggests the user is working much more than they are resting, which is closely linked to chronic stress and burnout.

---

## 3. heart_rate_avg

**Description:**  
The average resting heart rate for the day.

**Rationale:**  
Elevated heart rate over time is a physiological marker of stress and poor recovery. Chronic stress can keep heart rates high, increasing the risk of burnout.

---

## 4. screen_time_hours

**Description:**  
Total hours spent on screens outside of work (e.g., phone, TV, computer).

**Rationale:**  
High screen time, especially late at night or in excess, is associated with poor sleep, reduced physical activity, and increased mental fatigue, all of which contribute to burnout.

---

## 5. work_hours

**Description:**  
Total hours worked in a day.

**Rationale:**  
Sustained long work hours are a direct contributor to burnout, reducing time for recovery and increasing the risk of chronic stress and exhaustion.

---

## 6. screen_steps_ratio

**Description:**  
The ratio of screen time to steps (physical activity).

**Rationale:**  
This metric highlights the trade-off between sedentary (screen) and active (steps) behavior. A high ratio indicates more time spent on screens than moving, which is linked to higher stress and burnout risk.

---

## 7. heart_rate_avg_rolling_var

**Description:**  
Variance in heart rate over the past 7 days.

**Rationale:**  
High variability in heart rate can indicate unstable or erratic stress patterns, reflecting periods of acute stress or poor recovery.

---

## 8. sleep_hours_rolling_mean

**Description:**  
Average sleep hours over the past 7 days.

**Rationale:**  
This smooths out daily fluctuations and highlights persistent sleep deprivation or recovery. Chronic short sleep over a week is more predictive of burnout than a single bad night.

---

## 9. screen_time_hours_rolling_mean

**Description:**  
Average screen time over the past 7 days.

**Rationale:**  
Sustained high screen time over a week can indicate ongoing digital overload and poor work-life balance.

---

## 10. heart_rate_avg_rolling_mean

**Description:**  
Average heart rate over the past 7 days.

**Rationale:**  
Persistent elevation in heart rate across a week is a strong sign of ongoing strain and insufficient recovery.

---

## 11. sleep_hours_rolling_var

**Description:**  
Variance in sleep hours over the past 7 days.

**Rationale:**  
High variance indicates irregular sleep patterns, which are linked to poor recovery and increased burnout risk, even if the average sleep is adequate.

---

## 12. steps

**Description:**  
Number of steps taken per day.

**Rationale:**  
Physical activity is protective against burnout. Lower step counts can indicate sedentary behavior, which is associated with higher stress and poorer mental health.

---

## 13. work_hours_rolling_mean

**Description:**  
Average work hours over the past 7 days.

**Rationale:**  
Chronic overwork across a week is a stronger predictor of burnout than a single long day. This feature helps detect ongoing excessive workload.

---

## 14. screen_time_hours_rolling_var

**Description:**  
Variance in screen time over the past 7 days.

**Rationale:**  
Irregular screen habits can reflect inconsistent routines, which are stressful for the body and mind.

---

## 15. work_hours_rolling_var

**Description:**  
Variance in work hours over the past 7 days.

**Rationale:**  
Fluctuating work schedules can be stressful and make it harder for users to recover, increasing burnout risk.

---

## 16. cumulative_work_hours

**Description:**  
Total work hours accumulated by the user up to that date.

**Rationale:**  
This feature captures the long-term buildup of work demands. Chronic overwork, even with some rest days, increases the risk of eventual burnout.

---