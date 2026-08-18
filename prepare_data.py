"""
Convert the raw thesis spreadsheet into a clean, analysis-ready CSV.

Run once:  python prepare_data.py path/to/DATA_SHEET_THESIS.xlsx

Key cleaning step: the raw 'Height (ft)' column is stored in feet-inches
notation as a decimal (5.6 means 5 feet 6 inches, NOT 5.6 feet). Reading it
as a plain decimal produces heights that are wrong by up to 9 cm and BMI
values wrong by up to 7 units. The decoding below is validated against the
BMI column that was computed by hand in the original sheet.
"""

import os
import sys
import numpy as np
import pandas as pd

RAW_TO_CLEAN = {
    "Age": "age",
    "Gender": "sex",
    "Weight (kg)": "weight_kg",
    "BMI": "bmi_original",
    "Category": "bmi_category",
    "Liver Right Lobe Length (mm)": "liver_right_lobe_mm",
    "liver left lobe length (mm)": "liver_left_lobe_mm",
    "Kidney Right Length (mm)": "kidney_right_length_mm",
    "Kidney Left Length (mm)": "kidney_left_length_mm",
    "Kidney Right Width (mm)": "kidney_right_width_mm",
    "Kidney Left Width (mm)": "kidney_left_width_mm",
    "Cortical Thickness Right (mm)": "cortex_right_mm",
    "Cortical Thickness Left (mm)": "cortex_left_mm",
}


def feet_inches_to_cm(value: float) -> float:
    """5.6 -> 5 ft 6 in -> 167.6 cm ;  5.11 -> 5 ft 11 in -> 180.3 cm"""
    text = f"{value:.10g}"
    feet_part, _, dec_part = text.partition(".")
    feet = int(feet_part)
    inches = int(dec_part) if dec_part else 0      # "11" -> 11, "6" -> 6
    return round((feet * 12 + inches) * 2.54, 1)


def main(xlsx_path: str) -> None:
    raw = pd.read_excel(xlsx_path)
    raw.columns = [c.strip() for c in raw.columns]

    df = raw.rename(columns=RAW_TO_CLEAN)[list(RAW_TO_CLEAN.values())].copy()

    # anonymous sequential ID — the raw sheet carries no names or MR numbers
    df.insert(0, "participant_id", [f"P{i:03d}" for i in range(1, len(df) + 1)])

    df["height_cm"] = raw["Height (ft)"].apply(feet_inches_to_cm)
    df["bmi"] = (df["weight_kg"] / (df["height_cm"] / 100) ** 2).round(1)
    # Mosteller body surface area
    df["bsa_m2"] = np.sqrt(df["height_cm"] * df["weight_kg"] / 3600).round(3)

    # validate the height decoding against the hand-computed BMI in the sheet
    drift = (df["bmi"] - df["bmi_original"]).abs()
    print(f"BMI validation: max drift {drift.max():.2f}, mean {drift.mean():.3f}")
    if drift.max() > 0.5:
        raise SystemExit("Height decoding failed validation — check the raw column.")

    df = df.drop(columns=["bmi_original"])

    order = ["participant_id", "age", "sex", "height_cm", "weight_kg", "bmi",
             "bsa_m2", "bmi_category", "liver_right_lobe_mm", "liver_left_lobe_mm",
             "kidney_right_length_mm", "kidney_left_length_mm",
             "kidney_right_width_mm", "kidney_left_width_mm",
             "cortex_right_mm", "cortex_left_mm"]
    df = df[order]

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/liver_morphometry.csv", index=False)
    print(f"Wrote data/liver_morphometry.csv  ({df.shape[0]} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "DATA_SHEET_THESIS.xlsx")
