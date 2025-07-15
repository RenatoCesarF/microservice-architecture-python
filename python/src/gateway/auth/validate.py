from typing import Optional, Tuple

import os, requests


def token(request)-> Tuple[Optional[str], Optional[Tuple[str, int]]]:
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token:
        return None, ("missing credentials", 401)

    route = os.environ.get("AUTH_SERVICE_ADDRESS")
    response = requests.post(
        f"http://{route}/validate",
        headers={"Authorization": token},
    )

    if response.status_code != 200:
        return None, (response.text, response.status_code)

    return response.text, None


