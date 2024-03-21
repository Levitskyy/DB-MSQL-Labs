from pyodbc import *

def tab1_get_values(cursor: Cursor):
    cursor.execute('''
                   SELECT tblVisit.datBegin, tblVisit.datEnd,
                   tblClient.txtClientSurname, tblClient.txtClientName, tblClient.txtClientSecondName,
                   tblVisit.intRoomNumber, tblRoom.intFloor, tblVisit.fltRoomSum, tblVisit.intVisitId, tblClient.intClientId
                   FROM tblVisit
                   JOIN tblClient ON tblVisit.intClientId = tblClient.intClientId
                   JOIN tblRoom ON tblVisit.intRoomNumber = tblRoom.intRoomNumber ''')
    return cursor.fetchall()

def get_all_clients(cursor: Cursor):
    cursor.execute('''
                   SELECT 
                   tblClient.intClientId, tblClient.txtClientSurname, tblClient.txtClientName, tblClient.txtClientSecondName
                   FROM tblClient
                    ''')
    return cursor.fetchall()

def add_new_visit(cursor: Cursor, clientId, roomNumber, dateBegin, dateEnd, roomSum, serviceSum):
    print(dateBegin)
    print(dateEnd)
    cursor.execute(f'''
                   INSERT INTO tblVisit VALUES
                   ({clientId}, {roomNumber}, '{dateBegin}', '{dateEnd}', {roomSum}, {serviceSum})
                   ''')
    cursor.commit()

def get_client_by_id(cursor: Cursor, clientId):
    cursor.execute(f'''
                   SELECT txtClientSurname, txtClientName, txtClientSecondName, txtClientAddress, txtClientPassportNumber
                   FROM tblClient
                   WHERE intClientId = {clientId}''')
    return cursor.fetchone()

def get_service_by_visit_id(cursor: Cursor, visitId):
    cursor.execute(f'''
                   SELECT st.txtServiceTypeName, s.intServiceCount, s.fltServiceSum, s.datServiceDate, st.fltServiceTypePrice
                   FROM tblService AS s
                   JOIN tblServiceType AS st ON s.intServiceTypeId = st.intServiceTypeId
                   WHERE s.intVisitId = {visitId}
                   ''')
    return cursor.fetchall()

def get_new_service_window_info(cursor: Cursor, visitId):
    cursor.execute(f'''
                   SELECT c.txtClientSurname, c.txtClientName, c.txtClientSecondName,
                          v.intRoomNumber, v.datBegin, v.datEnd
                   FROM tblVisit AS v
                   JOIN tblClient AS c ON v.intClientId = c.intClientId
                   WHERE v.intVisitId = {visitId}
                   ''')
    return cursor.fetchone()

def get_all_service_types(cursor: Cursor):
    cursor.execute('''
                   SELECT 
                   intServiceTypeId, txtServiceTypeName
                   FROM tblServiceType
                    ''')
    return cursor.fetchall()

def get_service_price_list(cursor: Cursor):
    cursor.execute('''
                   SELECT 
                   fltServiceTypePrice
                   FROM tblServiceType
                   ORDER BY intServiceTypeId
                    ''')
    return cursor.fetchall()

def new_service(cursor: Cursor, serviceType, visitId, serviceCount, serviceSum, serviceDate):
    cursor.execute(f'''
                   INSERT INTO tblService VALUES
                   ({serviceType}, {visitId}, {serviceCount}, {serviceSum}, '{serviceDate}')
                   ''')    
    cursor.commit()