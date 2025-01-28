from modules.api_access_module.process_http_request import HTTPUtil
from helper import helper_fetch_token_from_response, helper_proxy_settings
from base64 import b64encode
from requests.models import PreparedRequest
import logging
from sets_log_uniformity.main import LogUniformity

loggers = LogUniformity()
loggers.override_config("FileHandler", level="Debug", file_name="config.log")
logger = logging.getLogger(__name__)

class ApiAuthPlugin:
    """
    Handles API authentication based on configurations in config.yaml.
    Supports both Basic Authentication and Token-based authentication.
    """
    def __init__(self, API, config_data, PROXY_USERNAME, PROXY_PASSWORD):
        api_config = config_data.get(API)
        
        self.auth_type = api_config['AUTHENTICATION']['AUTH_TYPE']
        self.base_url = api_config['APIS']['BASE_URL']
        self.endpoint = api_config['APIS']['API_ENDPOINT']
        self.token_auth_type = api_config['AUTHENTICATION']['TOKEN_AUTH_TYPE']
        self.input_params = api_config.get('Params')
        self.username = api_config['AUTHENTICATION']['USERNAME']
        self.password = api_config['AUTHENTICATION']['PASSWORD']
        self.PROXY_USERNAME = PROXY_USERNAME
        self.PROXY_PASSWORD = PROXY_PASSWORD
        self.http = HTTPUtil()

    def __call__(self):
        try:
            return self.functionToExecuteBasedOn_auth_type()
        except Exception as ex:
            logger.error(f"Exception error: {ex}")

    def functionToExecuteBasedOn_auth_type(self):
        """
        Executes authentication based on the specified auth type.
        """
        if str(self.auth_type) == "authentication_via_basic_auth":
            return self.apiAuthBasedOnCredentials()
        else:
            return self.apiAuthBasedOnToken()

    def basic_auth(self, username, password):
        """
        Generates a Basic auth token using base64 encoding.
        """
        try:
            token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
            return f"Basic {token}"
        except Exception as ex:
            logger.error(f"Exception occurred: {ex}")
            raise Exception(f"{ex}")

    def apiAuthBasedOnCredentials(self):
        """
        Authenticates using username and password credentials.
        """
        proxies = helper_proxy_settings.get_proxy(self.PROXY_USERNAME, self.PROXY_PASSWORD)
        req = PreparedRequest()
        req.prepare_url(f"{self.base_url}{self.endpoint}", self.input_params)

        headers = {"Authorization": self.basic_auth(self.username, self.password)}

        try:
            response = self.http.process_request(req.url, "GET", data=None, json=None, auth=None,
                                                 api_header=headers, proxies=proxies, verify_ssl=False)
            return response
        except Exception as ex:
            logger.error(f"Exception occurred while generating session token: {ex}")
            raise Exception(f"{ex}")

    def apiAuthBasedOnToken(self):
        """
        Authenticates using token-based methods.
        """
        if self.token_auth_type == "basicauth":
            return self.basicAuthorizationViaToken()
        return self.requestParametersAuthViaToken()

    def basicAuthorizationViaToken(self):
        """
        Generates a session token via Basic Authentication.
        """
        proxies = helper_proxy_settings.get_proxy(self.PROXY_USERNAME, self.PROXY_PASSWORD)
        url = self.base_url + self.endpoint
        headers = {"Authorization": self.basic_auth(self.username, self.password)}

        try:
            response = self.http.process_request(url, "POST", data=None, json=None, auth=None,
                                                 api_header=headers, proxies=proxies, verify_ssl=False)
            get_token = helper_fetch_token_from_response.get_token_field_from_auth_response(self, response)
            return get_token
        except Exception as ex:
            logger.error(f"Exception occurred while generating session token: {ex}")
            raise Exception(f"{ex}")

    def requestParametersAuthViaToken(self):
        """
        Generates a session token by sending credentials as request parameters.
        """
        proxies = helper_proxy_settings.get_proxy(self.PROXY_USERNAME, self.PROXY_PASSWORD)
        req = PreparedRequest()
        req.prepare_url(f"{self.base_url}{self.endpoint}", self.input_params)

        payload = {"username": self.username, "password": self.password}
        headers = {"Content-Type": "application/json"}

        try:
            response = self.http.process_request(req.url, "POST", None, payload, headers, proxies, False)
            get_token = helper_fetch_token_from_response.get_token_field_from_auth_response(self, response)
            return get_token
        except Exception as ex:
            logger.error(f"Exception occurred while generating session token: {ex}")
            raise Exception(f"{ex}")