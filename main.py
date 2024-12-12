from models import *
from database import *
from db_init import db_init

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db_init()
