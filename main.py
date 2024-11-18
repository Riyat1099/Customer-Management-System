import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime
import re#used to extract numerical data from the text strings

st.set_page_config(page_title="CMS",page_icon="data:image/jpeg;base64,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")

#Customization for the theme.
st.markdown(
    """
    <style>
    /* Global page background color */
    .stApp {
        background-color: #E6E6FA;  /* Soft lilac */
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #7B83EB;  /* Deep periwinkle */
        color: #FFFFFF;  /* White text */
    }
    .css-1d391kg .css-10trblm {
        color: #FFFFFF;  /* Adjust the color for sidebar selectbox text */
    }

    /* Highlight color for select boxes, buttons, and radio options */
    .css-1cpxqw2, .css-14xtw13, .css-1hb7zxy {
        background-color: #7B83EB;  /* Deep periwinkle */
        color: #FFFFFF;  /* White text */
    }

    /* Text input fields and buttons */
    .css-1ps7xv7, .css-1cdq5ya {
        background-color: #DCDCF7;  /* Light periwinkle */
        color: #000000;  /* Black */
        border-color: #7B83EB;  /* Deep periwinkle border */
    }

    /* Main section headers */
    h3 {
        color: #4B4B4B;  /* Dark gray for better readability */
        text-align: center;
    }

    /* DataFrames and tables styling */
    .dataframe, .stDataFrame {
        background-color: #FFFFFF;  /* White */
        color: #000000;  /* Black */
    }

    /* Chart styling */
    .stPlotlyChart {
        background-color: #FFFFFF;  /* White background */
        border: 2px solid #7B83EB;  /* Deep periwinkle border */
        border-radius: 5px;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #DCDCF7;  /* Light periwinkle */
    }
    ::-webkit-scrollbar-thumb {
        background-color: #7B83EB;  /* Deep periwinkle */
        border-radius: 10px;
        border: 3px solid #DCDCF7;  /* Border around thumb */
    }

    /* Button hover effect */
    .css-1ps7xv7:hover, .css-1cdq5ya:hover {
        background-color: #8A92EF;  /* Slightly lighter periwinkle on hover */
        color: #FFFFFF;  /* White text */
    }
    </style>
    """,
    unsafe_allow_html=True
)




if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None   
    
st.title("CMS  Dashboard : Bright Solutions")
choice=st.sidebar.selectbox("Navigation",("Dashboard","Users","Customers","Interactions","Projects","Company Reports","Support Tickets"))
if (choice=="Dashboard"):

    # Connecting the MySQL database to fetch the metrics data
    mydb = mysql.connector.connect(host="localhost", user="root", password="mumbaikar@1099", database="cms_db")
    c = mydb.cursor()

    # Fetching and calculating metrics
    c.execute("SELECT COUNT(*) FROM customers")
    total_customers = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM projects WHERE ProjectStatus = 'Active'")
    active_projects = c.fetchone()[0]

    c.execute("SELECT AVG(AvgResolutionTime) FROM company_reports WHERE ReportType = 'CustomerSatisfaction'")
    avg_resolution_time = float(c.fetchone()[0] or 0)  

    c.execute("SELECT SUM(RevenueGrowth) FROM company_reports WHERE ReportType = 'SalesPerformance' AND GeneratedAt >= DATE_SUB(NOW(), INTERVAL 1 MONTH)")
    monthly_revenue_growth = float(c.fetchone()[0] or 0) 

    c.execute("SELECT COUNT(*) FROM customers WHERE CreatedAt >= DATE_SUB(NOW(), INTERVAL 1 MONTH)")
    new_customers = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM projects WHERE ProjectStatus = 'Completed' AND EndDate >= DATE_SUB(NOW(), INTERVAL 1 MONTH)")
    closed_projects = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM supporttickets WHERE Priority = 'High' AND Status != 'Resolved'")
    high_priority_tickets = c.fetchone()[0]

    # Display metrics in cards
    st.markdown("<h4 style='text-align: center;'>Key Metrics</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", total_customers)
    col2.metric("Active Projects", active_projects)
    col3.metric("Avg. Resolution Time (hrs)", round(avg_resolution_time, 2))
    col4.metric("Revenue Growth (Last Month)", f"{monthly_revenue_growth:.2f}%")

    # Display more metrics in the next row
    col5, col6, col7 = st.columns(3)
    col5.metric("New Customers (This Month)", new_customers)
    col6.metric("Closed Projects (This Month)", closed_projects)
    col7.metric("High Priority Tickets", high_priority_tickets)

    # Conditional alert for high-priority tickets
    if high_priority_tickets > 0:
        st.error(f"⚠️ High Priority Unresolved Tickets: {high_priority_tickets}")

    st.image("https://www.ftols.in/gif/software.gif",width=600)
    st.markdown("<h3 style='text-align: center;'>This application is only for Sales, Support, Management, and Project Team</h3>", unsafe_allow_html=True)
        
elif(choice=="Users"):
    if"login" not in st.session_state:
        st.session_state['login']=False
    eid=st.text_input("Enter Email ID")
    pwd=st.text_input("Enter Password")
    btn=st.button("Login")
    if btn:
        mydb=mysql.connector.connect(host="localhost",user="root",password="mumbaikar@1099",database="cms_db")
        c=mydb.cursor()
        c.execute("select * from users")
        d=c.fetchall()
        
        # Looping through the dataset to find matching credentials
        for r in d:
            if(r[3]==eid and r[5]==pwd):
                st.session_state['login']=True
                st.session_state['user_role'] = r[4]
                break
            
        # To Check if login is successful
        if(not st.session_state['login']):
            st.write("Incorrect ID or Password")
    if(st.session_state['login']):
        st.write("Login Successfull")
        st.markdown("<h3 style='text-align: center;'> You are viewing Users</h3>", unsafe_allow_html=True)
        choice2=st.radio("User Accessibility",("View Users","Create New Users","Update User Roles and Permissions","Delete Users"))

        if(choice2=="View Users"):
            mydb=mysql.connector.connect(host="localhost",user="root",password="mumbaikar@1099",database="cms_db")
            c=mydb.cursor()
            c.execute("select * from users where Email=%s",(eid,))
            d=c.fetchall()
            if d:
                user_data = d[0]  
                st.write("Name:", user_data[1])
                st.write("User ID:", user_data[0])
                st.write("Password:", user_data[5])
                st.write("Role:", user_data[4])

            
                

        elif choice2 == "Create New Users":
            if st.session_state['user_role'] == 'Management':
                st.subheader("Create New User")
                First_Name=st.text_input("First Name")
                Last_Name=st.text_input("Last_Name")
                Email = st.text_input("Email")
                Password = st.text_input("Password", type="password")
                Role = st.selectbox("Role", ["Sales", "Support", "Management", "Project Manager"])
                Create_btn = st.button("Create User")
                if Create_btn:
                    try:
                        c.execute("""INSERT INTO users (FirstName, LastName, Email, Role, PasswordHash, CreatedAt)VALUES (%s, %s, %s, %s, %s, NOW())""", (First_Name, Last_Name, Email, Role, Password))
                        mydb.commit()
                        st.success("User created successfully!")
                    except mysql.connector.Error as e:
                        st.error(f"Error creating user: {e}")
            else:
                st.error("You do not have permission to create users.")

        elif choice2 == "Update User Roles and Permissions":
            if st.session_state['user_role'] == 'Management':
                st.subheader("Update User Role")
                update_user_email = st.text_input("Enter Email of User to Update Role")
                new_role = st.selectbox("New Role", ["Sales", "Support", "Management", "Project Manager"])
                update_btn = st.button("Update Role")

                if update_btn:
                    try:
                        c = mydb.cursor()
                        c.execute("UPDATE users SET Role = %s WHERE Email = %s", (new_role, update_user_email))
                        mydb.commit()
                        st.success(f"Role updated successfully for {update_user_email} to {new_role}")
                    except mysql.connector.Error as e:
                        st.error(f"Error updating user role: {e}")

            else:st.error("You do not have permission to update user roles.")

        
        elif choice2 == "Delete Users":
            if st.session_state['user_role'] == 'Management':
                st.subheader("Delete User")
                delete_user_email = st.text_input("Enter Email of User to Delete")
                delete_btn = st.button("Delete User")

                if delete_btn:
                    confirmation = st.radio(f"Are you sure you want to delete {delete_user_email}?", ("No", "Yes"))
                    if confirmation == "Yes":
                        try:
                            c = mydb.cursor()
                            c.execute("DELETE FROM users WHERE Email = %s", (delete_user_email,))
                            mydb.commit()
                            st.success(f"User {delete_user_email} deleted successfully!")
                        except mysql.connector.Error as e:
                            st.error(f"Error deleting user: {e}")
            else:
                st.error("You do not have permission to delete users.")
                
                            

elif choice == "Customers":
    st.markdown("<h3 style='text-align: center;'>You are viewing Customers</h3>", unsafe_allow_html=True)
    choice3 = st.selectbox(
        "Select Customer Management Action:",
        ("View Customer Information", "Add New Customer", "Update Customer Details","Change Customer Status")
    )

    # Connect to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="mumbaikar@1099", 
        database="cms_db"
    )
    c = mydb.cursor()

    # Handling different choices
    if choice3 == "View Customer Information":
        c.execute("SELECT * FROM customers")
        customers = c.fetchall()
        
        # Filters for viewing customer data
        filter_city = st.text_input("Filter by City")
        filter_state = st.text_input("Filter by State")
        filter_status = st.multiselect(
        "Select Customer Status", 
        options=["Active", "Inactive", "Churned"], 
        default=["Active", "Inactive", "Churned"]
    )

        # Apply filters to the retrieved customer data
        filtered_customers = [
            customer for customer in customers 
            if (filter_city.lower() in customer[6].lower() or not filter_city) and 
               (filter_state.lower() in customer[7].lower() or not filter_state)and
               (customer[10] in filter_status)
        ]

        # Display filtered customer data using expandable sections
        for customer in filtered_customers:
            with st.expander(f"Customer: {customer[1]} {customer[2]} (ID: {customer[0]})"):
                st.write(f"**Name**: {customer[1]} {customer[2]}")
                st.write(f"**Email**: {customer[3]}")
                st.write(f"**Phone Number**: {customer[4]}")
                st.write(f"**Address**: {customer[5]}, {customer[6]}, {customer[7]}, {customer[8]}")
                st.write(f"**Created At**: {customer[9]}")
                st.write(f"**Status**: {customer[10]}")

                # Allowing to edit and delete if the user is from the Sales role
                if st.session_state['user_role'] == 'Sales':
                    edit_btn = st.button(f"Edit Customer {customer[0]}", key=f"edit_{customer[0]}")
                    

                    if edit_btn:
                        with st.form(key=f"edit_customer_form_{customer[0]}"):
                            new_first_name = st.text_input("First Name", value=customer[1])
                            new_last_name = st.text_input("Last Name", value=customer[2])
                            new_email = st.text_input("Email", value=customer[3])
                            new_phone = st.text_input("Phone Number", value=customer[4])
                            new_address = st.text_input("Address", value=customer[5])
                            new_city = st.text_input("City", value=customer[6])
                            new_state = st.text_input("State", value=customer[7])
                            new_zipcode = st.text_input("Zip Code", value=customer[8])
                            new_status = st.selectbox("Status", ["Active", "Inactive", "Churned"], index=["Active", "Inactive", "Churned"].index(customer[10]))
                            submit_edit = st.form_submit_button("Save Changes")

                            if submit_edit:
                                try:
                                    c.execute(
                                        """UPDATE customers 
                                           SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s, Address = %s, City = %s, State = %s, ZipCode = %s 
                                           WHERE CustomerID = %s""",
                                        (new_first_name, new_last_name, new_email, new_phone, new_address, new_city, new_state, new_zipcode, new_status, customer[0])
                                    )
                                    mydb.commit()
                                    st.success(f"Customer {customer[0]} updated successfully!")
                                except mysql.connector.Error as e:
                                    st.error(f"Error updating customer: {e}")

                    

    elif choice3 == "Add New Customer":
        if st.session_state['user_role'] == 'Sales':
            st.subheader("Add New Customer")
            with st.form(key="add_customer"):
                new_first_name = st.text_input("First Name")
                new_last_name = st.text_input("Last Name")
                new_email = st.text_input("Email")
                new_phone = st.text_input("Phone Number")
                new_address = st.text_input("Address")
                new_city = st.text_input("City")
                new_state = st.text_input("State")
                new_zipcode = st.text_input("Zip Code")
                submit_add = st.form_submit_button("Add Customer")

                if submit_add:
                    try:
                        c.execute(
                            """INSERT INTO customers (FirstName, LastName, Email, PhoneNumber, Address, City, State, ZipCode, CreatedAt)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
                            (new_first_name, new_last_name, new_email, new_phone, new_address, new_city, new_state, new_zipcode)
                        )
                        mydb.commit()
                        st.success("Customer added successfully!")
                    except mysql.connector.Error as e:
                        st.error(f"Error adding customer: {e}")
        else:
            st.error("You do not have permission to add new customers.")

    elif choice3 == "Update Customer Details":
        if st.session_state['user_role'] == 'Sales':
            st.subheader("Update Customer Details")
            update_customer_id = st.text_input("Enter Customer ID to Update Details")
            find_customer_btn = st.button("Find Customer")

            if find_customer_btn:
                c.execute("SELECT * FROM customers WHERE CustomerID = %s", (update_customer_id,))
                customer = c.fetchone()

                if customer:
                    with st.form(key=f"edit_customer_form_{customer[0]}"):
                        new_first_name = st.text_input("First Name", value=customer[1])
                        new_last_name = st.text_input("Last Name", value=customer[2])
                        new_email = st.text_input("Email", value=customer[3])
                        new_phone = st.text_input("Phone Number", value=customer[4])
                        new_address = st.text_input("Address", value=customer[5])
                        new_city = st.text_input("City", value=customer[6])
                        new_state = st.text_input("State", value=customer[7])
                        new_zipcode = st.text_input("Zip Code", value=customer[8])
                        submit_edit = st.form_submit_button("Save Changes")

                        if submit_edit:
                            try:
                                c.execute(
                                    """UPDATE customers SET FirstName = %s, LastName = %s, Email = %s, PhoneNumber = %s, Address = %s, City = %s, State = %s, ZipCode = %s 
                                       WHERE CustomerID = %s""",
                                    (new_first_name, new_last_name, new_email, new_phone, new_address, new_city, new_state, new_zipcode, customer[0])
                                )
                                mydb.commit()
                                st.success(f"Customer {customer[0]} updated successfully!")
                            except mysql.connector.Error as e:
                                st.error(f"Error updating customer: {e}")
                else:
                    st.error("Customer not found.")
        else:
            st.error("You do not have permission to update customer details.")

    elif choice3 == "Change Customer Status":
        if st.session_state['user_role'] == 'Sales':
            st.subheader("Change Customer Status")
            change_status_id = st.text_input("Enter Customer ID to Change Status")
            new_status = st.selectbox("Select New Status", ["Active", "Inactive", "Churned"])
            change_status_btn = st.button("Update Status")

            if change_status_id.strip() and change_status_btn:
                try:
                    # Update the status of the selected customer
                    change_status_id = int(change_status_id)
                    c.execute(
                        "UPDATE customers SET Status = %s WHERE CustomerID = %s", 
                        (new_status, change_status_id)
                    )
                    mydb.commit()
                    st.success(f"Customer {change_status_id} status updated to {new_status} successfully!")
                except ValueError:
                    st.error("Customer ID must be a valid number.")
                except mysql.connector.Error as e:
                    st.error(f"Error updating status: {e}")
        else:
            st.error("You do not have permission to change customer status.")



           
elif(choice=="Interactions"):
    st.markdown("<h3 style='text-align: center;'> You are viewing Interactions</h3>", unsafe_allow_html=True)
    mydb = mysql.connector.connect(host="localhost", user="root", password="mumbaikar@1099", database="cms_db")
    c = mydb.cursor()
    c.execute("SELECT InteractionID, CustomerID, InteractionType, InteractionDate, InteractionNotes, InteractionByUserID FROM interactions")
    interaction_data = c.fetchall()
    df = pd.DataFrame(interaction_data, columns=["InteractionID", "CustomerID", "InteractionType", "InteractionDate", "InteractionNotes", "InteractionByUserID"])
    df['InteractionDate'] = pd.to_datetime(df['InteractionDate'])

    #Filters
    st.sidebar.header("Filter Interactions")
    interaction_type_filter = st.sidebar.multiselect("Select Interaction Type", options=df['InteractionType'].unique(), default=df['InteractionType'].unique())
    date_filter_start = st.sidebar.date_input("Start Date", value=datetime(2023, 1, 1))
    date_filter_end = st.sidebar.date_input("End Date", value=datetime.now())

    # Apply filters to DataFrame
    filtered_df = df[(df['InteractionType'].isin(interaction_type_filter)) & 
                     (df['InteractionDate'] >= pd.to_datetime(date_filter_start)) &
                     (df['InteractionDate'] <= pd.to_datetime(date_filter_end))]

    # Number of Interactions Over Time
    st.subheader("Number of Interactions Over Time")
    interactions_over_time = filtered_df.groupby(filtered_df['InteractionDate'].dt.to_period('M')).size().reset_index(name='Count')
    interactions_over_time['InteractionDate'] = interactions_over_time['InteractionDate'].dt.to_timestamp()
    fig_interactions_over_time = px.line(interactions_over_time, x='InteractionDate', y='Count', title='Number of Interactions Over Time')
    st.plotly_chart(fig_interactions_over_time)

    # Interaction Types Distribution
    st.subheader("Interaction Types Distribution")
    interaction_types_count = filtered_df['InteractionType'].value_counts().reset_index()
    interaction_types_count.columns = ['InteractionType', 'Count']
    fig_interaction_types = px.pie(interaction_types_count, values='Count', names='InteractionType', title='Interaction Types Distribution')
    st.plotly_chart(fig_interaction_types)

    # User Performance
    st.subheader("User Performance")
    user_performance = filtered_df['InteractionByUserID'].value_counts().reset_index()
    user_performance.columns = ['InteractionByUserID', 'Count']
    fig_user_performance = px.bar(user_performance, x='InteractionByUserID', y='Count', title='User Performance - Number of Interactions Handled')
    st.plotly_chart(fig_user_performance)

    # Prepare data for bubble chart
    interaction_summary = filtered_df.groupby(['CustomerID', 'InteractionType']).size().reset_index(name='Count')

    fig_bubble = px.scatter(
        interaction_summary,
        x='CustomerID',
        y='InteractionType',
        size='Count',
        color='InteractionType',
        title='Customer Engagement - Bubble Chart',
        labels={"CustomerID": "Customer ID", "Count": "Number of Interactions"},
        size_max=30  # Adjust size_max for bubble size scaling
    )
    st.plotly_chart(fig_bubble)



elif choice == "Projects":
    st.markdown("<h3 style='text-align: center;'>You are viewing Projects</h3>", unsafe_allow_html=True)

    # Connect to the MySQL database
    mydb = mysql.connector.connect(host="localhost", user="root", password="mumbaikar@1099", database="cms_db")
    c = mydb.cursor()

    # Fetch project data from the database
    c.execute("SELECT ProjectID, CustomerID, LEADUSERID, ProjectName, StartDate, EndDate, ProjectStatus, Budget FROM projects")
    projects_data = c.fetchall()

    # Create a DataFrame for project data
    df = pd.DataFrame(projects_data, columns=["ProjectID", "CustomerID", "LEADUSERID", "ProjectName", "StartDate", "EndDate", "ProjectStatus", "Budget"])
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['EndDate'] = pd.to_datetime(df['EndDate'])

    # Debugging: Show the original DataFrame
    st.write("Original Project Data:", df)

    # Filters for Projects
    st.sidebar.header("Filter Projects")
    status_filter = st.sidebar.multiselect("Select Project Status", options=df['ProjectStatus'].unique(), default=df['ProjectStatus'].unique())
    lead_filter = st.sidebar.multiselect("Select Lead User", options=df['LEADUSERID'].unique(), default=df['LEADUSERID'].unique())
    date_filter_start = st.sidebar.date_input("Start Date", value=datetime(2023, 1, 1))
    date_filter_end = st.sidebar.date_input("End Date", value=datetime.now())

    # Apply filters
    filtered_df = df[(df['ProjectStatus'].isin(status_filter)) &
                     (df['LEADUSERID'].isin(lead_filter)) &
                     (df['StartDate'] >= pd.to_datetime(date_filter_start)) &
                     (df['EndDate'] <= pd.to_datetime(date_filter_end))]

    # Debugging: Show the filtered DataFrame
    st.write("Filtered Data:", filtered_df)

    # Visualization 1: Project Status Distribution
    st.subheader("Project Status Distribution")
    if not filtered_df.empty:
        status_counts = filtered_df['ProjectStatus'].value_counts().reset_index()
        status_counts.columns = ['ProjectStatus', 'Count']
        fig_status_distribution = px.pie(status_counts, values='Count', names='ProjectStatus', title='Project Status Distribution')
        st.plotly_chart(fig_status_distribution)
    else:
        st.warning("No projects available with the selected filters for Project Status Distribution.")

    # Visualization 2: Project Timelines
    st.subheader("Project Timelines")
    if not filtered_df.empty:
        fig_timelines = px.timeline(filtered_df, x_start='StartDate', x_end='EndDate', y='ProjectName', color='ProjectStatus',
                                    title='Project Timelines (Gantt Chart)', labels={"ProjectName": "Project"})
        fig_timelines.update_yaxes(categoryorder='total ascending')  # Sort projects by start date in ascending order
        st.plotly_chart(fig_timelines)
    else:
        st.warning("No projects available with the selected filters for Project Timelines.")

    # Visualization 3: Budget Allocation per Project
    st.subheader("Budget Allocation per Project")
    if not filtered_df.empty:
        fig_budget = px.bar(filtered_df, x='ProjectName', y='Budget', color='ProjectStatus',
                            title='Budget Allocation per Project', labels={"ProjectName": "Project", "Budget": "Budget (in $)"})
        st.plotly_chart(fig_budget)
    else:
        st.warning("No projects available with the selected filters for Budget Allocation per Project.")

    # Summary Chart for Budget per Status
    st.subheader("Total Budget Allocated by Project Status")
    if not filtered_df.empty:
        budget_by_status = filtered_df.groupby('ProjectStatus')['Budget'].sum().reset_index()
        fig_budget_summary = px.bar(budget_by_status, x='ProjectStatus', y='Budget', title='Total Budget by Project Status',
                                    labels={"ProjectStatus": "Project Status", "Budget": "Total Budget (in $)"})
        st.plotly_chart(fig_budget_summary)
    else:
        st.warning("No projects available with the selected filters for Total Budget by Project Status.")

    # Visualization 4: Projects by Lead User
    st.subheader("Projects by Lead User")
    if not filtered_df.empty:
        lead_counts = filtered_df['LEADUSERID'].value_counts().reset_index()
        lead_counts.columns = ['LEADUSERID', 'Count']
        fig_lead_projects = px.bar(lead_counts, x='LEADUSERID', y='Count', title='Projects by Lead User',
                                   labels={"LEADUSERID": "Lead User ID", "Count": "Number of Projects"})
        st.plotly_chart(fig_lead_projects)
    else:
        st.warning("No projects available with the selected filters for Projects by Lead User.")


elif choice == "Company Reports":
    st.markdown("<h3 style='text-align: center;'>You are viewing Company Reports</h3>", unsafe_allow_html=True)
    
    # Connect to the MySQL database
    mydb = mysql.connector.connect(host="localhost", user="root", password="mumbaikar@1099", database="cms_db")
    c = mydb.cursor()
    c.execute("SELECT ReportID, ReportType, GeneratedAt, SalesClosed, RevenueGrowth, AvgResolutionTime, OpenTickets, ResolvedTickets, InProgressTickets, ClosedTickets, CustomerInteractions FROM company_reports")
    reports_data = c.fetchall()
    
    # Create DataFrame for the reports data with the appropriate columns
    df_reports = pd.DataFrame(reports_data, columns=["ReportID", "ReportType", "GeneratedAt", "SalesClosed", "RevenueGrowth", 
                                                     "AvgResolutionTime", "OpenTickets", "ResolvedTickets", 
                                                     "InProgressTickets", "ClosedTickets", "CustomerInteractions"])
    df_reports['GeneratedAt'] = pd.to_datetime(df_reports['GeneratedAt'])
    
    # Map report types to user-friendly labels
    report_type_mapping = {
        "SalesPerformance": "Sales Performance",
        "CustomerSatisfaction": "Customer Satisfaction",
        "TicketStatus": "Ticket Status",
        "CustomerInteractions": "Customer Interactions"
    }
    
    # Reverse map to get back the original ReportType from user-friendly label
    reverse_report_type_mapping = {v: k for k, v in report_type_mapping.items()}
    
    # Select Report Type for visualization using user-friendly labels
    selected_label = st.selectbox("Select Report Type", list(report_type_mapping.values()))
    selected_report_type = reverse_report_type_mapping[selected_label]
    
    # Filter DataFrame based on the selected report type
    df_selected_report = df_reports[df_reports['ReportType'] == selected_report_type]
    
    # Display data for the selected report type
    st.write("Filtered Data for Selected Report Type:", df_selected_report)
    
    # Visualization based on report type
    if selected_report_type == "SalesPerformance":
        st.subheader("Sales Performance")
        
        # Line Chart for Sales Closed over time
        fig_sales = px.line(df_selected_report, x='GeneratedAt', y='SalesClosed', title='Sales Closed Over Time')
        st.plotly_chart(fig_sales)
        
        # Bar Chart for Revenue Growth
        fig_revenue = px.bar(df_selected_report, x='GeneratedAt', y='RevenueGrowth', title='Revenue Growth Over Time',
                             labels={"RevenueGrowth": "Revenue Growth (%)"})
        st.plotly_chart(fig_revenue)
    
    elif selected_report_type == "CustomerSatisfaction":
        st.subheader("Customer Satisfaction")
        
        # Bar Chart for Average Resolution Time
        fig_resolution_time = px.bar(df_selected_report, x='GeneratedAt', y='AvgResolutionTime', title='Average Resolution Time Over Time',
                                     labels={"AvgResolutionTime": "Avg. Resolution Time (hours)"})
        st.plotly_chart(fig_resolution_time)
    
    elif selected_report_type == "TicketStatus":
        st.subheader("Ticket Status")
        
        # Donut Chart for Ticket Status Distribution
        ticket_counts = {
            "Open": df_selected_report['OpenTickets'].sum(),
            "Resolved": df_selected_report['ResolvedTickets'].sum(),
            "In Progress": df_selected_report['InProgressTickets'].sum(),
            "Closed": df_selected_report['ClosedTickets'].sum()
        }
        fig_ticket_status = px.pie(values=ticket_counts.values(), names=ticket_counts.keys(), hole=0.4,
                                   title='Ticket Status Distribution')
        st.plotly_chart(fig_ticket_status)
    
    elif selected_report_type == "CustomerInteractions":
        st.subheader("Customer Interactions")
        
        # Convert CustomerInteractions column from JSON string to dictionary
        df_selected_report['CustomerInteractions'] = df_selected_report['CustomerInteractions'].apply(lambda x: eval(x) if x else {})
        
        # Aggregate interactions per customer
        interaction_data = {}
        for interactions in df_selected_report['CustomerInteractions']:
            for customer_id, count in interactions.items():
                if customer_id in interaction_data:
                    interaction_data[customer_id] += count
                else:
                    interaction_data[customer_id] = count
        
        # Convert to DataFrame for visualization
        interaction_df = pd.DataFrame(list(interaction_data.items()), columns=["CustomerID", "InteractionCount"])
        fig_customer_interactions = px.bar(interaction_df, x='CustomerID', y='InteractionCount', 
                                           title='Customer Interactions',
                                           labels={"CustomerID": "Customer ID", "InteractionCount": "Number of Interactions"})
        st.plotly_chart(fig_customer_interactions)




elif choice == "Support Tickets":
    if st.session_state['user_role'] == 'Support':
        st.markdown("<h3 style='text-align: center;'>You are viewing Support Tickets</h3>", unsafe_allow_html=True)

        # Create tabs for different actions
        tab1, tab2, tab3 = st.tabs(["View Support Tickets", "Create New Support Ticket", "Manage Existing Support Tickets"])

        # Connect to the MySQL database
        mydb = mysql.connector.connect(host="localhost", user="root", password="mumbaikar@1099", database="cms_db")
        c = mydb.cursor()

        with tab1:
            # 1. View Support Tickets
            st.subheader("View Support Tickets")
            # Fetch support ticket data from the database
            c.execute("SELECT TicketID, CustomerID, IssueDescription, Status, Priority, CreatedAt, ResolvedAt, AssignedUserID FROM supporttickets")
            tickets_data = c.fetchall()

            # Create DataFrame for ticket data
            df_tickets = pd.DataFrame(tickets_data, columns=["TicketID", "CustomerID", "IssueDescription", "Status", "Priority", "CreatedAt", "ResolvedAt", "AssignedUserID"])

            # Filters for Tickets
            st.sidebar.header("Filter Support Tickets")
            status_filter = st.sidebar.multiselect("Select Ticket Status", options=df_tickets['Status'].unique(), default=df_tickets['Status'].unique())
            priority_filter = st.sidebar.multiselect("Select Priority", options=df_tickets['Priority'].unique(), default=df_tickets['Priority'].unique())
            assigned_user_filter = st.sidebar.multiselect("Select Assigned User", options=df_tickets['AssignedUserID'].unique(), default=df_tickets['AssignedUserID'].unique())

            # Apply filters and sort tickets
            filtered_df_tickets = df_tickets[
                (df_tickets['Status'].isin(status_filter)) &
                (df_tickets['Priority'].isin(priority_filter)) &
                (df_tickets['AssignedUserID'].isin(assigned_user_filter))
            ]

            # Display filtered tickets in a table
            if not filtered_df_tickets.empty:
                st.dataframe(filtered_df_tickets)
            else:
                st.warning("No tickets available with the selected filters.")

        with tab2:
            # 2. Create a New Support Ticket
            st.subheader("Create a New Support Ticket")
            with st.form(key="create_ticket_form"):
                new_customer_id = st.text_input("Customer ID")
                new_issue_description = st.text_area("Issue Description")
                new_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                new_assigned_user = st.text_input("Assigned User ID")
                create_ticket_btn = st.form_submit_button("Create Ticket")

                if create_ticket_btn:
                    try:
                        c.execute("""INSERT INTO supporttickets (CustomerID, IssueDescription, Status, Priority, CreatedAt, AssignedUserID) 
                                     VALUES (%s, %s, %s, %s, NOW(), %s)""",
                                  (new_customer_id, new_issue_description, "Open", new_priority, new_assigned_user))
                        mydb.commit()
                        st.success("Support ticket created successfully!")
                    except mysql.connector.Error as e:
                        st.error(f"Error creating support ticket: {e}")

        with tab3:
            # 3. Manage Existing Support Tickets
            st.subheader("Manage Existing Support Tickets")
            ticket_id_to_manage = st.text_input("Enter Ticket ID to Manage")

            # Fetch specific ticket to manage
            if ticket_id_to_manage:
                c.execute("SELECT TicketID, CustomerID, IssueDescription, Status, Priority, CreatedAt, ResolvedAt, AssignedUserID FROM supporttickets WHERE TicketID = %s", (ticket_id_to_manage,))
                ticket_to_manage = c.fetchone()

                if ticket_to_manage:
                    with st.form(key=f"manage_ticket_{ticket_to_manage[0]}"):
                        updated_issue_description = st.text_area("Issue Description", value=ticket_to_manage[2])
                        updated_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"], index=["Open", "In Progress", "Resolved"].index(ticket_to_manage[3]))
                        updated_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(ticket_to_manage[4]))
                        updated_assigned_user = st.text_input("Assigned User ID", value=ticket_to_manage[7])
                        update_ticket_btn = st.form_submit_button("Update Ticket")

                        if update_ticket_btn:
                            try:
                                if updated_status == "Resolved" and not ticket_to_manage[6]:
                                    c.execute("""UPDATE supporttickets SET IssueDescription = %s, Status = %s, Priority = %s, ResolvedAt = NOW(), AssignedUserID = %s WHERE TicketID = %s""",
                                              (updated_issue_description, updated_status, updated_priority, updated_assigned_user, ticket_id_to_manage))
                                else:
                                    c.execute("""UPDATE supporttickets SET IssueDescription = %s, Status = %s, Priority = %s, AssignedUserID = %s WHERE TicketID = %s""",
                                              (updated_issue_description, updated_status, updated_priority, updated_assigned_user, ticket_id_to_manage))
                                mydb.commit()
                                st.success("Support ticket updated successfully!")
                            except mysql.connector.Error as e:
                                st.error(f"Error updating support ticket: {e}")
