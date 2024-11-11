import random
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import UTC, datetime, timedelta

import requests

BASE_URL = "http://localhost:8001"

user_id_pool: list[str] = []
team_id_pool: list[str] = []


def _teams_create(token: str):
    response = requests.post(
        BASE_URL + "/teams",
        json={"title": f"team_{random.randint(1, 1_000_000)}"},
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        print(response.text, BASE_URL + "/teams")
        return

    response_body = response.json()
    team_id_pool.append(response_body["id"])


def _get_teams_by_id(token: str):
    team_id = random.choice(team_id_pool)
    response = requests.get(
        BASE_URL + f"/teams/{team_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        print(response.text, BASE_URL + "/teams")
        return


def _users_register(token: str):
    response = requests.post(
        BASE_URL + "/users/register",
        json={
            "username": f"user_{random.randint(1, 1_000_000)}",
            "firstName": "",
            "secondName": "",
            "password": "totallyValidPassword_123",
        },
    )

    if response.status_code != 200:
        print(response.text, BASE_URL + "/users/register")
        return

    response_body = response.json()
    user_id_pool.append(response_body["id"])


def _get_users_me(token: str):
    response = requests.get(
        BASE_URL + "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        print(response.text, BASE_URL + "/users/me")
        return


def _get_users_by_id(token: str):
    user_id = random.choice(user_id_pool)
    response = requests.get(
        BASE_URL + f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        print(response.text, BASE_URL + f"/users/{user_id}")
        return


def _authorize_new_user() -> str:
    username = f"client_{random.randint(1, 1_000_000)}"
    password = "totallyValidPassword_123"

    response = requests.post(
        BASE_URL + "/users/register",
        json={
            "username": username,
            "firstName": "",
            "secondName": "",
            "password": password,
        },
    )

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    response = requests.post(
        BASE_URL + "/users/auth",
        data={"grant_type": "password", "username": username, "password": password},
    )

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response.json()["access_token"]


actions = {
    "post_teams": _teams_create,
    "get_teams_by_id": _get_teams_by_id,
    "post_users_register": _users_register,
    "get_users_me": _get_users_me,
    "get_users_by_id": _get_users_by_id,
}


def act(duration_minutes: int = 10):
    token = _authorize_new_user()

    print(f"Starting with token: {token}")

    duration = timedelta(minutes=duration_minutes)
    started = datetime.now(tz=UTC)

    while True:
        action = random.choice(list(actions.keys()))
        action_func = actions[action]

        action_func(token)

        if datetime.now(tz=UTC) - started > duration:
            print("Stopping")
            break


CLIENT_COUNT = 50


def run():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(act, 20) for _ in range(CLIENT_COUNT)]
        wait(futures)


if __name__ == "__main__":
    run()
