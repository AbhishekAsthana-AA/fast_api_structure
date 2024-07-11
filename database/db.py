from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_setting

settings = get_setting()
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL) #echo=True
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection():
    try:
        # Create a new session
        with SessionLocal() as session:
            # Execute a simple query
            result = session.execute(text("SELECT 1")).fetchone()
            if result:
                print("Database connection successful!")
            else:
                print("Database connection failed.")
    except Exception as e:
        print(f"Database connection failed: {e}")
