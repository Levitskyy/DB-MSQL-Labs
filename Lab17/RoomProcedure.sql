USE db;

GO

CREATE PROCEDURE GetRoomInfo
@roomId INT
AS
BEGIN
    IF OBJECT_ID('tempdb..##RoomInfo') IS NOT NULL
    BEGIN
    DROP TABLE ##RoomInfo
    END
    IF OBJECT_ID('tempdb..##RoomClientsInfo') IS NOT NULL
    BEGIN
    DROP TABLE ##RoomClientsInfo
    END
    IF OBJECT_ID('tempdb..##RoomServiceInfo') IS NOT NULL
    BEGIN
    DROP TABLE ##RoomServiceInfo
    END

    CREATE TABLE ##RoomInfo
    (
        RoomNumber INT,
        Floor INT,
        RoomPrice DECIMAL(18, 2),
        RoomDescription NVARCHAR(100)
    )

    CREATE TABLE ##RoomClientsInfo
    (
        txtName NVARCHAR(100),
        txtAddress NVARCHAR(100),
        txtClientPassportNumber NVARCHAR(10),
        datBegin DATE,
        datEnd DATE
    )

    CREATE TABLE ##RoomServiceInfo
    (
        txtServiceName NVARCHAR(100),
        datService DATE,
        fltServiceSum DECIMAL(18, 2)
    )

    INSERT INTO ##RoomInfo (RoomNumber, Floor, RoomPrice, RoomDescription)
        SELECT TOP 1 intRoomNumber, intFloor, fltRoomPrice, txtRoomDescription
        FROM tblRoom
        WHERE intRoomNumber = @roomId

    INSERT INTO ##RoomClientsInfo (txtName, txtAddress, txtClientPassportNumber, datBegin, datEnd)
        SELECT
            C.txtClientSurname + ' ' + C.txtClientName + ' ' + C.txtClientSecondName AS FullName,
            C.txtClientAddress,
            C.txtClientPassportNumber,
            V.datBegin,
            V.datEnd
        FROM tblClient AS C
        JOIN tblVisit V ON V.intClientId = C.intClientId AND V.intRoomNumber = @roomId

    INSERT INTO ##RoomServiceInfo (txtServiceName, datService, fltServiceSum)
        SELECT
            ST.txtServiceTypeName,
            S.datServiceDate,
            S.fltServiceSum
        FROM tblService AS S
        JOIN tblVisit V ON V.intRoomNumber = @roomId AND V.intVisitId = S.intVisitId
        JOIN tblServiceType ST ON ST.intServiceTypeId = S.intServiceTypeId

END;
    