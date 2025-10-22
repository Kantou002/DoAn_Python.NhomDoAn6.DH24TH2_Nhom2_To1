create database qlxevalaixe character set utf8mb4 collate utf8mb4_unicode_ci;
use qlxevalaixe;
Create table xebuyt(
    maxb varchar(10) primary key,
    bienso varchar(20) unique,
    hangxe varchar(50) not null,
    soghe int not null,
    tinhtrang varchar(20) not null,
    namsx int not null
);
CREATE TABLE taixe (
    maso VARCHAR(10) PRIMARY KEY,
    holot VARCHAR(50) NOT NULL,
    ten VARCHAR(20) NOT NULL,
    phai VARCHAR(5),
    ngaysinh DATE,
    sdt VARCHAR(15),
    banglai VARCHAR(10)
);
drop table xebuyt;
show tables;
select * from xebuyt;	
select * from taixe;	
