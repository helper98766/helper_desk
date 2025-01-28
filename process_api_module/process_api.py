from modules.api_access_module.process_http_request import HTTPUtil
from helper import helper_proxy_settings
from requests.models import PreparedRequest
from datetime import datetime, timedelta
import json, os, copy, logging, requests
from sets_log_uniformity.main import LogUniformity

loggers = LogUniformity()
loggers.override_config("FileHandler", level="Debug", file_name="config.log")
logger = logging.getLogger(__name__)

class ProcessApi:
    def __init__(self, API, config_data, get_token, PROXY_USERNAME, PROXY_PASSWORD):
        api_config = config_data.get(API)
        self.input_params = api_config.get("Params")
        self.get_incident_url = api_config["APIS"]["GET_INCIDENT_URL"]
        self.key_header = api_config["HEADERS"]["KEY"]
        self.PROXY_USERNAME = PROXY_USERNAME
        self.PROXY_PASSWORD = PROXY_PASSWORD
        self.get_token = get_token
        self.http = HTTPUtil()

    def __call__(self):
        try:
            return self.get_process_api()
        except Exception as e:
            logger.error(f"Exception error : {e}")

    def get_process_api(self):
        formatted_time = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M")
        end_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
        last_run_file_path = "last_run_time.txt"

        try:
            with open(last_run_file_path, "r") as file:
                start_data = file.read().strip()
        except FileNotFoundError:
            raise Exception(f"{last_run_file_path} file not found.")
        finally:
            file.close()

        if not start_data:
            start_time = formatted_time
        else:
            start_time = start_data

        proxies = helper_proxy_settings.get_proxy(self, self.PROXY_USERNAME, self.PROXY_PASSWORD)
        header = {"key": self.get_token}
        req = PreparedRequest()
        req.prepare_url(self.get_incident_url, {'start_time': start_time, 'end_time': end_time})

        file_name = copy.deepcopy(start_time)
        file_name = file_name.replace(":", "-")

        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        output_file_name = f"{file_name}.json"
        output_file_path = os.path.join(output_dir, output_file_name)
        logging.info(output_file_path)

        try:
            response = self.http.process_request(
                req.url, "GET", data=None, json=None, auth=None, api_header=header,
                proxies=proxies, verify_ssl=False
            )
            json_object = json.dumps(response, indent=4)
            with open(output_file_path, "w") as outfile:
                outfile.write(json_object)
        except FileNotFoundError:
            raise Exception(f"{output_file_path} file not found.")
        finally:
            outfile.close()

        try:
            with open(last_run_file_path, "w") as file:
                file.write(datetime.now().strftime("%Y-%m-%dT%H:%M"))
        except FileNotFoundError:
            raise Exception(f"{last_run_file_path} file not found.")
        finally:
            file.close()

        return response

        try:
            pass
        except requests.exceptions.HTTPError as errh:
            logger.error(f"HTTP Error: {errh}")
            return
        except Exception as err:
            logger.error(f"Other Error: {err}")
            return