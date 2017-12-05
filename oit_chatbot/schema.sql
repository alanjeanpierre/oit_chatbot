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

-- topic is like, office hours
-- qualifier is dr niu's (office hours)
-- ex 2: topic=due date, qualifier=financial aid
-- WHICH|WHOSE $topic
create table knowledge (
	id int primary key,
	topic text,
    qualifier text,
    what text,
    where text,
    how text,
    when text,
    who text
	lvl int -- priviledge level
);

