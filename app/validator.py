
import pandas as pd


REQUIRED_COLUMNS = [
    "customer_id",
    "name",
    "email",
    "age"
]


def validate_dataset(file_path):
    """
    Validate a CSV dataset against predefined quality rules.
    """

    errors = []

    # 1. Read the CSV dataset
    try:
        df = pd.read_csv(file_path)
    except Exception as error:
        return [f"Unable to read dataset: {error}"]

    # 2. Validate required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )
        return errors

    # 3. Check for missing values
    for column in REQUIRED_COLUMNS:
        if df[column].isnull().any():
            errors.append(
                f"Column '{column}' contains missing values"
            )

    # 4. Check for duplicate customer IDs
    if df["customer_id"].duplicated().any():
        errors.append("Duplicate customer IDs detected")

    # 5. Validate age data type
    age = pd.to_numeric(df["age"], errors="coerce")

    if age.isnull().any():
        errors.append("Age contains invalid numeric values")
    else:
        # 6. Validate age range
        if ((age < 0) | (age > 120)).any():
            errors.append("Age must be between 0 and 120")

    return errors


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage: python validator.py <dataset.csv>")
        sys.exit(1)

    dataset = sys.argv[1]

    validation_errors = validate_dataset(dataset)

    if validation_errors:
        print("DATA VALIDATION FAILED")

        for error in validation_errors:
            print(f"- {error}")

        sys.exit(1)

    print("DATA VALIDATION PASSED")
    sys.exit(0)
