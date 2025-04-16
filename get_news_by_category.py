import json
from ..models.news import NewsModel

def handler(event, context):
    """Lambda handler for getting news articles by category"""
    try:
        category = event['pathParameters']['category']
        news_model = NewsModel()
        items = news_model.get_by_category(category)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps(items)
        }
        
    except KeyError:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({'error': 'Category parameter is required'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({'error': str(e)})
        } 