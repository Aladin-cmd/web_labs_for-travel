import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth


def m2m_request(access_key, secret_key, lat, lng):
    api_url = "https://api.geox-ai.com/poc/v2"  # os.environ.get('API_URL')
    aws_details = {
        'aws_access_key': access_key,  # os.environ.get('AWS_ACCESS_KEY'),
        'aws_secret_access_key': secret_key,  # os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'aws_host': "api.geox-ai.com",  # os.environ.get('AWS_HOST'),
        'aws_region': "us-west-1",  # os.environ.get('AWS_REGION'),
        'aws_service': "execute-api"
    }
    auth = AWSRequestsAuth(**aws_details)
    params = {
        "lat": lat,
        "lng": lng,
    }
    res = requests.get(api_url, auth=auth, params=params)
    #assert res.status_code == 200, f"Request failed with status: {res.status_code}"
    res_data = res.json()
    return res

def m2m_request_get(access_key, secret_key, lat, lng):
    api_url = "https://api.geox-ai.com/api/v2/locations"
    aws_details = {
        'aws_access_key': access_key,
        'aws_secret_access_key': secret_key,
        'aws_host': "api.geox-ai.com",
        'aws_region': "us-east-1",
        'aws_service': "execute-api"
    }
    auth = AWSRequestsAuth(**aws_details)
    params = {
        "lat": lat,
        "lng": lng,
    }
    res = requests.get(api_url, auth=auth, params=params)
    #assert res.status_code == 200, f"Request failed with status: {res.status_code}"
    res_data = res.json()
    return res
def m2m_request_post(access_key, secret_key):
    api_url = "https://api.geox-ai.com/api/v2/locations"
    aws_details = {
        'aws_access_key': access_key,
        'aws_secret_access_key': secret_key,
        'aws_host': "api.geox-ai.com",
        'aws_region': "us-east-1",
        'aws_service': "execute-api"
    }
    auth = AWSRequestsAuth(**aws_details)

    data = {
        "locations": [
            {
                "lat": 45.6696163800542,
                "lng": -122.5038830583887,
                "corellationId": "unique_id"
            },
            # ... more locations
        ]
    }

    res = requests.post(api_url, json=data, auth=auth)
    #assert res.status_code == 200, f"Request failed with status: {res.status_code}"
    res_data = res.json()
    return res
