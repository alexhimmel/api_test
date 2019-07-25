import requests
import braintree
from requests.auth import HTTPBasicAuth

request_url = 'https://stag.castlery.com/api/braintree_client_tokens'
request_data = {
    ':authority': 'stag.castlery.com',
    ':method': 'POST',
    ':path': '/api/braintree_client_tokens',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'authorization': 'Basic YWRtaW46YWRtaW4xMjM=',
    'cache-control': 'no-cache',
    'content-length': '0',
    'cookie': 'city=%7B%22city%22%3A%22Singapore%22%7D; __stripe_mid=797aba23-30e8-4079-916d-6b152df5d162; _ga=GA1.2.13'
              '73815076.1558492836; fixbar_hidden=true; cto_lwid=f9243fe5-7dea-4f9c-b39f-4bb875b8b408; _gcl_au=1.1.9208'
              '9227.1558497480; _fbp=fb.1.1558497480458.2036079251; fbm_1088947447879262=base_domain=.castlery.com; fbs'
              'r_1088947447879262=mbnIvYSzW4xX_CBHx_Daqa1nAfbKf6cEeS9UaygWkPo.eyJ1c2VyX2lkIjoiMTAyNDI1MzUwOTA5NDIwIiwiY'
              '29kZSI6IkFRRHFQLXgwMmk2cndzdVR1LXdLODVySGRrZHAzdWg5eHk3bEpma00xWGFHRmNoS1c2RlU5LXVJU3QwbnBsRV9MUTJRSnR2W'
              'ms0cnNwQ19wSjdpRjNBaC1GanQxcDdfLTBRTEROWHZMVGxuX1BlSjBTNmcwUnVPQUdrMzNWUFA5bnQtRlVqbHNsZWl5WTMyUTZWdlZZR'
              '0hqYzFWSGFsVVY1djRFd0ZXaWEtTVhiekhCWDloV1gzd3dYdl9mSHEtTEVCVmtoY2puZ2VMMUVfODZnaEJvWFhMc2JxbDAwTm9TbFliV'
              'GtfSF9lWDFiLUdZTE11aFlzcHJtUlZkMzVpSXVaV0RkdzVzaG1lbUkyVk9LRDMtYnJQY0tncTA3MzlFTUN4T3BKb3RSbDJFcVpRSHZyL'
              'WZid3BJcnNsX2M0YlNUVlltcVF0TnAtdXZNRjlCWlhyQU9vVEIwIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiO'
              'jE1NTkwMzE4NTd9; cto_idcpy=56f70361-3e07-4cae-92d7-7d40f74b7554; _gid=GA1.2.1104497758.1560127196; locat'
              'ion=%7B%22ip_address%22%3A%2254.255.136.223%22%2C%22country_code%22%3A%22SG%22%2C%22country_name%22%3A%2'
              '2Singapore%22%2C%22city%22%3A%22Singapore%22%7D; viewed_products=[1413]; access_token=d20c44d6334356ba04'
              '2e5bb985bc0fc8811217be397cc4c44bfa7a17e6e7c3b0; refresh_token=c0d3a1b6742aaedb3a0afe83346423371ea63fe8c7'
              '6bab63e8e15bbe5cac3c93; __stripe_sid=caf78056-aff5-466e-a43f-7d2cccf841ef; _gat=1; order_id=R584416411',
    'origin': 'https://stag.castlery.com',
    'pragma': 'no-cache',
    'referer': 'https://stag.castlery.com/checkout/payment',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3'
                  '770.80 Safari/537.36',
    'x-channel': 'web'
}

requests_auth = HTTPBasicAuth('admin', 'admin123')

res = requests.post(url=request_url, data=request_data, auth=requests_auth)

payment_token = res.json()['client_token']

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="84wcn37stqbkpm5r",
        public_key="y9ktvvmhkqh6hdmm",
        private_key="6c71d39442d373cda630c1081f49e386"
    )
)

result = gateway.payment_method_nonce.create(payment_token)
nonce = result.payment_method_nonce.nonce