'''
作业需求：
1、生成一副扑克牌（自己设计扑克牌的结构，小王和大王可以分别用14、15表示 ）

2、3个玩家(玩家也可以自己定义)

3、发牌规则
默认先给用户发一张牌，其中 J、Q、K、小王、大王代表的值为0.5，其他就是则就是当前的牌面值。
用户根据自己的情况判断是否继续要牌。
    要，则再给他发一张。（可以一直要牌，但是如果自己手中的牌总和超过11点，你的牌就爆掉了(牌面变成0)）
    不要，则开始给下个玩家发牌。（没有牌则则牌面默认是0）
如果用户手中的所有牌相加大于11，则表示爆了，此人的分数为0，并且自动开始给下个人发牌。

4、最终计算并获得每个玩家的分值，例如：
result = {
    "alex":8,
    "武沛齐":9,
    "李路飞":0
}

必备技术点：随机抽排
import random

total_poke_list = [("红桃", 1), ("黑桃", 2), ......,("大王", 15), ("小王", 14)]

# 随机生成一个数，当做索引。
index = random.randint(0, len(total_poke_list) - 1)
# 获取牌
print("抽到的牌为：", total_poke_list[index])
# 踢除这张牌
total_poke_list.pop(index)

print("抽完之后，剩下的牌为：", total_poke_list)
请补充完善你的代码
result = {}    # 存储最终各位玩家的得分
user_list = ["alex","武沛齐","李路飞"]
# 补充代码

'''
import random
#发牌
def draw_card(user, poke_list):
    n = 1   
    index = random.randint(0, len(poke_list) - 1) 
    card = poke_list.pop(index)
    score = card[1]
    if score > 10:
        a_score = 0.5
        print(f'{user}第{n}次抽到的牌为:',card,f'分数为：{a_score}分') 
    if 0 < score <= 10:
        a_score = score
        print(f'{user}第{n}次抽到的牌为:',card,f'分数为：{a_score}分') 
    while True:
        index = random.randint(0, len(poke_list) - 1)
        card = poke_list.pop(index)
        score = card[1] 
        user_info = input(f'{user}是否要继续抽牌？(Y/N)')
        if user_info.upper() == 'N':
            break
        else:
            n += 1
            if 0< score <= 10:
                a_score = a_score + score
                print(f'{user}第{n}次抽到的牌为:',card,f'分数为：{a_score}分') 
            if score > 10:
                a_score = a_score + 0.5
                print(f'{user}第{n}次抽到的牌为:',card,f'分数为：{a_score}分') 
            if a_score > 11:
                a_score = 0
                print('boom!')
                break
    return a_score
#比较大小
def get_winner(result):
    alex = result['alex']
    wu = result['武沛齐']
    lufi = result['李路飞']
    if alex >= wu and alex >= lufi:
        winner = 'alex'
    elif wu >= alex and wu >= lufi:
        winner = '武沛齐'
    else:
        winner = '李路飞'
    return winner
 #创建存储各位玩家最终得分的字典

if __name__ == '__main__':
    result = {}
    #创建一副扑克牌
    poke_list = [('红桃',1),('红桃',2),('红桃',3),('红桃',4),('红桃',5),('红桃',6),('红桃',7),('红桃',8),('红桃',9),('红桃',10),('红桃',11),('红桃',12),('红桃',13),
                ('黑桃',1),('黑桃',2),('黑桃',3),('黑桃',4),('黑桃',5),('黑桃',6),('黑桃',7),('黑桃',8),('黑桃',9),('黑桃',10),('黑桃',11),('黑桃',12),('黑桃',13),
                ('方块',1),('方块',2),('方块',3),('方块',4),('方块',5),('方块',6),('方块',7),('方块',8),('方块',9),('方块',10),('方块',11),('方块',12),('方块',13),
                ('梅花',1),('梅花',2),('梅花',3),('梅花',4),('梅花',5),('梅花',6),('梅花',7),('梅花',8),('梅花',9),('梅花',10),('梅花',11),('梅花',12),('梅花',13),
                ("大王", 15), ("小王", 14)]
    #三个玩家
    user_list = ["alex","武沛齐","李路飞"]
    for user in user_list:
        result[user] = draw_card(user, poke_list)
    winner = get_winner(result)
    print(f'游戏结束，alex的总分为：{result["alex"]}分，武沛齐的总分为：{result["武沛齐"]}分，李路飞的总分为:{result["李路飞"]}分,恭喜{winner}获得最终胜利！！！')
            
