
-- �Ыؤ��G��
CREATE TABLE Fruits (
    fruit_id INT IDENTITY(1,1) PRIMARY KEY, -- ���G�s�� (�D��)
    name NVARCHAR(50) NOT NULL, -- ���G�W��
    category NVARCHAR(50), -- ���G�����]�p���a���G�B�űa���G�^
    unit_price DECIMAL(10, 2), -- ���
    stock_quantity INT DEFAULT 0 -- �w�s�ƶq
);

-- �Ыب����Ӫ�
CREATE TABLE Suppliers (
    supplier_id INT IDENTITY(1,1) PRIMARY KEY, -- �����ӽs�� (�D��)
    name NVARCHAR(100) NOT NULL, -- �����ӦW��
    phone NVARCHAR(20), -- �q��
    email NVARCHAR(100), -- �q�l�l��
    address NVARCHAR(255) -- �a�}
);

-- �Ыضi�f�O����
CREATE TABLE Purchases (
    purchase_id INT IDENTITY(1,1) PRIMARY KEY, -- �i�f�s�� (�D��)
    fruit_id INT NOT NULL, -- ���G�s�� (�~��)
    supplier_id INT NOT NULL, -- �����ӽs�� (�~��)
    quantity INT NOT NULL, -- �i�f�ƶq
    purchase_date DATE NOT NULL, -- �i�f���
    total_cost DECIMAL(10, 2), -- �`����
    FOREIGN KEY (fruit_id) REFERENCES Fruits(fruit_id),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- �Ы��U�Ȫ�
CREATE TABLE Customers (
    customer_id INT IDENTITY(1,1) PRIMARY KEY, -- �U�Ƚs�� (�D��)
    name NVARCHAR(100) NOT NULL, -- �U�ȩm�W
    phone NVARCHAR(20), -- �q��
    email NVARCHAR(100), -- �q�l�l��
    address NVARCHAR(255) -- �a�}
);

-- �ЫؾP��O����
CREATE TABLE Sales (
    sale_id INT IDENTITY(1,1) PRIMARY KEY, -- �P��s�� (�D��)
    fruit_id INT NOT NULL, -- ���G�s�� (�~��)
    quantity INT NOT NULL, -- �P��ƶq
    sale_date DATE NOT NULL, -- �P����
    total_price DECIMAL(10, 2), -- �`����
    customer_id INT NOT NULL, -- �U�Ƚs�� (�~��)
    FOREIGN KEY (fruit_id) REFERENCES Fruits(fruit_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);


SELECT 
    FORMAT(S.sale_date, 'yyyy-MM') AS ���,  -- �榡�Ƭ� "YYYY-MM"
    SUM(S.total_price) AS ����`���J,      -- �P���`���J
    SUM(P.total_cost) AS ����`��X    -- �i�f�`��X
FROM Sales S
FULL OUTER JOIN Purchases P
    ON FORMAT(S.sale_date, 'yyyy-MM') = FORMAT(P.purchase_date, 'yyyy-MM')
GROUP BY FORMAT(S.sale_date, 'yyyy-MM')
ORDER BY ���;


