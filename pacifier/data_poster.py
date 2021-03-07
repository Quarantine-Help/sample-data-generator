import http
import json

import requests


class DataPoster(object):
    auth_key = None
    target = None
    data = None

    TARGET_URLS = {
        "staging": "https://stage-api.quarantine-help.space",
        "production": "https://api.quarantine-help.space",
        "local": "http://127.0.0.1:8000",
    }

    def __init__(self, auth_key=None, target=None, data=None):
        self.auth_key = auth_key
        self.target = target
        self.data = data

    def post_to_target(self):
        """
        Does the actual POST to target
        :param fake_data:
        :return:
        """
        request_response = requests.post(
            url=f"{self.TARGET_URLS.get(self.target)}/api/v1/auth/bulk-register/",
            data=json.dumps({"participants": self.data}),
            headers={
                "Authorization": f"Token {self.auth_key}",
                "Content-Type": "application/json",
            },
        )
        if request_response.status_code == http.HTTPStatus.OK:
            return True

        return request_response.json()
