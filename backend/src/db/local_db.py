"""
In-memory database for local testing.
Replaces DynamoDB when testing locally.
"""
from typing import Dict, List, Optional, Any
from datetime import datetime


class LocalDatabase:
    """Simple in-memory database for local testing."""
    
    def __init__(self):
        self.data = {}
        print("[LocalDB] ✅ Initialized in-memory database")
    
    def put_item(self, item: Dict[str, Any]) -> bool:
        """Store an item."""
        key = f"{item['PK']}#{item['SK']}"
        self.data[key] = item
        print(f"[LocalDB] 💾 Stored: {key}")
        return True
    
    def get_item(self, pk: str, sk: str) -> Optional[Dict[str, Any]]:
        """Get an item."""
        key = f"{pk}#{sk}"
        item = self.data.get(key)
        print(f"[LocalDB] 🔍 Retrieved: {key} - {'✅ Found' if item else '❌ Not found'}")
        return item
    
    def update_item(self, pk, sk, updates, condition_expression=None):
        key = f"{pk}#{sk}"
        if key not in self.data:
            self.data[key] = {"PK": pk, "SK": sk}
        self.data[key].update(updates)
        print(f"[LocalDB] ✏️ Updated: {key}")
        return True

    
    def query(self, pk: str, sk_condition: Optional[str] = None,
              index_name: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Query items."""
        results = [item for key, item in self.data.items() if item.get('PK') == pk]
        if limit:
            results = results[:limit]
        print(f"[LocalDB] 🔎 Query: {pk} - Found {len(results)} items")
        return results
    
    def delete_item(self, pk: str, sk: str) -> bool:
        """Delete an item."""
        key = f"{pk}#{sk}"
        if key in self.data:
            del self.data[key]
            print(f"[LocalDB] 🗑️  Deleted: {key}")
            return True
        return False


# Global instance
local_db = LocalDatabase()