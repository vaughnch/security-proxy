import re
import urlparse

# To install the required packages run: 
# pip install requests boto3 aws-requests-auth
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth
from aws_requests_auth import boto_utils


# We got this URL from our provisioned stack's output. This should be passed as a configuration variable, 
# but since there's no secrets in there, you could hard-code this
GITHUB_PROXY_URL = 'https://ynxga79izl.execute-api.us-east-1.amazonaws.com/dev/repos/vaughnch/security/issues'


def get_aws_auth(url):
    # These next variables are needed for the signing process
    api_gateway_netloc = urlparse.urlparse(url).netloc
    api_gateway_region = re.match(
        r"[a-z0-9]+\.execute-api\.(.+)\.amazonaws\.com",
        api_gateway_netloc
    ).group(1)
    
    return AWSRequestsAuth(
        aws_host=api_gateway_netloc,
        aws_region=api_gateway_region,
        aws_service='execute-api',
        # This is how we query the temporary credentials of the EC2 instance, as simple as that
        **boto_utils.get_credentials()
    )


list_issues_response = requests.get(
    url=GITHUB_PROXY_URL,
    auth=get_aws_auth(GITHUB_PROXY_URL)
)

print list_issues_response.json()
