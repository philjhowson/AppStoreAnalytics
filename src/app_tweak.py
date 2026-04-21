import elt_utils
import argparse
import os
import pandas as pd
from config import config
from dotenv import load_dotenv

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
        metrics['metrics'].to_csv('data/processed/dataframes/metrics_df.csv')
        metrics['ratings']['app'] = metrics['ratings']['app'].replace(config.app_map)
        metrics['ratings'].to_csv('data/processed/dataframes/ratings_df.csv')

    if keywords:
        keywords_params = elt_utils.build_keywords_params(base_params, config.keywords, config.keywords_metrics)
        elt_utils.save_json(keywords_params, 'data/parameters', 'keywords_params')

        keywords_output = elt_utils.query_metrics(keywords_params,
                                                  'https://public-api.apptweak.com/api/public/store/apps/keywords-rankings/history.json',
                                                  headers, 'keywords')
        
        keywords_df = elt_utils.parse_apptweak_keywords(keywords_output)
        keywords_df['app'] = keywords_df['app'].replace(config.app_map)
        keywords_df.to_csv('data/processed/dataframes/keywords_df.csv')  

    if categories:
        categories_params = elt_utils.build_category_params(config.start_date, config.end_date, config.countries, config.categories_map, config.category_metrics)
        elt_utils.save_json(categories_params, 'data/parameters', 'category_params')

        categories_output = elt_utils.query_metrics(categories_params,
                                                  'https://public-api.apptweak.com/api/public/store/categories/metrics',
                                                  headers, 'category')
        
        categories_df = elt_utils.parse_apptweak_categories(categories_output)
        categories_df.to_csv('data/processed/dataframes/categories_df.csv') 

    if rankings:
        category_rankings_params = elt_utils.build_category_params(config.start_date, config.end_date, config.countries, config.categories_map, config.category_metrics)
        elt_utils.save_json(category_rankings_params, 'data/parameters', 'category_rankings_params')

        category_rankings_output = elt_utils.query_metrics(category_rankings_params,
                                                  'https://public-api.apptweak.com/api/public/store/categories/metrics',
                                                  headers, 'category')
        
        category_ranking_df = elt_utils.parse_apptweak_category_ranking(category_rankings_output)
        category_ranking_df['app'] = category_ranking_df['app'].replace(config.app_map)
        category_ranking_df['category_name'] = category_ranking_df['category_name'].replace({'category all' : 'all'})
        category_ranking_df.to_csv('data/processed/dataframes/category_ranking_df.csv') 

if '__name__' == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--metrics', default = True)
    parser.add_argument('--keywords', default = True)
    parser.add_argument('--categories', default = True)
    parser.add_argument('--rankings', default = True)    

    args = parser.parse_args()

    prepare_and_request_apptweak(metrics = args.metrics, keywords = args.keywords,
                                 categories = args.categories, rankings = args.rankings)