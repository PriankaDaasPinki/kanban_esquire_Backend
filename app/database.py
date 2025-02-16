from sqlalchemy import create_engine, event
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/kanban_esquire"
# SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
# ALGORITHM = "HS256"
# TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(DATABASE_URL)


# engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Check database connection
try:
    # Establish a test connection
    with engine.connect() as connection:
        print("============================================= Database connected Successfully! =============================================")
except OperationalError as e:
    print(f"Database connection failed: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        pass
