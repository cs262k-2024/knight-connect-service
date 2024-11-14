from datetime import datetime
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Event:
    title: str
    timestamp: int
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


def date_to_timestamp(date: str) -> int:
    date_format = '%b %d, %Y'
    if '–' in date:
        year = date.split(',')[1].strip()
        day = date.split('–')[0].strip()
        date = day + ', ' + year
    return int(datetime.strptime(date, date_format).timestamp())


def time_to_timestamp(time: str) -> int:
    time_format = '%I:%M %p'
    time = time.split('–')[0].strip()
    time = datetime.strptime(time, time_format).time()
    return (time.hour + 4) * 3600 + time.minute * 60 + time.second # EST time + daylight saving is 4 hours ahead of UTC


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
    title = event.find('h4', class_='event-calendar__title').text.strip()
    time = event.find(
        'div', class_='event-calendar__date-location__date').text.strip()
    timestamp = date_to_timestamp(date) + time_to_timestamp(time)
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
        picture = 'https://calvin.edu' + picture['src']
    return Event(title, timestamp, price, location, description, picture)


def get_events(day: str):
    """
    Call this function to get a list of events for a specific day.
    The day must be in the format 'YYYYMMDD'.
    Exceptions will be raised if anything goes wrong, so make sure to catch them.
    """
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
