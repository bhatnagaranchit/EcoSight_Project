from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, EnergyRecord
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecosight.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Coordinates for Live Weather API
COUNTRY_COORDS = {
    "USA":      {"lat": 38.90, "lon": -77.03},
    "China":    {"lat": 39.90, "lon": 116.40},
    "Germany":  {"lat": 52.52, "lon": 13.41},
    "India":    {"lat": 28.61, "lon": 77.20},
    "Brazil":   {"lat": -15.82, "lon": -47.92}
}

def get_live_weather(country_name):
    coords = COUNTRY_COORDS.get(country_name, COUNTRY_COORDS["Germany"])
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=shortwave_radiation,wind_speed_10m&timezone=auto"
        res = requests.get(url).json()
        current = res.get('current', {})
        return {
            "solar_rad": current.get('shortwave_radiation', 0),
            "wind_speed": current.get('wind_speed_10m', 0),
            "status": "Online"
        }
    except:
        return {"solar_rad": 0, "wind_speed": 0, "status": "Offline"}

@app.route('/')
def dashboard():
    countries = db.session.query(EnergyRecord.country).distinct().all()
    countries = [c[0] for c in sorted(countries)]
    return render_template('dashboard.html', countries=countries)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        new_record = EnergyRecord(
            year=int(request.form['year']),
            country=request.form['country'],
            solar_gw=float(request.form['solar']),
            wind_gw=float(request.form['wind']),
            coal_gw=float(request.form['coal']),
            co2_mt=float(request.form['co2']),
            gdp_growth=float(request.form['gdp'])
        )
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('admin'))
    
    all_records = EnergyRecord.query.order_by(EnergyRecord.year.desc()).all()
    return render_template('admin.html', records=all_records)

@app.route('/api/data')
def api_data():
    country = request.args.get('country', 'USA')
    
    # 1. Historical Data (Database)
    records = EnergyRecord.query.filter_by(country=country).order_by(EnergyRecord.year).all()
    
    # 2. Live Data (API)
    live_data = get_live_weather(country)
    
    data = {
        "years": [r.year for r in records],
        "solar": [r.solar_gw for r in records],
        "wind": [r.wind_gw for r in records],
        "coal": [r.coal_gw for r in records],
        "co2": [r.co2_mt for r in records],  # Included
        "gdp": [r.gdp_growth for r in records], # Included
        "live": live_data
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)