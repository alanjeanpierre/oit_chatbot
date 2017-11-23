drop table if exists users;
drop table if exists logs;
drop table if exists knowledge;
create table users (
	id text primary key,
	pwd text not null,
	lvl int not null
);

create table logs (
	date datetime,
	id int,
	lvl int
);

create table knowledge (
	id int,
	answer text,
	lvl int
);

