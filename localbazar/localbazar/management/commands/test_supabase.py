"""
Django management command to test Supabase connection.
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from utils.supabase_client import get_supabase_client, test_supabase_connection


class Command(BaseCommand):
    help = 'Test Supabase database connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Testing Supabase Configuration...'))
        
        # Check environment variables
        self.stdout.write('\n1. Checking environment variables:')
        
        if settings.SUPABASE_URL:
            self.stdout.write(self.style.SUCCESS(f'   ✓ SUPABASE_URL: {settings.SUPABASE_URL}'))
        else:
            self.stdout.write(self.style.ERROR('   ✗ SUPABASE_URL: Not configured'))
        
        if settings.SUPABASE_KEY:
            masked_key = settings.SUPABASE_KEY[:10] + '...' + settings.SUPABASE_KEY[-10:]
            self.stdout.write(self.style.SUCCESS(f'   ✓ SUPABASE_KEY: {masked_key}'))
        else:
            self.stdout.write(self.style.ERROR('   ✗ SUPABASE_KEY: Not configured'))
        
        if settings.SUPABASE_SERVICE_ROLE_KEY:
            masked_service_key = settings.SUPABASE_SERVICE_ROLE_KEY[:10] + '...' + settings.SUPABASE_SERVICE_ROLE_KEY[-10:]
            self.stdout.write(self.style.SUCCESS(f'   ✓ SUPABASE_SERVICE_ROLE_KEY: {masked_service_key}'))
        else:
            self.stdout.write(self.style.WARNING('   ! SUPABASE_SERVICE_ROLE_KEY: Not configured (optional)'))
        
        # Check database configuration
        self.stdout.write('\n2. Checking database configuration:')
        db_config = settings.DATABASES['default']
        
        self.stdout.write(f'   Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'   Host: {db_config["HOST"]}')
        self.stdout.write(f'   Port: {db_config["PORT"]}')
        self.stdout.write(f'   Database: {db_config["NAME"]}')
        self.stdout.write(f'   User: {db_config["USER"]}')
        
        # Test Supabase client
        self.stdout.write('\n3. Testing Supabase client:')
        
        client = get_supabase_client()
        if client:
            self.stdout.write(self.style.SUCCESS('   ✓ Supabase client initialized'))
            
            # Test connection
            if test_supabase_connection():
                self.stdout.write(self.style.SUCCESS('   ✓ Supabase connection test passed'))
            else:
                self.stdout.write(self.style.ERROR('   ✗ Supabase connection test failed'))
        else:
            self.stdout.write(self.style.ERROR('   ✗ Failed to initialize Supabase client'))
        
        # Test Django database connection
        self.stdout.write('\n4. Testing Django database connection:')
        
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS('   ✓ Django database connection successful'))
                else:
                    self.stdout.write(self.style.ERROR('   ✗ Django database connection failed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Django database connection error: {e}'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.HTTP_INFO('Supabase configuration test completed!'))