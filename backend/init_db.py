"""Initialize the database tables for the Todo App backend."""
from sqlmodel import SQLModel
from database.session import engine
from models.user import User
from models.task import Task  # Import all models to register them


def create_tables():
    """Create all database tables."""
    print("Dropping existing database tables...")
    SQLModel.metadata.drop_all(bind=engine)
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()