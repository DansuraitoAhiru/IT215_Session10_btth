create database ecommerce_db;
use ecommerce_db;

create table shipments (
	id int primary key auto_increment,
    tracking_number varchar(50) not null,
    status varchar(50) default 'PREPARING'
);