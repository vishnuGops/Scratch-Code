from datetime import datetime


def count_days_from_date(date_string):
    try:
        provided_date = datetime.strptime(date_string, '%Y-%m-%d')
        today = datetime.now()
        days_difference = (today - provided_date).days
        return days_difference
    except ValueError:
        return "Invalid date format. Please provide the date in the format 'YYYY-MM-DD'."


# Replace 'YYYY-MM-DD' with the desired date in the format 'YYYY-MM-DD'
year = input("Enter the year : ")
month = input("Enter the month : ")
day = input("Enter the date : ")
provided_date_string = year+"-"+month+"-"+day
days_difference = count_days_from_date(provided_date_string)

if isinstance(days_difference, int):
    print(
        f"Number of days from {provided_date_string} to today's date: {days_difference} days")
else:
    print(days_difference)
