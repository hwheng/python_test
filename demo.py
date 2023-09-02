import pymysql

def csv():
    """处理csv文件"""
    data_list = []
    with open('db.csv', 'r',encoding='utf-8') as f:
        for line in f:
            num, others= line.strip().split(',',maxsplit=1)
            title, url = others.strip().split(',', maxsplit=1)
            db(num, title, url)


def db(*args):
    """存入数据库"""
    conn = pymysql.connect(host='123.207.74.26', port=3306, user='root', passwd='Cloud12#$', charset="utf8", db="DEMOdb")
    cursor = conn.cursor()
    sql = "insert into demo (num, title, url) values (%s, %s, %s);"
    cursor.execute(sql, args)
    conn.commit()
if __name__ == '__main__':
    csv()