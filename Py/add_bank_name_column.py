#!/usr/bin/env python3
"""
Migration script to add missing bank_name column to freelancers table
Run this once to fix the database schema
"""

import sqlite3

def add_missing_column():
    """Add bank_name column to freelancers table"""
    db_name = "financial_statement.db"
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(freelancers)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "bank_name" in columns:
            print("✅ bank_name column already exists!")
            return True
        
        print("Adding bank_name column...")
        
        # Add the missing column
        cursor.execute('''
            ALTER TABLE freelancers 
            ADD COLUMN bank_name TEXT
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Successfully added bank_name column!")
        print("\nUpdated schema:")
        
        # Show updated schema
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(freelancers)")
        columns = cursor.fetchall()
        
        print(f"\n{'Column Name':<20} {'Type':<15}")
        print("-" * 35)
        for col in columns:
            print(f"{col[1]:<20} {col[2]:<15}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("DATABASE MIGRATION: Add bank_name Column")
    print("=" * 50)
    print()
    
    success = add_missing_column()
    
    if success:
        print("\n✅ Migration complete!")
        print("   You can now use the get_all_freelancers endpoint")
    else:
        print("\n❌ Migration failed!")
