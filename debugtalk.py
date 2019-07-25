import datetime
import random
import string
import os
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests_html import HTMLSession


def setup_hook_basicauth(request):
    request['auth'] = HTTPBasicAuth('admin', 'admin123')
    request['timeout'] = (60, 60)


def skip_subscription():
    session = requests.session()
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/75.0.3770.100 Safari/537.36",
        "content-type": "application/json",
        "x-channel": "web"
    }
    basic_auth = HTTPBasicAuth('admin', 'admin123')
    login_url = 'https://stag.castlery.com/api/oauth/token'
    login_json = {
        "grant_type": "password",
        "username": "alex.castlery+api_test@gmail.com",
        "password": "7787782",
        "refresh_token": "",
    }
    login_res = session.post(url=login_url, headers=headers, json=login_json, auth=basic_auth)
    access_token = login_res.json()["access_token"]
    subscription_url = "https://stag.castlery.com/api/users/me/subscriptions"
    subscription_headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/75.0.3770.100 Safari/537.36",
        "content-type": "application/json",
        "x-channel": "web",
        "x-access-token": access_token
    }
    subscription_res = session.get(url=subscription_url, headers=subscription_headers, auth=basic_auth)
    subscription = subscription_res.json()
    subscription_status = subscription["status"]
    return subscription_status == 'subscribed'


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_web_access_token():
    url = 'https://stag.castlery.com/api/oauth/token'
    headers = {
        "referer": "https://stag.castlery.com/login",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chro"
                      "me/75.0.3770.100 Safari/537.36",
        "content-type": "application/json",
    }
    json = {
        "grant_type": "password",
        "username": "alex.castlery+api_test@gmail.com",
        "password": "7787782",
        "refresh_token": "",
    }
    auth = HTTPBasicAuth('admin', 'admin123')
    res = requests_retry_session().post(url=url, headers=headers, json=json, auth=auth)
    result = res.json()
    access_token = result["access_token"]
    #status_code = res.status_code
    return access_token


def appointment_date():
    date = (datetime.datetime.now() + datetime.timedelta(days=10))
    appoint_on = date.strftime("%Y-%m-%dT04:00:00Z")
    return appoint_on


def delivery_date():
    date = (datetime.datetime.now() - datetime.timedelta(days=10))
    delivery_at = date.strftime("%Y-%m-%dT04:00:00Z")
    return delivery_at


def today():
    date = datetime.datetime.now()
    today_date = date.strftime("%Y-%m-%dT04:00:00Z")
    return today_date


def teardown_hook_sleep(response):
    if response.status_code == 200 or 201:
        sleep(1)
    else:
        sleep(5)


def random_alphabet():
    alphabet = chr(random.randint(65, 90))
    return alphabet


def create_random_email():
    ran_str_8 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    ran_email = "alex.castlery" + "+" + ran_str_8 + "@" + "gmail.com"
    return ran_email


def create_random_password():
    ran_str_8 = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    ran_pass = "alex" + "_" + ran_str_8
    return ran_pass


def create_random_zipcode():
    zipcode = random.randint(100000, 999999)
    return zipcode


def create_random_phone_number():
    number = random.randint(10000000, 99999999)
    return number


def create_random_order_number():
    number = random.randint(100003220, 100071058)
    return str(number)


def create_random_qty():
    qty = random.randint(1, 10)
    return qty


def create_random_variant_id():
    variant_id = random.randint(20, 23060)
    return str(variant_id)


def create_random_product_id():
    product_id = random.randint(5, 3752)
    return product_id


def create_random_string():
    ran_str_10 = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    return ran_str_10


def create_random_name():
    ran_str_10 = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    name = 'alex' + ran_str_10
    return name


def get_file(file_path):
    return open(file_path, "rb")


def change_order_delivery_status():
    os.system('python2 ./files/selenium/make_order_deliveryed.py')


def set_order_delivered():
    session = HTMLSession()
    login_url = 'https://knight-stag.castlery.sg/spree/admin/login'
    login_page = session.get(url=login_url)
    authenticity_token = login_page.html.xpath("//input[@name='authenticity_token']/@value")[0]
    form_data = {
        "utf8": "✓",
        "authenticity_token": authenticity_token,
        "spree_user[email]": "alex.ac@qq.com",
        "spree_user[password]": "7787782",
        "spree_user[remember_me]": 0,
        "commit": "Login"
    }
    login_res = session.post(url=login_url, data=form_data)
    first_order_href = login_res.html.xpath("//tbody/tr[1]/td[10]/a/@href")[0]
    base_url = 'https://knight-stag.castlery.sg'
    first_order_url = base_url + first_order_href
    first_order_edit_page = session.get(url=first_order_url)
    shipment_id = first_order_edit_page.html.xpath("//span[@class='shipment-number']/text()")[0]
    shipped_url = "https://knight-stag.castlery.sg/spree/api/shipments/" + shipment_id + "/ship"
    shipped_data = {
        "send_mailer": "true"
    }
    admin_token = "c8e776623190ed753b12d457cf81728940a9ff67db4f2992"
    admin_headers = {
        "x-spree-token": admin_token,
        "x-requested-with": "XMLHttpRequest"
    }
    make_shipped = session.put(url=shipped_url, headers=admin_headers, data=shipped_data)
    delivery_url = "https://knight-stag.castlery.sg/spree/api/shipments/" + shipment_id + "/deliver"
    make_delivery = session.put(url=delivery_url, headers=admin_headers)


def get_casehub_login_token():
    login_url = 'https://casehub-stag.castlery.com/api/auth/login'
    login_json = {
        "email": "wei.wei@castlery.com",
        "password": "cslr123*"
    }
    login_res = requests.post(url=login_url, json=login_json)
    token = login_res.json()["token"]
    return token


def get_casehub_login_cookie():
    cookie = 'X-Token=' + get_casehub_login_token() + '; ' + 'sidebarStatus=1'
    return cookie


def get_casehub_login_authorization():
    authorization = 'Bearer ' + get_casehub_login_token()
    return authorization


def get_casehub_configurations():
    url = "https://casehub-stag.castlery.com/api/configurations"
    headers = {
        "cookie": get_casehub_login_cookie(),
        "authorization": get_casehub_login_authorization()
    }
    configurations_res = requests.get(url=url, headers=headers)
    return configurations_res


def get_delivery_team_id():
    res = get_casehub_configurations().json()
    id_number = random.randint(0,19)
    delivery_team_id = res["delivery_team"][id_number]["id"]
    return delivery_team_id


def get_issue_type_id():
    res = get_casehub_configurations().json()
    id_number = random.randint(0,69)
    issue_type_id = res["issue_type"][id_number]["id"]
    return issue_type_id


def get_resolution_type_id():
    res = get_casehub_configurations().json()
    id_number = random.randint(0,14)
    resolution_type_id = res["resolution_type"][id_number]["id"]
    return resolution_type_id


def get_supplier_id():
    res = get_casehub_configurations().json()
    id_number = random.randint(0,54)
    supplier_id = res["supplier"][id_number]["id"]
    return supplier_id











