#!/usr/bin/env python

import domains
from   MPS.shared import sqlio
from   sqllib     import sqlcld


class SQL_test_1(sqlcld.SQLjoin):
    table = '''(\
SELECT * 
FROM cl_customer 
)'''

#class SQL_table_v(sqlcld.SQLjoin):
#    table = '''(\
#SELECT DISTINCT table_name 
#FROM information_schema.columns 
#WHERE column_name 
#LIKE '%" + search_item + "%';"
#)'''

def onTheFly():
    print("OnTheFly")
    
    # connect to the database
    print("connecting to database...")
    sqlcld.connectonce()

    search_col  = 'customer_id'
    search_item = '2098'
    table_name  = 'cl_customer'
    where = { search_col : search_item }

    class SQL_test_2(sqlcld.SQLjoin):
        table = '''(\
    SELECT * 
    FROM cl_customer 
    )'''

    # make test call
    print("making test call...")
    database = SQL_test_2(fetchall=True, dictmode=None)
    test_data = database.select(**where)

    print("closing to database...")
    sqlcld.close()
    


def main():
    print("In main")
    
    # connect to the database
    print("connecting to database...")
    sqlcld.connectonce()

    # add a var for storing the type of search we want to do
    search_col = 'customer_id'

    # add a var for storing the specific search item we are looking for
    search_item = '2098' # <-- seems to work for numbers and strings...

    # attempt to capture search string in a dict to be used when calling select

    # example where we hard code the where dict
    # where = { 'short_name' : '1008' }

    # example using variables in where dict
    where = { search_col : search_item }

    # LIKE example
    #where = { search_col : sqlio.LIKE('%' + search_item + '%') }

    # make test call
    print("making test call...")
    database = SQL_test_1(fetchall=True, dictmode=None)
    #test_data = database.select(search_col=search_item)
    test_data = database.select(**where)

    print "what did we get?"
    print ""
    for item in test_data:
       print item

    print("closing to database...")
    sqlcld.close()

    print("")
    print("Calling onTheFly()")
    onTheFly()



if __name__ == "__main__":
    main()

