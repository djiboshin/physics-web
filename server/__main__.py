from aiohttp import web
from server import app

if __name__ == '__main__':
    web.run_app(app, port=9565)
