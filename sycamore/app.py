"""
Sycamore - Baby Growth Percentile Calculator
A simple web app to track infant growth using WHO standards.
"""

from flask import Flask, render_template, request, jsonify
from percentile import calculate_both

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """Calculate percentiles from form data."""
    try:
        data = request.get_json()

        sex = data.get("sex")
        age_months = int(data.get("age_months", 0))
        weight_kg = float(data.get("weight_kg", 0))
        length_cm = float(data.get("length_cm", 0))

        if sex not in ["male", "female"]:
            return jsonify({"error": "Please select sex"}), 400

        if age_months < 0 or age_months > 24:
            return jsonify({"error": "Age must be between 0 and 24 months"}), 400

        if weight_kg <= 0:
            return jsonify({"error": "Please enter a valid weight"}), 400

        if length_cm <= 0:
            return jsonify({"error": "Please enter a valid length"}), 400

        result = calculate_both(sex, age_months, weight_kg, length_cm)
        return jsonify(result)

    except (ValueError, TypeError) as e:
        return jsonify({"error": "Please check your inputs"}), 400


@app.route("/health")
def health():
    """Health check endpoint for deployment."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
