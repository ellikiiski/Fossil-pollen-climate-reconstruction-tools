"""
Fetch the metadata from Neotoma dabase through the API.
Filter by location or limit the number of searches if desired.
Function fetch_sites returns a json file containing the info of the datasets.
"""

from ..helpers import json_handler as json
from ..helpers import api_requests as req

# TODO: tsekkaa käytetäänkö ageoldest ja ageyoungest ikinä

# FUNCTION TO BE USED BY OTHER MODULES
def get_sites(metadata_url, dataset_url, write_file_path, coordinates=None, max_searches=None):
    """Fetches the pollen data anf chronology metada from Neotoma
    and writes it into a json file in write_file_path.
    Can be filtered by location or age."""

    # fetch both pollen and chronology sites
    print(f' Fetching pollen sites.....')
    pollen_ids = _get_siteids(metadata_url, 'pollen', max_searches)
    print(f' DONE')
    print(f' Checking for carbon dating data.....')
    chrono_ids = _get_siteids(metadata_url, 'geochronologic', max_searches)
    print(f' DONE')

    # comibine the dictionaries
    combined = _combine_ids(pollen_ids, chrono_ids)
    print(f' Found {len(combined)} (out of {len(pollen_ids)}) pollen sites with geochronological data.')

    # get the site infos filtered by given parameters
    print(f' Filtering with the coordinates.....')
    sites = _get_site_infos(combined, dataset_url, coordinates)
    print(f' Found {len(sites)} sites within the area.')

    # write the info into a json file of given name
    json.write_json(sites, write_file_path)
    

# INTERNAL HELP FUNCTIONS BELOW

def _get_siteids(url, type, max_searches=None):
    """Accesses the Neotoma database through API and
    fetches the sites that have the specified dataset type and returns
    a dictionary of siteid:datasetid pairs.
    The number of fetches can be restricted with the max_searches parameter."""

    data = req.fetch_site_data(url, type, max_searches)

    ids = {}

    # loop over the sites and save the siteid:datasetid pairs in the dictionary
    for site in data:
                
        siteid = site['siteid']
        dataset = site['collectionunits'][0]['datasets'][0]
        datasetid = dataset['datasetid']

        ids[siteid] = datasetid

    return ids


def _combine_ids(dict1, dict2):
    """Combines two dictionaries of {siteid : datasetid}
    into one {siteid : [datasetid, datasetid]} dictionary."""

    # get the set of common ids
    common_ids = set(set(dict1.keys()).intersection(set(dict2.keys())))
    # form the joint dictionary
    combined_dict = {key: [dict1[key], dict2[key]] for key in common_ids}

    return combined_dict


def _location_check(data, loc_limits):
    """Returns true or false according to whether the data is within desired area."""

    # in case location is not restricted
    if loc_limits == None:
        return True

    # extraxt the location parameters
    [min_lat, max_lat, min_long, max_long] = loc_limits

    # get the coordinates and
    # compare it to parameters
    try:
        site = data['data'][0]['site']
        lat = site['latitudesouth']
        long = site['longitudeeast']

        if lat >= min_lat and lat <= max_lat and long >= min_long and long <= max_long:
            return True # location is within wanted area
        
    except:
        print(f'Failed to check the location.')

    return False # location is outside wanted area or the check failed


def _get_site_infos(sites, base_url, loc_limits=None):
    """Collects relevant info of the sites with given ids
    and filters by location and age if wanted."""

    siteinfos = []
    progress = 0
    total = len(sites)

    # loop over sites and get the info
    for (siteid, dataset_ids) in sites.items():

        data = req.fetch_site_info(siteid, base_url)

        # FILTER
        if _location_check(data, loc_limits):

            # gather info
            site =  data['data'][0]['site']
            sitename = site['sitename']
            latitude = site['latitudesouth']
            longitude = site['longitudeeast']

            # build info dictionary
            siteinfo = {
                'siteid' : siteid,
                'sitename' : sitename,
                'latitude' : latitude,
                'longitude' : longitude,
                'ageoldest' : None,
                'ageyoungest' : None,
                'pollen' : {
                    'datasetid' : dataset_ids[0]
                },
                'chronologies' : {
                    'datasetid' : dataset_ids[1]
                }
            }

            siteinfos.append(siteinfo)

        progress += 1 # update progress

        # print progress every 25 sites
        if progress % 25 == 0:
            print(f'  {progress}/{total} checked, {len(siteinfos)} accepted...')

    return siteinfos