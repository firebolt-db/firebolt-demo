import datetime
import json
import os

import requests


# Use Firebolt's REST API to connect to Firebolt and execute queries.
# More info: https://docs.firebolt.io/Guides/query-data/using-the-api.html.
class FireboltConnection:
    def __init__(
        self,
        client_id=os.getenv("FIREBOLT_ACCOUNT_ID"),
        client_secret=os.getenv("FIREBOLT_ACCOUNT_SECRET"),
        account_name=os.getenv("FIREBOLT_ACCOUNT_NAME"),
        engine_name=os.getenv("FIREBOLT_ACCOUNT_ENGINE_NAME"),
        database_name=os.getenv("FIREBOLT_ACCOUNT_DATABASE_NAME"),
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.account_name = account_name
        self.engine_name = engine_name
        self.database_name = database_name
        self.refresh_access_token()
        self.system_engine_url = self.get_system_engine_url()
        self.user_engine_url = self.get_user_engine_url()
        # Disable result caching to show Firebolt's true warm-cache performance.
        self.query_settings = "enable_result_cache=false&output_format=JSON_CompactLimited&append_explain_analyze_to_json_output_format=true"

    def refresh_access_token(self):
        url = "https://id.app.firebolt.io/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "audience": "https://api.firebolt.io",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(url, headers=headers, data=data)
        self.access_token = response.json()["access_token"]
        self.last_access_token_refresh = datetime.datetime.now()

    def maybe_refresh_access_token(self):
        # Refresh access token if it's older than 30 minutes.
        if (
            self.last_access_token_refresh + datetime.timedelta(minutes=30)
            < datetime.datetime.now()
        ):
            self.refresh_access_token()

    def get_system_engine_url(self):
        self.maybe_refresh_access_token()
        url = (
            f"https://api.app.firebolt.io/web/v3/account/{self.account_name}/engineUrl"
        )
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()["engineUrl"]

    def get_user_engine_url(self):
        self.maybe_refresh_access_token()
        url = f"https://{self.system_engine_url}/query"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query = f"SELECT url FROM information_schema.engines WHERE engine_name='{self.engine_name}';"
        response = requests.post(url, headers=headers, data=query)
        return response.json()["data"][0]["url"]

    def validate_query(self, query):
        try:
            self.execute_query_on_user_engine(f"EXPLAIN {query}")
            return "Success"
        except Exception as e:
            return f"Query validation failed: {e}"

    def execute_query_on_system_engine(self, query, limit_rows=100):
        self.maybe_refresh_access_token()
        url = f"https://{self.system_engine_url}&{self.query_settings}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(url, headers=headers, data=query)
        return self.transform_query_result(response.json(), limit_rows)

    def execute_query_on_user_engine(self, query, limit_rows=100):
        self.maybe_refresh_access_token()
        url = f"https://{self.user_engine_url}&database={self.database_name}&{self.query_settings}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(url, headers=headers, data=query)
        return self.transform_query_result(response.json(), limit_rows)

    def transform_query_result(self, query_result, limit_rows):
        if "errors" in query_result:
            # Query failed.
            raise Exception(
                json.dumps(
                    {
                        "query_id": query_result["query"]["query_id"],
                        "errors": query_result["errors"],
                    },
                    indent=2,
                )
            )

        expected_keys = ["query", "meta", "data", "statistics"]
        assert all(key in query_result for key in expected_keys), (
            f"Unexpected query result format: {json.dumps(query_result, indent=2)}"
        )

        return {
            "query_id": query_result["query"]["query_id"],
            "statistics": {
                "response_time_seconds": query_result["statistics"]["elapsed"],
                "rows_read": query_result["statistics"]["rows_read"],
                "bytes_read": query_result["statistics"]["bytes_read"],
                "scanned_bytes_cache": query_result["statistics"][
                    "scanned_bytes_cache"
                ],
                "scanned_bytes_storage": query_result["statistics"][
                    "scanned_bytes_storage"
                ],
            },
            "column_names": [col["name"] for col in query_result["meta"]],
            "rows": query_result["data"][:limit_rows],
        }
