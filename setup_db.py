from app import app
from models import db, EnergyRecord
import random

def init_database():
    with app.app_context():
        db.create_all()
        
        if not EnergyRecord.query.first():
            print("Generating Full Enterprise Dataset (Energy + GDP + CO2)...")
            
            countries = ["USA", "China", "Germany", "India", "Brazil"]
            years = range(2014, 2025)
            
            records = []
            for country in countries:
                solar = random.randint(50, 150)
                wind = random.randint(80, 200)
                coal = random.randint(300, 600)
                
                for year in years:
                    solar += random.randint(10, 30)
                    wind += random.randint(10, 25)
                    coal += random.randint(-20, 10)
                    co2 = (coal * 2.5) + random.randint(50, 100)
                    gdp = round(random.uniform(1.5, 5.5), 2)
                    
                    records.append(EnergyRecord(
                        year=year, country=country,
                        solar_gw=solar, wind_gw=wind, coal_gw=coal,
                        co2_mt=co2, gdp_growth=gdp
                    ))
            
            db.session.add_all(records)
            db.session.commit()
            print("Success! Database ready.")

if __name__ == '__main__':
    init_database()