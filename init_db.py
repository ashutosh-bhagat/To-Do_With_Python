from database import engine
from models import Task

Task.metadata.create_all(bind=engine)
