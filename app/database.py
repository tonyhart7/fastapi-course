from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(dbname='fastapi', user='postgres', password='superucer123', host='localhost', cursor_factory=RealDictCursor) 
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error :
#         print("Connection was failed")
#         print("Error: ", error)
#         time.sleep(3)