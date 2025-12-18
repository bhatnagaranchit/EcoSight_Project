from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EnergyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    
    # Energy Sources
    solar_gw = db.Column(db.Float, nullable=False)
    wind_gw = db.Column(db.Float, nullable=False)
    coal_gw = db.Column(db.Float, nullable=False)
    
    # Business Metrics
    co2_mt = db.Column(db.Float, nullable=False)
    gdp_growth = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'year': self.year,
            'country': self.country,
            'solar': self.solar_gw,
            'wind': self.wind_gw,
            'coal': self.coal_gw,
            'co2': self.co2_mt,
            'gdp': self.gdp_growth
        }