import requests, urllib, json, config

# moderation api
def moderation_api(comment):
    # Request headers
    headers = {
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': config.api_key
    }
    # Request parameters
    params = ({'classify': 'True'})
    body = [{'text' :comment}]
    url = config.api_url
    r = requests.post(url, json = body, params = params,headers= headers )
    return r.json()