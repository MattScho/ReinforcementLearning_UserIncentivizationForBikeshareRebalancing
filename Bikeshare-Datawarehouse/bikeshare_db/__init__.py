from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

# Create declarative_base for model creation
BASE = declarative_base()

user = "bikeshare_db"
password = "knAkWLfien9"
host = "localhost"
db = "bikeshare_db"

# Create engine/session
engine = create_engine("mysql+pymysql://"+user+":"+password+"@"+host+"/"+db)
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

from bikeshare_db.trip import Trip

BASE.metadata.bind = engine
BASE.metadata.create_all()
session.commit()
