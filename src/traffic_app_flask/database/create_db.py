"""Code used to create the traffic sqlite database.

This script creates the traffic.db SQLite database and adds the traffic flow data to the database.

The create_db function is used to create the database tables.
There are two tables created, the boroughs table and the traffic_flows table.
Year could have been added as a separate table. However, for simplicity, it is added as a column in the traffic_flows table.

The add_data() function is used to add the data to the database.

The main block calls these two functions to create the database and add the data.
"""

import sqlite3
from pathlib import Path

import pandas as pd


def create_db(cursor, conn):
    """Create the tables in the SQLite database.

    Parameters:
    ----------
    cursor : sqlite3.Cursor
        The cursor object to execute SQL commands.
    conn : sqlite3.Connection
        The connection object to the SQLite database.

    """
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS boroughs (
        borough_id INTEGER PRIMARY KEY AUTOINCREMENT,
        la_code TEXT NOT NULL,
        borough_name TEXT NOT NULL
    );
    """
    )

    # This table is related to the boroughs table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS traffic_flows (
        flow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        borough_id INTEGER,
        year INTEGER,
        cars REAL, 
        all_vehicles REAL,
        FOREIGN KEY (borough_id) REFERENCES boroughs(borough_id)
    );
    """
    )

    # Commit the changes
    conn.commit()


def add_data(cursor, conn):
    """Add the borough traffic flow data to the database.

    Parameters:
    ----------
    cursor : sqlite3.Cursor
        The cursor object to execute SQL commands.
    conn : sqlite3.Connection
        The connection object to the SQLite database.
    """

    borough_data = str(Path(__file__).parent.joinpath("traffic-flow-borough.xlsx"))

    # BOROUGHS TABLE
    # Get the local authority codes and names from the excel file
    cols = ["LA Code", "Local Authority"]
    boroughs_df = pd.read_excel(
        borough_data, sheet_name="Traffic Flows Cars", usecols=cols
    )
    # Get a unique list of values by dropping duplicates
    boroughs_df = boroughs_df.drop_duplicates()
    # Drop any rows with missing values
    boroughs_df = boroughs_df.dropna()
    # Insert borough data into the boroughs table
    for index, row in boroughs_df.iterrows():
        values = (row["LA Code"], row["Local Authority"])
        cursor.execute(
            "INSERT INTO boroughs (la_code, borough_name) VALUES (?, ?)", values
        )
    # Commit the changes to the database
    conn.commit()

    # TRAFFIC FLOWS TABLE
    # Get the list of years which are the column C to AG in the spreadsheet
    years = pd.read_excel(
        borough_data, sheet_name="Traffic Flows Cars", usecols="C:AG"
    ).columns
    # Get the data from the cars traffic flow sheet
    cars_df = pd.read_excel(borough_data, sheet_name="Traffic Flows Cars")
    # Drop any rows with missing values, there are some spacer rows in the excel file
    cars_df = cars_df.dropna()
    # Add the values to the traffic_flows table using the borough_id
    for index, row in cars_df.iterrows():
        # Use Column A "LA Code" to get the borough_id from the boroughs table
        borough_id = cursor.execute(
            "SELECT borough_id FROM boroughs WHERE la_code = ?", (row["LA Code"],)
        ).fetchone()[0]
        # Now iterate for this row through the values in Columns C to AG, the year corresponds to the header of the column, then add the data to the table
        for year, value in zip(years, row[2:]):
            cursor.execute(
                "INSERT INTO traffic_flows (year, borough_id, cars) VALUES (?, ?, ?)",
                (year, borough_id, value),
            )
    conn.commit()

    # Add the 'all vehicles' traffic flow data to the traffic_flows table
    # This adds the 'all' column to the existing rows in the traffic_flows table
    all_df = pd.read_excel(borough_data, sheet_name="Traffic Flows All vehicles")
    # Drop any rows with missing values, there are some spacer rows in the excel file
    all_df = all_df.dropna()
    # To add the values to the traffic_flows table, find the row that corresponds to the borough_id and year_id, then add the value to the 'all' column
    for index, row in all_df.iterrows():
        # Find the borough_id, the query returns a tuple
        result = cursor.execute(
            "SELECT borough_id FROM boroughs WHERE la_code = ?", (row["LA Code"],)
        )
        # Get the first element of the tuple which is the borough_id
        borough_id = result.fetchone()[0]
        for year, value in zip(years, row[2:]):
            cursor.execute(
                "UPDATE traffic_flows SET all_vehicles = ? WHERE year = ? AND borough_id = ?",
                (value, year, borough_id),
            )
    conn.commit()


if __name__ == "__main__":
    # Create the SQLite database
    # Get the filepath as a string
    db_file = str(Path(__file__).parent.joinpath("traffic.db"))
    # Create a sqlite connection to the database
    conn = sqlite3.connect(db_file)
    # Create a sqlite cursor object
    cursor = conn.cursor()
    # Enable foreign key constraints, not done by default and is required to create the relationships between tables
    cursor.execute("PRAGMA foreign_keys = ON")
    create_db(cursor, conn)
    add_data(cursor, conn)
    conn.close()
