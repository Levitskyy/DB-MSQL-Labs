USE db;
GO
CREATE TRIGGER trgPreventDuplicateServices
ON tblService
AFTER INSERT, UPDATE
AS
BEGIN
    IF (
        SELECT COUNT(*)
        FROM inserted I1
        JOIN inserted I2 ON I1.intServiceId <> I2.intServiceId
                         AND I1.intServiceTypeId = I2.intServiceTypeId
                         AND I1.intVisitId = I2.intVisitId
                         AND I1.datServiceDate = I2.datServiceDate
    ) > 1
    BEGIN
        THROW 50001, 'Дубликаты услуг одного типа в тот же день для одного клиента запрещены', 1
        ROLLBACK;
    END;

    IF EXISTS (
        SELECT 1
        FROM tblService S
        JOIN inserted I ON S.intServiceId <> I.intServiceId
                        AND S.intServiceTypeId = I.intServiceTypeId
                        AND S.intVisitId = I.intVisitId
                        AND S.datServiceDate = I.datServiceDate
    )
    BEGIN
        THROW 50000, 'Дубликаты услуг одного типа в тот же день для одного клиента запрещены', 1
        ROLLBACK;
    END;
END;