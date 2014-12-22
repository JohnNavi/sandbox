#!/usr/bin/env python

import domains
from   MPS.shared import sqlio
from   sqllib import sqlcld


class SQL_test_v(sqlcld.SQLjoin):
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


def main():
    print("In main")
    
    # connect to the database
    print("connecting to database...")
    sqlcld.connectonce()


    # add a var for storing the type of search we want to do
    search_col = 'customer_name'

    # add a var for storing the specific search item we are looking for
    search_item = 'Navi'

    # attempt to capture search string in a dict to be used when calling select
    # where = { 'short_name' : '1008' }
    #where = { search_col : search_item }
    where = { search_col : sqlio.LIKE('%' + search_item + '%') }

    # make test call
    print("making test call...")
    database = SQL_test_v(fetchall=True, dictmode=None)
    #test_data = database.select(search_col=search_item)
    test_data = database.select(**where)

    print "what did we get?"
    print ""
    for item in test_data:
       print item

    sqlcld.close()



if __name__ == "__main__":
    main()

