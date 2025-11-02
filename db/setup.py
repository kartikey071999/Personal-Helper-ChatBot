import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import event

DB_FILE = "tasks.db"
# The 'engine' is the main connection point to our database
engine = create_engine(f"sqlite:///{DB_FILE}")

# This is the base class our models will inherit from
Base = declarative_base()

# This is the "association table" for the many-to-many relationship.
# We define it using the SQLAlchemy Table object, not a model class.
task_user_relationship_table = Table(
    "task_user_relationship",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("task_id", Integer, ForeignKey("task.id"), primary_key=True),
)

# --- Model Definitions ---

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    
    # This 'tasks' attribute creates the many-to-many relationship.
    # SQLAlchemy will automatically handle the 'task_user_relationship' table.
    tasks = relationship(
        "Task",
        secondary=task_user_relationship_table,
        back_populates="users"
    )

class Task(Base):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default="todo")
    
    # This 'users' attribute is the other side of the relationship.
    users = relationship(
        "User",
        secondary=task_user_relationship_table,
        back_populates="tasks"
    )


# --- Function to create tables ---

def create_tables():
    """Creates all tables in the database based on the Base metadata."""
    print("Creating database tables...")
    # This one command creates all tables that inherit from Base
    Base.metadata.create_all(bind=engine)
    print(f"Database '{DB_FILE}' and tables created successfully.")

# --- Enable Foreign Key Support for SQLite ---
# This is important! SQLite doesn't enforce foreign keys by default.
# This code ensures that every time a connection is made, PRAGMA foreign_keys=ON is set.
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


if __name__ == "__main__":
    # If you run this file directly, it will create the tables.
    create_tables()