USE db;
SELECT
    C.txtClientSurname AS ClientSurname,
    V.fltRoomSum AS RoomSum,
    V.datBegin AS ArrivalDate
FROM
    tblVisit AS V
JOIN
    tblClient AS C ON V.intClientId = C.intClientId
WHERE
    (V.datBegin BETWEEN '2014-01-01' AND '2014-02-01' OR V.datBegin BETWEEN '2014-05-01' AND '2014-06-01')
    AND V.fltRoomSum BETWEEN 3000.00 AND 7000.00
ORDER BY
    V.datBegin ASC;
