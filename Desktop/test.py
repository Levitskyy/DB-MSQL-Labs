from pdf import PDF
import pyodbc


conn = pyodbc.connect(driver ='{SQL Server}',server = 'DESKTOP-D1E0GE4' , database = 'db', user = 'DESKTOP-D1E0GE4\orkee', Trusted_Connection='yes')
cursor = conn.cursor()


cursor.execute('''
    SELECT 
               ''')

print(cursor.fetchall())



# pdf = PDF()
# pdf.create_table(TABLE_DATA)
# pdf.output('table.pdf')

cursor.close()
conn.close()
