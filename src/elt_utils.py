import json
from pathlib import Path
import requests

def save_json(data, path: str, filename: str):
    """
    Save Python object as JSON.
    - Creates folders if they don't exist
    - Saves with indent = 2
    """
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

    file_path = path / filename

    with open(file_path, 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2, ensure_ascii = False)

def request_data(url: str, headers: dict, params: dict, path: str) -> dict:
    """
    Makes requests and returns the response as a json.
    Requires target url, required headers (as dict), paramters
    (as a dict), and the file path (e.g., 'path/filename') to
    save the data.
    """
    response = requests.get(url, headers = headers, params = params)

    if response.status_code != 200:
        print(f"Error Code: {response.status_code} for {url}")
        print(response.text[:300])
        return None

    data = response.json()
    save_json(data, f"{path}.json")

    return data

def build_base_params(apps_by_device: dict, start_date: str,
                      end_date: str, countries: list) -> dict:
    """
    Builds the base parameters used by the further functions
    to make specific AppTweak API calls.
    Requires a dictionary of apps by device. That is, specific
    formats for iphone ids or google play store ids are required.
    Start and End date for the query as strings and a list of
    countries to be queried.
    """
    base_params_dict = {}

    for country in countries:
        for device, apps in apps_by_device.items():

            key = f"{country}_{device}"
        
            params = {'apps': ','.join(apps),
                      'start_date': start_date,
                      'end_date': end_date,
                      'country': country,
                      'device': device,}

            base_params_dict[key] = params

    return base_params_dict

def build_metrics_params(base_params: dict, metrics: list) -> dict:
    """
    Takes the base metrics and formats them for an AppTweak
    metrics request.
    Requires the base_params and a list of metrics from
    downloads, revenues, app-power, ratings, daily-ratings.
    """
    new_params = {}

    for key, params in base_params.items():
        new_params[key] = params.copy()
        new_params[key]['metrics'] = ','.join(metrics)

    return new_params

def build_keywords_params(base_params: dict, keywords: list,
                          keywords_metrics: list) -> dict:
    """
    Takes the base metrics and prepares a dictionary of keyword
    queries. It seperated device and country and injects app ids,
    keywords, and other required parameters from base_params.
    Requires a list of keywords. Currently, AppTweak allows a
    max of 5 keywords (not currently enforced) and two possible
    metrics, rank and installs.
    """
    new_params = {}

    for key, params in base_params.items():
        new_params[key] = params.copy()
        new_params[key]['keywords'] = ','.join(keywords)
        new_params[key]['metrics'] = ','.join(keywords_metrics)

    return new_params

def build_category_params(start_date: str, end_date: str,
                          countries: list, categories_map: dict,
                          category_metrics: list) -> dict:
    """
    Builds API parameter sets for category-level metrics across
    devices and countries.

    Creates a dictionary of request parameters for each combination
    of device and metric, using category mappings to structure API
    calls for AppTweak category data.
    """
    category_params = {}
    categories = {}

    for _, platform_map in categories_map.items():
        for device, value in platform_map.items():

            if device not in categories:
                categories[device] = []

            categories[device].append(value)

    for device in categories.keys():
        for metric in category_metrics:

            params = {
            'metric': metric,
            'categories': ','.join(categories[device]),
            'countries': ','.join(countries),
            'start_date': start_date,
            'end_date': end_date,
            'type': 'free',
            'device': device
            }

            category_params[f"{device}_{metric}"] = params

    return category_params

def query_metrics(params: dict, url: str, headers: dict) -> dict:
    """
    Queries AppTweak API for multiple metric parameter sets and saves
    raw responses.

    Iterates over metric configurations, requests data from the API,
    and stores both individual and compiled JSON outputs for
    downstream processing.
    """
    metrics_output = {}

    for key in metrics_params.keys():

        print(f"Fetching data for {key}...")

        data = request_data(keywords_ranking_url, headers, metrics_params[key])

        if data:
            metrics_output[key] = data
            save_json(data, '../data/raw/metrics/single', f"{key}_metrics.json")
        else:
            print(f"Request for {key} metrics produced no results!")

    save_json(metrics_output, '../data/raw/metrics/compiled', 'all_metrics.json')

    return metrics_output


def query_keywords(params: dict, url: str, headers: dict) -> dict:
    """
    Queries AppTweak API for multiple metric parameter sets and saves
    raw responses.

    Iterates over metric configurations, requests data from the API,
    and stores both individual and compiled JSON outputs for
    downstream processing.
    """
    keywords_output = {}

    for key in keywords_params.keys():

        print(f"Fetching data for {key}...")

        data = request_data(keywords_ranking_url, headers, keywords_params[key])

        if data:
            keywords_output[key] = data
            save_json(data, '../data/raw/keywords/single', f"{key}_keywords.json")
        else:
            print(f"Request for {key} metrics produced no results!")

    save_json(keywords_output, '../data/raw/keywords/compiled', 'all_keywords.json')

    return keywords_output









