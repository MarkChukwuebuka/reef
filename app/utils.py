import requests
import pandas
import json
from datetime import date, timedelta, datetime
import os
from django.core.cache import cache
from core.settings import CACHE_TTL


BASE_URL = 'https://mutator.reef.pl'

def auth_user():
    url = f'{BASE_URL}/v139/accounts/authentication'

    form_data = {
        "email" : os.getenv('EMAIL'),
        "password" : os.getenv('PASSWORD')
    }

    params = {
        "app_token" : os.getenv("APP_TOKEN")
    }

    response = requests.post(url, data=form_data, params=params)
    data = json.loads(response.text)

    return data["auth_token"]


def get_organization():

    auth_token = auth_user()

    url = f'{BASE_URL}/v139/groups'

    headers = {
        "AuthToken" : auth_token
    }
    params = {
        "app_token" : os.getenv("APP_TOKEN")
    }

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    data = {
        'org_id' : data['organizations'][0]['id'],
        'org_name' : data['organizations'][0]['name']
    }

    return data



def get_org_projects():

    org_id = get_organization()['org_id']
    auth_token = auth_user()

    url = f'{BASE_URL}/v139/groups/{org_id}/subprojects'

    headers = {
        "AuthToken" : auth_token
    }
    params = {
        "app_token" : os.getenv("APP_TOKEN")
    }

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    project_list = []
    for id in data['projects']:
        project_list.append(id['id'])

    return project_list



def get_daily_org_projects():

    org_id = get_organization()['org_id']
    auth_token = auth_user()
    today = date.today()
    yesterday = today - timedelta(days = 1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')

    url = f'{BASE_URL}/v139/groups/{org_id}/operations/daily'

    headers = {
        "AuthToken" : auth_token,
        "DateStart" : yesterday  
    }
    params = {
        "app_token" : os.getenv("APP_TOKEN"),
        'date[stop]': yesterday
    }

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    return data


def get_project(project_id):

    url = f'{BASE_URL}/v139/subprojects/{project_id}'
    
    auth_token = auth_user()

    headers = {
        "AuthToken" : auth_token
    }
    params = {
        "app_token" : os.getenv("APP_TOKEN")
    }

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    return data



def get_user(user_id):

    url = f'{BASE_URL}/v139/accounts/{user_id}'
    
    auth_token = auth_user()

    headers = {
        "AuthToken" : auth_token
    }
    params = {
        "app_token" : os.getenv("APP_TOKEN")
    }

    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    return data



def formulate_table():
    index = []
    columns = []
    d = []

    data = get_daily_org_projects()
    
    for i in data['daily_activities']:
        index.append(get_project(i['project_id'])['project']['name'])
        columns.append(get_user(i['user_id'])['user']['name'])
        d.append(i['tracked'])

    df = pandas.DataFrame(d, index=index, columns=columns)
    html_table = df.to_html()

    directory = "files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    today = date.today()
    yesterday = today - timedelta(days = 1)
    filename = yesterday.strftime('%Y-%m-%d.csv')

    df.to_csv(f'{directory}/{filename}')
    html_table = df.to_html()
    cache.set('html_table', html_table, CACHE_TTL)
    print('running')

    return html_table
