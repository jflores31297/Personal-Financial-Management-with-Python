import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import matplotlib.pyplot as plt


### Helper Functions:
# Function to calculate total budget
def calculate_total_budget(budget_df):
    """
    Calculate the total budget from a DataFrame.    
    Parameters:
        budget_df (DataFrame): A DataFrame with a 'BudgetAmount' column.    
    Returns:
        float: The total budget.
    """
    return round(budget_df['BudgetAmount'].sum(), 2)

# Function to calculate total monthly spending
def calculate_total_monthly_spending(monthly_expenses):
    """
    Calculate total MTD spending.

    Parameters:
        monthly_expenses: Expenses DataFrame filtered by specified month and year

    Returns:
        float: total mtd spending
    """
    return round(monthly_expenses['Amount'].sum(), 2)

# Function to calculate month-to-date spending grouped by category
def calculate_mtd_spending_by_category(monthly_expenses):
    """
    Calculate Month-to-date spending grouped by category.

    Parameters:
        monthly_expenses" Expenses DataFrame filtered by specified month and year        
    """
    return monthly_expenses.groupby('Category')['Amount'].sum().reset_index()

# Function to calculate monthly budget variance (remaining budget)
def calculate_monthly_budget_variance(total_monthly_budget, total_mtd_spending):
    """
    Calculate Monthly Budget Variance (total remaining budget for specified month and year)

    Parameters:
        total_monthly_budget,
        total_mtd_spending

    Returns
        float: monthly budget variance
    """
    return round(total_monthly_budget-total_mtd_spending, 2)

# Function to calculate total ytd spending
def calculate_total_ytd_spending(ytd_expenses):
    """
    Calculate the total year-to-date spending.

    Parameters:
        ytd_expenses

    Return: 
        float: total ytd spending
    """
    return round(ytd_expenses['Amount'].sum(), 2)

# Function to calculate total ytd budget
def calculate_total_ytd_budget(budget, selected_month_num):
    """
    Calculate Total YTD Budget.

    Parameters:
        budget: Budget DataFrame
        month: Current month or month of interest

    Return: 
        float: total ytd budget amount
    """
    return budget['BudgetAmount'].sum() * selected_month_num

# Function to calculate yearly budget variance
def calculate_ytd_budget_variance(total_ytd_budget, total_ytd_spending):
    """
    Calculate YTD Budget Variance.

    Parameters:
        total_ytd_budget
        total_ytd_spending

    Return:
        float: YTD budget variance
    """
    return round(total_ytd_budget - total_ytd_spending, 2)

#Function to calculate total monthly income
def calculate_total_monthly_income(monthly_income):
    """
    Calculate total monthly income.

    Parameters:
        monthly_income: Income DataFrame filtered by specified month and year 

    Returns:
        float: Total income for the specified month
    """
    return round(monthly_income['Amount'].sum(), 2)

# Function to calculate monthly net income
def calculate_monthly_net_income(total_monthly_income, total_mtd_spending):
    """
    Calculate Monthly Net Income.

    Parameters:
        total_monthly_income
        total_mtd_spending
    Returns:
        float: monthly net income     
    """
    return round(total_monthly_income - total_mtd_spending, 2)

# Function to calculate total ytd income
def calculate_total_ytd_income(ytd_income):
    """
    Calculate total ytd income.

    Parameters:
        ytd_income

    Returns:
        float: total ytd income
    """
    return round(ytd_income['Amount'].sum(), 2)

# Function to calculate yearly net income
def calculate_ytd_net_income(total_ytd_income, total_ytd_spending):
    """
    Calculate YTD Net Income

    Parameters:
        total_ytd_income
        total_ytd_spending
    """
    return round(total_ytd_income - total_ytd_spending, 2)
###


# App Title
st.title("Personal Finance Dashboard")

# Sidebar for Inputs
st.sidebar.header("Upload Data and Select Period")

# File Upload
budget_file = st.sidebar.file_uploader("Upload Budget Data (CSV)", type=['csv'])
income_file = st.sidebar.file_uploader("Upload Income Data (CSV)", type=['csv'])
expense_file = st.sidebar.file_uploader("Upload Expense Data (CSV)", type=['csv'])


# Select Month and Year
year = st.sidebar.selectbox("Select Year", range(2020, 2031), index=4)
month = st.sidebar.selectbox("Select Month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])

# Month mapping to numbers
month_mapping = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
    "June": 6, "July": 7, "August": 8, "September": 9,
    "October": 10, "November": 11, "December": 12
}
selected_month_num = month_mapping[month]

# Process and Display Data
if budget_file:
    # Load data
    budget_df = pd.read_csv(budget_file, dtype={'BudgetAmount': float})
    # Ensure proper column names
    if "Category" not in budget_df.columns or "BudgetAmount" not in budget_df.columns:
        st.error("Budget file must have 'Category' and 'BudgetAmount' columns.")
    else:
        # Call the function to calculate total budget
        total_monthly_budget = calculate_total_budget(budget_df)

        st.header("Budget Allocation")
        col1, col2 = st.columns(2)

        with col1:
            # Display budget allocation
            st.metric("Total Monthly Budget", f"${total_monthly_budget:,.2f}")
            # Define custom colors
            custom_colors = ['#6d8c73', '#789a7f', '#84a98c', '#9aba9d', '#b0caae', '#dceacf']
            st.dataframe(budget_df, hide_index=True)

        with col2:
            # Create a matplotlib pie chart
            fig, ax = plt.subplots()
            budget_df.plot(
                kind='pie',
                y='BudgetAmount',
                labels=budget_df['Category'],
                autopct='%1.1f%%',
                colors=custom_colors,
                legend=False,
                ax=ax
            )
            ax.set_ylabel('')
            ax.set_title("Budget Allocation")
            # Display the plot in Streamlit
            st.pyplot(fig)
else:
    st.warning("Please upload budget file.")

# Process and Display Data
if income_file and expense_file:
    # Load data
    income = pd.read_csv(income_file)
    expenses = pd.read_csv(expense_file)

    # Ensure proper column names
    if "Date" not in income.columns or "Amount" not in income.columns:
        st.error("Income file must have 'Date' and 'Amount' columns.")
    elif "Date" not in expenses.columns or "Amount" not in expenses.columns or "Category" not in expenses.columns:
        st.error("Expense file must have 'Date', 'Amount', and 'Category' columns.")
    else:
        # Convert 'Date' columns to datetime
        income['Date'] = pd.to_datetime(income['Date'])
        expenses['Date'] = pd.to_datetime(expenses['Date'])
        
        # Filter data for the selected month and year
        # Filter expenses 
        monthly_expenses = expenses[(expenses['Date'].dt.month == selected_month_num) & (expenses['Date'].dt.year == year)]
        # Filter income 
        monthly_income = income[(income['Date'].dt.month == selected_month_num) & (income['Date'].dt.year == year)]
else:
    st.warning("Please upload both income and expense files.")


# Calculate Metrics

# Calculate total month-to-date spending
total_mtd_spending = calculate_total_monthly_spending(monthly_expenses)
# Calculate month-to-date spending grouped by category
mtd_spending_by_category = calculate_mtd_spending_by_category(monthly_expenses)
# Merge the MTD spending with the Budget DataFrame
budget_with_spending = pd.merge(budget_df, mtd_spending_by_category, on='Category', how='left')
# Fill NaN values in the 'Amount' column with 0 (if there's no spending for a category)
budget_with_spending['Amount'] = budget_with_spending['Amount'].fillna(0)
# Calculate the remaining budget by subtracting MTD spending from BudgetAmount
budget_with_spending['RemainingBudget'] = budget_with_spending['BudgetAmount'] - budget_with_spending['Amount']
# Calculate the total remaining budget
total_remaining_budget = calculate_monthly_budget_variance(total_monthly_budget, total_mtd_spending)

# Filter Year-to-Date Expenses
ytd_expenses = expenses[(expenses['Date'].dt.month <= selected_month_num) & (expenses['Date'].dt.year == year)]
# Calculate Total YTD Spending
total_ytd_spending = calculate_total_ytd_spending(ytd_expenses)
# Calculate Total YTD Budget
total_ytd_budget = calculate_total_ytd_budget(budget_df, selected_month_num)
# Calculate YTD Budget Variance
ytd_budget_variance =  calculate_ytd_budget_variance(total_ytd_budget, total_ytd_spending)

# Calculate total monthly income
total_monthly_income = calculate_total_monthly_income(monthly_income)
# Calculate Monthly Net Income
monthly_net_income = calculate_monthly_net_income(total_monthly_income, total_mtd_spending)

# Calculate Total YTD Income
ytd_income = income[(income['Date'].dt.month <= selected_month_num) & (income['Date'].dt.year == year)]
total_ytd_income = calculate_total_ytd_income(ytd_income)
# Calculate YTD Net Income
ytd_net_income = calculate_ytd_net_income(total_ytd_income, total_ytd_spending)

# Display Metrics
st.header(f"Summary for {month} {year}")
with st.expander("Definitions of Metrics", icon=":material/info:"):    
    st.markdown('''
        **Budget variance** is the difference between what you planned to spend (your budget) and what you actually spent. A positive variance means you spent less than expected, while a negative variance indicates overspending.
        
        **Net income** is the amount of money left after subtracting all expenses, taxes, and deductions from total income. It represents your actual take-home pay or earnings after all costs.
    ''')
col1, col2 = st.columns(2)
with col1:
    st.metric("Total MTD Spending", f"${total_mtd_spending:,.2f}")
    st.metric("Monthly Budget Variance", f"${total_remaining_budget:,.2f}")
    st.metric("YTD Budget Variance", f"${ytd_budget_variance:,.2f}")
with col2:
    st.metric("Total Monthly Income", f"${total_monthly_income:,.2f}")
    st.metric("Monthly Net Income", f"${monthly_net_income:,.2f}")
    st.metric("YTD Net Income", f"${ytd_net_income:,.2f}")
    
# Expense Breakdown by Category
st.subheader("Monthly Budget and Spending")
st.dataframe(budget_with_spending, hide_index=True)


# Plot
data = {
    'Category': budget_with_spending['Category'],
    'Budget Amount': budget_with_spending['BudgetAmount'],
    'Actual Spending': budget_with_spending['Amount']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set the position and width of the bars
fig1, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = range(len(df))

# Plot bars
ax.barh(index, df['Budget Amount'], bar_width, label='Budget Amount', color='#84a98c')
ax.barh([i + bar_width for i in index], df['Actual Spending'], bar_width, label='Actual Spending', color='#dceacf')

# Add labels and title
ax.set_xlabel('Amount')
ax.set_title(f"{month} {year} Budget and Monthly Spending")
ax.set_yticks([i + bar_width / 2 for i in index])
ax.set_yticklabels(df['Category'])
ax.legend()

# Display the plot
st.pyplot(fig1)
