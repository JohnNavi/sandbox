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

def search_for_ip_addr(cursor, ip_table_columns, ip_addr):
    """
    Search the provided list of tables/column/data_type table for the provided ip_addr

    args
       cursor    - handle to the database
       ip_tables - list of tuples that contains the table name / column name / column data type
                   for all tables that contained 'ip' in their name and column that contains
                   ip data
       ip_addr   - ip address that we will be searching the provided table list for

    returns
       list of tables for which we find an ip match
    """

    ip_table_match = []

    # rip through the provided table / column list and look for provided ip address
    for table_column in ip_table_columns:
        cursor.execute("SELECT * FROM " + table_column[0] + " WHERE " + table_column[1] + " = '" + ip_addr + "';" )
        records = cursor.fetchall()

        # if we find a match save it off
        if records:
            ip_table_match.append(table_column)
            

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print ip_table_match
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@"

    return ip_table_match


def search_ip_tables(cursor, tables):
    """
    Search a provided list of database tables for a columns that contains 'ip' 
    and also where 'ip' column is of the correct 'string' type (ip values are
    stored in the database as strings).

    args
       cursor  - handle to the database
       tables  - list of tables containing 'ip' in their name

    returns
       list of tuples that describe the table, column name and column data type
       for table columns that contain 'ip' and are of the expected ip data type
    """

    ip_data_type       = 1043 # data type for ip address in the database (character varying)
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

        # rip column list and find the column names that contain 'ip'
        for column_name in column_names:
            contains_ip          = column_name[0].lower().find("ip")
            is_correct_data_type = column_name[1] == ip_data_type

            # add table name and column name to list of columns with 'ip' in thier name
            # if we did indeed find 'ip' in their name, the name starts with 'ip and
            # the ip address is of the correct data type
            if  contains_ip != -1 and is_correct_data_type:
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
    

def get_ip_tables(cursor):
    """
    Get list of tables from proddb that contain columns with 'ip'.  NOTE - method will filter
    out non 'cl' and 'cladm' tables from the return list.  List will also contain only 
    DISTINCT table names (duplicate table names will be filtered out).

    args
       None.

    returns
       List of table names from proddb that contain columns with 'ip' in thier name. 
    """

    ip_tables       = []
    potential_issue = False


    # make SQL query and get result from cursor
    cursor.execute("SELECT DISTINCT table_name FROM information_schema.columns WHERE column_name LIKE '%ip%';")
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
    print "Connected!\n"

    return cursor


def main(ip_addr):
    """
    main entry point for global ip search.
    """

    # connect to the database
    cursor = connect_to_db()

    # get list of tables in database that contain columns with the text 'ip'
    ip_tables = get_ip_tables(cursor)

    # search list of ip tables for provided ip address
    ip_table_columns = search_ip_tables(cursor, ip_tables)

    search_for_ip_addr(cursor, ip_table_columns, ip_addr)

        
if __name__ == "__main__":
    ipAddr = sys.argv[1]
    main(ipAddr)

