#!/usr/bin/env python

"""
Script to perform global database search for ips

Copyright 2014, NaviSite, Inc.
"""


#from sqllib import sqlcld
import sys
import psycopg2
import sys
import re

def search_for_search_item(cursor, table_columns, search_value):
    """
    Search the provided list of tables/column/data_type table for the provided 'search_item'

    args
       cursor        - handle to the database
       table_columns - list of tuples that contains the table name / column name / column data type
                       for all tables that contained 'search_item' in their name and column that 
                       is of the correct 'search_item_type'
       search_value  - item that we will be searching the provided table list for

    returns
       list of tables for which we find an 'search_value' match
    """

    table_match = []

    # rip through the provided table / column list and look for provided ip address
    for table_column in table_columns:
        cursor.execute("SELECT * FROM " + table_column[0] + " WHERE " + table_column[1] + " = '" + search_value + "';" )
        records = cursor.fetchall()

        # if we find a match save it off
        if records:
            table_match.append(table_column)
            

    # for now just dump out our table matches
    print "Table matche(s): "
    print table_match

    return table_match


def search_for_tables(cursor, tables, search_item, search_item_type):
    """
    Search a provided list of database tables for a columns that contains provided search_item
    and also where 'search_itme' column is of the correct 'search_item_type'.

    args
       cursor           - handle to the database
       tables           - list of tables containing 'search_item' in their column name(s)
       search_item      - the search being requested (e.g.,  'ip', 'email', 'cust_id', etc...)
       search_item_type - for the search item being requested this is the type of that item in the database

    returns
       list of tuples that describe the table, column name and column data type
       for table columns that contain 'search_item' and are of the expected 'search_item_type'
    """

    #print "------------------------------------"
    #print "args: search_item, search_item_type:"
    #print search_item
    #print search_item_type 
    #print type(search_item)
    #print type(search_item_type)
    #print "------------------------------------"
    

    table_column_names = []

    # make SQL query to get list of columns in provided table
    for table in tables:
        #print "table: " + table
        cursor.execute("SELECT * FROM " + table + " LIMIT 0;")

        # list to hold column names and associated data type for that column
        column_names       = []

        # extract column names and associated data type from tables
        for description in cursor.description:
            column_names.append( (description[0], description[1]) )
            
        # DEBUG
        #print "=========================="
        #print column_names
        #print "=========================="

        # rip column list and find the column names that contain 'search_item'
        for column_name in column_names:
            contains_search_item = column_name[0].lower().find(search_item)
            is_correct_data_type = column_name[1] == search_item_type

            # add table name and column name to list of columns with 'ip' in thier name
            # if we did indeed find 'ip' in their name, the name starts with 'ip and
            # the ip address is of the correct data type
            if  contains_search_item != -1 and is_correct_data_type:
                table_column_names.append( (table, column_name[0], column_name[1]) )

        # DEBUG
        #print "--------------------------"
        #print table_column_names
        #print "--------------------------"

    # DEBUG
    #print "00000000000000000000000000"
    #print table_column_names
    #print "00000000000000000000000000"

    return table_column_names
    

def get_tables(cursor, search_item):
    """
    Get list of tables from proddb that contain columns with 'ip'.  NOTE - method will filter
    out non 'cl' and 'cladm' tables from the return list.  List will also contain only 
    DISTINCT table names (duplicate table names will be filtered out).

    args
       cursor      - handle to the database cursor
       search_item - the search being requested (e.g.,  'ip', 'email', 'cust_id', etc...)

    returns
       List of table names from proddb that contain columns with 'search_item' in thier name. 
    """

    ip_tables       = []
    potential_issue = False

    # make SQL query and get result from cursor
    cursor.execute("SELECT DISTINCT table_name FROM information_schema.columns WHERE column_name LIKE '%" + search_item + "%';")
    records = cursor.fetchall()

    # rip through the result of SQL query
    for record in records:
        # first element of the returned tuple is the string with the resulting table name of our query
        record_string = record[0]
        
        # remove formatting characters so we are left with just the table name
        match = re.search(r'\w*', record_string)
        
        # save off the table name once we have removed the formatting characters and if
        # table is a cl or cladm table
        if match and match.group().lower().startswith('cl'):
            # save off table name for later processing
            ip_tables.append(match.group())
            #print(match.group())
            
        else:
            print "Table filtered out: " + record_string

    #print ip_tables

    return ip_tables


def connect_to_db():
    """
    Connects to local database (currently setup for local test and checkout only).

    args
       none.

    returns
       cursor - handle to the local prod database.
    """
    #Define our connection string
    conn_string = "host='localhost' dbname='clouddb' user='cloud' password='jrdlocaldb'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print "Connected!"

    return cursor


def main(search_value, search_item, search_item_type):
    """
    main entry point for global ip search.

    args
       search_value     - the specific value being searched for (e.g., '10.0.0.23', 'Bob's Burger Shack', etc...)
       search_item      - the search being requested (e.g.,  'ip', 'email', 'cust_id', etc...)
       search_item_type - for the search item being requested this is the type of that item in the database
                          (e.g., ip addresses in the database are strings of type 1043)

    returns
       NA
    """

    # connect to the database
    cursor = connect_to_db()

    # get list of tables in database that contain columns with the text 'ip'
    tables = get_tables(cursor, search_item)

    # search list of tables for provided search item
    table_columns = search_for_tables(cursor, tables, search_item, search_item_type)

    # search the returned list of tables for a matching 
    search_for_search_item(cursor, table_columns, search_value)

        
if __name__ == "__main__":
    search_value     = sys.argv[1]
    search_item      = sys.argv[2]
    search_item_type = int(sys.argv[3])
    main(search_value, search_item, search_item_type)

''' cursor - handle to the database cursor
       search_value     - the specific value being searched for (e.g., '10.0.0.23', 'Bob's Burger Shack', etc...)
       search_item      - the search being requested (e.g.,  'ip', 'email', 'cust_id', etc...)
       search_item_type - for the search item being requested this is the type of that item in the database '''
