CREATE PROCEDURE InsertIntoOrderCalc

AS

INSERT INTO OrderCalc (OrderId, CountofProduct, Amount)

SELECT

    OrderId,

    COUNT(OrderId) AS CountofProduct,

    SUM(UnitPrice * Quantity) AS Amount

FROM

OrderDetails

GROUP BY OrderId;

 

EXEC InsertIntoOrderCalc;

 

SELECT * FROM OrderCalc;