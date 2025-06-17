from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import StaticPool
from datetime import datetime
import os

# Database URL - use SQLite for local development
DATABASE_URL = "sqlite:///./tasks.db"

# Create SQLAlchemy engine with optimized settings
engine = create_engine(
    DATABASE_URL, 
    connect_args={
        "check_same_thread": False,  # Needed for SQLite
        "timeout": 30,  # 30 second timeout
    },
    poolclass=StaticPool,  # Better for SQLite
    pool_pre_ping=True,  # Verify connections before use
    echo=False  # Set to True for debugging SQL queries
)

# Create SessionLocal class with better settings
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine,
    expire_on_commit=False  # Prevent lazy loading issues
)

# Create Base class
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with tasks
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship with user
    user = relationship("User", back_populates="tasks")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency with better error handling
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close() 