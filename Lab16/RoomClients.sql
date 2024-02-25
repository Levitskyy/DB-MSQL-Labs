USE db;

GO

CREATE PROCEDURE GetRoomClientsNumber AS
BEGIN
    IF OBJECT_ID('tempdb..##RoomClients') IS NOT NULL
    BEGIN
    DROP TABLE ##RoomClients
    END

    CREATE TABLE ##RoomClients
    (intRoomId INT PRIMARY KEY,
    ClientsNumber INT)

    INSERT INTO ##RoomClients (intRoomId, ClientsNumber)
        SELECT intRoomNumber, COUNT(DISTINCT intClientId) AS ClientsNumber
        FROM tblVisit
        GROUP BY intRoomNumber
END;
    