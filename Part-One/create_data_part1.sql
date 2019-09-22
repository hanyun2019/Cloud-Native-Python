# Haowen Huang modified on Sep 21, 2019
# Implementation of Cloud Native web applications
# Part One: Developing a RESTful micro service in Python 
# 
# Create the tables and insert the sample data for Part One Demo
#

$sqlite3
sqllite>.open mydb.db
        create table apirelease(
            buildtime date,
            version varchar(30) primary key,
            links varchar2(30), 
            methods varchar2(30)
        );

        insert into apirelease values('2019-09-21 10:00:00', "v1", "api/v1/users", "get, post, put, delete");

        create table users(
            username varchar2(30),
            emailid varchar2(30),
            password varchar2(30), 
            full_name varchar(30),
            id integer primary key autoincrement)
        );

        insert into users values("haowen", "popkee@126.com", "haowen123","Haowen Huang", 1)


$sqlite3
sqlite>.open mydb.db
        create table tweets(
            id integer primary key autoincrement,
            username varchar2(30),
            body varchar2(30),
            tweet_time date
        );
