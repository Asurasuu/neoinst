from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Параметры подключения к базе данных PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://pan_user:pan_password@172.17.0.2:5432/pan_db"

# Создание движка базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()