import elt_utils
import argparse
import os
import pandas as pd
from config import config
from dotenv import load_dotenv
from pathlib import Path

def prepare_and_request_apptweak(metrics: bool, keywords: bool, categories: bool, rankings: bool):
    """
    Runs Apptweak data extraction pipeline for selected data domains.

    Depending on the provided flags, this function:
    - Builds API request parameters
    - Calls the Apptweak API
    - Parses responses into DataFrames
    - Saves both raw parameters and processed outputs to disk

    Args:
        metrics (bool): Whether to fetch app-level metrics and ratings data.
        keywords (bool): Whether to fetch keyword ranking data.
        categories (bool): Whether to fetch category-level metrics data.
        rankings (bool): Whether to fetch category ranking data.

    Outputs:
        Saves processed DataFrames as CSV files in 'data/processed/dataframes/'.
        Saves request parameter JSONs in 'data/parameters/'.
    """
    load_dotenv()
    api_key = os.getenv('apptweak_api_key')

    headers = {'accept': 'application/json',
            'X-Apptweak-Key': api_key}
    
    base_params = elt_utils.build_base_params(config.apps_by_device, config.start_date, config.end_date, config.countries)
    if metrics:
        print('Preparing parameters for metrics call...')
        metrics_params = elt_utils.build_metrics_params(base_params, config.metrics)
        elt_utils.save_json(metrics_params, 'data/parameters', 'metrics_params')

        metrics_output = elt_utils.query_metrics(metrics_params,
                                                 'https://public-api.apptweak.com/api/public/store/apps/metrics/history.json',
                                                 headers, 'metrics')

        metrics = elt_utils.parse_apptweak_metrics(metrics_output)

        Path('data/processed/dataframes').mkdir(parents = True, exist_ok = True)

        metrics['metrics'].to_csv('data/processed/dataframes/metrics_df.csv')
        metrics['ratings']['app'] = metrics['ratings']['app'].replace(config.app_map)
        metrics['ratings'].to_csv('data/processed/dataframes/ratings_df.csv')
    
    if keywords:
        print('Preparing parameters for keywords call...')
        keywords_params = elt_utils.build_keywords_params(base_params, config.keywords, config.keywords_metrics)
        elt_utils.save_json(keywords_params, 'data/parameters', 'keywords_params')

        keywords_output = elt_utils.query_metrics(keywords_params,
                                                  'https://public-api.apptweak.com/api/public/store/apps/keywords-rankings/history.json',
                                                  headers, 'keywords')
        
        keywords_df = elt_utils.parse_apptweak_keywords(keywords_output)
        keywords_df['app'] = keywords_df['app'].replace(config.app_map)

        Path('data/processed/dataframes').mkdir(parents = True, exist_ok = True)

        keywords_df.to_csv('data/processed/dataframes/keywords_df.csv')  

    if categories:
        print('Preparing parameters for categories call...')
        categories_params = elt_utils.build_category_params(config.start_date, config.end_date, config.countries, config.categories_map, config.category_metrics)
        elt_utils.save_json(categories_params, 'data/parameters', 'category_params')

        categories_output = elt_utils.query_metrics(categories_params,
                                                  'https://public-api.apptweak.com/api/public/store/categories/metrics',
                                                  headers, 'category')
        
        categories_df = elt_utils.parse_apptweak_categories(categories_output)

        Path('data/processed/dataframes').mkdir(parents = True, exist_ok = True)

        categories_df.to_csv('data/processed/dataframes/categories_df.csv') 

    if rankings:
        print('Preparing parameters for category rankings call...')
        category_rankings_output = elt_utils.query_metrics(base_params,
                                                  'https://public-api.apptweak.com/api/public/store/apps/category-rankings/history.json',
                                                  headers, 'categories')
        
        category_ranking_df = elt_utils.parse_apptweak_category_ranking(category_rankings_output)
        category_ranking_df['app'] = category_ranking_df['app'].replace(config.app_map)
        category_ranking_df['category_name'] = category_ranking_df['category_name'].replace({'category all' : 'all'})

        Path('data/processed/dataframes').mkdir(parents = True, exist_ok = True)

        category_ranking_df.to_csv('data/processed/dataframes/category_ranking_df.csv') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--metrics', type = elt_utils.str_to_bool, default = True)
    parser.add_argument('--keywords', type = elt_utils.str_to_bool, default = True)
    parser.add_argument('--categories', type = elt_utils.str_to_bool, default = True)
    parser.add_argument('--rankings', type = elt_utils.str_to_bool, default = True)    

    args = parser.parse_args()

    prepare_and_request_apptweak(metrics = args.metrics, keywords = args.keywords,
                                 categories = args.categories, rankings = args.rankings)
