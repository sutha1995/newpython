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
            
            # Freelancers/Employees table with PIN and is_superuser
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS freelancers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    bank_name TEXT, 
                    bank_account TEXT,
                    epf_percentage REAL DEFAULT 8.0,
                    pin TEXT DEFAULT '0000',
                    is_superuser BOOLEAN DEFAULT 0,
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

    def add_freelancer(self, name, email, phone, bank_name, bank_account, epf_percentage=8.0, pin="0000", is_superuser=False):
        """Add a new freelancer to the database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO freelancers (name, email, phone, bank_name, bank_account, epf_percentage, pin, is_superuser) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, email, phone, bank_name, bank_account, epf_percentage, pin, is_superuser))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error adding freelancer: {e}")
            return None

    def verify_login(self, freelancer_id, pin):
        """Verify freelancer login with PIN"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, is_superuser, pin FROM freelancers WHERE id = ?', (freelancer_id,))
                result = cursor.fetchone()
                
                if result and result[3] == pin:  # result[3] is pin
                    return {
                        "freelancer_id": result[0],
                        "freelancer_name": result[1],
                        "is_superuser": bool(result[2])
                    }
                return None
        except Exception as e:
            print(f"Error verifying login: {e}")
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
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, email, phone, bank_name, bank_account, epf_percentage, is_superuser FROM freelancers')
                results = cursor.fetchall()
                
                return [
                    {
                        "id": r[0],
                        "name": r[1],
                        "email": r[2],
                        "phone": r[3],
                        "bank_name": r[4],
                        "bank_account": r[5],
                        "epf_percentage": r[6],
                        "is_superuser": bool(r[7])
                    }
                    for r in results
                ]
        except Exception as e:
            print(f"Error getting freelancers: {e}")
            return []

    def get_freelancer(self, freelancer_id):
        """Get a specific freelancer"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, name, email, phone, bank_name, bank_account, epf_percentage, is_superuser FROM freelancers WHERE id = ?', (freelancer_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "name": result[1],
                        "email": result[2],
                        "phone": result[3],
                        "bank_name": result[4],
                        "bank_account": result[5],
                        "epf_percentage": result[6],
                        "is_superuser": bool(result[7])
                    }
                return None
        except Exception as e:
            print(f"Error getting freelancer: {e}")
            return None

    def get_freelancer_projects(self, freelancer_id):
        """Get all projects for a specific freelancer"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, project_name, project_amount, epf_deduction, project_date, notes
                    FROM projects 
                    WHERE freelancer_id = ? 
                    ORDER BY project_date DESC
                ''', (freelancer_id,))
                results = cursor.fetchall()
                
                return [
                    {
                        "id": r[0],
                        "project_name": r[1],
                        "project_amount": r[2],
                        "epf_deduction": r[3],
                        "project_date": r[4],
                        "notes": r[5]
                    }
                    for r in results
                ]
        except Exception as e:
            print(f"Error getting projects: {e}")
            return []

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
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Get freelancer info
                cursor.execute('SELECT name FROM freelancers WHERE id = ?', (freelancer_id,))
                freelancer = cursor.fetchone()
                if not freelancer:
                    return None
                
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
                    'freelancer_name': freelancer[0],
                    'total_income': total_income,
                    'epf_deduction': total_epf,
                    'socso_deduction': socso,
                    'pcb_deduction': pcb,
                    'other_deduction': other,
                    'total_deductions': total_epf + socso + pcb + other,
                    'net_amount': total_income - (total_epf + socso + pcb + other)
                }
        except Exception as e:
            print(f"Error getting financial summary: {e}")
            return None

    def get_freelancer_financial_summary_range(self, freelancer_id, start_date, end_date):
        """Get financial summary for a freelancer for a date range"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Get freelancer info
                cursor.execute('SELECT name FROM freelancers WHERE id = ?', (freelancer_id,))
                freelancer = cursor.fetchone()
                if not freelancer:
                    return None
                
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
                    'freelancer_name': freelancer[0],
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
        except Exception as e:
            print(f"Error getting financial summary range: {e}")
            return None

    def delete_freelancer(self, freelancer_id):
        """Delete a freelancer and all related projects and deductions"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM projects WHERE freelancer_id = ?', (freelancer_id,))
                cursor.execute('DELETE FROM monthly_deductions WHERE freelancer_id = ?', (freelancer_id,))
                cursor.execute('DELETE FROM freelancers WHERE id = ?', (freelancer_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting freelancer: {e}")
            return False