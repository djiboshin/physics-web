import bs4
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import base64
import datetime as dt
import pdfkit
import imgkit
import pathlib
from urllib.parse import urljoin
from jinja2 import Environment, FileSystemLoader, select_autoescape

HOST = 'https://physics.itmo.ru'

color_table = {
    "Microwave seminar": "#e9ad56",
    "Optical seminar": "#2e5399",
    "Theoretical seminar": "#e7874b",
    "General seminar": "#008b6c",
    "Evening seminar": "#022950"
}
text_color_table = {
    "Optical seminar": "white",
    "General seminar": "white",
    "Evening seminar": "white"
}

PATH_TEMPLATES = pathlib.Path(__file__).parent.joinpath('templates')

env = Environment(
    loader=FileSystemLoader(PATH_TEMPLATES),
    autoescape=True
)


@dataclass
class Seminar:
    name: str = None
    university: str = None
    speaker_name: str = None
    type: str = None
    datetime: dt.datetime = None
    photo_src: str = None
    date_color: str = "#e9ad56"
    background_color: str = "white"
    text_color: str = "black"


def text_or_none(tag: bs4.Tag or None):
    if isinstance(tag, bs4.Tag):
        return tag.text.strip()
    return None


def img_to_base64(url: str):
    r = requests.get(url)
    return f"data:{r.headers['Content-Type']};base64,{base64.b64encode(r.content).decode('utf-8')}"


def get_seminars(week_forward: int or None = 0):
    S = requests.Session()
    r = S.get(urljoin(HOST, '/en/seminars'))
    soup = BeautifulSoup(r.text, features="html.parser")
    sem_divs = soup.find_all('div', class_='views-row')
    seminars = []
    for div in sem_divs:
        seminar = Seminar()
        seminar.name = text_or_none(div.find('div', class_='speaker-talk-name'))
        seminar.university = text_or_none(div.find('div', class_='speaker-affilation'))
        seminar.speaker_name = text_or_none(div.find('div', class_='external-speaker-wrapper'))
        seminar.type = text_or_none(div.find('div', class_='seminar-type-value'))

        if seminar.type in color_table.keys():
            seminar.date_color = color_table[seminar.type]
        if seminar.type in text_color_table.keys():
            seminar.text_color = text_color_table[seminar.type]

        date = text_or_none(div.find('div', class_='dte'))
        time = text_or_none(div.find('div', class_='tme'))
        if date is not None and time is not None:
            seminar.datetime = dt.datetime.strptime(f'{date} {time}', '%d %B %Y %H:%M')

        img = div.find('img', class_='img-responsive')
        seminar.photo_src = img_to_base64(urljoin(HOST, img.get('src'))) if img is not None else None

        delta_weeks = int(seminar.datetime.strftime('%W')) - int(dt.datetime.now().strftime('%W'))
        if delta_weeks == week_forward or week_forward is None:
            seminars.append(seminar)
    return sorted(seminars, key=lambda x: x.datetime)


def render_html(seminars: list, friday_seminar: Seminar):
    template = env.get_template('table.html')
    return template.render(seminars=seminars, friday_seminar=friday_seminar)


def html_to_png(html: str):
    options = {
        'format': 'png',
        'encoding': "UTF-8",
        # 'quiet': None,
        # 'no-outline': " ",
        # 'disable-external-links': None,
        'disable-javascript': None,
        'disable-local-file-access': None,
        'width': 650,
        # 'no-background': None
            }
    return imgkit.from_string(html, output_path=False, options=options)


def html_to_pdf(html: str) -> bytes:
    options = {
        'encoding': "UTF-8",
        'quiet': None,
        'no-outline': None,
        'disable-external-links': None,
        'disable-javascript': None,
        'disable-local-file-access': None,
               }
    return pdfkit.from_string(html, output_path=False, options=options)
