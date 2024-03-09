 -- ************** ГРУППЫ ********************
--создать группу пользователей на чтение users
CREATE ROLE users WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	NOINHERIT
	NOLOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;

--создать группу пользователей на чтение и запись admins
CREATE ROLE admins WITH 
	NOSUPERUSER
	CREATEDB
	NOCREATEROLE
	NOINHERIT
	NOLOGIN
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1;
	
--  ************* ПОЛЬЗОВАТЕЛИ *****************
--создать пользователя read / 1234567
CREATE ROLE "read" WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	inherit --с наследием
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	password '1234567'
	IN role users --добавить read в группу users 
	CONNECTION LIMIT -1;

--создать пользователя admin / admin1234567
CREATE ROLE "admin" WITH 
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	inherit --с наследием
	LOGIN
	NOREPLICATION
	NOBYPASSRLS
	password 'admin1234567'
	IN role admins --добавить admin в группу admins
	CONNECTION LIMIT -1;