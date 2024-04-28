from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pytrends.request import TrendReq
import pandas as pd 
from urllib.parse import quote_plus
from models import Trend, Base


# Database connection setup
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%s@localhost:5432/postgres' % quote_plus("!Q@W#E$R1q2w3e4r")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create the database table
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_google_trends(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword], geo='US', timeframe='today 12-m')
    df = pytrend.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    return df

def store_in_database(keyword, df, db):
    sorted_df = df.sort_values(by=keyword, ascending=False).head(5)
    top_regions = {state: int(value) for state, value in sorted_df.iterrows()}

    # Create a new trend entry
    trend_entry = Trend(
        keyword=keyword,
        top1=str(list(top_regions.items())[0]),
        top2=str(list(top_regions.items())[1]),
        top3=str(list(top_regions.items())[2]),
        top4=str(list(top_regions.items())[3]),
        top5=str(list(top_regions.items())[4])
    )
    
    db.add(trend_entry)
    db.commit()

# Main execution
def makeTable(keyword):
    db = next(get_db())  # Get a database session
    df = fetch_google_trends(keyword)
    store_in_database(keyword, df, db)