from datetime import datetime, timedelta
from dataclasses import dataclass
import os

import pytz
import requests
from bs4 import BeautifulSoup
import psycopg

DBHOST = os.environ['DBHOST']
DBPORT = os.environ['DBPORT']
DBNAME = os.environ['DBNAME']
DBUSER = os.environ['DBUSER']
DBPSWD = os.environ['DBPSWD']

@dataclass
class Event:
    name: str
    start_date: datetime
    end_date: datetime
    price: str
    location: str
    description: str
    cover_uri: str


def check_day(day: str):
    assert isinstance(day, str), "day must be a string"
    assert len(day) == 8, "day must be in the format 'YYYYMMDD'"
    assert day.isdigit(), "day must contain only digits"
    year = int(day[:4])
    month = int(day[4:6])
    day_num = int(day[6:8])
    assert 2000 <= year <= 2099, "year must be between 2000 and 2099"
    assert 1 <= month <= 12, "month must be between 1 and 12"
    assert 1 <= day_num <= 31, "day must be between 1 and 31"


def to_timestamp(date: str, time: str) -> tuple[datetime, datetime]:
    time_format = '%I:%M %p'
    start, end = time.split('–')
    start.strip()
    end.strip()

    date_format = '%Y%m%d'

    est = pytz.timezone('America/New_York')

    start = datetime.strptime(date + ' ' + start, date_format + ' ' + time_format).astimezone(est)
    end = datetime.strptime(date + ' ' + end, date_format + ' ' + time_format).astimezone(est)

    return start, end


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


def extract_event(date: str, event: BeautifulSoup) -> Event:
    name = event.find('h4', class_='event-calendar__title').text.strip()
    time = event.find(
        'div', class_='event-calendar__date-location__date').text.strip()
    start, end = to_timestamp(date, time)
    location = event.find(
        'div', class_='field--name-field-on-campus-location')
    if location is not None:
        location = location.text.strip()
    else:
        location = ''
    description = event.find('div', class_='event-calendar__summary')
    if description is not None:
        description = description.text.strip()
        if len(description) > 255:
            description = description[:255]
    else:
        description = ''
    price = event.find(
        'div', class_='field--name-field-price')
    if price is not None:
        price = price.text.strip()
    else:
        price = ''
    picture = event.find('img')
    if picture is not None:
        picture: str = 'https://calvin.edu' + picture['src']
    else:
        picture = ''
    return Event(name, start, end, price, location, description, picture)


def get_events(day: str):
    """
    Call this function to get a list of events for a specific day.
    The day must be in the format 'YYYYMMDD'.
    Exceptions will be raised if anything goes wrong, so make sure to catch them.
    """
    data = get_data(day)
    return [extract_event(day, event) for event in data]


def generate_dates(start_date_str: str):
    # Parse the start date from the given string
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    
    # Generate dates day by day
    current_date = start_date
    while True:
        # Print the current date in YYYYMMDD format
        yield current_date.strftime('%Y%m%d')
        
        # Move to the next day
        current_date += timedelta(days=1)

def tag_event(event: Event):
    print('Event:', event.name)
    print('Location:', event.location)
    print('Description:', event.description)
    tag_options: list[str] = [
        '🎤 Music',
        '🏫 Education',
        '🏈 Sports',
        '🏘️ Residence Life',
        '⛪️ Chapel',
        '👫 Social Activities',
        '🎨 Arts & Culture',
        '🧬 Science & Tech',
        '🗓️ Other',
        '🩺 Health & Fitness',
        '💼 Career & Business',
        '🎮 Gaming',
        '🎬 Film & Media',
        '🍔 Food & Drink',
    ]
    for i, tag_option in enumerate(tag_options):
        print(f'\t{i}. {tag_option}')
    tags_str = input('Tags:')
    while True:
        tags: list[str] = []
        for tag in tags_str.split(','):
            tag = tag.strip()
            try:
                index = int(tag)
            except Exception as e:
                print(f'Error: {e}')
                continue
            if index < len(tag_options):
                tags.append(tag_options[index])
            else:
                print('Index out of range. Try again!')
                continue
        break
    return tags


def main():
    start_day = input('start_day: ')
    day_count = int(input('day_count: '))
    date_gen = generate_dates(start_day)
    conn_str = f'host={DBHOST} port={DBPORT} dbname={DBNAME} user={DBUSER} password={DBPSWD} connect_timeout=10 sslmode=require'
    print(f'Connection Params: {conn_str}')
    with psycopg.connect(conn_str) as conn:
        print('db connected')
        for _ in range(day_count):
            day = next(date_gen)
            print(f'Getting day {day}... ', end='')
            events = get_events(day)
            print(f'{len(events)} events... ')
            for event in events:
                tags = tag_event(event)
                with conn.cursor() as cur:
                    cur.execute(
                        'INSERT INTO event_event (id, name, date_created, start_date, end_date, price, location, description, cover_uri, tags, organizer_id) VALUES (gen_random_uuid(), %s, NOW(), %s, %s, %s, %s, %s, %s, %s, \'81dd6d6f-e5b4-4395-a2db-e06ee489b9f0\')',
                        (event.name, event.start_date, event.end_date, event.price, event.location, event.description, event.cover_uri, tags))
                    conn.commit()
            print('day competed')
        print('done')


if __name__ == '__main__':
    main()
