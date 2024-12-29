import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from db import DB_connection

# Function to retrieve the SQLite database connection from the DB_connection class
def get_db_connection(db_connection: DB_connection) -> sqlite3.Connection:
    try:
        return db_connection._DB_connection__db  # Access the private database connection attribute
    except AttributeError:
        raise ConnectionError("Could not access database connection")  # Raise error if the connection is inaccessible

# Function to check if the 'history' table exists in the database
def check_history_table_exists(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='history';
    """)
    if not cursor.fetchone():  # Check if any result is returned
        print("History table not found in database")
        return False
    return True

# Function to check if the 'history' table contains any data
def check_data_exists(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM history")  # Count the number of rows in the table
    return cursor.fetchone()[0] > 0  # Return True if there are rows, else False

# Function to generate visualization graphs based on financial data
def generate_graphs(db_connection: DB_connection):
    try:
        conn = get_db_connection(db_connection)  # Get the database connection
        
        # Check if the history table exists
        if not check_history_table_exists(conn):
            print("Please ensure the history table is created before running visualizations.")
            return
        
        # Check if there is any data in the history table
        if not check_data_exists(conn):
            print("No data found in the database. Please add some transactions first.")
            return
            
        # Query to fetch transaction data
        query = """
        SELECT time, operation, amount, category, currency 
        FROM history 
        ORDER BY time;
        """
        
        try:
            df = pd.read_sql_query(query, conn)  # Load data into a pandas DataFrame
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading from database: {e}")
            return
            
        if df.empty:  # Check if the DataFrame is empty
            print("No transactions found in the database.")
            return

        # Convert the 'time' column to datetime format, handling invalid dates
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df = df.dropna(subset=['time'])  # Remove rows with invalid dates
        
        # Get the unique currencies from the dataset
        currencies = df['currency'].unique()
        
        if len(currencies) == 0:  # Check if there are any currencies in the data
            print("No currency data found in transactions.")
            return
            
        for currency in currencies:  # Loop through each currency
            try:
                currency_data = df[df['currency'] == currency].copy()  # Filter data for the current currency
                
                if currency_data.empty:  # Skip if there's no data for this currency
                    continue
                    
                # Create a figure with two subplots
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
                fig.suptitle(f'Financial Analysis ({currency})')  # Set the figure title
                
                # Pie Chart for spending by category
                category_data = currency_data[currency_data['operation'] == 'DEPO']
                if not category_data.empty:  # Check if there are deposits to analyze
                    category_totals = category_data.groupby('category')['amount'].sum().abs()
                    
                    # Handle null categories
                    if pd.isna(category_totals.index).any():
                        category_totals.index = category_totals.index.fillna('Uncategorized')
                    
                    ax1.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%')
                    ax1.set_title('Spending by Category')
                else:
                    # Display a placeholder message if no spending data exists
                    ax1.text(0.5, 0.5, 'No spending data available',
                            horizontalalignment='center', verticalalignment='center')
                
                # Line Chart for balance over time
                currency_data = currency_data.sort_values('time')  # Sort data by time
                running_balance = []
                balance = 0
                
                # Calculate the running balance
                for _, row in currency_data.iterrows():
                    try:
                        amount = float(row['amount'])  # Ensure the amount is a float
                        if row['operation'] == 'WITH':  # WITH adds to the balance
                            balance += amount
                        elif row['operation'] == 'DEPO':  # DEPO subtracts from the balance
                            balance -= amount
                        running_balance.append(balance)
                    except (ValueError, TypeError) as e:  # Handle invalid amount values
                        print(f"Warning: Invalid amount value found: {row['amount']}")
                        running_balance.append(balance)  # Keep the previous balance
                
                currency_data['balance'] = running_balance
                currency_data.plot(x='time', y='balance', ax=ax2, kind='line')  # Plot the balance
                ax2.set_title('Balance Over Time')
                ax2.set_xlabel('Date')
                ax2.set_ylabel(f'Balance ({currency})')
                ax2.grid(True)  # Add a grid to the plot
                
                plt.tight_layout()  # Adjust layout to avoid overlapping
                plt.show()  # Display the plots
                
            except Exception as e:  # Handle any errors during processing
                print(f"Error processing currency {currency}: {e}")
                continue

    except Exception as e:  # Handle errors related to database connection or query
        print(f"An error occurred while generating graphs: {e}")

# Function to generate a breakdown of spending by category
def generate_category_breakdown(db_connection: DB_connection):
    try:
        conn = get_db_connection(db_connection)  # Get the database connection
        
        # Check if the history table exists
        if not check_history_table_exists(conn):
            print("Please ensure the history table is created before generating breakdown.")
            return pd.DataFrame()
        
        # Query to calculate statistics for each category
        query = """
        SELECT 
            COALESCE(category, 'Uncategorized') as category,
            currency, 
            operation,
            SUM(CAST(amount AS FLOAT)) as total_amount,
            COUNT(*) as transaction_count,
            MIN(CAST(amount AS FLOAT)) as min_amount,
            MAX(CAST(amount AS FLOAT)) as max_amount,
            AVG(CAST(amount AS FLOAT)) as avg_amount
        FROM history
        WHERE operation = 'DEPO'
        GROUP BY COALESCE(category, 'Uncategorized'), currency
        ORDER BY total_amount DESC;
        """
        
        try:
            df = pd.read_sql_query(query, conn)  # Load query results into a DataFrame
            return df
        except pd.io.sql.DatabaseError as e:
            print(f"Error reading from database: {e}")
            return pd.DataFrame()
            
    except Exception as e:  # Handle errors during database query
        print(f"An error occurred while generating category breakdown: {e}")
        return pd.DataFrame()

# Main function to orchestrate the application logic
def main():
    try:
        db = DB_connection()  # Initialize the database connection
        
        generate_graphs(db)  # Generate visualization graphs
        
        # Generate and display category breakdown
        category_stats = generate_category_breakdown(db)
        if not category_stats.empty:
            print("\nCategory Spending Analysis:")
            print(category_stats.to_string())  # Display the breakdown as a formatted string
        else:
            print("\nNo category statistics available.")
            
    except Exception as e:  # Handle any errors during the main execution
        print(f"An error occurred in the main function: {e}")

# Run the main function when the script is executed directly
if __name__ == "__main__":
    main()
