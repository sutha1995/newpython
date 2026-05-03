import sqlite3
from datetime import datetime

class FinancialDatabaseManager:
    def __init__(self, db_name="financial_statement.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize database with tables for freelancer financial tracking"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Freelancers/Employees table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS freelancers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    bank_account TEXT,
                    epf_percentage REAL DEFAULT 8.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Projects table with EPF deduction
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    freelancer_id INTEGER NOT NULL,
                    project_name TEXT NOT NULL,
                    project_amount REAL NOT NULL,
                    epf_deduction REAL,
                    project_date DATE NOT NULL,
                    status TEXT DEFAULT 'completed',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (freelancer_id) REFERENCES freelancers (id)
                )
            ''')

            # Monthly deductions table (SOCSO, PCB)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_deductions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    freelancer_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    socso_deduction REAL DEFAULT 0.0,
                    pcb_deduction REAL DEFAULT 0.0,
                    other_deduction REAL DEFAULT 0.0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (freelancer_id) REFERENCES freelancers (id),
                    UNIQUE(freelancer_id, year, month)
                )
            ''')

            conn.commit()

    def add_freelancer(self, name, email, phone, bank_account, epf_percentage=8.0):
        """Add a new freelancer to the database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO freelancers (name, email, phone, bank_account, epf_percentage) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, email, phone, bank_account, epf_percentage))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error adding freelancer: {e}")
            return None

    def add_project(self, freelancer_id, project_name, project_amount, project_date, notes=""):
        """Add a project and auto-calculate EPF deduction based on freelancer's EPF percentage"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Get freelancer's EPF percentage
                cursor.execute('SELECT epf_percentage FROM freelancers WHERE id = ?', (freelancer_id,))
                result = cursor.fetchone()
                if not result:
                    print(f"Freelancer with ID {freelancer_id} not found")
                    return None
                
                epf_percentage = result[0]
                epf_deduction = (project_amount * epf_percentage) / 100
                
                cursor.execute('''
                    INSERT INTO projects 
                    (freelancer_id, project_name, project_amount, epf_deduction, project_date, notes) 
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (freelancer_id, project_name, project_amount, epf_deduction, project_date, notes))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding project: {e}")
            return None

    def add_monthly_deduction(self, freelancer_id, year, month, other=0.0, notes=""):
        """Add or update monthly SOCSO and PCB deductions (auto-calculated at 0.2% and 1%)"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Get total project income for the month
                cursor.execute('''
                    SELECT SUM(project_amount) FROM projects 
                    WHERE freelancer_id = ? AND strftime('%Y-%m', project_date) = ?
                ''', (freelancer_id, f"{year:04d}-{month:02d}"))
                income_data = cursor.fetchone()
                gross_income = income_data[0] or 0.0
                
                # Auto-calculate SOCSO (0.2%) and PCB (1%)
                socso_deduction = (gross_income * 0.2) / 100
                pcb_deduction = (gross_income * 1.0) / 100
                
                cursor.execute('''
                    INSERT OR REPLACE INTO monthly_deductions 
                    (freelancer_id, year, month, socso_deduction, pcb_deduction, other_deduction, notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (freelancer_id, year, month, socso_deduction, pcb_deduction, other, notes))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error adding monthly deduction: {e}")
            return None

    def get_all_freelancers(self):
        """Get all freelancers"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM freelancers')
            return cursor.fetchall()

    def get_freelancer_projects(self, freelancer_id):
        """Get all projects for a specific freelancer"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM projects 
                WHERE freelancer_id = ? 
                ORDER BY project_date DESC
            ''', (freelancer_id,))
            return cursor.fetchall()

    def get_monthly_deductions(self, freelancer_id, year, month):
        """Get monthly deductions for a specific month"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM monthly_deductions 
                WHERE freelancer_id = ? AND year = ? AND month = ?
            ''', (freelancer_id, year, month))
            return cursor.fetchone()

    def get_freelancer_financial_summary(self, freelancer_id, year, month):
        """Get financial summary for a freelancer for a specific month"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Get freelancer info
            cursor.execute('SELECT name, email FROM freelancers WHERE id = ?', (freelancer_id,))
            freelancer = cursor.fetchone()
            
            # Get total project income for the month
            cursor.execute('''
                SELECT SUM(project_amount), SUM(epf_deduction) FROM projects 
                WHERE freelancer_id = ? AND strftime('%Y-%m', project_date) = ?
            ''', (freelancer_id, f"{year:04d}-{month:02d}"))
            projects_data = cursor.fetchone()
            
            total_income = projects_data[0] or 0.0
            total_epf = projects_data[1] or 0.0
            
            # Auto-calculate SOCSO (0.2%) and PCB (1%)
            socso = (total_income * 0.2) / 100
            pcb = (total_income * 1.0) / 100
            
            # Get other deductions if stored
            cursor.execute('''
                SELECT other_deduction FROM monthly_deductions 
                WHERE freelancer_id = ? AND year = ? AND month = ?
            ''', (freelancer_id, year, month))
            deductions = cursor.fetchone()
            other = deductions[0] if deductions else 0.0
            
            return {
                'freelancer': freelancer,
                'total_income': total_income,
                'epf_deduction': total_epf,
                'socso_deduction': socso,
                'pcb_deduction': pcb,
                'other_deduction': other,
                'total_deductions': total_epf + socso + pcb + other,
                'net_amount': total_income - (total_epf + socso + pcb + other)
            }

    def get_freelancer_financial_summary_range(self, freelancer_id, start_date, end_date):
        """Get financial summary for a freelancer for a date range"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Get freelancer info
            cursor.execute('SELECT name, email FROM freelancers WHERE id = ?', (freelancer_id,))
            freelancer = cursor.fetchone()
            
            # Get total project income for the date range
            cursor.execute('''
                SELECT SUM(project_amount), SUM(epf_deduction) FROM projects 
                WHERE freelancer_id = ? AND project_date >= ? AND project_date <= ?
            ''', (freelancer_id, start_date, end_date))
            projects_data = cursor.fetchone()
            
            total_income = projects_data[0] or 0.0
            total_epf = projects_data[1] or 0.0
            
            # Auto-calculate SOCSO (0.2%) and PCB (1%)
            socso = (total_income * 0.2) / 100
            pcb = (total_income * 1.0) / 100
            
            # Get total other deductions for the date range
            cursor.execute('''
                SELECT SUM(other_deduction) FROM monthly_deductions 
                WHERE freelancer_id = ? AND 
                strftime('%Y-%m-%d', (year || '-' || printf('%02d', month) || '-01')) >= ?
                AND strftime('%Y-%m-%d', (year || '-' || printf('%02d', month) || '-01')) <= ?
            ''', (freelancer_id, start_date, end_date))
            other_data = cursor.fetchone()
            other = other_data[0] or 0.0
            
            return {
                'freelancer': freelancer,
                'start_date': start_date,
                'end_date': end_date,
                'total_income': total_income,
                'epf_deduction': total_epf,
                'socso_deduction': socso,
                'pcb_deduction': pcb,
                'other_deduction': other,
                'total_deductions': total_epf + socso + pcb + other,
                'net_amount': total_income - (total_epf + socso + pcb + other)
            }

    def delete_freelancer(self, freelancer_id):
        """Delete a freelancer and all related projects and deductions"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM projects WHERE freelancer_id = ?', (freelancer_id,))
            cursor.execute('DELETE FROM monthly_deductions WHERE freelancer_id = ?', (freelancer_id,))
            cursor.execute('DELETE FROM freelancers WHERE id = ?', (freelancer_id,))
            conn.commit()
            return cursor.rowcount > 0

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("     FREELANCER FINANCIAL STATEMENT MANAGER")
    print("="*50)
    print("1. Add New Freelancer")
    print("2. View All Freelancers")
    print("3. Add Project")
    print("4. View Freelancer Projects")
    print("5. Register Monthly Deductions (SOCSO 0.2%, PCB 1% auto-calculated)")
    print("6. View Financial Summary (by Month)")
    print("7. View Financial Summary (by Date Range)")
    print("8. Delete Freelancer")
    print("9. Exit")
    print("-"*50)

def main():
    """Main interactive CLI function"""
    db = FinancialDatabaseManager()

    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()

        if choice == '1':
            print("\n---Add New Freelancer---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            phone = input("Enter phone: ").strip()
            bank_account = input("Enter bank account: ").strip()
            try:
                epf = float(input("Enter EPF percentage (default 8.0): ").strip() or "8.0")
                freelancer_id = db.add_freelancer(name, email, phone, bank_account, epf)
                if freelancer_id:
                    print(f"✓ Freelancer added successfully! ID: {freelancer_id}")
                else:
                    print("✗ Failed to add freelancer")
            except ValueError:
                print("✗ Invalid EPF percentage. Please enter a number.")
        
        elif choice == '2':
            print("\n---All Freelancers---")
            freelancers = db.get_all_freelancers()
            if freelancers:
                for freelancer in freelancers:
                    print(f"ID: {freelancer[0]} | Name: {freelancer[1]} | Email: {freelancer[2]}")
            else:
                print("No freelancers found.")
        
        elif choice == '3':
            print("\n--- Add Project ---")
            try:
                freelancer_id = int(input("Enter freelancer ID: ").strip())
                project_name = input("Enter project name: ").strip()
                project_amount = float(input("Enter project amount: ").strip())
                project_date = input("Enter project date (YYYY-MM-DD): ").strip()
                notes = input("Enter notes (optional): ").strip()
                project_id = db.add_project(freelancer_id, project_name, project_amount, project_date, notes)
                if project_id:
                    print(f"✓ Project added successfully! ID: {project_id}")
                else:
                    print("✗ Failed to add project")  
            except ValueError:
                print("✗ Invalid input. Please check your entries.")
        
        elif choice == '4':
            print("\n--- View Freelancer Projects ---")
            try:
                freelancer_id = int(input("Enter freelancer ID: ").strip())
                projects = db.get_freelancer_projects(freelancer_id)
                if projects:
                    for project in projects:
                        print(f"\nProject ID: {project[0]}")
                        print(f"Name: {project[2]}")
                        print(f"Amount (RM): RM {project[3]:.2f}")
                        print(f"EPF Deduction (RM): RM {project[4]:.2f}")
                        print(f"Date: {project[5]}")
                        print("-"*30)
                else:
                    print("No projects found for this freelancer.")
            except ValueError:
                print("✗ Invalid freelancer ID. Please enter a number.")
        
        elif choice == '5':
            print("\n--- Register Monthly Other Deductions ---")
            print("NOTE: SOCSO (0.2%) and PCB (1%) are auto-calculated based on monthly income")
            try:
                freelancer_id = int(input("Enter freelancer ID: ").strip())
                year = int(input("Enter year: ").strip())
                month = int(input("Enter month (1-12): ").strip())
                other = float(input("Enter other deductions (optional) (RM): ").strip() or "0")
                notes = input("Enter notes (optional): ").strip()
                deduction_id = db.add_monthly_deduction(freelancer_id, year, month, other, notes)
                if deduction_id:
                    print(f"✓ Monthly deductions registered successfully! ID: {deduction_id}")
                    print(f"  SOCSO (0.2%) and PCB (1%) will be calculated based on monthly income")
                else:
                    print("✗ Failed to register deductions")
            except ValueError:
                print("✗ Invalid input. Please check your entries.")
        
        elif choice == '6':
            print("\n--- Financial Summary (by Month) ---")
            try:
                freelancer_id = int(input("Enter freelancer ID: ").strip())
                year = int(input("Enter year: ").strip())
                month = int(input("Enter month (1-12): ").strip())
                summary = db.get_freelancer_financial_summary(freelancer_id, year, month)
                if summary['freelancer']:
                    print(f"\nFreelancer: {summary['freelancer'][0]}")
                    print(f"Period: {year}-{month:02d}")
                    print("-"*40)
                    print(f"Total Income: RM {summary['total_income']:.2f}")
                    print(f"EPF Deduction (auto): RM {summary['epf_deduction']:.2f}")
                    print(f"SOCSO Deduction (0.2%): RM {summary['socso_deduction']:.2f}")
                    print(f"PCB Deduction (1.0%): RM {summary['pcb_deduction']:.2f}")
                    print(f"Other Deduction: RM {summary['other_deduction']:.2f}")
                    print("-"*40)
                    print(f"Total Deductions: RM {summary['total_deductions']:.2f}")
                    print(f"Net Amount: RM {summary['net_amount']:.2f}")
                else:
                    print("Freelancer not found.")
            except ValueError:
                print("✗ Invalid input. Please check your entries.")
        
        elif choice == '7':
            print("\n--- Financial Summary (by Date Range) ---")
            try:
                freelancer_id = int(input("Enter freelancer ID: ").strip())
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                summary = db.get_freelancer_financial_summary_range(freelancer_id, start_date, end_date)
                if summary['freelancer']:
                    print(f"\nFreelancer: {summary['freelancer'][0]}")
                    print(f"Period: {summary['start_date']} to {summary['end_date']}")
                    print("-"*40)
                    print(f"Total Income: RM {summary['total_income']:.2f}")
                    print(f"EPF Deduction (auto): RM {summary['epf_deduction']:.2f}")
                    print(f"SOCSO Deduction (0.2%): RM {summary['socso_deduction']:.2f}")
                    print(f"PCB Deduction (1.0%): RM {summary['pcb_deduction']:.2f}")
                    print(f"Other Deduction: RM {summary['other_deduction']:.2f}")
                    print("-"*40)
                    print(f"Total Deductions: RM {summary['total_deductions']:.2f}")
                    print(f"Net Amount: RM {summary['net_amount']:.2f}")
                else:
                    print("Freelancer not found.")
            except ValueError:
                print("✗ Invalid input. Please check your entries.")
        
        elif choice == '8':
            print("\n--- Delete Freelancer ---")
            try:
                freelancer_id = int(input("Enter freelancer ID to delete: ").strip())
                confirm = input(f"Are you sure you want to delete freelancer {freelancer_id}? (y/N): ").strip().lower()
                if confirm == 'y':
                    if db.delete_freelancer(freelancer_id):
                        print("✓ Freelancer deleted successfully!")
                    else:
                        print("✗ Freelancer not found or deletion failed")
                else:
                    print("Deletion cancelled")
            except ValueError:
                print("✗ Invalid Freelancer ID. Please enter a number")
        
        elif choice == '9':
            print("\nGoodbye!")
            break
        
        else:
            print("✗ Invalid choice. Please enter 1-9.")

        input("\nPress Enter to continue")

if __name__ == "__main__":
    main()