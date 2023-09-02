表设计参照`myblog.xlsx`，创建数据库代码如下：

```sql
create database blogdb DEFAULT CHARSET utf8 COLLATE utf8_general_ci; -- 创建数据库

use blogdb;

create table user(
    -- user	table
	id int not null auto_increment primary key,
    username varchar(16) not null,
    nickname varchar(16) not null,
    passwd varchar(64) not null,
    mobile char(11) not null,
    email varchar(64) not null,
    ctime datetime not null
)default charset=utf8;

create index ix_user_pwd on user(username,passwd); -- 创建联合索引
create unique index ix_nickname on user(nickname); -- 创建唯一索引
create unique index ix_mobile on user(mobile); -- 创建唯一索引

create table article(
    -- article table
	id int not null auto_increment primary key,
    title varchar(255) not null,
    text text not null,
	read_count int default 0,
	comment_count int default 0,
	up_count int default 0,
	down_count int default 0,
    user_id int not null,
    ctime datetime not null,
    constraint fk_article_user foreign key (user_id) references user(id) -- 设置外键user_id
)default charset=utf8;

create table comment(
    -- comment table
    id int not null auto_increment primary key,
    content varchar(255) not null,
    user_id int not null,
	article_id int not null,
    ctime datetime not null,
    constraint fk_comment_user foreign key (user_id) references user(id), -- 设置外键user_id
    constraint fk_comment_article foreign key (article_id) references article(id) -- 设置外键article_id
)default charset=utf8;

create table up_down(
    -- up_down table
    id int not null auto_increment primary key,
    choice tinyint not null,
    user_id int not null,
	article_id int not null,
    ctime datetime not null,
    constraint fk_up_down_user foreign key (user_id) references user(id), -- 设置外键user_id
    constraint fk_up_down_article foreign key (article_id) references article(id) -- 设置外键article_id
)default charset=utf8;
	
create unique index ix_user_article on up_down(user_id,article_id); -- 创建联合唯一索引
```

需要修改相关配置的路径：`/config/setting`

启动：

```python
python3.11 main.py
```

