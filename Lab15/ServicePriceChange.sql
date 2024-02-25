USE db;
GO
CREATE TRIGGER trgServicePriceAdd
ON tblService
AFTER INSERT
AS
BEGIN
    UPDATE tblVisit
    SET tblVisit.fltServiceSum = tblVisit.fltServiceSum + I.TotalSum
    FROM tblVisit
    JOIN (
        SELECT intVisitId, SUM(fltServiceSum) AS TotalSum
        FROM inserted
        GROUP BY intVisitId
    ) I ON tblVisit.intVisitId = I.intVisitId
END;

GO

CREATE TRIGGER trgServicePriceDec
ON tblService
AFTER DELETE
AS
BEGIN
    UPDATE tblVisit
    SET tblVisit.fltServiceSum = tblVisit.fltServiceSum - D.TotalSum
    FROM tblVisit
    JOIN (
        SELECT intVisitId, SUM(fltServiceSum) AS TotalSum
        FROM deleted
        GROUP BY intVisitId
    ) D ON tblVisit.intVisitId = D.intVisitId
END;