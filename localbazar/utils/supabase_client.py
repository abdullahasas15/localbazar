"""
Supabase client utility for LocalBazar project.
This module provides a centralized way to interact with Supabase.
"""

from django.conf import settings
from supabase import create_client, Client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """
    Singleton class for Supabase client management.
    """
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'SupabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Supabase client."""
        try:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                logger.warning("Supabase URL or Key not configured")
                return
            
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self._client = None
    
    @property
    def client(self) -> Optional[Client]:
        """Get the Supabase client instance."""
        return self._client
    
    def is_connected(self) -> bool:
        """Check if Supabase client is properly initialized."""
        return self._client is not None
    
    def test_connection(self) -> bool:
        """Test the connection to Supabase."""
        if not self.is_connected():
            return False
        
        try:
            # Try to fetch from a system table to test connection
            response = self._client.table('information_schema.tables').select('table_name').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Supabase connection test failed: {e}")
            return False

# Global instance
supabase_client = SupabaseClient()

def get_supabase_client() -> Optional[Client]:
    """
    Get the Supabase client instance.
    
    Returns:
        Client: Supabase client instance or None if not configured
    """
    return supabase_client.client

def test_supabase_connection() -> bool:
    """
    Test the Supabase connection.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    return supabase_client.test_connection()