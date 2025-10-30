DROP DATABASE IF EXISTS qlxevalaixe;
CREATE DATABASE qlxevalaixe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE qlxevalaixe;

CREATE TABLE xebuyt(
    maxb VARCHAR(10) PRIMARY KEY,
    bienso VARCHAR(20) UNIQUE,
    hangxe VARCHAR(50) NOT NULL,
    soghe INT NOT NULL,
    tinhtrang VARCHAR(20) NOT NULL,
    namsx INT NOT NULL
);

CREATE TABLE taixe(
    maso VARCHAR(10) PRIMARY KEY,
    holot VARCHAR(50) NOT NULL,
    ten VARCHAR(20) NOT NULL,
    phai VARCHAR(5),
    ngaysinh DATE,
    sdt VARCHAR(15),
    banglai VARCHAR(10)
);

CREATE TABLE phancong(
    mapc INT AUTO_INCREMENT PRIMARY KEY,
    maxb VARCHAR(10) NOT NULL,
    maso VARCHAR(10) NOT NULL,
    ngayphancong DATE NOT NULL,
    trangthaichuyen VARCHAR(20) NOT NULL,
    giodi TIME,
    gioden TIME,
    
    FOREIGN KEY (maxb) REFERENCES xebuyt(maxb) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (maso) REFERENCES taixe(maso) ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO xebuyt (maxb, bienso, hangxe, soghe, tinhtrang, namsx) VALUES
('B001', '51B-123.45', 'Hyundai', 45, 'available', 2018),
('B002', '51B-999.88', 'Thaco', 35, 'maintenance', 2020), -- Xe này cần bảo trì
('B003', '51B-001.01', 'Isuzu', 45, 'available', 2019); -- Sửa lại thành 'available'
INSERT INTO taixe (maso, holot, ten, phai, ngaysinh, sdt, banglai) VALUES
('TX01', 'Nguyễn Văn', 'An', 'Nam', '1985-05-15', '0901234567', 'D'),
('TX02', 'Trần Thị', 'Bình', 'Nữ', '1990-11-20', '0918765432', 'E'),
('TX03', 'Lê Hữu', 'Cường', 'Nam', '1978-01-01', '0987654321', 'D');
INSERT INTO phancong (maxb, maso, ngayphancong, trangthaichuyen,giodi,gioden) VALUES
('B003', 'TX02', CURDATE(), 'Đã đi','7:00:00',null), 
('B001', 'TX01', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'Chưa đi','11:00:00','16:00:00');
SHOW TABLES;
SELECT * FROM xebuyt;	
SELECT * FROM taixe;	
SELECT * FROM phancong;
SHOW CREATE TABLE phancong;
