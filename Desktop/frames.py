import tkinter as tk
from tkinter import ttk
from pyodbc import *
from pdf import PDF
import mydb

class TreeviewFrame(ttk.Frame):
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
          self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
          self.treeview = ttk.Treeview(
               self,
               xscrollcommand=self.hscrollbar.set,
               yscrollcommand=self.vscrollbar.set
          )
          self.hscrollbar.config(command=self.treeview.xview)
          self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
          self.vscrollbar.config(command=self.treeview.yview)
          self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
          self.treeview.pack(fill='both', expand=True)

class MainFrame(ttk.Frame):
     def __init__(self, cursor: Cursor, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.cursor = cursor
          self.refresh_btn = ttk.Button(self, text='Обновить', command=self.refresh)
          self.add_btn = ttk.Button(self, text='Новый визит', command=self.add_visit)
          self.refresh_btn.pack(anchor='nw')
          self.add_btn.pack(anchor='nw', pady=5)

          self.table = TreeviewFrame(self)
          self.table.pack(fill='both', expand=True)
          self.table.treeview.config(columns=('visitId', 'dateBegin', 'dateEnd', 'fullName', 'room', 'floor', 'price'),
                              show='headings', 
                              selectmode='browse')
          self.table.treeview.heading('visitId', text='Номер визита')
          self.table.treeview.heading('dateBegin', text='Дата приезда')
          self.table.treeview.heading('dateEnd', text='Дата отъезда')
          self.table.treeview.heading('fullName', text='ФИО клиента')
          self.table.treeview.heading('room', text='Номер комнаты')
          self.table.treeview.heading('floor', text='Этаж')
          self.table.treeview.heading('price', text='Стоимость услуг')
          self.table.treeview.bind('<Double-Button-1>', self.get_visit_info)

     def refresh(self):
          result = mydb.tab1_get_values(self.cursor)
          self.table.treeview.delete(*self.table.treeview.get_children())
          for row in result:
               self.table.treeview.insert(
                    '', tk.END,
                    values=(row[8], row[0], row[1], row[2] + ' ' + row[3] + ' ' + row[4] + ' (' + str(row[9]) + ')', row[5], row[6], row[7])
               )

     def add_visit(self):
          window = NewVisitWindow(self.cursor)

     def get_visit_info(self, event):
          curItem = self.table.treeview.focus()
          itemValue = self.table.treeview.item(curItem)
          visitId = int(itemValue['values'][0])
          clientIdPosStart = itemValue['values'][3].find('(') + 1
          clientIdPosEnd = itemValue['values'][3].find(')')
          clientId = int(itemValue['values'][3][clientIdPosStart:clientIdPosEnd])
          infoWindow = VisitInfoWindow(cursor=self.cursor, visitId=visitId, clientId=clientId)

class NewVisitWindow(tk.Toplevel):
     def __init__(self, cursor: Cursor, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.cursor = cursor
          self.title('Новый визит')
          self.geometry('600x450')

          self.clientIdFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.clientIdLable = ttk.Label(self.clientIdFrame, text='Клиент')
          self.clientIdLable.pack(anchor='nw')
          
          clients = mydb.get_all_clients(cursor)
          clients_list = [str(row[0]) + '. ' + row[1] + ' ' + row[2] + ' ' + row[3] for row in clients]
          self.clientIdList = ttk.Combobox(self.clientIdFrame, values=clients_list, state='readonly')
          self.clientIdList.pack(anchor='nw')
          
          self.clientIdFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.roomNumberFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.roomNumberLable = ttk.Label(self.roomNumberFrame, text='Номер комнаты')
          self.roomNumberLable.pack(anchor='nw')

          self.roomNumberList = ttk.Spinbox(self.roomNumberFrame, from_=0, to=100, increment=1, state='readonly')
          self.roomNumberList.pack(anchor='nw')

          self.roomNumberFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.dateBeginFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.dateBeginLable = ttk.Label(self.dateBeginFrame, text='Дата заселения (ГГГГ-ММ-ДД)')
          self.dateBeginLable.pack(anchor='nw')

          self.dateBeginInput = ttk.Entry(self.dateBeginFrame)
          self.dateBeginInput.pack(anchor='nw')

          self.dateBeginFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.dateEndFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.dateEndLable = ttk.Label(self.dateEndFrame, text='Дата выселения (ГГГГ-ММ-ДД)')
          self.dateEndLable.pack(anchor='nw')

          self.dateEndInput = ttk.Entry(self.dateEndFrame)
          self.dateEndInput.pack(anchor='nw')

          self.dateEndFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.roomSumFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.roomSumLable = ttk.Label(self.roomSumFrame, text='Стоимость проживания')
          self.roomSumLable.pack(anchor='nw')

          self.roomSumInput = ttk.Entry(self.roomSumFrame)
          self.roomSumInput.pack(anchor='nw')

          self.roomSumFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.serviceSumFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.serviceSumLable = ttk.Label(self.serviceSumFrame, text='Стоимость оказанных услуг')
          self.serviceSumLable.pack(anchor='nw')

          self.serviceSumInput = ttk.Entry(self.serviceSumFrame)
          self.serviceSumInput.pack(anchor='nw')

          self.serviceSumFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.add_btn = ttk.Button(self, text='Добавить запись', command=self.add_row)
          self.add_btn.pack(anchor='sw', padx=5, pady=5)

          self.grab_set()

     def add_row(self):
          clientIdSubStr = self.clientIdList.get().find('.')
          clientId = int(self.clientIdList.get()[0:clientIdSubStr])
          mydb.add_new_visit(cursor=self.cursor,
                             clientId=clientId,
                             roomNumber=self.roomNumberList.get(),
                             dateBegin=self.dateBeginInput.get(),
                             dateEnd=self.dateEndInput.get(),
                             roomSum=self.roomSumInput.get(),
                             serviceSum=self.serviceSumInput.get())
          self.destroy()

class VisitInfoWindow(tk.Toplevel):
     def __init__(self, cursor: Cursor, visitId, clientId, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.cursor = cursor
          self.visitId = visitId
          self.clientId = clientId
          self.title('Услуги')
          self.geometry('600x450')

          clientInfo = mydb.get_client_by_id(cursor, clientId)

          self.clientFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.clientName = ttk.Label(self.clientFrame, text=f'ФИО: {clientInfo[0]} {clientInfo[1]} {clientInfo[2]}')
          self.clientName.pack(anchor='nw')
          self.clientAddress = ttk.Label(self.clientFrame, text=f'Адрес: {clientInfo[3]}')
          self.clientAddress.pack(anchor='nw')
          self.clientPassport = ttk.Label(self.clientFrame, text=f'Паспорт: {clientInfo[4]}')
          self.clientPassport.pack(anchor='nw')

          self.clientFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.refresh_btn = ttk.Button(self, text='Обновить', command=self.refresh)
          self.add_btn = ttk.Button(self, text='Добавить услугу', command=self.add_service)
          self.refresh_btn.pack(anchor='nw')
          self.add_btn.pack(anchor='nw', pady=5)

          self.table = TreeviewFrame(self)
          self.table.pack(fill='both', expand=True)
          self.table.treeview.config(columns=('serviceName', 'serviceCount', 'serviceSum', 'serviceDate', 'servicePrice'),
                                     show='headings', 
                                     selectmode='browse')
          self.table.treeview.heading('serviceName', text='Наименование услуги')
          self.table.treeview.heading('serviceCount', text='Количество услуг')
          self.table.treeview.heading('serviceSum', text='Сумма')
          self.table.treeview.heading('serviceDate', text='Дата оказания')
          self.table.treeview.heading('servicePrice', text='Стоимость услуги')

          

          self.grab_set()

     def refresh(self):
          result = mydb.get_service_by_visit_id(self.cursor, self.visitId)
          self.table.treeview.delete(*self.table.treeview.get_children())
          for row in result:
               self.table.treeview.insert(
                    '', tk.END,
                    values=(row[0], row[1], row[2], row[3], row[4])
               )
     
     def add_service(self):
          self.serviceWindow = NewServiceWindow(self.cursor, self.clientId, self.visitId)

class NewServiceWindow(tk.Toplevel):
     def __init__(self, cursor: Cursor, clientId, visitId, *args, **kwargs):
          super().__init__(*args, **kwargs)

          self.cursor = cursor
          self.clientId = clientId
          self.visitId = visitId
          self.title('Новая услуга')
          self.geometry('600x450')

          clientInfo = mydb.get_new_service_window_info(cursor, visitId)

          self.clientFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.clientName = ttk.Label(self.clientFrame, text=f'ФИО: {clientInfo[0]} {clientInfo[1]} {clientInfo[2]}')
          self.clientName.pack(anchor='nw')
          self.clientRoom = ttk.Label(self.clientFrame, text=f'Номер комнаты: {clientInfo[3]}')
          self.clientRoom.pack(anchor='nw')
          self.clientDateBegin = ttk.Label(self.clientFrame, text=f'Дата приезда: {clientInfo[4]}')
          self.clientDateBegin.pack(anchor='nw')
          self.clientDateEnd = ttk.Label(self.clientFrame, text=f'Дата отъезда: {clientInfo[5]}')
          self.clientDateEnd.pack(anchor='nw')

          self.clientFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.serviceTypeFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.serviceTypeLable = ttk.Label(self.serviceTypeFrame, text='Наименование услуги')
          self.serviceTypeLable.pack(anchor='nw')
          
          serviceTypes = mydb.get_all_service_types(cursor)
          serviceTypes_list = [str(row[0]) + '. ' + row[1] for row in serviceTypes]
          self.serviceTypeList = ttk.Combobox(self.serviceTypeFrame, values=serviceTypes_list, state='readonly')
          self.serviceTypeList.bind('<<ComboboxSelected>>', self.update_price_bind)
          self.serviceTypeList.pack(anchor='nw')
          
          self.serviceTypeFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.servicesNumberFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.servicesNumberLable = ttk.Label(self.servicesNumberFrame, text='Кол-во услуг')
          self.servicesNumberLable.pack(anchor='nw')

          self.servicesNumberList = ttk.Spinbox(self.servicesNumberFrame, from_=0, to=100, increment=1, command=self.update_price, state='readonly')
          self.servicesNumberList.pack(anchor='nw')

          self.servicesNumberFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.servicesPriceFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.servicesPriceLable = ttk.Label(self.servicesPriceFrame, text='Стоимость услуг: ')
          self.servicesPriceLable.pack(anchor='nw')

          self.servicePriceList = mydb.get_service_price_list(cursor)

          self.servicesPriceFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.dateBeginFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          
          self.dateBeginLable = ttk.Label(self.dateBeginFrame, text='Дата оказания (ГГГГ-ММ-ДД)')
          self.dateBeginLable.pack(anchor='nw')

          self.dateBeginInput = ttk.Entry(self.dateBeginFrame)
          self.dateBeginInput.pack(anchor='nw')

          self.dateBeginFrame.pack(anchor='nw', fill='x', padx=5, pady=5)

          self.add_btn = ttk.Button(self, text='Добавить запись', command=self.add_row)
          self.add_btn.pack(anchor='sw', padx=5, pady=5)

          self.grab_set()

     def update_price(self):
          serviceId = int(self.serviceTypeList.get()[:self.serviceTypeList.get().find('.')]) - 1
          serviceCount = int(self.servicesNumberList.get())
          self.servicesPriceLable['text'] = f'Стоимость услуг: {self.servicePriceList[serviceId][0] * serviceCount}'

     def update_price_bind(self, event):
          self.update_price()

     def add_row(self):
          serviceType = int(self.serviceTypeList.get()[:self.serviceTypeList.get().find('.')])
          serviceCount = int(self.servicesNumberList.get())
          serviceSum = self.servicePriceList[serviceType-1][0] * serviceCount
          mydb.new_service(
               cursor=self.cursor,
               serviceType=serviceType,
               visitId=self.visitId,
               serviceCount=serviceCount,
               serviceSum=serviceSum,
               serviceDate=self.dateBeginInput.get()
          )
          self.destroy()


class PDFWindow(ttk.Frame):
     def __init__(self, cursor: Cursor, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
          self.cursor = cursor

          self.serviceFrame = ttk.Frame(self, borderwidth=1, relief='solid', padding=[5, 5])
          self.services_pdf_btn = ttk.Button(self.serviceFrame, text='Создать PDF с услугами', command=self.services_pdf_com)
          self.services_pdf_btn.pack(anchor='nw')
          self.serviceFrame.pack(anchor='nw', fill='x', padx=5, pady=5)


          self.pack(anchor='nw')

     def services_pdf_com(self):
          cursor = self.cursor

          pdf = PDF()
          cursor.execute(f'''
               SELECT *
               FROM tblServiceType
                         ''')

          service_types = cursor.fetchall()
          service_clients = {}
          finalizing_reports = {}
          for i in service_types:
               cursor.execute(f'''
                    SELECT CONCAT(c.txtClientSurname, ' ', c.txtClientName, ' ', c.txtClientSecondName),
                         c.txtClientAddress, c.txtClientPassportNumber,
                         SUM(s.intServiceCount), SUM(s.fltServiceSum)  
                    FROM tblService as s
                    JOIN tblVisit AS v ON v.intVisitId = s.intVisitId
                    JOIN tblClient AS c ON v.intClientId = c.intClientId
                    WHERE s.intServiceTypeId = {i[0]}
                    GROUP BY CONCAT(c.txtClientSurname, ' ', c.txtClientName, ' ', c.txtClientSecondName), c.txtClientAddress, c.txtClientPassportNumber
                              ''')
               service_clients[i[0]] = cursor.fetchall()
               finalizing_reports[i[0]] = (str(len(service_clients[i[0]])), str(sum(x[4] for x in service_clients[i[0]])))
               service_clients[i[0]].insert(0, ('Name', 'Address', 'Passport', 'Amount', 'Sum'))
               pdf.write(text=f"\nService: {i[1]}    Price: {i[2]}\n")
               pdf.create_table(service_clients[i[0]])
               
               pdf.write(text=f'\nAmount of clients: {finalizing_reports[i[0]][0]}  Final sum: {finalizing_reports[i[0]][1]}\n')

          unique_clients = set(y[0] for x in service_clients.items() for y in x[1][1:])
          average_service_cost = str("{:.2f}".format((sum(float(y[4]) / float(y[3]) for x in service_clients.items() for y in x[1][1:]) / sum(len(x[1:]) for x in service_clients.items()))))
          pdf.write(text='\n\n' + '-' * 80 + '\n\n')
          pdf.write(text='Clients: ')
          for client in unique_clients:
               pdf.write(text=f'{client}, ')
          pdf.write(text=f'\nAverage service cost: {average_service_cost}\n')
          pdf.output('Services.pdf')
          