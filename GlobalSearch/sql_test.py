#!/usr/bin/env python

import domains
from   sqllib import sqlcld

class SQL_get_tables(sqlcld.SQLjoin):
    table = """(
        SELECT DISTINCT table_name
        FROM            information_schema.columns
        WHERE           column_name LIKE '%email%'
    )"""
    



