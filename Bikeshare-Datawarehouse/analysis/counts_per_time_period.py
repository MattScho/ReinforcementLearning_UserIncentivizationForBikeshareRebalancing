'''
Compute counts for trips occurring within various temporal conditions

:author: Matthew Schofield
'''

from bikeshare_db.trip import Trip
import datetime
from datetime import date

print("Beginning Counts per Time Period")

def count_yearly():
    '''
    Count yearly trips

    :return: outputs list of years and counts per year
    '''
    print("Yearly:")
    # Set-up
    years = list(range(2011, 2020))
    yearly_counts = [0 for _ in years]

    # Count
    for i, year in enumerate(years):
        print("\tProcessing: Year ", year)
        year_count = Trip.count_in_time_range(datetime.date(year, 1, 1), datetime.date(year, 12, 31))
        yearly_counts[i] += year_count

    return years, yearly_counts

def count_monthly():
    '''
    Count monthly trips

    :return: outputs list of months and counts per month
    '''
    print("Monthly:")
    # Set-up
    years = list(range(2011, 2020))
    months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
    month_years = []
    monthly_counts = []

    # Count
    for year in years:
        print("\tProcessing Months in Year ", year)
        for i, month in enumerate(months):
            # Days in month
            if i < 11:
                days = (date(year, i+2, 1) - date(year, i+1, 1)).days
            else:
                days = 31
            # Get trips in month
            month_count = Trip.count_in_time_range(datetime.date(year, i+1, 1), datetime.date(year, i+1, days))
            monthly_counts.append(month_count)
            month_years.append(str(year) + " " + month)

    return month_years, monthly_counts

def average_monthly():
    '''
    Computes average number of trips per month

    :return: outputs months and average number of trips per month
    '''
    print("Monthly:")
    # Set-up
    years = list(range(2015, 2020))
    months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
    monthly_counts = [0 for _ in months]

    # Count
    for year in years:
        print("\tProcessing Months in Year ", year)
        for i, month in enumerate(months):
            # Days in month
            if i < 11:
                days = (date(year, i+2, 1) - date(year, i+1, 1)).days
            else:
                days = 31
            # Get trips in month
            month_count = Trip.count_in_time_range(datetime.date(year, i+1, 1), datetime.date(year, i+1, days))
            monthly_counts[i] += month_count

    # Average
    monthly_counts = [elem/len(years) for elem in monthly_counts]
    return months, monthly_counts

def average_per_weekday():
    '''
    Relative number of trips per weekday

    :return: weekdays and relative number of trips per weekday
    '''
    print("Per Week Day:")
    # Set-up
    years = list(range(2015, 2020))
    weekdays = ["Sat.", "Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sun."]
    weekday_counts = []
    weekday_year_names = []

    # Count
    for year in years:
        print("\tProcessing Weekdays in Year ", year)
        # Get trips per weekday
        for i, weekday in enumerate(weekdays):
            print("\tWeekday ", i)
            weekday_count = Trip.count_weekday(datetime.date(year, 1, 1), datetime.date(year, 12, 31), i)
            print("\t\tCount: ", weekday_count)
            weekday_year_names.append(str(year) + " " + weekday)
            weekday_counts.append(weekday_count)

    return weekday_year_names, weekday_counts

def average_per_hour():
    '''
    Relative number of trips per hour

    :return: hours and relative number of trips per hour
    '''
    print("Per Hour:")
    # Set-up
    years = list(range(2015, 2020))
    hours = range(24)
    hour_counts = [0 for h in hours]
    # 52 days per year, 4 years, every day has an extra day every few years this will not be perfectly accurate but adding 53 helps
    hours_number = 52*4 + 53

    # Count
    for year in years:
        print("\tProcessing Hours in Year ", year)
        # Get trips per weekday
        for hour in hours:
            print("\tHour ", hour)
            hour_count = Trip.count_hour(datetime.date(year, 1, 1), datetime.date(year, 12, 31), hour)
            print("\t\tCount: ", hour_count)
            hour_counts[hour] += hour_count
    hour_counts = [h/hours_number for h in hour_counts]
    return hours, hour_counts

# Example usage
years, year_counts = count_yearly()
print(years)
print(year_counts)