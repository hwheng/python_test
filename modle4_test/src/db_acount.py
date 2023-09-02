import datetime
from src.dbtool import db
from until.context import ArticleModel,UpDownModel

# 登录
def login(username, password):
    result = db.fetch_one("select * from user where username=%(username)s and passwd=%(passwd)s", username=username, passwd=password)
    return result

# 注册
def register(user, pwd, nickname, mobile, email):
    result = db.exec("insert into user(username,passwd,nickname,mobile,email,ctime) values(%(username)s,%(passwd)s,%(nickname)s,%(mobile)s,%(email)s,%(ctime)s)", username=user, passwd=pwd, nickname=nickname, mobile=mobile, email=email, ctime=datetime.datetime.now())
    return result

# 发布
def publish_blog(title, text, user_id):
    """发布博客功能"""
    result = db.exec("insert into article(title,text,user_id,ctime) values(%(title)s,%(text)s,%(user_id)s,%(ctime)s)", title=title, text=text, user_id=user_id, ctime=datetime.datetime.now())
    return result

# 查看所有文章以及文章详情
def search_page_all():
    result = db.fetch_one("select count(1) as ct from article") # 获取总条数
    if not result:
        return 0
    if result['ct']: # result = {"ct": 总条数}
        return result['ct']

def page_list(page_count, this_page):
    result = db.fetch_all("select id,title from article order by id desc limit %(page_count)s offset %(this_page)s", page_count=page_count, this_page=this_page)
    return result

def get(id):
    # 获取文章的标题，正文，作者，发布时间，阅读量，点赞数，踩数
    # 在数据库中得到出对应行的数据
    # select article.title,article.text,article.read_count,article.up_count,article.down_count,user.nickname from article left join user on article.user_id=user.id where article.id=%(id)s
    # ArticleModel.db_fields() = "title,text,read_count,up_count,down_count,nickname"
    result = db.fetch_one(f"select {ArticleModel.db_fields()} from article left join user on article.user_id=user.id where article.id=%(id)s",id=id)
    if not result:
        return None
    # 数据封装
    return ArticleModel(result)

def read_count_up(id):
    db.exec("update article set read_count=read_count+1 where id=%(id)s", id=id)

def comment_up(user_id, article_id, comment):
    """添加评论"""
    result = db.exec("insert into comment(content,article_id,user_id,ctime) values(%(content)s,%(article_id)s,%(user_id)s,%(ctime)s)", content=comment, article_id=article_id, user_id=user_id, ctime=datetime.datetime.now())
    db.exec("update article set comment_count=comment_count+1 where id=%(id)s", id=article_id)
    return result

# 点赞&&点踩
def feach_up_down(user_id, article_id):
    result = db.fetch_one("select id,choice from up_down where user_id=%(user_id)s and article_id=%(article_id)s", user_id=user_id, article_id=article_id)
    if result:
        # 返回一个封装值
        return UpDownModel(result)
def feach_up(user_id, article_id):
    result = db.exec("insert into up_down(user_id,article_id,choice,ctime) values(%(user_id)s,%(article_id)s,%(choice)s,%(ctime)s)", user_id=user_id,article_id=article_id,choice=1,ctime=datetime.datetime.now())
    db.exec("update article set up_count=up_count+1 where id = %(id)s",id=article_id)
    return result
def feach_down(user_id, article_id):
    result = db.exec(
        "insert into up_down(user_id,article_id,choice,ctime) values(%(user_id)s,%(article_id)s,%(choice)s,%(ctime)s)",
        user_id=user_id, article_id=article_id, choice=0, ctime=datetime.datetime.now())
    db.exec("update article set down_count=down_count+1 where id = %(id)s", id=article_id)
    return result
def update_down_to_up(aid, id):
    result = db.exec("update up_down set choice=1 where id=%(id)s and article_id=%(article_id)s", id=id, article_id=aid)
    db.exec("update article set up_count=up_count+1,down_count=down_count-1 where id=%(id)s", id=aid)
    return result
def update_up_to_down(aid, id):
    result = db.exec("update up_down set choice=0 where user_id=%(id)s and article_id=%(article_id)s", id=id, article_id=aid)
    db.exec("update article set up_count=up_count-1,down_count=down_count+1 where id=%(id)s",id=aid)
    return result