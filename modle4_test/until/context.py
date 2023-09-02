class Context(object):
    '''实例化:文章，方法'''
    def __init__(self, text, method):
        self.text = text
        self.method = method

class User_dict(object):
    def __init__(self):
        self.id = None
        self.nickname = None

    def login(self, user_dict):
        self.id = user_dict['id']
        self.nickname = user_dict['nickname']

    def logined(self):
        if self.id:
            return True


class ArticleModel(object):
    """数据封装"""
    search_dict = {
        "title": "标题",
        "text": "内容",
        "read_count": "阅读数",
        "comment_count": "评论数",
        "up_count": "赞数",
        "down_count": "踩数",
        "nickname": "作者",
    }
    def __init__(self, row_dict):
        """
        row_dict是从数据库中查询出来的一行数据
        在db_acount的get方法中，查询出来的数据，通过ArticleModel类进行封装
        """
        # self.title = xxx
        # self.text = xxx
        for k in self.search_dict:
            setattr(self, k, row_dict.get(k))

    @classmethod
    def db_fields(cls):
        # title,text,read_count,comment_count,up_count,down_count,nickname
        result = ",".join([key for key in cls.search_dict])
        return result

    def show_page(self):
        """显示文章详情"""
        title_text_list = ["title", "text"]
        for i in title_text_list:
            value = getattr(self,i)
            print(f"{self.search_dict[i]}:{value}")
        commount_article_list = ["read_count", "comment_count", "up_count", "down_count", "nickname"]
        commount_list = []
        for k in commount_article_list:
            value = getattr(self,k)
            commount_list.append(f"{self.search_dict[k]}:{value}")
        count = " ".join(commount_list)
        print(count)

class UpDownModel(object):
    """数据封装"""
    fields = {
        "id": "ID",
        "choice": "赞或踩",  # 1，表示是赞；0，表示是踩
    }

    def __init__(self, row_dict):
        for k in self.fields:
            setattr(self, k, row_dict.get(k))
