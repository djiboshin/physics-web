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
    week_forward = data.get('week_forward')
    if not isinstance(week_forward, int) and week_forward is not None:
        return web.Response(status=400)
    extra_seminar = data.get('extra_seminar')
    friday_seminar = Seminar(**extra_seminar) if isinstance(extra_seminar, dict) else Seminar()

    html = render_html(seminars=get_seminars(week_forward), friday_seminar=friday_seminar)
    if file_type == 'png':
        res = html_to_png(html)
        return web.Response(body=res, content_type="image/png")
    elif file_type == 'pdf':
        res = html_to_pdf(html)
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


@routes.get('/')
async def main(request: web.Request) -> web.Response:
    context = {'static_url': 'app'}
    return aiohttp_jinja2.render_template('svelte_app.html', request, context=context)
