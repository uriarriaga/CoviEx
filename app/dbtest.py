import mysql.connector

cnx = mysql.connector.connect(user='uli', password='Kr4k3n1808!',
                              host='192.168.100.24',
                              database='teleconsulta',
                              auth_plugin='mysql_native_password')





cnx.close()