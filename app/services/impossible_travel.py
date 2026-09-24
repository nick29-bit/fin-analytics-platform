import numpy as np
import pandas as pd

def haversine_km(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        np.sin(delta_lat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(delta_lon / 2) ** 2
    )

    a = np.clip(a, 0, 1)
    return earth_radius_km * 2 * np.arcsin(np.sqrt(a))
def flag_impossible_travel(
    df: pd.DataFrame,
    max_speed_kmh: float = 900,
) -> pd.DataFrame:
    result = df.sort_values(
        ["card_number", "transaction_timestamp"],
        kind="stable",
    ).copy()

    previous = result.groupby("card_number")[
        ["transaction_timestamp", "merchant_lat", "merchant_long"]
    ].shift(1)

    result["distance_km"] = haversine_km(
        previous["merchant_lat"],
        previous["merchant_long"],
        result["merchant_lat"],
        result["merchant_long"],
    )

    elapsed_hours = (
        result["transaction_timestamp"]
        - previous["transaction_timestamp"]
    ).dt.total_seconds() / 3600

    result["elapsed_hours"] = elapsed_hours

    # Calculate speed only where elapsed time is positive.
    result["required_speed_kmh"] = (
        result["distance_km"]
        / elapsed_hours.where(elapsed_hours > 0)
    )

    # Different locations at the same timestamp need explicit handling.
    simultaneous_travel = (
        elapsed_hours.eq(0) & result["distance_km"].gt(0)
    )
    result.loc[
        simultaneous_travel, "required_speed_kmh"
    ] = np.inf

    result["impossible_travel_flag"] = (
        result["required_speed_kmh"] > max_speed_kmh
    )

    return result