
-- 創建水果表
CREATE TABLE Fruits (
    fruit_id INT IDENTITY(1,1) PRIMARY KEY, -- 水果編號 (主鍵)
    name NVARCHAR(50) NOT NULL, -- 水果名稱
    category NVARCHAR(50), -- 水果類型（如熱帶水果、溫帶水果）
    unit_price DECIMAL(10, 2), -- 單價
    stock_quantity INT DEFAULT 0 -- 庫存數量
);

-- 創建供應商表
CREATE TABLE Suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY, -- 供應商編號 (主鍵)
    name NVARCHAR(100) NOT NULL, -- 供應商名稱
    phone NVARCHAR(20), -- 電話
    email NVARCHAR(100), -- 電子郵件
    address NVARCHAR(255) -- 地址
);

-- 創建進貨記錄表
CREATE TABLE Purchases (
    purchase_id INT IDENTITY(1,1) PRIMARY KEY, -- 進貨編號 (主鍵)
    fruit_id INT NOT NULL, -- 水果編號 (外鍵)
    supplier_id INT NOT NULL, -- 供應商編號 (外鍵)
    quantity INT NOT NULL, -- 進貨數量
    purchase_date DATE NOT NULL, -- 進貨日期
    total_cost DECIMAL(10, 2), -- 總成本
    FOREIGN KEY (fruit_id) REFERENCES Fruits(fruit_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- 創建顧客表
CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY, -- 顧客編號 (主鍵)
    name NVARCHAR(100) NOT NULL, -- 顧客姓名
    phone NVARCHAR(20), -- 電話
    email NVARCHAR(100), -- 電子郵件
    address NVARCHAR(255) -- 地址
);

-- 創建銷售記錄表
CREATE TABLE Sales (
    sale_id INT IDENTITY(1,1) PRIMARY KEY, -- 銷售編號 (主鍵)
    fruit_id INT NOT NULL, -- 水果編號 (外鍵)
    quantity INT NOT NULL, -- 銷售數量
    sale_date DATE NOT NULL, -- 銷售日期
    total_price DECIMAL(10, 2), -- 總價格
    customer_id INT NOT NULL, -- 顧客編號 (外鍵)
    FOREIGN KEY (fruit_id) REFERENCES Fruits(fruit_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);


SELECT 
    FORMAT(S.sale_date, 'yyyy-MM') AS 月份,  -- 格式化為 "YYYY-MM"
    SUM(S.total_price) AS 月份總收入,      -- 銷售總收入
    SUM(P.total_cost) AS 月份總支出    -- 進貨總支出
FROM Sales S
FULL OUTER JOIN Purchases P
    ON FORMAT(S.sale_date, 'yyyy-MM') = FORMAT(P.purchase_date, 'yyyy-MM')
GROUP BY FORMAT(S.sale_date, 'yyyy-MM')
ORDER BY 月份;


