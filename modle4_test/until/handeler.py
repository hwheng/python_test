import time
from src import db_acount
from until.context import Context, User_dict


class handeler(object):

    def __init__(self):
        self.NAV = []
        self.LOGIN_USER_DICT = User_dict()

    def wapper(self, method):
        """装饰器"""

        def inner(*args, **kwargs):
            print(" > ".join(self.NAV).center(50, "*"))
            res = method(*args, **kwargs)
            self.NAV.pop(-1)
            return res

        return inner

    def login(self):
        """登录模块"""
        while True:
            user_info = input("请输入用户名(Q/q退出)：")
            if not user_info:
                continue
            if user_info.upper().strip() == 'Q':
                return
            password = input("请输入密码：")
            user_dict = db_acount.login(user_info, password)
            if not user_dict:
                print("用户名或密码错误，请重新输入。")
                continue
            print("登录成功")
            self.LOGIN_USER_DICT.login(user_dict)
            self.NAV.insert(0, self.LOGIN_USER_DICT.nickname)
            return

    def register(self):
        """注册模块"""
        while True:
            user_info = input("请输入用户名(Q/q退出)：")
            if not user_info:
                print("用户名不能为空，请重新输入。")
                continue
            if user_info.upper().strip() == 'Q':
                return
            password = input("请输入密码：")
            if not password:
                print("密码不能为空，请重新输入。")
                continue
            nickname = input("请输入昵称：")
            if not nickname:
                print("昵称不能为空，请重新输入。")
                continue
            mobile = input("请输入手机号：")
            if not mobile:
                print("手机号不能为空，请重新输入。")
                continue
            email = input("请输入邮箱：")
            if not email:
                print("邮箱不能为空，请重新输入。")
                continue

            user_register_dict = db_acount.register(user_info, password, nickname, mobile, email)
            if not user_register_dict:
                print("注册失败，请重新注册。")
                continue
            print("注册成功，请使用新账户去登录。")
            return

    def publish_blog(self):
        """发布博客模块"""
        if not self.LOGIN_USER_DICT.logined():  # 判断是否登录
            time.sleep(1)
            print("未登录用户不允许发布博客，请登录后再访问。")
            return
        while True:
            title = input("请输入标题：")
            if not title:
                print("标题不能为空，请重新输入。")
                continue
            if title.upper().strip() == 'Q':
                print("退出发布博客模块。")
                return
            text = input("请输入正文：")
            if not text:
                print("正文不能为空，请重新输入。")
                continue
            is_blog = db_acount.publish_blog(title, text, self.LOGIN_USER_DICT.id)
            if not is_blog:  # 标题，正文，用户id
                print("发布失败，请重新发布")
                continue
            print("发布成功，可进入博客列表查看")
            return

    def view_blog(self):
        """
        分页：10行一页
        查看博客列表，显示博客标题、创建时间、阅读数量、评论数量等
        """
        # 分页操作
        view_blog_page = db_acount.search_page_all()
        # 10行一页
        page_count = 10
        max_page_num, div = divmod(view_blog_page, page_count)
        if div:
            max_page_num += 1
        # 当前页
        tager_page_num = 1

        if not max_page_num:
            print("系统当前暂无文章")
            return
        count = 0
        while True:
            """查看当前页文章列表，查看文章详细"""
            if count:
                print(" > ".join(self.NAV).center(50, "*"))
            count += 1

            data_list = db_acount.page_list(page_count, (tager_page_num - 1) * page_count)
            for kwargs in reversed(data_list):  # 倒叙输出：1 2 3 顺序输出：3 2 1
                print("{id}.{title}".format(**kwargs))
            print(
                f"\n当前页数：{tager_page_num}，总页数：{max_page_num}\n注意：输入p数字格式，表示翻页； 仅数字表示文章ID，可查看文章详细。\n")
            info = input("请输入(Q/q退出)：").strip()
            if info.upper().strip() == "Q":
                return
            if info.startswith("p"):
                tager_page = int(info[1:])
                if 0 < tager_page <= max_page_num:
                    tager_page_num = tager_page
                continue
            # 查看文章详细
            if not info.isalnum():
                print("输入错误，请重新输入。")
                continue
            article_id = int(info)
            article_obj = db_acount.get(article_id)
            if not article_obj:
                print("文章不存在，请重新输入。")
                continue
            self.NAV.append("文章详情页")
            self.wapper(self.article_show)(article_id, article_obj)

    def article_show(self, article_id, article_obj):
        """
        展示文章详情
        article_id = 目标文章ID
        article_obj = 一共被封装的值
        """
        article_obj.show_page()
        # 阅读数+1
        db_acount.read_count_up(article_id)

        def up():
            # 显示是否有点赞
            updown_obj = db_acount.feach_up_down(self.LOGIN_USER_DICT.id, article_id)
            if not updown_obj:
                if db_acount.feach_up(self.LOGIN_USER_DICT.id, article_id):
                    print("点赞成功")
                else:
                    print("点赞失败")
                return
            if updown_obj.choice == '1':
                print("已赞过，不能重复操作")
                return

            if db_acount.update_down_to_up(article_id, updown_obj.id):
                print("点赞成功")
            else:
                print("点赞失败")

        def down():
            updown_obj = db_acount.feach_up_down(self.LOGIN_USER_DICT.id, article_id)
            if not updown_obj:
                if db_acount.feach_down(self.LOGIN_USER_DICT.id, article_id):
                    print("点踩成功")
                else:
                    print("点踩失败")
                return
            if updown_obj.choice == '1':
                print("已踩过，不能重复操作")
                return

            if db_acount.update_up_to_down(article_id, updown_obj.id):
                print("点踩成功")
            else:
                print("点踩失败")

        def comm():
            comment = input("请输入要评论的内容：")
            result = db_acount.comment_up(self.LOGIN_USER_DICT.id, article_id, comment)
            if not result:
                print("评论失败...")
            else:
                print("评论成功...")

        mapping = {
            "1": Context('评论', comm),
            "2": Context('点赞', up),
            "3": Context('踩', down),
        }
        # 获取字典mapping中所有键值并拼接成字符串{k}.{v.text}
        message = " ".join(["{}.{}".format(k, v.text) for k, v in mapping.items()])
        while True:
            print(message)
            choice = input("请输入：(Q/q退出)")
            if choice.upper().strip() == 'Q':
                break
            if not self.LOGIN_USER_DICT.logined():
                print("用户未登录，请登录后重试...")
                time.sleep(1)
                return
            if not choice.isalnum():
                print("输入错误，请重新输入。")
                continue
            choice_get = mapping.get(choice)
            if not choice_get:
                print('输入错误，请重新输入。')
                continue
            choice_get.method()

    def run(self):
        """主程序"""
        self.NAV.append("系统首页")

        mapping = {
            "1": Context('用户登录', self.wapper(self.login)),
            "2": Context('用户注册', self.wapper(self.register)),
            "3": Context('发布博客', self.wapper(self.publish_blog)),
            "4": Context('查看文章', self.wapper(self.view_blog)),
        }

        # 获取字典mapping中所有键值并拼接成字符串{k}.{v.text}
        message = "\n".join(["{}.{}".format(k, v.text) for k, v in mapping.items()])

        while True:
            print(" > ".join(self.NAV).center(50, "*"))
            print(message)
            choice = input("请输入序号：").strip()
            if not choice:
                continue

            if choice.upper().strip() == "Q":
                print('bye~~')
                return

            context = mapping.get(choice)
            if not context:
                print("序号输入错误，请重新输入。\n")
                continue

            self.NAV.append(context.text)
            context.method()


obj = handeler()
