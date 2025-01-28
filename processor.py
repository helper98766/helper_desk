from modules.database.core.engine import engine
from modules.database.core.engine import session_scope
from helper.DynamicORM import ORMClassGenerator
from modules.api_access_module.api_auth_access_plugin import ApiAuthPlugin
from config_provider import ConfigProvider
from process_api_module.process_api import ProcessApi
from sets_log_uniformity.main import LogUniformity
from app import reading_output_file, convert_json_to_dict
import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

loggers = LogUniformity()
loggers.override_config("FileHandler", level="Debug")
log = logging.getLogger(__name__)

class Processor:
    def __init__(self, api, PROXY_USERNAME, PROXY_PASSWORD):
        self.config_data = ConfigProvider("config.yaml").config_data
        self.engine = engine()
        self.session = session_scope()
        self.orm_class = ORMClassGenerator(self.engine, self.session)
        self.PROXY_USERNAME = PROXY_USERNAME  # This will not be part of class parameters; it should be fetched by secret module.
        self.PROXY_PASSWORD = PROXY_PASSWORD  # Same as above.
        self.get_api = self.get_API_module()
        self.get_response = self.get_response_from_API(self.get_api)  # Fixed self.output reference to self.get_api

    def get_secrets(self):
        # Code to fetch secrets using secrets module
        pass

    def get_API_module(self):
        automation_obj = ApiAuthPlugin(self.api, self.config_data, self.PROXY_USERNAME, self.PROXY_PASSWORD)
        output = automation_obj()
        return output

    def get_response_from_API(self, output):
        get_response = ProcessApi(self.api, self.config_data, output, self.PROXY_USERNAME, self.PROXY_PASSWORD)
        result = get_response()
        return result

    def write_data_to_database(self):
        table_name = self.config_data['DATABASE']['TABLE_NAME']
        columns_input = self.config_data['DATABASE']['COLUMNS']
        primary_key = self.config_data['DATABASE']['PRIMARY_KEY']
        columns = {}
        for item in columns_input.split(','):
            col_name, col_type = item.split(':')
            columns[col_name.strip()] = col_type.strip()
        dynamic_column = self.orm_class.create_dynamic_class(columns, primary_key)
        class_code = self.orm_class.mapping_file(dynamic_column, f"modules/database/mapping/{table_name}_mapping.py")
        orm_class = self.orm_class.create_orm_class(class_code, table_name)
        return orm_class

if __name__ == "__main__":
    process = Processor("APISCHEMA", PROXY_USERNAME="", PROXY_PASSWORD="")
    orm_class = process.write_data_to_database()
    ipaddress = reading_output_file("Output/output_2025-01-03T16-10.json")
    data = convert_json_to_dict("JSON/data.json")
    data['IPAddress'] = ipaddress
    table_name = process.config_data['DATABASE']['TABLE_NAME']
    primary_key = process.config_data['DATABASE']['PRIMARY_KEY']
    process.orm_class.insert_data(orm_class, table_name, primary_key)
    process.orm_class.fetch_data_with_filter(orm_class, ScanZone="For Testing Purpose")
