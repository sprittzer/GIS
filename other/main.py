from datetime import datetime, timedelta

def get_week_number(year, day_of_year):
    january_1 = datetime(year, 1, 1)
    first_thursday = january_1 + timedelta(days=(3 - january_1.weekday() + 7) % 7)
    target_date = january_1 + timedelta(days=day_of_year - 1)
    days_diff = (target_date - first_thursday).days
    week_number = (days_diff // 7) + 1
    return week_number
