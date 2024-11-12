from datetime import datetime
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Event:
    title: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    price: str | None
    location: str | None
    description: str | None
    picture: str | None


def check_day(day: str):
    assert isinstance(day, str), "day must be a string"
    assert len(day) == 8, "day must be in the format 'YYYYMMDD'"
    assert day.isdigit(), "day must contain only digits"
    year = int(day[:4])
    month = int(day[4:6])
    day = int(day[6:8])
    assert 2000 <= year <= 2099, "year must be between 2000 and 2099"
    assert 1 <= month <= 12, "month must be between 1 and 12"
    assert 1 <= day <= 31, "day must be between 1 and 31"


def convert_to_postgres_time(time_range: str) -> str:
    # Define the input time format and the PostgreSQL format
    time_format = "%I:%M %p"  # 12-hour format with AM/PM

    # Split the input string by the '–' (en dash)
    start_time_str, end_time_str = time_range.split('–')

    # Strip any leading/trailing whitespace
    start_time_str = start_time_str.strip()
    end_time_str = end_time_str.strip()

    # Convert the times to 24-hour format using strptime
    start_time = datetime.strptime(start_time_str, time_format).time()
    end_time = datetime.strptime(end_time_str, time_format).time()

    # Return the start and end times in PostgreSQL-compatible time format
    return start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S')


def convert_to_postgres_date(date_str):
    # Define the date format for both single dates and ranges
    date_format = "%b %d, %Y"  # Abbreviated month name, day, and year (e.g., "Sep 03, 2024")

    # Check if the input string contains a date range (indicated by an en dash '–')
    if '–' in date_str:
        # Split the range into start and end dates
        start_date_str, end_date_str = date_str.split('–')

        # Strip whitespace
        start_date_str = start_date_str.strip()
        end_date_str = end_date_str.strip()

        # Ensure that the start date has the year (add the year from the end date if missing)
        # Check if the start date string has the year, and add the year from the end date if not
        if len(start_date_str.split(',')) == 1:  # No year found
            start_date_str = f"{start_date_str}, {end_date_str.split(', ')[1]}"

        # Parse both dates using strptime
        start_date = datetime.strptime(start_date_str, date_format).date()
        end_date = datetime.strptime(end_date_str, date_format).date()

        # Return both start and end dates in PostgreSQL format (YYYY-MM-DD)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    else:
        # Handle a single date
        date_str = date_str.strip()
        date_obj = datetime.strptime(date_str, date_format).date()

        # Return the date in PostgreSQL format
        result = date_obj.strftime('%Y-%m-%d')
        return result, result


def get_data(day: str):
    check_day(day)

    url = 'https://calvin.edu/events/day/' + day
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "Referer": "https://calvin.edu",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception('Failed to request data')

    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', class_='views-row')
    return data


def extract_event(event):
    date = event.find('div', class_='event-calendar__date').text.strip()
    start_date, end_date = convert_to_postgres_date(date)
    title = event.find('h4', class_='event-calendar__title').text.strip()
    time = event.find(
        'div', class_='event-calendar__date-location__date').text.strip()
    start_time, end_time = convert_to_postgres_time(time)
    location = event.find(
        'div', class_='event-calendar__date-location__location')
    if location is not None:
        location = location.text.strip()
    description = event.find('div', class_='event-calendar__summary')
    if description is not None:
        description = description.text.strip()
    price = event.find(
        'div', class_='field--name-field-price')
    if price is not None:
        price = price.text.strip()
    picture = event.find('img')
    if picture is not None:
        picture = picture['src']
    return Event(title, start_date, end_date, start_time, end_time, price, location, description, picture)


def get_events(day: str):
    '''
    Call this function to get a list of events for a specific day.
    The day must be in the format 'YYYYMMDD'.
    Exceptions will be raised if anything goes wrong, so make sure to catch them.
    '''
    data = get_data(day)
    return [extract_event(event) for event in data]


def main():
    # Example usage
    day = input('day: ')
    events = get_events(day)
    for event in events:
        print(event)


if __name__ == '__main__':
    main()
