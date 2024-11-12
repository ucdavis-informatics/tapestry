secrets={
"example_oracle_database":    
    { 
        "dbtype": "oracle",
        "username": "<oracle username>", 
        "password": "<oracle password>", 
        "tns": "<name of tns entry in tnsnames.ora>", 
        "url": "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=<host name>)(PORT = <port>)))(CONNECT_DATA=(SERVICE_NAME = <service name>)))" 
    },

"example_mssql_database":
    { 
        "authtype": "sql", 
        "db": "<mssql db name>", 
        "dbtype": "mssql",
        "driver": "{ODBC Driver 17 for SQL Server}", 
        "fqdn": "<fully qualified domain name of the host>", 
        "server": "<host short name>",
        "username": "<mssql username>",
        "password": "<mssql password>", 
        "port": "<mssql port>"
    }
}