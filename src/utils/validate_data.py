from typing import Tuple, List


def validate_telco_data(df) -> Tuple[bool, List[str]]:
    """
    Data validation for Telco Customer Churn dataset.
    Checks schema, values, and numeric ranges.
    """
    print("Starting data validation...")

    failed_expectations = []

    # === SCHEMA VALIDATION ===
    required_columns = [
        "customerID", "gender", "Partner", "Dependents",
        "PhoneService", "InternetService", "Contract",
        "tenure", "MonthlyCharges", "TotalCharges"
    ]
    for col in required_columns:
        if col not in df.columns:
            failed_expectations.append(f"missing_column_{col}")
        elif df[col].isnull().all():
            failed_expectations.append(f"all_null_{col}")

    # === VALUE SET VALIDATION ===
    value_checks = {
        "gender": ["Male", "Female"],
        "Partner": ["Yes", "No"],
        "Dependents": ["Yes", "No"],
        "PhoneService": ["Yes", "No"],
        "Contract": ["Month-to-month", "One year", "Two year"],
        "InternetService": ["DSL", "Fiber optic", "No"],
    }
    for col, valid_values in value_checks.items():
        if col in df.columns:
            invalid = set(df[col].dropna().unique()) - set(valid_values)
            if invalid:
                failed_expectations.append(f"invalid_values_{col}: {invalid}")

    # === NUMERIC RANGE VALIDATION ===
    if "tenure" in df.columns:
        if df["tenure"].min() < 0:
            failed_expectations.append("tenure_negative")
        if df["tenure"].max() > 120:
            failed_expectations.append("tenure_out_of_range")

    if "MonthlyCharges" in df.columns:
        if df["MonthlyCharges"].min() < 0:
            failed_expectations.append("MonthlyCharges_negative")

    if "TotalCharges" in df.columns:
        tc = df["TotalCharges"]
        if tc.dtype == "object":
            tc = tc.replace(" ", None)
            tc = tc.dropna()
        if len(tc) > 0 and tc.astype(float).min() < 0:
            failed_expectations.append("TotalCharges_negative")

    # === NULL CHECKS ===
    for col in ["tenure", "MonthlyCharges"]:
        if col in df.columns and df[col].isnull().any():
            failed_expectations.append(f"null_values_{col}")

    # === RESULTS ===
    if failed_expectations:
        print(f"Data validation FAILED: {len(failed_expectations)} issues found")
        print(f"   Issues: {failed_expectations}")
        return False, failed_expectations
    else:
        print("Data validation PASSED")
        return True, []
