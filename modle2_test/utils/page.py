'''
分页看新闻（每页显示10条），提示用户输入页码，根据页码显示指定页面的数据。

- 提示用户输入页码，根据页码显示指定页面的数据。
- 当用户输入的页码不存在时，默认显示第1页
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def get_page(page_num,per_page_count):
    '''获取要展示的页面列表
    :param page_num:页码
    :param per_page_count:每页数据条数
    :return:数据列表
    '''
    # 开始位置
    start_index = (page_num - 1) * per_page_count
    # 结束位置
    end_index = page_num * per_page_count
    data_list = []
    # 定义一个索引位置
    read_row_count = 0
    with open(f'{config.CSV_FILE_PATH}\Video.csv', mode='r', encoding='utf-8') as file_object:
        for line in file_object:
            # 索引值在开始和结束间，就加入列表中 
            if start_index <= read_row_count < end_index:
                data_list.append(line.strip())
            if read_row_count >= end_index:
                break
            read_row_count += 1
    return data_list

def show_table(page_num, per_page_count, data_list):
    """ 在页面展示分页信息（输出）
    :param page_num:页码
    :param per_page_count:每页数据条数
    :param data_list:
    :return:
    """
    row_list = []
    index = (page_num - 1) * per_page_count + 1
    # 遍历 data_list 列表，并打印每行的行号和第二个元素：
    for num, line in enumerate(data_list, index):
        row_list = line.split(',')
        print(num, row_list[1])

def news_ready():
    print('分页看新闻模块（每页显示10条）')
    # 每页显示10条 & 总数据LEN_LINE_IN_CSV条
    per_page_count, total_count = 10 , config.LEN_LINE_IN_CSV
    # 计算页码最大值
    max_page_num, remainder = divmod(total_count, per_page_count)
    # print(max_page_num,remainder)
    #如果有余数，那么就加多一页
    if remainder:
        max_page_num += 1
    while True:
        page_info = input(f'请输入页码(范围：{1}-{max_page_num}):(输入Q/q返回上一级)')
        if page_info.upper() == 'Q':
            back = 1
            return back
        if not page_info.isdecimal():
            print("页码错误，请重新输入！")
            continue
        num = int(page_info)
        if num <1 or num > max_page_num:
            num = 1
        page_str = f'第{num}页'
        print(page_str)
        item = get_page(num,per_page_count)
        show_table(num, per_page_count, item)

        