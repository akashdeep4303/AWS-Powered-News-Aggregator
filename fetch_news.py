import os
import json
import requests
from typing import Dict, List
from ..models.news import NewsModel

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

CATEGORIES = ['business', 'technology', 'science', 'health', 'entertainment', 'sports']

def fetch_news_by_category(category: str) -> List[Dict]:
    """Fetch news from NewsAPI for a specific category"""
    params = {
        'apiKey': NEWS_API_KEY,
        'category': category,
        'language': 'en',
        'pageSize': 10
    }
    
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    return []

def handler(event, context):
    """Lambda handler for fetching news"""
    try:
        news_model = NewsModel()
        
        for category in CATEGORIES:
            articles = fetch_news_by_category(category)
            
            for article in articles:
                # Skip if required fields are missing
                if not all([article.get('title'), article.get('description'), article.get('url')]):
                    continue
                    
                news_model.create(
                    title=article['title'],
                    description=article['description'],
                    url=article['url'],
                    category=category,
                    source=article.get('source', {}).get('name', 'Unknown')
                )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'News articles fetched and stored successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 