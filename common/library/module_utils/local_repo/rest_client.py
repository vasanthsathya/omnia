import json
import http.client
import ssl
import base64
from urllib.parse import urlparse


class RestClient:
    """
    REST client to interact with HTTP(S) endpoints using JSON-based POST and GET requests.
    SSL verification is disabled for all requests.

    Args:
        base_url (str): The base URL of the server (e.g., https://localhost:443).
        username (str): Username for basic authentication.
        password (str): Password for basic authentication.
    """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        auth = f"{username}:{password}"
        auth_encoded = base64.b64encode(auth.encode()).decode()
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Basic {auth_encoded}"
        }

    def get_connection(self):
        """
        Creates an HTTPS connection to the server with SSL verification disabled.

        Returns:
            http.client.HTTPSConnection: An HTTPS connection instance.
        """
        parsed_url = urlparse(self.base_url)
        context = ssl._create_unverified_context()
        return http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port, context=context, timeout=60)

    def post(self, uri, data):
        """
        Sends a POST request with a JSON body to the specified URI.

        Args:
            uri (str): The endpoint URI.
            data (dict): Data to send as JSON.

        Returns:
            dict or None: Parsed JSON response if successful, None otherwise.
        """
        conn = self.get_connection()
        try:
            conn.request("POST", uri, body=json.dumps(data), headers=self.headers)
            response = conn.getresponse()
            if response.status != 202:
                return None
            return json.loads(response.read())
        except Exception as e:
            return None
        finally:
            conn.close()

    def get(self, uri):
        """
        Sends a GET request and parses the response as JSON.

        Args:
            uri (str): The endpoint URI.

        Returns:
            dict or None: Parsed JSON response if status is 200, None otherwise.
        """
        conn = self.get_connection()
        try:
            conn.request("GET", uri, headers=self.headers)
            response = conn.getresponse()
            if response.status != 200:
                return None
            return json.loads(response.read())
        except Exception as e:
            return None
        finally:
            conn.close()

    def raw_get(self, uri):
        """
        Sends a GET request and returns the raw HTTP response.

        Args:
            uri (str): The endpoint URI.

        Returns:
            http.client.HTTPResponse or None: Response object if request succeeds, None otherwise.
        """
        conn = self.get_connection()
        try:
            conn.request("GET", uri, headers=self.headers)
            return conn.getresponse()
        except Exception as e:
            return None
