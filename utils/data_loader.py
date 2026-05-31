from pathlib import Path

import pandas as pd

from config.settings import DATA_DIR


def load_test_profiles(csv_path: Path | None = None) -> list[dict]:
    """Load employee profile rows from CSV test data."""
    path = csv_path or (DATA_DIR / "test_profiles.csv")
    dataframe = pd.read_csv(path)
    return dataframe.to_dict(orient="records")


def get_profile_by_name(name: str, csv_path: Path | None = None) -> dict:
    """Return a single profile row matching the given name."""
    profiles = load_test_profiles(csv_path)
    for profile in profiles:
        if profile["name"] == name:
            return profile
    raise ValueError(f"No profile found for name: {name}")
