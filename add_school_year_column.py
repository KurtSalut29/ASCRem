#!/usr/bin/env python
"""
Quick script to add school_year column to myproject_setting table
Run this from the ASCREM directory: python add_school_year_column.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASCREM.settings')
django.setup()

from django.db import connection

def add_school_year_column():
    with connection.cursor() as cursor:
        try:
            # Check if column exists
            cursor.execute("SHOW COLUMNS FROM myproject_setting LIKE 'school_year'")
            if cursor.fetchone():
                print("✅ school_year column already exists!")
                return
            
            # Add the column
            cursor.execute("""
                ALTER TABLE myproject_setting 
                ADD COLUMN school_year VARCHAR(20) DEFAULT '25-1'
            """)
            
            print("✅ Successfully added school_year column to myproject_setting table!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_school_year_column()