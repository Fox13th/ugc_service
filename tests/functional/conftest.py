import asyncio

import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='cl_session', scope='session')
async def cl_session():
    cl_session = aiohttp.ClientSession()
    yield cl_session
    await cl_session.close()


@pytest_asyncio.fixture(name='make_request')
def make_request(cl_session):
    async def inner(method, api_url, payload=None, headers=None):
        async with cl_session.request(
                method=method,
                url=api_url,
                headers=headers,
                json=payload
        ) as response:
            status = response.status
            body = await response.json()
            return {'status': status, 'body': body}

    return inner
