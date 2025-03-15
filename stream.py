from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd

#Why I am using streamlit? 
#1. Simplicity & Speed
#I can create interactive web apps with just a few lines of Python code.
#2. Instant UI Components
#Comes with built-in widgets like sliders, buttons, text inputs, file uploaders, etc.
#3. Fast Development
#Streamlit is really quick and with just small amount of code i can create a to many functionalities.

def initialize_data():
    if 'transactions' not in st.session_state:
        st.session_state.transactions = pd.DataFrame(
            columns=['Date','Type','Category','Amount','Description']
        )
        
    if 'type_trans' not in st.session_state:
        st.session_state.type_trans="Expense"


def get_categories_for_type(type_trans):
    categories = {
        "Expense":["Food","Transport","Shopping","Bills","Entertainment","Other Expenses"],
        "Income":["Salary","Freelance","Investment","Other Income"]
    }
    return categories[type_trans]


def main():
    # Page config
    st.set_page_config(
        page_title="Personal Finance Tracker",
        layout="wide"
    )

    #Welcome Section
    st.title("Welcome to Personal Finance Tracker! ")

    #Introduction 
    st.markdown("""
    This mini-project will help you to take control of your financial life through:
    
    - **Track Every Transaction**: Easily note your income and expenses
    - **Categorize Spending**: Organize by categories transactions
    - **Visual Insights**: Your spending patterns visible via interactive charts
    - **Real-time Balance**: Track your current account status

    To get started:
    1. Click on your sidebar to add your transactions
    2. Choose transaction type (Income/Expense)
    3. Pick a category and add the amount
    4. Instantly view your financial summary and spending patterns!
    ---
    """)

    initialize_data()
    #Sidebar 
    st.sidebar.header("Add New Transaction")

    #Transaction type selection
    type_trans=st.sidebar.selectbox(
        "Transaction Type",
        ["Expense", "Income"],
        key='type_trans'
    )

    #Transaction form
    with st.sidebar.form("transaction_form"):
        date=st.date_input("Date", datetime.now())

        #Get categories based on selected type
        categories=get_categories_for_type(type_trans)
        category=st.selectbox("Category", categories)
        amount=st.number_input("Amount", min_value=0.0, format="%.2f")
        description=st.text_input("Description")
        submit=st.form_submit_button("Add Transaction")

        if submit and amount > 0:
            new_transaction = pd.DataFrame([{
                'Date':date,
                'Type':type_trans,
                'Category':category,
                'Amount':amount,
                'Description':description
            }])
            st.session_state.transactions=pd.concat(
                [st.session_state.transactions, new_transaction],
                ignore_index=True
            )

    #Main content area
    col1,col2=st.columns(2)
    with col1:
        st.subheader("📋Financial Summary")
        if not st.session_state.transactions.empty:
            total_income=st.session_state.transactions[
                st.session_state.transactions['Type']=='Income'
            ]['Amount'].sum()

            total_expenses=st.session_state.transactions[
                st.session_state.transactions['Type']=='Expense'
            ]['Amount'].sum()

            balance=total_income-total_expenses
            st.metric("Total Income", f"₹{total_income:,.2f}")
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
            st.metric("Current Balance", f"₹{balance:,.2f}")

    with col2:
        st.subheader("📈Spending by Category")
        if not st.session_state.transactions.empty:
            expenses_by_category=st.session_state.transactions[
                st.session_state.transactions['Type']=='Expense'
            ].groupby('Category')['Amount'].sum()

            if not expenses_by_category.empty:
                st.bar_chart(expenses_by_category)


    #Transaction History
    st.subheader("📝Recent Transactions")
    if not st.session_state.transactions.empty:
        st.dataframe(
            st.session_state.transactions.sort_values('Date', ascending=False),
            use_container_width=True
        )
    else:
        st.info("No transactions yet. Add your first transaction!")

if __name__=="__main__":
    main()