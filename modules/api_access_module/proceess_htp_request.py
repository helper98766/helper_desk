import requests
from utilities.log import LogUtil
from logging import config, getLogger
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json

class HTTPUtil:
    """
    Utility class for handling HTTP requests with persistent session management,
    error handling, and detailed logging of request outcomes.
    """
    def __init__(self):
        pass
        self.logger = getLogger(__name__)

    def process_request(self, url, method, data_json, auth, api_header, proxies, verify_ssl):
        self.sessionobj = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.sessionobj.mount("https://", HTTPAdapter(max_retries=retries))
        try:
            endpoint = url
            if method.upper() != "GET" and method.upper() != "POST":
                raise NotImplementedError("Method is not supported -> " + method)

            if method.upper() == "POST":
                resp = self.sessionobj.request(
                    method, url=endpoint, data=data_json, auth=auth,
                    headers=api_header, proxies=proxies, verify=verify_ssl
                )
            else:
                resp = self.sessionobj.request(
                    method, url=endpoint, json=data_json, auth=auth,
                    headers=api_header, proxies=proxies, verify=verify_ssl
                )

            resp.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 400:
                self.logger.info(f"---- Bad Request 400 ---- {ex}")
            elif ex.response.status_code == 503:
                self.logger.info(f"---- Service Unavailable 503 ---- {ex}")
            elif ex.response.status_code == 403:
                self.logger.info(f"---- Unauthorized 403 ---- {ex}")
            else:
                self.logger.info(f"---- Error connecting ---- {ex}")
        except Exception as ex:
            self.logger.info(f"---- Error ---- {ex}")
        else:
            self.logger.info(f"---- Request successful ----")
            return resp.json()
        except Exception as e:
            self.logger.info(f"Error: {e}")
            return resp