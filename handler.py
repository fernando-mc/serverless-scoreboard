import json
import boto3
import requests

def handler(event, context):
    # Set of Repos to look for metadata
    frameworks = [
        'serverless/serverless',
        'miserlou/zappa',
        'aws-amplify/amplify-js',
        'awslabs/serverless-application-model',
        'jorgebastida/gordon',
        'architect/architect',
        'mweagle/Sparta',
        'aws/chalice',
        'claudiajs/claudia',
        'brefphp/bref',
    ]
    # Request data from the GitHub API
    results = []
    for framework in frameworks:
        r = requests.get('https://api.github.com/repos/' + framework)
        data = json.loads(r.text)
        framework_stats = {
            "name": data["name"],
            "subscribers_count": data["subscribers_count"],
            "stargazers_count": data["stargazers_count"],
            "forks_count": data["forks_count"],
        }
        results.append(framework_stats)
    json_result = json.dumps(results)
    # Output data to S3 file
    s3 = boto3.client('s3')
    s3.put_object(
        ACL='public-read',
        Body=json_result,
        Bucket="fmc-data-utils", 
        Key="recent_results.json",
    )
    print("RESULTS:")
    print(results)
    return "Success"
