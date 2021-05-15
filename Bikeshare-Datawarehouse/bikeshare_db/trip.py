import sqlalchemy as sa
from sqlalchemy import func
from bikeshare_db import BASE, session

class Trip(BASE):
    '''
    Table to describe bikeshare Trips
    '''
    __tablename__ = 'trips_15_19'


    # Definition of columns
    trip_id = sa.Column(sa.Integer, primary_key=True)
    duration = sa.Column(sa.Integer, nullable=False)
    start_date = sa.Column(sa.Date, nullable=False)
    end_date = sa.Column(sa.Date, nullable=False)
    start_station_number = sa.Column(sa.String(10), nullable=False)
    end_station_number = sa.Column(sa.String(10), nullable=False)
    bike_number = sa.Column(sa.String(10), nullable=False)
    member_type = sa.Column(sa.String(10), nullable=False)
    start_day_epoch = sa.Column(sa.Integer, nullable=False)
    end_day_epoch = sa.Column(sa.Integer, nullable=False)
    start_station_lat = sa.Column(sa.Numeric(6,2), nullable=False)
    start_station_lon = sa.Column(sa.Numeric(6,2), nullable=False)
    end_station_lat = sa.Column(sa.Numeric(6,2), nullable=False)
    end_station_lon = sa.Column(sa.Numeric(6,2), nullable=False)
    start_r_x = sa.Column(sa.Integer, nullable=False)
    start_r_y = sa.Column(sa.Integer, nullable=False)
    end_r_x = sa.Column(sa.Integer, nullable=False)
    end_r_y = sa.Column(sa.Integer, nullable=False)

    @classmethod
    def get_in_time_range(cls, start_date_range, end_date_range):
        '''
        Count number of entries in time range

        :param start_date: start date of range
        :param end_date: end date of range
        :return: number of trips in range
        '''
        return session.query(Trip).filter(Trip.start_date.between(start_date_range, end_date_range))

    @classmethod
    def count_in_time_range(cls, start_date_range, end_date_range):
        '''
        Count number of entries in time range

        :param start_date: start date of range
        :param end_date: end date of range
        :return: number of trips in range
        '''
        return cls.get_in_time_range(start_date_range, end_date_range).count()

    @classmethod
    def count_weekday(cls, start_date_range, end_date_range, weekday):
        return cls.get_in_time_range(start_date_range, end_date_range).filter(func.date_format(Trip.start_date, '%w') == str(weekday)).count()

    @classmethod
    def count_hour(cls, start_date_range, end_date_range, hour):
        return cls.get_in_time_range(start_date_range, end_date_range).filter(
            Trip.start_day_epoch.between(3600*hour, 3600*(hour+1))).count()

    @classmethod
    def bin_duration(cls, start_date_range, end_date_range, dur, step):
        return cls.get_in_time_range(start_date_range, end_date_range).filter(Trip.duration.between(dur, dur+step)).count()

    @classmethod
    def create_trip(cls, duration, start_date, end_date, start_station_number, end_station_number, bike_number,
                    member_type,start_day_epoch, end_day_epoch, start_station_lat, start_station_lon,
                        end_station_lat, end_station_lon, start_r_x, start_r_y, end_r_x, end_r_y):
        '''
        Create a File
        '''
        trip = Trip(duration=duration, start_date=start_date, end_date=end_date,
                    start_station_number=start_station_number, end_station_number=end_station_number,
                    bike_number=bike_number, member_type=member_type, start_day_epoch=start_day_epoch, end_day_epoch=end_day_epoch,
                    start_station_lat=start_station_lat, start_station_lon=start_station_lon,
                    end_station_lat=end_station_lat, end_station_lon=end_station_lon, start_r_x=start_r_x,
                    start_r_y=start_r_y, end_r_x=end_r_x, end_r_y=end_r_y
                    )

        session.add(trip)
