
import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    route = os.environ.get("AUTH_SERVICE_ADDRESS")
    response = requests.post(
        f"http://{route}/login",
        auth=basicAuth,
    )

    if response.status_code == 200:
        return response.text, None

    return None, (response.text, response.status_code)



