import requests


def request(url, method='GET', data=None, params=None):
    is_succeeded = False
    res = None
    try:
        if method == 'GET':
            res = requests.get(url, params=params)
        elif method == 'POST':
            res = requests.post(url, data=data)
        else:
            res = requests.request(method, url)
    except requests.HTTPError:
        print('API request failed! status_Code:', res.status_code)
    except Exception as e:
        print('Something went wrong during making request!', e)
    else:
        is_succeeded = True
    finally:
        return is_succeeded, res
