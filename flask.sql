DROP DATABASE IF EXISTS flaskr;
CREATE DATABASE flaskr;
use flaskr;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username varchar(30) UNIQUE NOT NULL,
  password varchar(120) NOT NULL,
  adm boolean default false,
  master boolean default false
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  title varchar(50) NOT NULL,
  body  varchar(500) NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

select * from user inner join post on user.id = author_id;


insert into user(username, password)
values('admin', 'admin');

update user
set
adm = true,
master = true,
password = 'pbkdf2:sha256:260000$L9JTgrtvFs5I9MTJ$0fa29e1310e626a00889dfb4bd18d8eabf4f9efed8e90b77c025276c3b4e8baf'
where user.username='admin';

select * from user; 


SELECT username, adm
from user 
WHERE username !='admin'
ORDER BY id;


update user
set user.adm = True
where user.id = 3