# Sleep, Steps, and Screen Time Analysis Pipeline

This project processes MiBand data and Screen Data (StayFree app) to analyze how daily habits  affect sleep quality. It includes data cleaning, feature engineering, merging, and model evaluation using classification and hypothesis testing.

---

##  Run Order

**To set up your data correctly, run the following scripts in this exact order:**

1. **`DataSeperation.py`**
   - Parses the original raw CSV data.
   - Converts timestamps, separates data by type (`sleep.csv`, `steps.csv`, etc.).
   - Saves cleaned datasets to individual files including `sleep_items.csv`.

2. **`SleepGrading.py`**
   - Reads `sleep.csv`.
   - Computes a numeric `sleep_score` and labels each night as `"Good"`, `"Average"`, or `"Bad"`.
   - Flags days where naps occurred.
   - Outputs `sleep_processed.csv`.

3. **`ScreenTimeCleaning.py`**
   - Processes Excel files with screen usage and unlock data.
   - Extracts total screen time, per-app usage, and unlock count.
   - Calculates `social_media_ratio` and `game_ratio`.
   - Saves the result to `screen_cleaned_with_ratios.csv`.

4. **`StepsProcessing.py`**
   - Matches daily steps with sleep sessions from `sleep_processed.csv`.
   - Filters out steps taken during sleep.
   - Computes total steps and steps 2 hours before sleep.
   - Outputs `steps_cleaned.csv`.

5. **`Merging.py`**
   - Merges `sleep_processed.csv`, `steps_cleaned.csv`, and `screen_cleaned_with_ratios.csv` into two model-ready datasets:
     - `model_ready_steps_sleep.csv`: only sleep + steps data.
     - `model_ready_all.csv`: full dataset with screen time.

---

## 📊 Analysis & Modeling

These scripts can be run **independently after merging**:

- **`hypothesis test.py`**
  - Performs ANOVA tests to evaluate if screen time or steps vary significantly across sleep quality groups.
  - Visualizes results with boxplots.

- **`RandomForestClassifier.py`**
  - Builds and evaluates a Random Forest model to predict sleep quality.
  - Uses features like steps, screen time, app usage, etc.
  - Includes synthetic data balancing and visualizes feature importance.

---

## 📁 Output Files

- `sleep.csv`, `steps.csv`, `spo2.csv`, etc. — from `DataSeperation.py`
- `sleep_processed.csv` — after scoring and labeling
- `steps_cleaned.csv` — daily step summaries
- `screen_cleaned_with_ratios.csv` — screen usage metrics
- `model_ready_steps_sleep.csv` and `model_ready_all.csv` — merged, cleaned datasets for modeling

---

##  Notes

- Ensure your raw input files are located in the `Data/` folder before starting.
- All scripts assume specific paths and file names, so keep the folder structure intact.
