from dataclasses import dataclass
"""
This config is passed to 
"""
@dataclass
class Config:
    apps: list
    apps_by_device: dict
    start_date: str
    end_date: str
    countries: list
    metrics: list
    keywords: list
    keywords_metrics: list
    categories_map: dict
    category_metrics: list

config = Config(
    apps = ['Tinder', 'Bumble', 'Hinge', 'Coffee Meets Bagel']
    apps_by_device = {
    'android': ['com.tinder', 'com.bumble.app', 'co.hinge.app', 'com.coffeemeetsbagel'],
    'iphone': ['547702041','930441707', '595287172', '6502307144']
    }
    start_date ='2026-03-01'
    end_date = '2026-03-31'
    countries = ['us', 'de', 'jp']
    metrics = ['downloads', 'revenues' , 'ratings']
    keywords = ['dating app', 'online dating', 'meet people', 'find love', 'chat app']
    keywords_metrics = ['rank', 'installs']
    categories_map = {
    'social' : {'android' : 'SOCIAL', 'iphone': '6005'},
    'lifestyle': {'android': 'LIFESTYLE', 'iphone': '6012'},
    'entertainment': {'android': 'ENTERTAINMENT', 'iphone': '6016'},
    'dating': {'android': 'DATING'}
    }
    category_metrics = ['downloads', 'revenues']
)