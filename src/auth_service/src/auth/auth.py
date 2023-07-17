import logging

from aiohttp import web, hdrs

from . import nginx
from .utils import GetAdditionalHeaders, OnAuthFail

routes = web.RouteTableDef()


async def auth(req: web.Request, *, get_headers: GetAdditionalHeaders, on_fail: OnAuthFail):
    headers = 'Headers: \n' + '\n'.join(f'{k}: {v}' for k, v in req.headers.items())
    logging.info(headers)

    storage = req.app.storage
    session_id = req.cookies.get('session_id')
    logging.info(f'Session id: {session_id}')
    session = storage.get_session(session_id)
    logging.info(f'Session: {session}')

    if not session:
        response = await on_fail(req, req.match_info.get('req_url'))
        return response

    additional = get_headers(req, session)
    logging.info(f'Additional headers: {additional}')

    headers = {
        **session,
        **additional
    }
    logging.info(f'Summary headers: {headers}')

    return web.Response(headers=headers)


@routes.route(hdrs.METH_ANY, '/auth/nginx{req_url:/?.*}')
async def nginx_auth(req: web.Request):
    response = await auth(req, get_headers=nginx.get_headers, on_fail=nginx.on_auth_fail)
    return response
