#!/usr/bin/env python3
"""
Script to make a freelancer a superuser
Run this on your machine where you have write access to the database
"""

import sqlite3
import sys

def make_superuser(db_name="financial_statement.db", freelancer_id=2):
    """Make a freelancer a superuser"""
    try:
        # Connect to database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Check if freelancer exists
        cursor.execute("SELECT id, name, is_superuser FROM freelancers WHERE id = ?", (freelancer_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Error: Freelancer with ID {freelancer_id} not found")
            return False
        
        # Update to superuser
        cursor.execute("UPDATE freelancers SET is_superuser = 1 WHERE id = ?", (freelancer_id,))
        conn.commit()
        
        # Verify the change
        cursor.execute("SELECT id, name, is_superuser FROM freelancers WHERE id = ?", (freelancer_id,))
        updated = cursor.fetchone()
        
        conn.close()
        
        if updated[2]:  # is_superuser = 1 (True)
            print(f"✅ Successfully updated!")
            print(f"   ID: {updated[0]}")
            print(f"   Name: {updated[1]}")
            print(f"   Superuser: Yes")
            return True
        else:
            print(f"❌ Update failed - is_superuser still 0")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    # You can change these values if needed
    db_path = "financial_statement.db"  # Path to your database
    freelancer_id = 2  # Make ID 2 superuser
    
    print("=" * 50)
    print("MAKE FREELANCER SUPERUSER")
    print("=" * 50)
    print(f"\nDatabase: {db_path}")
    print(f"Freelancer ID: {freelancer_id}\n")
    
    success = make_superuser(db_path, freelancer_id)
    
    if success:
        print("\n✅ Done! Freelancer ID 2 is now a superuser.")
    else:
        print("\n❌ Failed to update superuser status.")
        sys.exit(1)
