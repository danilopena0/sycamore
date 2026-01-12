"""
Percentile calculation using the WHO LMS method.

The LMS method uses three parameters:
- L (Box-Cox power) for the skewness
- M (median) for the central tendency
- S (coefficient of variation) for the spread

Z-score formula:
  When L != 0: Z = ((value/M)^L - 1) / (L * S)
  When L == 0: Z = ln(value/M) / S

Percentile is then derived from the Z-score using the standard normal CDF.
"""

import math
from who_data import get_lms_data


def calculate_z_score(value: float, L: float, M: float, S: float) -> float:
    """Calculate Z-score using LMS parameters."""
    if value <= 0 or M <= 0:
        return None

    if abs(L) < 0.001:  # L approximately 0
        z = math.log(value / M) / S
    else:
        z = ((value / M) ** L - 1) / (L * S)

    return z


def normal_cdf(z: float) -> float:
    """Standard normal CDF using the error function."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def z_to_percentile(z: float) -> float:
    """Convert Z-score to percentile using standard normal CDF."""
    if z is None:
        return None
    return normal_cdf(z) * 100


def calculate_percentile(
    measurement_type: str, sex: str, age_months: int, value: float
) -> dict:
    """
    Calculate percentile for a given measurement.

    Args:
        measurement_type: 'weight' (kg) or 'length' (cm)
        sex: 'male' or 'female'
        age_months: Age in months (0-24)
        value: Measurement value (weight in kg, length in cm)

    Returns:
        Dictionary with z_score, percentile, and interpretation
    """
    if age_months < 0 or age_months > 24:
        return {"error": "Age must be between 0 and 24 months"}

    lms = get_lms_data(measurement_type, sex, age_months)
    if not lms:
        return {"error": "Could not find growth data for this age"}

    z = calculate_z_score(value, lms["L"], lms["M"], lms["S"])
    if z is None:
        return {"error": "Invalid measurement value"}

    percentile = z_to_percentile(z)

    return {
        "z_score": round(z, 2),
        "percentile": round(percentile, 1),
        "median": lms["M"],
        "interpretation": get_interpretation(percentile, measurement_type),
    }


def get_interpretation(percentile: float, measurement_type: str) -> str:
    """Generate a simple interpretation of the percentile."""
    metric = "weight" if measurement_type == "weight" else "length"

    if percentile < 3:
        return f"Your baby's {metric} is below the 3rd percentile, which may need medical attention."
    elif percentile < 15:
        return f"Your baby's {metric} is in the lower range but within normal limits."
    elif percentile <= 85:
        return f"Your baby's {metric} is in the typical range for their age."
    elif percentile <= 97:
        return f"Your baby's {metric} is in the higher range but within normal limits."
    else:
        return f"Your baby's {metric} is above the 97th percentile, which may need medical attention."


def calculate_both(sex: str, age_months: int, weight_kg: float, length_cm: float) -> dict:
    """Calculate percentiles for both weight and length."""
    weight_result = calculate_percentile("weight", sex, age_months, weight_kg)
    length_result = calculate_percentile("length", sex, age_months, length_cm)

    return {
        "weight": weight_result,
        "length": length_result,
        "age_months": age_months,
        "sex": sex,
    }
