import pyodbc
import tkinter as tk
from tkinter import ttk
from frames import *
from pdf import PDF

# Установление соединения с базой данной
conn = pyodbc.connect(driver ='{SQL Server}',server = 'DESKTOP-D1E0GE4' , database = 'db', user = 'DESKTOP-D1E0GE4\orkee', Trusted_Connection='yes')
cursor = conn.cursor()
  
# Создание графического интерфейса    
root = tk.Tk()                             # Основное окно
root.title("База данных отеля")
root.geometry('600x300')
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Проживание')
tab_control.add(tab2, text='Два')
tab_control.pack(expand=2, fill='both')

main_frame = MainFrame(cursor, tab1)
main_frame.pack(anchor='nw', expand=True, fill='both')


pdf_tab = PDFWindow(cursor, tab2)

# Передача управления пользователю
root.mainloop()

# Закрытие курсора и соединения с базой данной
cursor.close()
conn.close()

