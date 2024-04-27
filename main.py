# main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from trend_fetcher import fetch_google_trends, store_in_database
from urllib.parse import quote_plus

# Database connection setup
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%s@localhost/postgres' % quote_plus("!Q@W#E$R1q2w3e4r")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database table
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    keyword = input("Enter the keyword to search on Google Trends: ")
    db = next(get_db())  # Get a database session
    df = fetch_google_trends(keyword)
    store_in_database(keyword, df, db)
    print(f"Data for '{keyword}' has been stored successfully.")