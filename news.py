import os
import boto3
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class NewsModel:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    def create(self, title: str, description: str, url: str, category: str, source: str) -> Dict:
        """Create a new news article"""
        timestamp = datetime.utcnow().isoformat()
        item = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'url': url,
            'category': category,
            'source': source,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }

        self.table.put_item(Item=item)
        return item

    def get_all(self) -> List[Dict]:
        """Get all news articles"""
        result = self.table.scan()
        return result.get('Items', [])

    def get_by_category(self, category: str) -> List[Dict]:
        """Get news articles by category"""
        result = self.table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression='category = :category',
            ExpressionAttributeValues={
                ':category': category
            }
        )
        return result.get('Items', [])

    def get(self, news_id: str) -> Optional[Dict]:
        """Get a specific news article"""
        result = self.table.get_item(
            Key={
                'id': news_id
            }
        )
        return result.get('Item') 