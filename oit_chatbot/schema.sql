drop table if exists users;
drop table if exists unknown;
drop table if exists knowledge;

-- id is username
-- pwd is password for username
create table users (
	id text primary key,
	pwd text not null,
	lvl int not null
);

-- topic of unknown question
-- qualifier of unknown question
create table unknown (
	date datetime,
	topic text,
	qualifier text
);

-- topic is like, office hours
-- qualifier is dr niu's (office hours)
-- ex 2: topic=due date, qualifier=financial aid
-- WHICH|WHOSE $topic
create table knowledge (
	id integer primary key AUTOINCREMENT,
	topic text,
    qualifier text,
    answer text,
	lvl int, -- priviledge level
	count int -- keep track of how many times a question is asked 
);

