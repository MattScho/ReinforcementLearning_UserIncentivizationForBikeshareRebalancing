from sqlalchemy import create_engine
from sqlalchemy import orm
from bikeshare_db import BASE

class Bikeshare_Database:
    '''
    Creates Bikeshare Database

    :author: Matthew Schofield
    :version: 2.13.2021
    '''

    def __init__(self):
        '''
        Open initial connection
        '''
        # Set-up database connection
        # Settings
        self.user = "bikeshare_db"
        self.password = "knAkWLfien9"
        self.host = "localhost"
        self.db = "bikeshare_db"

        # Create engine/session
        self.engine = create_engine("mysql+pymysql://"+self.user+":"+self.password+"@"+self.host+"/"+self.db, echo=True)
        self.session = orm.scoped_session(orm.sessionmaker())(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        '''
        Create database initial tables
        '''
        from bikeshare_db.trip import Trip
        BASE.metadata.bind = self.engine
        BASE.metadata.create_all()
        self.session.commit()

