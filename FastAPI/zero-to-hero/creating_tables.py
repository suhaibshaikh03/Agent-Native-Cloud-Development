from sqlmodel import SQLModel, create_engine

# place this code after definining all table in the file
# 1 time run this code to create all tables
def create_tables():
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully")

create_tables()
