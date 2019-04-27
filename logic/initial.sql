drop table if exists oj_user;
create table oj_user(
ur_id INTEGER primary key AUTOINCREMENT,
name text not null,
password text not null,
school text,
grade text,
telephone text,
attempt int,
ac int,
isadmin int
);

drop table if exists oj_problem;

create table oj_problem(
pr_id INTEGER primary key AUTOINCREMENT,
title string not null,
img_url string,
txt_url string,
pdf_url string,
class string,
pro_level string,
tag string,
input_url string,
output_url string
);
