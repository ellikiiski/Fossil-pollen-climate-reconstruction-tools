
import requests

def fetch_site_data(url, type, max_searches=None):
    """Accesses the Neotoma database through API and
    fetches the sites that have the specified dataset type and returns
    the sites data as a list.
    The number of fetches can be restricted with the max_searches parameter."""

    limit = max_searches if max_searches != None and max_searches < 1000 else 1000
    params = {
        'datasettype': type,    # filtering by dataset type
        'limit': limit,         # how many sites to fetch
        'offset': 0             # initial offset, starting from the beginning
    }

    data = []
    has_more_data = True    # stops the while loop when all data has been fetched
    enough_data = False     # stops the while loop when the max_searches has been reached

    while has_more_data and not enough_data: # loop new API fetches until there's no more data (wanted)
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data.extend(response.json()['data'])

            # check if max number of searches is reached
            if max_searches != None and len(data) >= max_searches:
                enough_data = True # stops the loop before next round

            # check if more data is available
            if len(data) < params['limit']:
                has_more_data = False # stops the loop before next round

            else:
                params['offset'] += params['limit'] # updates parameters to use get the next page of results

        else: # if request was not successful
            print(f"Failed to retrieve data: {response.status_code}")
            has_more_data = False

    return data

def fetch_site_info(id, base_url):
    """Fetches the site with given ids through the API."""

    response = requests.get(f'{base_url}/{id}')
    if response.status_code == 200:
        return response.json()

    else:
        print(f"Failed to retrieve data of id {id}: {response.status_code}")


def fetch_dataset(base_url, datasetid):
    """Accesses the Neotoma database through API,
    fetches the data of given dataset id
    and returns it as dictionary.
    """

    response = requests.get(f'{base_url}/{datasetid}')
    if response.status_code == 200:

        return response.json()
        
    else:
        print(f'Failed to download the data with dataset id {datasetid} (pollen data)')
    
    return None
