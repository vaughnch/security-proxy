#this proxy will obfusate credentials for the target service
#credentials are stored centrally to the proxy

import re
import urlparse
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth import boto_utils


#Proxy URL
APP_PROXY_URL = 'https://ynxga79izl.execute-api.us-east-1.amazonaws.com/dev/repos/vaughnch/security-proxy'


def get_aws_auth(url):
    # The following signs the request
    api_gateway_netloc = urlparse.urlparse(url).netloc
    api_gateway_region = re.match(
        r"[a-z0-9]+\.execute-api\.(.+)\.amazonaws\.com",
        api_gateway_netloc
    ).group(1)
    
    return AWSRequestsAuth(
        aws_host=api_gateway_netloc,
        aws_region=api_gateway_region,
        aws_service='execute-api',
        **boto_utils.get_credentials()
    )


list_issues_response = requests.get(
    url=APP_PROXY_URL,
    auth=get_aws_auth(APP_PROXY_URL)
)

print list_issues_response.json()
