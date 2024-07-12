from http import HTTPStatus
import pytest

from settings import get_settings

config = get_settings()


@pytest.mark.parametrize(
    'method, user_data, payload, expected_answer',
    [
        (
                'POST',
                {
                    'login': 'admin@admin.com',
                    'password': '123'
                },
                {
                    'event': 'some_event'
                },
                {
                    'status': HTTPStatus.BAD_REQUEST,
                }
        ),
        (
                'POST',
                {
                    'login': 'admin@admin.com',
                    'password': '123'
                },
                {
                    "event_data": {
                        "123": "asd"
                    }
                },
                {
                    'status': HTTPStatus.OK,
                }
        )
    ]
)
@pytest.mark.asyncio
async def test_ugc(
        make_request,
        method: str,
        user_data: dict,
        payload: dict,
        expected_answer: dict
):
    response_auth = await make_request(
        method=method,
        api_url=f'{config.auth_service_url}/api/v1/auth/login',
        payload=user_data
    )

    access_data = response_auth['body']

    response = await make_request(
        method=method,
        api_url=f'{config.service_url}/api/v1/statistics/send',
        payload=payload,
        headers={'Authorization': f'Bearer {access_data["access_token"]}'}
    )

    assert response['status'] == expected_answer['status']
