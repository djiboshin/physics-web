from aiohttp import web
import pathlib
from .routes import routes
import aiohttp_jinja2
import jinja2
import logging
import sys

PATH = pathlib.Path(__file__).parent

handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[handler])

app = web.Application()
app.add_routes(routes)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(PATH.joinpath('templates')))
