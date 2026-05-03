import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import json

# Page configuration
st.set_page_config(
    page_title="Freelancer Financial Statement",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user_id = None
    st.session_state.current_user_name = None
    st.session_state.is_superuser = False

# Helper function to make API calls
def api_call(method, endpoint, data=None, params=None, headers=None):
    """Make API call with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        
        if method == "GET":
            response = requests.get(url, params=params, headers=default_headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=default_headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=default_headers)
        else:
            return None, "Invalid method"
        
        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except:
                error_detail = response.text
            return None, error_detail
    except Exception as e:
        return None, str(e)

# ==================== LOGIN PAGE ====================
if not st.session_state.logged_in:
    st.title("💰 Freelancer Financial Statement Manager")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            freelancer_id = st.number_input(
                "Freelancer ID",
                min_value=1,
                step=1,
                help="Enter your freelancer ID"
            )
            
            pin = st.text_input(
                "PIN",
                type="password",
                help="Enter your 4-digit PIN"
            )
            
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not pin or len(pin) == 0:
                    st.error("❌ Please enter your PIN")
                else:
                    # Call login endpoint
                    payload = {
                        "freelancer_id": int(freelancer_id),
                        "pin": pin
                    }
                    
                    result, error = api_call("POST", "/login/", data=payload)
                    
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.current_user_id = result.get("freelancer_id")
                        st.session_state.current_user_name = result.get("freelancer_name")
                        st.session_state.is_superuser = result.get("is_superuser", False)
                        st.success("✓ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {error}")
        
    st.info("""
    📝 **Demo Login Credentials:**
    - **Superuser:** ID: 2, PIN: 0000
    - **Regular User:** ID: 3 or 4, PIN: 0000
    """)
else:
    # ==================== MAIN APP ====================

    st.title("💰 Freelancer Financial Statement Manager")
    st.markdown("---")

        # User info in sidebar
    st.sidebar.info(f"""
    👤 **Logged in as:**
    - {st.session_state.current_user_name} (ID: {st.session_state.current_user_id})
    - Role: {'🔑 Superuser' if st.session_state.is_superuser else 'Regular User'}
    """)
    
    # Logout button
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user_id = None
        st.session_state.current_user_name = None
        st.session_state.is_superuser = False
        st.rerun()
    
    st.sidebar.markdown("---")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Dashboard", "Freelancers", "Projects", "Deductions", "Financial Summary"]
    )

    # Helper function to make API calls
    def api_call(method, endpoint, data=None, params=None):
        """Make API call with error handling"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            headers = {"Content-Type": "application/json"}
            
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                return None, "Invalid method"
            
            if response.status_code in [200, 201]:
                return response.json(), None
            else:
                return None, response.json().get("detail", "Unknown error")
        except Exception as e:
            return None, str(e)

    # ==================== DASHBOARD PAGE ====================
    if page == "Dashboard":
        st.header("📊 Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        # Get total freelancers (only superuser can see this)
        freelancers_data, error = api_call("GET", "/freelancers/")
        if freelancers_data:
            with col1:
                if st.session_state.is_superuser:
                    st.metric("Total Freelancers", len(freelancers_data))
                else:
                    st.metric("Your ID", st.session_state.current_user_id)
        
        st.subheader("Quick Start")
        st.info(f"""
        Welcome, {st.session_state.current_user_name}!
        
        **Your Access Level:** {'🔑 Superuser - View all earnings' if st.session_state.is_superuser else '👤 Regular User - View your earnings only'}
        
        **How to use:**
        1. **Freelancers** - View freelancer profiles
        2. **Projects** - Record and view projects
        3. **Deductions** - Register monthly deductions
        4. **Financial Summary** - View financial statements
        """)
        
        st.subheader("API Status")
        status, error = api_call("GET", "/")
        if status:
            st.success("✓ API is connected and running")
            st.write(f"API Version: {status.get('version', 'N/A')}")
        else:
            st.error("✗ Cannot connect to API. Make sure FastAPI is running on http://localhost:8000")

    # ==================== FREELANCERS PAGE ====================
    elif page == "Freelancers":
        st.header("👥 Freelancer Management")
        
        tab1, tab2 = st.tabs(["Add Freelancer", "View Freelancers"])
        
        # Add Freelancer
        # Add this list at the top of your file with other configuration
        MALAYSIAN_BANKS = [
            "Maybank",
            "Public Bank",
            "CIMB Bank",
            "Ambank",
            "Bank Rakyat",
            "Bank Simpanan Nasional",
            "Hong Leong Bank",
            "OCBC Bank",
            "RHB Bank",
            "Bank Islam",
            "Bank Muamalat",
            "Bank Kerjasama Rakyat",
            "Bank Pembangunan",
            "Affin Bank",
            "BMCE Bank",
            "ICBC Bank",
            "Standard Chartered",
            "HSBC Bank",
            "Citibank",
            "Bank of China",
            "MUFG Bank",
            "Mizuho Bank",
            "Barclays Bank",
            "Deutsche Bank",
            "Bank of Tokyo",
            "Bank Rakyat Indonesia",
        ]
        with tab1:
            st.subheader("Add New Freelancer")
            st.warning("⚠️ Only superusers can add new freelancers")
            
            if st.session_state.is_superuser:
                with st.form("freelancer_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        name = st.text_input("Name")
                        email = st.text_input("Email")
                        phone = st.text_input("Phone")
                        pin = st.text_input("PIN (4 digits)", type="password")
                
                    with col2:
                        bank_name = st.selectbox("Bank Name", MALAYSIAN_BANKS)
                        bank_account = st.text_input("Bank Account Number")
                        epf_percentage = st.number_input("EPF Percentage (%)", min_value=0.0, max_value=100.0, value=8.0, step=0.1)
                        is_superuser = st.checkbox("Is Superuser?")
                        
                        submit = st.form_submit_button("Add Freelancer", use_container_width=True)
                    
                    if submit:
                        if not all([name, email, phone, bank_account, pin]):
                            st.error("Please fill in all required fields")
                        elif len(pin) != 4 or not pin.isdigit():
                            st.error("PIN must be exactly 4 digits")
                        else:
                            payload = {
                                "name": name,
                                "email": email,
                                "phone": phone,
                                "bank_name": bank_name,
                                "bank_account": bank_account,
                                "epf_percentage": epf_percentage,
                                "pin": pin,
                                "is_superuser": is_superuser
                            }
                            result, error = api_call("POST", "/freelancers/", data=payload)
                            if result:
                                st.success(f"✓ Freelancer added successfully! ID: {result.get('freelancer_id')}")
                            else:
                                st.error(f"✗ Error: {error}")
            else:
                st.info("You don't have permission to add freelancers. Contact a superuser.")
       
        # View Freelancers
        with tab2:
            st.subheader("All Freelancers")
            
            if st.session_state.is_superuser:
                st.info("Superuser: You can view all freelancers")
                freelancers, error = api_call("GET", "/freelancers/")
            else:
                st.info("Regular User: You can only view your own profile")
                freelancers, error = api_call("GET", f"/freelancers/{st.session_state.current_user_id}")
                freelancers = [freelancers] if freelancers and not isinstance(freelancers, list) else freelancers
            
            if freelancers:
                if len(freelancers) > 0:
                    df = pd.DataFrame(freelancers)
                    # Hide PIN column for security
                    display_columns = [col for col in df.columns if col.lower() != 'pin']
                    st.dataframe(df[display_columns], use_container_width=True)
                else:
                    st.info("No freelancers found")
            else:
                st.error(f"Error: {error}")

    # ==================== PROJECTS PAGE ====================
    elif page == "Projects":
        st.header("📁 Project Management")
        
        tab1, tab2 = st.tabs(["Add Project", "View Projects"])
        
        # Add Project
        with tab1:
            st.subheader("Add New Project")
            
            freelancers, _ = api_call("GET", "/freelancers/")
            freelancer_options = {}
            if freelancers:
                if st.session_state.is_superuser:
                    freelancer_options = {f"{g['id']}: {g['name']}": g['id'] for g in freelancers}
                else:
                    # Regular users can only add projects for themselves
                    user_freelancer = next((g for g in freelancers if g['id'] == st.session_state.current_user_id), None)
                    if user_freelancer:
                        freelancer_options = {f"{user_freelancer['id']}: {user_freelancer['name']}": user_freelancer['id']}
            
            if not freelancer_options:
                st.warning("No freelancers found.")
            else:
                with st.form("project_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        freelancer_select = st.selectbox("Select Freelancer", list(freelancer_options.keys()))
                        project_name = st.text_input("Project Name")
                        project_amount = st.number_input("Project Amount (RM)", min_value=0.0, step=0.01)
                    
                    with col2:
                        project_date = st.date_input("Project Date")
                        notes = st.text_area("Notes (optional)", height=100)
                    
                    submit = st.form_submit_button("Add Project", use_container_width=True)
                    
                    if submit:
                        if not project_name or project_amount <= 0:
                            st.error("Please fill in all required fields with valid values")
                        else:
                            freelancer_id = freelancer_options[freelancer_select]
                            payload = {
                                "freelancer_id": freelancer_id,
                                "project_name": project_name,
                                "project_amount": project_amount,
                                "project_date": str(project_date),
                                "notes": notes
                            }
                            result, error = api_call("POST", "/projects/", data=payload)
                            if result:
                                st.success(f"✓ Project added successfully! ID: {result.get('project_id')}")
                            else:
                                st.error(f"✗ Error: {error}")
       
        # View Projects
        with tab2:
            st.subheader("View Freelancer Projects")
            
            freelancers, _ = api_call("GET", "/freelancers/")
            if freelancers:
                if st.session_state.is_superuser:
                    freelancer_options = {f"{g['id']}: {g['name']}": g['id'] for g in freelancers}
                    selected_freelancer = st.selectbox("Select Freelancer to View Projects", list(freelancer_options.keys()), key="view_projects")
                    freelancer_id = freelancer_options[selected_freelancer]
                else:
                    freelancer_id = st.session_state.current_user_id
                    st.info(f"Viewing projects for: {st.session_state.current_user_name}")
                
                projects, error = api_call("GET", f"/freelancers/{freelancer_id}/projects/")
                if projects:
                    if len(projects) > 0:
                        df = pd.DataFrame(projects)
                        st.dataframe(df, use_container_width=True)
                        
                        st.subheader("Summary")
                        total_income = sum(float(p['project_amount']) for p in projects)
                        total_epf = sum(float(p['epf_deduction']) for p in projects)
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Projects", len(projects))
                        col2.metric("Total Income", f"RM {total_income:,.2f}")
                        col3.metric("Total EPF Deduction", f"RM {total_epf:,.2f}")
                    else:
                        st.info("No projects found")
                else:
                    st.error(f"Error: {error}")
            else:
                st.warning("No freelancers found")

    # ==================== DEDUCTIONS PAGE ====================
    elif page == "Deductions":
        st.header("📝 Monthly Deductions")
        
        st.info("ℹ️ SOCSO (0.2%) and PCB (1.0%) are automatically calculated based on your monthly income.")
        
        st.subheader("Register Monthly Deductions")
        
        freelancers, _ = api_call("GET", "/freelancers/")
        if not freelancers:
            st.warning("No freelancers found.")
        else:
            if st.session_state.is_superuser:
                freelancer_options = {f"{g['id']}: {g['name']}": g['id'] for g in freelancers}
            else:
                user_freelancer = next((g for g in freelancers if g['id'] == st.session_state.current_user_id), None)
                freelancer_options = {f"{user_freelancer['id']}: {user_freelancer['name']}": user_freelancer['id']} if user_freelancer else {}
            
            if not freelancer_options:
                st.warning("No accessible freelancers found.")
            else:
                with st.form("deduction_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        freelancer_select = st.selectbox("Select Freelancer", list(freelancer_options.keys()), key="deduction_freelancer")
                        year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year)
                    
                    with col2:
                        month = st.selectbox("Month", [("January", 1), ("February", 2), ("March", 3), ("April", 4), 
                                                       ("May", 5), ("June", 6), ("July", 7), ("August", 8),
                                                       ("September", 9), ("October", 10), ("November", 11), ("December", 12)],
                                            format_func=lambda x: x[0], index=datetime.now().month - 1)
                        other_deduction = st.number_input("Other Deductions (RM)", min_value=0.0, step=0.01)
                    
                    notes = st.text_area("Notes (optional)", height=80)
                    
                    submit = st.form_submit_button("Register Deductions", use_container_width=True)
                    
                    if submit:
                        freelancer_id = freelancer_options[freelancer_select]
                        month_num = month[1]
                        payload = {
                            "freelancer_id": freelancer_id,
                            "year": year,
                            "month": month_num,
                            "other_deduction": other_deduction,
                            "notes": notes
                        }
                        result, error = api_call("POST", "/deductions/", data=payload)
                        if result:
                            st.success(f"✓ Deductions registered successfully! ID: {result.get('deduction_id')}")
                        else:
                            st.error(f"✗ Error: {error}")

    # ==================== FINANCIAL SUMMARY PAGE ====================
    elif page == "Financial Summary":
        st.header("📈 Financial Summary")
        
        tab1, tab2, tab3 = st.tabs(["Summary by Month", "Summary by Date Range", "Download Statement"])
        
        # Summary by Month
        with tab1:
            st.subheader("Financial Summary by Month")
            
            freelancers, _ = api_call("GET", "/freelancers/")
            if not freelancers:
                st.warning("No freelancers found")
            else:
                if st.session_state.is_superuser:
                    freelancer_options = {f"{g['id']}: {g['name']}": g['id'] for g in freelancers}
                else:
                    user_freelancer = next((g for g in freelancers if g['id'] == st.session_state.current_user_id), None)
                    freelancer_options = {f"{user_freelancer['id']}: {user_freelancer['name']}": user_freelancer['id']} if user_freelancer else {}
                
                if not freelancer_options:
                    st.warning("No accessible freelancers found")
                else:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        freelancer_select = st.selectbox("Select Freelancer", list(freelancer_options.keys()), key="summary_month_freelancer")
                    
                    with col2:
                        year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year, key="summary_month_year")
                    
                    with col3:
                        month = st.selectbox("Month", [("January", 1), ("February", 2), ("March", 3), ("April", 4), 
                                                       ("May", 5), ("June", 6), ("July", 7), ("August", 8),
                                                       ("September", 9), ("October", 10), ("November", 11), ("December", 12)],
                                            format_func=lambda x: x[0], index=datetime.now().month - 1, key="summary_month_select")
                    
                    if st.button("Generate Summary", key="btn_summary_month"):
                        freelancer_id = freelancer_options[freelancer_select]
                        month_num = month[1]
                        
                        summary, error = api_call("GET", f"/freelancers/{freelancer_id}/summary/{year}/{month_num}")
                        
                        if summary:
                            freelancer_name = summary.get("freelancer_name", "N/A")
                            
                            st.subheader(f"Summary for {freelancer_name} - {month[0]} {year}")
                            st.markdown("---")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Total Income", f"RM {summary.get('total_income', 0):,.2f}")
                            with col2:
                                st.metric("EPF Deduction", f"RM {summary.get('epf_deduction', 0):,.2f}")
                            with col3:
                                st.metric("SOCSO (0.2%)", f"RM {summary.get('socso_deduction', 0):,.2f}")
                            with col4:
                                st.metric("PCB (1.0%)", f"RM {summary.get('pcb_deduction', 0):,.2f}")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Other Deduction", f"RM {summary.get('other_deduction', 0):,.2f}")
                            with col2:
                                st.metric("Total Deductions", f"RM {summary.get('total_deductions', 0):,.2f}", delta=f"{(summary.get('total_deductions', 0) / summary.get('total_income', 1) * 100):.1f}%")
                            with col3:
                                st.metric("Net Amount", f"RM {summary.get('net_amount', 0):,.2f}", delta="Take Home", delta_color="off")
                        
                            # Display breakdown
                            st.subheader("Deduction Breakdown")
                            breakdown_data = {
                                "Deduction Type": ["EPF Deduction", "SOCSO (0.2%)", "PCB (1.0%)", "Other Deductions"],
                                "Amount (RM)": [
                                    summary.get('epf_deduction', 0),
                                    summary.get('socso_deduction', 0),
                                    summary.get('pcb_deduction', 0),
                                    summary.get('other_deduction', 0)
                                ]
                            }
                            breakdown_df = pd.DataFrame(breakdown_data)
                            st.bar_chart(breakdown_df.set_index("Deduction Type"))
                            
                        else:
                            st.error(f"✗ Error: {error}")
         
        # Summary by Date Range
        with tab2:
            st.subheader("Date Range Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input("Start Date", value=date(datetime.now().year, 1, 1), key="summary_start_date")
            with col2:
                end_date = st.date_input("End Date", value=date.today(), key="summary_end_date")
            
            if st.button("Get Summary", key="get_range_summary_btn"):
                # Validate dates
                if start_date > end_date:
                    st.error("❌ Start date must be before end date")
                else:
                    st.info(f"📅 Fetching data from {start_date} to {end_date}...")
                    
                    # Call API with proper error handling
                    summary, error = api_call(
                        "GET",
                        f"/freelancers/{st.session_state.current_user_id}/summary-range",
                        params={"start_date": str(start_date), "end_date": str(end_date)}
                    )
                    
                    if summary:
                        st.success("✓ Summary retrieved")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Income", f"RM {summary.get('total_income', 0):,.2f}")
                        with col2:
                            st.metric("Total Deductions", f"RM {summary.get('total_deductions', 0):,.2f}")
                        with col3:
                            st.metric("Net Amount", f"RM {summary.get('net_amount', 0):,.2f}")
                        with col4:
                            st.metric("EPF", f"RM {summary.get('epf_deduction', 0):,.2f}")
                        
                        st.markdown("---")
                        
                        breakdown_data = {
                            "Deduction Type": ["EPF", "SOCSO", "PCB", "Other"],
                            "Amount": [
                                summary.get('epf_deduction', 0),
                                summary.get('socso_deduction', 0),
                                summary.get('pcb_deduction', 0),
                                summary.get('other_deduction', 0)
                            ]
                        }
                        breakdown_df = pd.DataFrame(breakdown_data)
                        st.bar_chart(breakdown_df.set_index("Deduction Type"))
                    else:
                        st.error(f"✗ Error: {error}")
                        
                        # Helpful debug info
                        with st.expander("🔍 Debug Information"):
                            st.write(f"**Freelancer ID:** {st.session_state.current_user_id}")
                            st.write(f"**Date Range:** {start_date} to {end_date}")
                            st.write(f"**API Endpoint:** /freelancers/{st.session_state.current_user_id}/summary-range")
                            st.write("**Try:**")
                            st.code(f"curl 'http://127.0.0.1:8000/freelancers/{st.session_state.current_user_id}/summary-range?start_date={start_date}&end_date={end_date}'", language="bash")

        # Download Statement
        with tab3:
            st.subheader("📥 Download Financial Statement")
            st.info("Choose your preferred format and time period to download your financial statement.")
            
            freelancers, _ = api_call("GET", "/freelancers/")
            if not freelancers:
                st.warning("No freelancers found")
            else:
                if st.session_state.is_superuser:
                    freelancer_options = {f"{g['id']}: {g['name']}": g['id'] for g in freelancers}
                else:
                    user_freelancer = next((g for g in freelancers if g['id'] == st.session_state.current_user_id), None)
                    freelancer_options = {f"{user_freelancer['id']}: {user_freelancer['name']}": user_freelancer['id']} if user_freelancer else {}
                
                if not freelancer_options:
                    st.warning("No accessible freelancers found")
                else:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        freelancer_select = st.selectbox("Select Freelancer", list(freelancer_options.keys()), key="download_freelancer")
                        file_format = st.radio("File Format", ["CSV", "Excel", "PDF"], horizontal=True)
                    
                    with col2:
                        report_type = st.radio("Time Period", ["Month", "Year", "Date Range"], horizontal=True)
                    
                    st.markdown("---")
                    st.subheader("Period Selection")
                    
                    # Period selection based on report type
                    if report_type == "Month":
                        col1, col2 = st.columns(2)
                        with col1:
                            year_select = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year, key="download_year_month")
                        with col2:
                            month_select = st.selectbox("Month", [("January", 1), ("February", 2), ("March", 3), ("April", 4), 
                                                                   ("May", 5), ("June", 6), ("July", 7), ("August", 8),
                                                                   ("September", 9), ("October", 10), ("November", 11), ("December", 12)],
                                                        format_func=lambda x: x[0], index=datetime.now().month - 1, key="download_month_select")
                    
                    elif report_type == "Year":
                        year_select = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.now().year, key="download_year_only")
                        month_select = None
                    
                    else:  # Date Range
                        col1, col2 = st.columns(2)
                        with col1:
                            start_date_select = st.date_input("Start Date", value=date(datetime.now().year, 1, 1), key="download_start_date")
                        with col2:
                            end_date_select = st.date_input("End Date", value=date.today(), key="download_end_date")
                    
                    st.markdown("---")
                    st.subheader("Select Fields to Include")
                    
                    # Field selection
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        include_freelancer = st.checkbox("Freelancer Name", value=True)
                        include_income = st.checkbox("Total Income", value=True)
                        include_epf = st.checkbox("EPF Deduction", value=True)
                        include_socso = st.checkbox("SOCSO (0.2%)", value=True)
                    
                    with col2:
                        include_pcb = st.checkbox("PCB (1.0%)", value=True)
                        include_other = st.checkbox("Other Deductions", value=True)
                        include_total_ded = st.checkbox("Total Deductions", value=True)
                        include_net = st.checkbox("Net Amount", value=True)
                    
                    # Build fields list
                    selected_fields = []
                    if include_freelancer:
                        selected_fields.append("freelancer_name")
                    if include_income:
                        selected_fields.append("total_income")
                    if include_epf:
                        selected_fields.append("epf_deduction")
                    if include_socso:
                        selected_fields.append("socso_deduction")
                    if include_pcb:
                        selected_fields.append("pcb_deduction")
                    if include_other:
                        selected_fields.append("other_deduction")
                    if include_total_ded:
                        selected_fields.append("total_deductions")
                    if include_net:
                        selected_fields.append("net_amount")
                    
                    if not selected_fields:
                        st.warning("Please select at least one field to include")
                    
                    # Download button
                    if st.button("📥 Download Statement", use_container_width=True, key="download_btn"):
                        freelancer_id = freelancer_options[freelancer_select]
                        format_lower = file_format.lower()
                        file_ext = format_lower if format_lower == "csv" else ("xlsx" if format_lower == "excel" else "pdf")
                        
                        try:
                            payload = {
                                "freelancer_id": freelancer_id,
                                "file_format": format_lower,
                                "report_type": None,
                                "year": None,
                                "month": None,
                                "start_date": None,
                                "end_date": None
                            }
                            
                            if report_type == "Month":
                                payload["report_type"] = "month"
                                payload["year"] = year_select
                                payload["month"] = month_select[1]
                            elif report_type == "Year":
                                payload["report_type"] = "year"
                                payload["year"] = year_select
                            else:  # Date Range
                                payload["report_type"] = "date_range"
                                payload["start_date"] = str(start_date_select)
                                payload["end_date"] = str(end_date_select)

                            # Remove None values
                            payload = {k: v for k, v in payload.items() if v is not None}

                            # Add include_fields as JSON - need to send as body for this
                            payload_for_url = payload.copy()
                            payload = payload.copy()
                            payload["include_fields"] = selected_fields
                            
                            # Make request
                            url = f"{API_BASE_URL}/generate-report/"
                            headers = {"Content-Type": "application/json"}
                            response = requests.post(url, params=payload_for_url, json={"include_fields": selected_fields}, headers=headers)
                            
                            if response.status_code == 200:
                                # Determine filename
                                if report_type == "Month":
                                    filename = f"financial_statement_{year_select}-{month_select[1]:02d}.{file_ext}"
                                elif report_type == "Year":
                                    filename = f"financial_statement_{year_select}.{file_ext}"
                                else:
                                    filename = f"financial_statement_{start_date_select}_to_{end_date_select}.{file_ext}"
                                
                                mime_types = {
                                    "csv": "text/csv",
                                    "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    "pdf": "application/pdf"
                                }
                                
                                st.download_button(
                                    label=f"✓ Click here to download {file_format} file",
                                    data=response.content,
                                    file_name=filename,
                                    mime=mime_types.get(format_lower, "application/octet-stream"),
                                    key="download_file_btn"
                                )
                                st.success(f"✓ Statement generated successfully! {file_format} file is ready for download.")
                            else:
                                error_msg = response.json().get("detail", "Unknown error")
                                st.error(f"✗ Error: {error_msg}")
                        except Exception as e:
                            st.error(f"✗ Error: {str(e)}")
                            
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Freelancer Financial Statement Manager | Built with Streamlit & FastAPI</p>
        <p>Make sure the FastAPI backend is running at http://localhost:8000</p>
    </div>
    """, unsafe_allow_html=True)
