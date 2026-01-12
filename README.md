# Sycamore

A simple baby growth percentile calculator using WHO Child Growth Standards (0-24 months).

## Features

- Calculate weight-for-age and length-for-age percentiles
- Based on official WHO Growth Standards data
- Save measurements locally (browser localStorage)
- Compare growth between measurements
- Clean, mobile-friendly interface

## Local Development

```bash
cd sycamore
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Deploy to Render.com

1. Push this repo to GitHub
2. Create a new Web Service on Render.com
3. Connect your GitHub repo
4. Set the root directory to `sycamore`
5. Render will auto-detect the `render.yaml` configuration

Or manually configure:
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## Data Sources

WHO Child Growth Standards LMS parameters from:
- [CDC/WHO Growth Charts Data Files](https://www.cdc.gov/growthcharts/who-data-files.htm)
- [WHO Child Growth Standards](https://www.who.int/tools/child-growth-standards)

## Disclaimer

This calculator is for informational purposes only. Always consult your pediatrician for medical advice about your baby's growth.
