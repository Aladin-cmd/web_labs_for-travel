import os
import random
import secrets
from dataclasses import dataclass
from typing import Dict, Tuple

import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
#from dotenv import load_dotenv

from stress import StressTest, TestUtility

#load_dotenv('.env')


@dataclass
class M2MPostRequestUtility(TestUtility):
    num_locations_per_request: int = 10
    stats_header_line = ("We can serve {n_requests} POST requests(" +
                         str(num_locations_per_request) + " locations each) with following stats")

    def run_utility(self, child_conn) -> None:
        results = self.m2m_post_request(self.num_locations_per_request)
        child_conn.send(results)

    def m2m_post_request(self, num_locations: int) -> Tuple[float, Dict]:
        api_gateway_url = (f"https://{os.environ.get('AWS_HOST')}/{os.environ.get('M2M_STAGE')}"
                           f"/api/v2/locations")
        api_url = "https://api.geox-ai.com/api/v2/locations"
        aws_details = {
            'aws_access_key': "AKIA2TITFGWE5F7HF5PB",
            'aws_secret_access_key': "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",
            'aws_host': "api.geox-ai.com",
            'aws_region': "us-east-1",
            'aws_service': "execute-api"
        }
        auth = AWSRequestsAuth(**aws_details)

        def get_val(x):
            return (x - 0.00001) + random.random() * 0.00002

        data = {
            "locations": [{"lat": get_val(27.7913446268014),
                           "lng": get_val(-80.49404070625116),
                           "corellationId": secrets.token_hex(10)}
                          for _ in range(num_locations)]
        }

        response = requests.post(api_url, json=data, auth=auth)
        res_json = response.json()
        total_time_ms = response.elapsed.total_seconds() * 1000
        return total_time_ms, res_json

    def validate_response(self, data: Dict) -> None:
        assert len(data['data']) == self.num_locations_per_request
        for result_obj in data['data']:
            assert len(result_obj['results']) > 0


if __name__ == '__main__':
    try:
        utility = M2MPostRequestUtility()
        stress_obj = StressTest(utility)
        stress_obj.stress_test_for_specific_number_of_reqeusts(2)
        s=stress_obj.send_parallel_requests(3)
        print(s)
    except KeyError as e:
        print("Error happened")
        print(f"Error: {e}; Type: {type(e)}")
