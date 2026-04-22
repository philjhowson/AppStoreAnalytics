import json
from pathlib import Path
import pandas as pd
import requests

def str_to_bool(v):
    """
    Turns 'true, True, false, False' into the
    correct type, bool, when parsing argparse.
    """
    return str(v).lower() == "true"

def save_json(data, path: str, filename: str):
    """
    Save Python object as JSON.
    - Creates folders if they don't exist
    - Saves with indent = 2
    """
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

    file_path = path / filename

    with open(f"{file_path}.json", 'w', encoding = 'utf-8') as f:
        json.dump(data, f, indent = 2, ensure_ascii = False)

def request_data(url: str, headers: dict, params: dict) -> dict:
    """
    Makes requests and returns the response as a json.
    Requires target url, required headers (as dict), parameters
    (as a dict), and the file path (e.g., 'path/filename') to
    save the data.
    """
    response = requests.get(url, headers = headers, params = params)

    if response.status_code != 200:
        print(f"Error Code: {response.status_code} for {url}")
        print(response.text[:300])
        return None

    data = response.json()

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

def query_metrics(params: dict, url: str, headers: dict, filename: str) -> dict:
    """
    Queries AppTweak API for multiple metric parameter sets and saves
    raw responses.

    Iterates over metric configurations, requests data from the API,
    and stores both individual and compiled JSON outputs for
    downstream processing.
    """
    output = {}

    for key in params.keys():

        print(f"Fetching data for {key}...")

        data = request_data(url, headers, params[key])

        if data:
            output[key] = data
            save_json(data, f"data/raw/{filename}/single", f"{key}_{filename}.json")
        else:
            print(f"Request for {key} metrics produced no results!")

    save_json(output, f"data/raw/{filename}/compiled", f"all_{filename}.json")

    return output

import pandas as pd

def parse_apptweak_metrics(metrics_output: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parses Apptweak app metrics API response into two DataFrames:
    - metrics_df: time series values for non-rating metrics (e.g. downloads, revenue)
    - ratings_df: rating distribution breakdown over time (1–5 star counts + average)

    Splits data by app, country, and device.
    Returns a dict with keys 'metrics' and 'ratings'.
    """
    metrics_rows = []
    ratings_rows = []

    for run_key, payload in metrics_output.items():

        country, device = run_key.split('_')
        result = payload['result']

        for app, metrics in result.items():

            for metric_name, series in metrics.items():

                if metric_name == 'ratings':

                    for point in series:
                        breakdown = point.get('breakdown')

                        if not breakdown:
                            continue  # skip empty safely

                        ratings_rows.append({
                            'date': point['date'],
                            'app': app,
                            'country': country,
                            'device': device,
                            'avg_rating': breakdown.get('avg'),
                            'rating_1': breakdown.get('1'),
                            'rating_2': breakdown.get('2'),
                            'rating_3': breakdown.get('3'),
                            'rating_4': breakdown.get('4'),
                            'rating_5': breakdown.get('5'),
                            'rating_total': breakdown.get('total')
                        })

                else:

                    for point in series:
                        metrics_rows.append({
                            'date': point['date'],
                            'app': app,
                            'country': country,
                            'device': device,
                            'metric': metric_name,
                            'value': point['value'],
                            'precision': point.get('precision')
                        })

    metrics_df = pd.DataFrame(metrics_rows)
    ratings_df = pd.DataFrame(ratings_rows)

    return {'metrics': metrics_df, 'ratings': ratings_df}

def parse_apptweak_keywords(keywords_output: dict) -> pd.DataFrame:
    """
    Parses Apptweak keyword rankings API response into a single DataFrame.

    Extracts time series keyword metrics (e.g. rank, installs) per app, country, and device.
    Each row represents a keyword-level metric value at a specific date.
    """
    rows = []

    for run_key, payload in keywords_output.items():
        
        country, device = run_key.split('_')

        result = payload['result']

        for app, keywords in result.items():

            for keyword, metrics in keywords.items():

                for metric_name, series in metrics.items():

                    for point in series:

                        rows.append({
                            'date': point['date'],
                            'app': app,
                            'country': country,
                            'device': device,
                            'keyword': keyword,
                            'metric': metric_name,
                            'value': point['value'],
                            'effective_value': point.get('effective_value')
                        })

    keywords_df = pd.DataFrame(rows)

    return keywords_df

def parse_apptweak_category_ranking(category_ranking_output: dict) -> pd.DataFrame:
    """
    Parses Apptweak category ranking API response into a DataFrame.

    Extracts app ranking positions across categories over time, split by country and device.
    Each row represents a ranking snapshot for a given category and chart type.
    """
    rows = []

    for run_key, payload in category_ranking_output.items():

        country, device = run_key.split('_')

        result = payload['result']

        for app, app_data in result.items():

            rankings = app_data['rankings']

            for r in rankings:

                for v in r['value']:

                    rows.append({
                        'date': v['fetch_date'],
                        'app': app,
                        'country': country,
                        'device': device,
                        'category_name': v['category_name'].lower(),
                        'chart_type': v['chart_type'],
                        'rank': v['rank'],
                        'fetch_depth': v['fetch_depth']
                    })
                    
    category_ranking_df = pd.DataFrame(rows)

    return category_ranking_df

def parse_apptweak_categories(categories_output: dict) -> pd.DataFrame:
    """
    Parses Apptweak category metrics API response into a DataFrame.

    Extracts category-level performance metrics across countries and devices.
    Each row represents a time series value for a given category metric.
    """
    rows = []

    for run_key, payload in categories_output.items():

        device, metric = run_key.split('_')

        result = payload['result']

        for category, countries in result.items():

            for country, series in countries.items():

                for point in series:

                    rows.append({
                        'date': point['date'],
                        'category': category.lower(),
                        'country': country,
                        'device': device,
                        'metric': metric,
                        'value': point.get(metric) 
                    })

    categories_df = pd.DataFrame(rows)

    return categories_df

