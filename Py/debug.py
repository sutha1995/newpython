import sqlite3

conn = sqlite3.connect('financial_statement.db')
cursor = conn.cursor()

# Remove the sample projects for freelancer 2
sample_projects = [
    "Website Redesign",
    "Mobile App Dev",
    "Logo Design",
]

print("=== REMOVING SAMPLE PROJECTS ===\n")

for project_name in sample_projects:
    cursor.execute('''
        DELETE FROM projects 
        WHERE freelancer_id = 2 AND project_name = ?
    ''', (project_name,))
    
    if cursor.rowcount > 0:
        print(f"✅ Deleted: {project_name}")
    else:
        print(f"⚠️  Not found: {project_name}")

conn.commit()

# Verify deletion
print("\n=== REMAINING PROJECTS FOR FREELANCER 2 ===\n")
cursor.execute('''
    SELECT id, project_name, project_amount, project_date 
    FROM projects 
    WHERE freelancer_id = 2
    ORDER BY project_date
''')

remaining = cursor.fetchall()
if remaining:
    for row in remaining:
        print(f"ID: {row[0]}, Name: {row[1]}, Amount: {row[2]}, Date: {row[3]}")
else:
    print("✅ No projects found for freelancer 2")

conn.close()
print("\n✅ Done! Sample projects removed.")
