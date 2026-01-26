"""
DynamoDB client wrapper with retry logic.
"""
import boto3 
from botocore.exceptions import ClientError 
from typing import Any, Dict, List, Optional
from src.config.config_settings import settings
from src.utils.utils_logger import get_logger

import os

IS_LOCAL = os.getenv("LOCAL_MODE", "false").lower() == "true"

if IS_LOCAL:
    print("[INFO] ✅ Using LOCAL in-memory database")
    from db.local_db import local_db
    
    class LocalDBWrapper:
        def __init__(self):
            self.db = local_db
        def put_item(self, item): return self.db.put_item(item)
        def get_item(self, pk, sk): return self.db.get_item(pk, sk)
        def update_item(self, pk, sk, updates, condition_expression=None): 
            return self.db.update_item(pk, sk, updates, condition_expression)
        def query(self, pk, sk_condition=None, index_name=None, limit=None): 
            return self.db.query(pk, sk_condition, index_name, limit)
        def delete_item(self, pk, sk): return self.db.delete_item(pk, sk)
    db_client = LocalDBWrapper()


logger = get_logger(__name__)

class DynamoDBClient:
    """DynamoDB client wrapper with common operations."""
    
    def __init__(self):
        """Initialize DynamoDB client."""
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table = self.dynamodb.Table(settings.DYNAMODB_TABLE)
        self.client = boto3.client('dynamodb', region_name=settings.AWS_REGION)
    
    def put_item(self, item: Dict[str, Any]) -> bool:
        """
        Put an item into DynamoDB.
        
        Args:
            item: Item to store
            
        Returns:
            True if successful
            
        Raises:
            Exception: If operation fails
        """
        try:
            self.table.put_item(Item=item)
            logger.debug("Item stored successfully", pk=item.get('PK'), sk=item.get('SK'))
            return True
        except ClientError as e:
            logger.error("Failed to put item", error=str(e))
            raise
    
    def get_item(self, pk: str, sk: str) -> Optional[Dict[str, Any]]:
        """
        Get an item from DynamoDB.
        
        Args:
            pk: Partition key
            sk: Sort key
            
        Returns:
            Item if found, None otherwise
        """
        try:
            response = self.table.get_item(
                Key={'PK': pk, 'SK': sk}
            )
            return response.get('Item')
        except ClientError as e:
            logger.error("Failed to get item", pk=pk, sk=sk, error=str(e))
            return None
    
    def update_item(
        self,
        pk: str,
        sk: str,
        updates: Dict[str, Any],
        condition_expression: Optional[str] = None
    ) -> bool:
        """
        Update an item in DynamoDB.
        
        Args:
            pk: Partition key
            sk: Sort key
            updates: Dictionary of attributes to update
            condition_expression: Optional condition for update
            
        Returns:
            True if successful
        """
        try:
            # Build update expression
            update_expr_parts = []
            expr_attr_names = {}
            expr_attr_values = {}
            
            for idx, (key, value) in enumerate(updates.items()):
                attr_name = f"#attr{idx}"
                attr_value = f":val{idx}"
                update_expr_parts.append(f"{attr_name} = {attr_value}")
                expr_attr_names[attr_name] = key
                expr_attr_values[attr_value] = value
            
            update_expression = "SET " + ", ".join(update_expr_parts)
            
            update_kwargs = {
                'Key': {'PK': pk, 'SK': sk},
                'UpdateExpression': update_expression,
                'ExpressionAttributeNames': expr_attr_names,
                'ExpressionAttributeValues': expr_attr_values,
                'ReturnValues': 'UPDATED_NEW'
            }
            
            if condition_expression:
                update_kwargs['ConditionExpression'] = condition_expression
            
            self.table.update_item(**update_kwargs)
            logger.debug("Item updated successfully", pk=pk, sk=sk)
            return True
            
        except ClientError as e:
            logger.error("Failed to update item", pk=pk, sk=sk, error=str(e))
            raise
    
    def query(
        self,
        pk: str,
        sk_condition: Optional[str] = None,
        index_name: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query items from DynamoDB.
        
        Args:
            pk: Partition key value
            sk_condition: Optional sort key condition
            index_name: Optional GSI name
            limit: Optional result limit
            
        Returns:
            List of matching items
        """
        try:
            query_kwargs = {
                'KeyConditionExpression': boto3.dynamodb.conditions.Key('PK').eq(pk)
            }
            
            if index_name:
                query_kwargs['IndexName'] = index_name
            
            if limit:
                query_kwargs['Limit'] = limit
            
            response = self.table.query(**query_kwargs)
            return response.get('Items', [])
            
        except ClientError as e:
            logger.error("Failed to query items", pk=pk, error=str(e))
            return []
    
    def delete_item(self, pk: str, sk: str) -> bool:
        """
        Delete an item from DynamoDB.
        
        Args:
            pk: Partition key
            sk: Sort key
            
        Returns:
            True if successful
        """
        try:
            self.table.delete_item(Key={'PK': pk, 'SK': sk})
            logger.debug("Item deleted successfully", pk=pk, sk=sk)
            return True
        except ClientError as e:
            logger.error("Failed to delete item", pk=pk, sk=sk, error=str(e))
            raise


if IS_LOCAL:
    db_client = LocalDBWrapper()
else:
    db_client = DynamoDBClient()