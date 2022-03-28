import datetime as dt
import logging
import pathlib
import aiohttp_jinja2
from aiohttp import web
from server.parser import get_seminars, Seminar, html_to_pdf, html_to_png, render_html
from json import JSONDecodeError
import json
import aiohttp
import base64


routes = web.RouteTableDef()

PATH_SVELTE = pathlib.Path(__file__).parent.parent.joinpath('svelte/public')
routes.static('/app', PATH_SVELTE)


def from_data(data: dict, request: web.Request) -> web.Response:
    file_type = data.get('type')
    seminars_ = data.get('seminars')
    seminars_to_render = []
    if seminars_ is not None:
        seminars_to_render = []
        for s in seminars_:
            if s.get('datetime') is not  None:
                s['datetime'] = dt.datetime.strptime(s['datetime'], '%Y-%m-%d %H:%M:%S')
            seminars_to_render.append(Seminar(**s))

    try:
        html = render_html(seminars=seminars_to_render)
    except Exception as e:
        logging.error(e)
        html = render_html(seminars=[])

    if file_type == 'png':
        try:
            res = html_to_png(html)
        except Exception as e:
            logging.error(e)
            res = b""
        return web.Response(body=res, content_type="image/png")
    elif file_type == 'pdf':
        try:
            res = html_to_pdf(html)
        except Exception as e:
            logging.error(e)
            res = b""
        return web.Response(body=res, content_type="application/pdf")
    return web.Response(body=html)


@routes.get('/ws/render_b64')
async def w(request: web.Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = json.loads(msg.data)
                res = from_data(data, request)
                await ws.send_str(f"data:{res.content_type};base64,{base64.b64encode(res.body).decode('utf-8')}")


@routes.get('/render')
async def render(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except JSONDecodeError:
        return web.Response(status=400)
    return from_data(data, request)


@routes.get('/seminars')
async def seminars(request: web.Request) -> web.Response:
    return web.json_response(get_seminars())


@routes.get('/')
async def main(request: web.Request) -> web.Response:
    context = {'static_url': 'app'}
    return aiohttp_jinja2.render_template('svelte_app.html', request, context=context)
