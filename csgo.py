import asyncio
import base64
import os
import random
from re import T, match
import sqlite3
from datetime import datetime, timedelta
from io import SEEK_CUR, BytesIO
from time import sleep
from PIL import Image
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import copy
import json
import math
import pytz
import nonebot
from nonebot import on_command, on_request
from hoshino import sucmd
from nonebot import get_bot
from hoshino.typing import NoticeSession
from hoshino import R


DB_PATH = os.path.expanduser('~/.q2bot/csgo.db')
# 存储本玩法数据
class getcsgo:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_num()
        
        

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_num(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CSGO
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CSGOLEVEL
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_num(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGO (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_num(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM CSGO WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGO (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGO (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

    def _set_level(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_level(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM CSGOLEVEL WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_level(self, gid, uid, num1, num2):
        num = self._get_level(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_level(self, gid, uid, num1, num2):
        num = self._get_level(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM CSGO WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')
#获取列表
    def _get_uid_level_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM CSGOLEVEL WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

DB_PATH2 = os.path.expanduser('~/.q2bot/shichang.db')
# 玩家库存
class shichang:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH2), exist_ok=True)
        self._create_num()
        
        

    def _connect(self):
        return sqlite3.connect(DB_PATH2)

    def _create_num(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SHICHANG
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_num(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHICHANG (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_num(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM SHICHANG WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHICHANG (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHICHANG (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM SHICHANG WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

DB_PATH3 = os.path.expanduser('~/.q2bot/shopnew.db')
# 新商店
class shopnew:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH3), exist_ok=True)
        self._create_num()
        
        

    def _connect(self):
        return sqlite3.connect(DB_PATH3)

    def _create_num(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SYSNUM
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_num(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_num(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM SYSNUM WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM SYSNUM WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

chest = {100000001001:'命悬一线武器箱',100000001002:'梦魇武器箱'}

arc_chest = {'命悬一线武器箱':100000001001,'梦魇武器箱':100000001002}

gun_id = {1001:'PP-野牛 | 黑夜暴乱',
1002:'FN57 | 焰色反应',
1003:'MP9 | 黑砂',
1004:'P2000 | 都市危机',
1005:'R8 左轮手枪 | 稳',
1006:'SG 553 | 阿罗哈',
1007:'XM1014 | 锈蚀烈焰',
1008:'FN57 | 涂鸦潦草',
1009:'MAC-10 | 坐牢',
1010:'MAG-7 | 先见之明',
1011:'MP5-SD | 小小噩梦',
1012:'P2000 | 升天',
1013:'SCAR-20 | 暗夜活死鸡',
1014:'截短霰弹枪 | 灵应牌',

2001:'格洛克 18 型 | 城里的月光',
2002:'内格夫 | 狮子鱼',
2003:'新星 | 狂野六号',
2004:'MAG-7 | SWAG-7',
2005:'UMP-45 | 白狼',
2006:'PP-野牛 | 太空猫',
2007:'G3SG1 | 梦之林地',
2008:'M4A1 消音型 | 夜无眠',
2009:'XM1014 | 行尸攻势',
2010:'USP 消音版 | 地狱门票',

3001:'AUG | 湖怪鸟',
3002:'AWP | 死神',
3003:'USP 消音版 | 脑洞大开',
3004:'双持贝瑞塔 | 瓜瓜',
3005:'法玛斯 | 目皆转睛',
3006:'MP7 | 幽幻深渊',

4001:'M4A4 | 黑色魅影',
4002:'MP7 | 血腥运动',
4003:'AK-47 | 夜愿',
4004:'MP9 | 星使',

5001:'超稀有手套',
5002:'极其罕见的特殊物品',
}

arc_gun_id = {'PP-野牛 | 黑夜暴乱':1001,
'FN57 | 焰色反应':1002,
'MP9 | 黑砂':1003,
'P2000 | 都市危机':1004,
'R8 左轮手枪 | 稳':1005,
'SG 553 | 阿罗哈':1006,
'XM1014 | 锈蚀烈焰':1007,
'FN57 | 涂鸦潦草':1008,
'MAC-10 | 坐牢':1009,
'MAG-7 | 先见之明':1010,
'MP5-SD | 小小噩梦':1011,
'P2000 | 升天':1012,
'SCAR-20 | 暗夜活死鸡':1013,
'截短霰弹枪 | 灵应牌':1014,

'格洛克 18 型 | 城里的月光':2001,
'内格夫 | 狮子鱼':2002,
'新星 | 狂野六号':2003,
'MAG-7 | SWAG-7':2004,
'UMP-45 | 白狼':2005,
'PP-野牛 | 太空猫':2006,
'G3SG1 | 梦之林地':2007,
'M4A1 消音型 | 夜无眠':2008,
'XM1014 | 行尸攻势':2009,
'USP 消音版 | 地狱门票':2010,

'AUG | 湖怪鸟':3001,
'AWP | 死神':3002,
'USP 消音版 | 脑洞大开':3003,
'双持贝瑞塔 | 瓜瓜':3004,
'法玛斯 | 目皆转睛':3005,
'MP7 | 幽幻深渊':3006,

'M4A4 | 黑色魅影':4001,
'MP7 | 血腥运动':4002,
'AK-47 | 夜愿':4003,
'MP9 | 星使':4004,

'超稀有手套':5001,
'极其罕见的特殊物品':5002,
}

use_time_id = {1:'崭新出厂',2:'略有磨损',3:'久经沙场',4:'破损不堪',5:'战痕累累'}
stattrak_id = {0:'',1:'（StatTrak™）'}
level_id = {1:'蓝',2:'紫',3:'粉',4:'红',5:'金'}
arc_level_id = {'蓝':1,'紫':2,'粉':3,'红':4,'金':5}

have_id = {
100000:'崭新出厂',110000:'（StatTrak™）',
200000:'略有磨损',210000:'（StatTrak™）',
300000:'久经沙场',310000:'（StatTrak™）',
400000:'破损不堪',410000:'（StatTrak™）',
500000:'战痕累累',510000:'（StatTrak™）'
}

sv = Service('csgo')
sv2 = Service('csgo炼金', enable_on_default=False)    
#炼金指令最后更新时间为2022年10月31日，由于机器人于11月2日停止服务，不再提供后续更新，小狐已经为主人默认关闭此服务，需要的话再用lssv开启哦~❤
# create by hu-bao  2022年11月1日

@sv.on_rex(r'^go开箱(.*)$')
async def kaixiang(bot,ev:CQEvent):
    gid = ev.group_id
    uid = ev.user_id
    csgo = getcsgo()
    sc = shichang()
    shop = shopnew()
    if csgo._get_num(0,0,0) == 1:
        await bot.finish(ev,'有人正在炼金中！')
    if csgo._get_num(0,0,1) == 1:
        await bot.finish(ev,'有人正在开箱中！')
    open_chest_id =csgo._get_num(0,uid,1) #查询箱子ID
    if open_chest_id ==0: #没指定箱子ID
        csgo._set_num(0,uid,1,100000001001)
        open_chest_id ==100000001001
    match = (ev['match'])
    id = match.group(1)
    if id == '': 
        await bot.finish(ev,'未输入开启数量，请在后面加数字，例：<go开箱999>')
    id = int(id)
    if id >999:
        await bot.finish(ev,'开启数量超过上限999，拒绝开启！')
    open_chest_num = shop._get_num(0,uid,open_chest_id) #查询箱子数量
    if open_chest_num < id: #箱子数量不足
        open_chest_name = chest[open_chest_id]
        await bot.finish(ev,f'物品 {open_chest_name} 不足：{id}/{open_chest_num}\n你可以使用<设置箱子[箱子ID]>更换开启的箱子\n※刚玩不久两手空空？使用<go新手礼包>吧！')
    key = shop._get_num(0,uid,100000001000)
    if key < id:#钥匙不足
        await bot.finish(ev,f'钥匙不足：{id}/{key}')
    #检测完后开箱
    await bot.send(ev,'哐哐~开启中...')
    csgo._set_num(0,0,1,1) #锁
    msg = '开启完成：\n'
    blue = purple = pink = red = gold = addxp = new_blue = new_purple = new_pink = new_red = new_gold = 0
    num_w = 1
    while num_w <= id: 
        await asyncio.sleep(0.1)
        #检测开启进度
        num_f = int(id / 2)
        if num_w == num_f:
            await bot.send(ev,f'已开启{num_w}个，还请耐心等待')
        #展示结果
        num = random.randint(0,100) #生成随机数，决定武器品质
        #检索武器箱
        if open_chest_id == 100000001001: 
            gun_list1 = [1001,1002,1003,1004,1005,1006,1007]
            gun_list2 = [2001,2002,2003,2004,2005]
            gun_list3 = [3001,3002,3003]
            gun_list4 = [4001,4002]
            gun_list5 = 5001
        if open_chest_id == 100000001002:
            gun_list1 = [1008,1009,1010,1011,1012,1013,1014]
            gun_list2 = [2006,2007,2008,2009,2010]
            gun_list3 = [3004,3005,3006]
            gun_list4 = [4003,4004]
            gun_list5 = 5002
        #出货检索
        if num <=79: #蓝色
            gun_level = 1
            gun_name_id = random.choice(gun_list1)
            blue +=1
        elif 79<num<=95: #紫色
            gun_level = 2
            gun_name_id = random.choice(gun_list2)
            purple +=1
        elif 95<num<=98: #粉色
            gun_level = 3
            gun_name_id = random.choice(gun_list3)
            pink +=1
        elif num==99: #红色
            gun_level = 4
            gun_name_id = random.choice(gun_list4)
            red +=1
        else: #金色
            gun_level = 5
            #1、随机武器，磨损品质，是否ST(金色专属)
            gun_name_id = gun_list5
            gold +=1
            gun_use_time = round(random.random(),5)
            gun_stattrak = 0
        if gun_level !=5:
            #1、随机武器，磨损品质，是否ST
            gun_use_time = round(random.random(),5)
            num = random.randint(0,101)
            if num <95:
                gun_stattrak = 0
            else:
                gun_stattrak = 1 #'（StatTrak™）'
        #2、信息转换
        gun_name = gun_id[gun_name_id] #武器名字转换成ID
        if 0<=gun_use_time<0.07: #武器磨损度转换为ID
            gun_use_time_id = 1
        elif 0.07<=gun_use_time<0.15:
            gun_use_time_id = 2
        elif 0.15<=gun_use_time<0.38:
            gun_use_time_id = 3
        elif 0.38<=gun_use_time<0.45:
            gun_use_time_id = 4
        else:
            gun_use_time_id = 5
        #3、写入武器数据
        sc._add_num(0,uid,1,1) #写入用户已使用的存档数据
        gun_csgo_num = sc._get_num(0,uid,1)  #物品ID初始值读取
        gun_csgo_num += 100000000000
        sc._set_num(uid,gun_csgo_num,0,1) #设置为存在物品
        sc._set_num(uid,gun_csgo_num,2,gun_name_id) #写入武器识别ID
        sc._set_num(uid,gun_csgo_num,3,gun_stattrak) #写入武器是否是ST
        sc._set_num(uid,gun_csgo_num,4,gun_use_time) #写入武器磨损数据
        sc._set_num(uid,gun_csgo_num,5,gun_use_time_id) #写入武器磨损ID
        sc._set_num(uid,gun_csgo_num,6,gun_level) #写入武器稀有度
        #4、判定是否是全新获取  num = csgo._get_num(gid,uid,c)
        c = str(gun_use_time_id)+str(gun_stattrak)+str(gun_name_id)
        c = int(c)
        new = csgo._get_num(gid,uid,c)
        csgo._add_num(gid,uid,c,1)
        #4.1、输出msg
        if new ==0:
            new_text = '【new】'
            if gun_level ==1:
                new_blue +=1
            if gun_level ==2:
                new_purple +=1
            if gun_level ==3:
                new_pink +=1
            if gun_level ==4:
                new_red +=1
            if gun_level ==5:
                new_gold +=1
        else:
            new_text = ''
        msg += f'{gun_name}（{use_time_id[gun_use_time_id]}）{stattrak_id[gun_stattrak]}（{level_id[gun_level]}）{new_text}\n'
        #4.3、根据开到的稀有度增加经验
        addxp_list = {1:50,2:60,3:220,4:540,5:900}
        csgo._add_level(0,uid,1,addxp_list[gun_level]) # 加经验
        addxp += addxp_list[gun_level]
        #循环+1
        num_w +=1
    #5、展示结果
    if id ==1:
        msg = f'开启完成！\n{gun_name}{stattrak_id[gun_stattrak]}\n磨损率：{gun_use_time}（{use_time_id[gun_use_time_id]}）\n稀有度：{level_id[gun_level]}\n'
    if id >10:
        msg = f'开启完成！\n蓝x{blue}(new+{new_blue})\n紫x{purple}(new+{new_purple})\n粉x{pink}(new+{new_pink})\n红x{red}(new+{new_red})\n金x{gold}(new+{new_gold})\n'
    xp = csgo._get_level(0,uid,1) # 获取经验
    level = csgo._get_level(0,uid,0) 
    up_level = level * 500
    msg += f'喵go等级：{level}({xp}/{up_level}) +{addxp}'
    await bot.send(ev,msg,at_sender=True)
    #6、扣除道具
    shop._reduce_num(0,uid,100000001000,id) #扣钥匙
    shop._reduce_num(0,uid,open_chest_id,id) #扣箱子
    csgo._set_num(0,0,1,0) #解锁


@sv.on_rex(r'^设置箱子(1|2)$')
async def setchest(bot,ev:CQEvent):
    csgo = getcsgo()
    uid = ev.user_id
    match = (ev['match'])
    text = match.group(1)
    text = int(text)
    text += 100000001000
    try:
        text_id = chest[text]
        csgo._set_num(0,uid,1,text)
        await bot.send(ev,f'设置为{text_id}完成')
    except:
        await bot.send(ev,f'不存在此可设置内容：{text}\n目前可设置的箱子：（设置时输入前面的序号）\n1、命悬一线武器箱\n2、梦魇武器箱')

@sv.on_fullmatch(('箱子列表'))
async def listchest(bot,ev):
    msg = '''目前可设置的箱子：（设置时输入前面的序号）
1、命悬一线武器箱
2、梦魇武器箱
'''
    await bot.send(ev,msg)

@sv.on_fullmatch('go库存')
async def kucun(bot,ev:CQEvent):
    sc = shichang()
    csgo = getcsgo()
    gid = ev.group_id
    uid = ev.user_id
    #开始检视库存
    num_max = sc._get_num(0,uid,1) #读取用户已使用的存档数据量
    num_now = 0 #初始化已读取的存档数据量
    blue = purple = pink = red = gold = 0 #初始化稀有度
    have_blue = have_purple = have_pink = have_red = have_gold = 0 #初始化持有稀有度
    look_gun_id = 100000000000
    while num_now <= num_max:   
        look_gun_id += 1
        num_now += 1
        if sc._get_num(uid,look_gun_id,6) == 1: #是蓝稀有度
            blue +=1
            if sc._get_num(uid,look_gun_id,0) != 0: #武器存在
                have_blue +=1
        if sc._get_num(uid,look_gun_id,6) == 2: #是紫稀有度
            purple +=1
            if sc._get_num(uid,look_gun_id,0) != 0: #武器存在
                have_purple +=1
        if sc._get_num(uid,look_gun_id,6) == 3: #是粉稀有度
            pink +=1
            if sc._get_num(uid,look_gun_id,0) != 0: #武器存在
                have_pink +=1
        if sc._get_num(uid,look_gun_id,6) == 4: #是红稀有度
            red +=1
            if sc._get_num(uid,look_gun_id,0) != 0: #武器存在
                have_red +=1
        if sc._get_num(uid,look_gun_id,6) == 5: #是金稀有度
            gold +=1
            if sc._get_num(uid,look_gun_id,0) != 0: #武器存在
                have_gold +=1
    msg = f'''你的库存：\n总使用容量：{num_max}
蓝-现持有/历史获取：{have_blue}/{blue}
紫-现持有/历史获取：{have_purple}/{purple}
粉-现持有/历史获取：{have_pink}/{pink}
红-现持有/历史获取：{have_red}/{red}
金-现持有/历史获取：{have_gold}/{gold}
'''
    await bot.send(ev,msg,at_sender=True)


@sv2.on_fullmatch('快速炼金')
async def hecheng(bot,ev:CQEvent):
    sc = shichang()
    csgo = getcsgo()
    gid = ev.group_id
    uid = ev.user_id
    if csgo._get_num(0,0,0) == 1:
        await bot.finish(ev,'有人正在炼金中！')
    if csgo._get_num(0,0,1) == 1:
        await bot.finish(ev,'群友正在开箱中！')
    
    await bot.send(ev,'开始检视库存（库存越多炼金使用时间越久）')
    num1 = num2 = num3 = 0 #初始化一页显示数量值
    get_level_2 = get_level_3 = get_level_4 = get_level_2_new = get_level_3_new = get_level_4_new = running_num = 0
    #开始检视库存
    num_max = sc._get_num(0,uid,1) #读取用户已使用的存档数据量
    num_now = 0 #初始化已读取的存档数据量
    look_gun_id = 100000000000
    #预检和删库
    while True :   
            running_num +=1 #炼金计数
            print(running_num)
            look_gun_id += 1
            num_now += 1
            if sc._get_num(uid,look_gun_id,0) != 0: #搜索到这个物品存在
                #if sc._get_num(uid,look_gun_id,6) == level_num: #检查是否符合稀有度，符合就+1
                if sc._get_num(uid,look_gun_id,6) == 1:
                    sc._set_num(uid,look_gun_id,0,0)
                    num1 += 1
                    print('num1+1')
                if sc._get_num(uid,look_gun_id,6) == 2:
                    sc._set_num(uid,look_gun_id,0,0)
                    num2 += 1
                    print('num2+1')
                if sc._get_num(uid,look_gun_id,6) == 3:
                    sc._set_num(uid,look_gun_id,0,0)
                    num3 += 1
                    print('num3+1')
            if num_now >= num_max : #搜索量已达到用户的存档数据量（全部搜索完毕了）
                break
    #达到数量后开始删库
    print('已完成检视')
    #await bot.send(ev,'正在检视库存')
    csgo._set_num(0,0,0,1)    #锁功能，防止多消息并发
    #删库完成后开始炼金
    for z in range(1,num1):
            gun_list = [] #空列表
            level_num = 2 
            gun_name_id_max = level_num*1000 +1 #检索武器初始值
            try:
                while True:  #利用检索字典报错的方法检测该稀有度下有多少武器
                    look_list = gun_id[gun_name_id_max]
                    gun_list.append(gun_name_id_max) #一旦上面那行报错就不会运行这一条了，完全可以放心使用
                    gun_name_id_max += 1  #如果无报错会运行到这里+1
            except:
                pass
            gun_name_id = random.choice(gun_list) #生成武器id
            gun_use_time = round(random.random(),5) #生成磨损率
            num = random.randint(0,101) #判定是否ST
            if num <95:
                gun_stattrak = 0
            else:
                gun_stattrak = 1 #'（StatTrak™）'
            if 0<=gun_use_time<0.07: #武器磨损度转换为ID
                gun_use_time_id = 1
            elif 0.07<=gun_use_time<0.15:
                gun_use_time_id = 2
            elif 0.15<=gun_use_time<0.38:
                gun_use_time_id = 3
            elif 0.38<=gun_use_time<0.45:
                gun_use_time_id = 4
            else:
                gun_use_time_id = 5
            #3、写入武器数据
            sc._add_num(0,uid,1,1) #写入用户已使用的存档数据
            gun_csgo_num = sc._get_num(0,uid,1)  #物品ID初始值读取
            gun_csgo_num += 100000000000
            sc._set_num(uid,gun_csgo_num,0,1) #设置为存在物品
            sc._set_num(uid,gun_csgo_num,2,gun_name_id) #写入武器识别ID
            sc._set_num(uid,gun_csgo_num,3,gun_stattrak) #写入武器是否是ST
            sc._set_num(uid,gun_csgo_num,4,gun_use_time) #写入武器磨损数据
            sc._set_num(uid,gun_csgo_num,5,gun_use_time_id) #写入武器磨损ID
            sc._set_num(uid,gun_csgo_num,6,level_num) #写入武器稀有度
            #4、判定是否是全新获取  num = csgo._get_num(gid,uid,c)
            c = str(gun_use_time_id)+str(gun_stattrak)+str(gun_name_id)
            c = int(c)
            new = csgo._get_num(gid,uid,c)
            csgo._add_num(gid,uid,c,1)
            #4.1、判定稀有度和新获取
            get_level_2 += 1
            if new == 0:
                get_level_2_new +=1
            print(f'2新获取判定完成 {z}')
    for z in range(1,num2):
            gun_list = [] #空列表
            level_num = 3
            gun_name_id_max = level_num*1000 +1 #检索武器初始值
            try:
                while True:  #利用检索字典报错的方法检测该稀有度下有多少武器
                    look_list = gun_id[gun_name_id_max]
                    gun_list.append(gun_name_id_max) #一旦上面那行报错就不会运行这一条了，完全可以放心使用
                    gun_name_id_max += 1  #如果无报错会运行到这里+1
            except:
                pass
            gun_name_id = random.choice(gun_list) #生成武器id
            gun_use_time = round(random.random(),5) #生成磨损率
            num = random.randint(0,101) #判定是否ST
            if num <95:
                gun_stattrak = 0
            else:
                gun_stattrak = 1 #'（StatTrak™）'
            if 0<=gun_use_time<0.07: #武器磨损度转换为ID
                gun_use_time_id = 1
            elif 0.07<=gun_use_time<0.15:
                gun_use_time_id = 2
            elif 0.15<=gun_use_time<0.38:
                gun_use_time_id = 3
            elif 0.38<=gun_use_time<0.45:
                gun_use_time_id = 4
            else:
                gun_use_time_id = 5
            #3、写入武器数据
            sc._add_num(0,uid,1,1) #写入用户已使用的存档数据
            gun_csgo_num = sc._get_num(0,uid,1)  #物品ID初始值读取
            gun_csgo_num += 100000000000
            sc._set_num(uid,gun_csgo_num,0,1) #设置为存在物品
            sc._set_num(uid,gun_csgo_num,2,gun_name_id) #写入武器识别ID
            sc._set_num(uid,gun_csgo_num,3,gun_stattrak) #写入武器是否是ST
            sc._set_num(uid,gun_csgo_num,4,gun_use_time) #写入武器磨损数据
            sc._set_num(uid,gun_csgo_num,5,gun_use_time_id) #写入武器磨损ID
            sc._set_num(uid,gun_csgo_num,6,level_num) #写入武器稀有度
            #4、判定是否是全新获取  num = csgo._get_num(gid,uid,c)
            c = str(gun_use_time_id)+str(gun_stattrak)+str(gun_name_id)
            c = int(c)
            new = csgo._get_num(gid,uid,c)
            csgo._add_num(gid,uid,c,1)
            #4.1、判定稀有度和新获取
            get_level_3 += 1
            if new == 0:
                    get_level_3_new +=1   
            print(f'3新获取判定完成 {z}')
    for z in range(1,num3):
            gun_list = [] #空列表
            level_num = 4
            gun_name_id_max = level_num*1000 +1 #检索武器初始值
            try:
                while True:  #利用检索字典报错的方法检测该稀有度下有多少武器
                    look_list = gun_id[gun_name_id_max]
                    gun_list.append(gun_name_id_max) #一旦上面那行报错就不会运行这一条了，完全可以放心使用
                    gun_name_id_max += 1  #如果无报错会运行到这里+1
            except:
                pass
            gun_name_id = random.choice(gun_list) #生成武器id
            gun_use_time = round(random.random(),5) #生成磨损率
            num = random.randint(0,101) #判定是否ST
            if num <95:
                gun_stattrak = 0
            else:
                gun_stattrak = 1 #'（StatTrak™）'
            if 0<=gun_use_time<0.07: #武器磨损度转换为ID
                gun_use_time_id = 1
            elif 0.07<=gun_use_time<0.15:
                gun_use_time_id = 2
            elif 0.15<=gun_use_time<0.38:
                gun_use_time_id = 3
            elif 0.38<=gun_use_time<0.45:
                gun_use_time_id = 4
            else:
                gun_use_time_id = 5
            #3、写入武器数据
            sc._add_num(0,uid,1,1) #写入用户已使用的存档数据
            gun_csgo_num = sc._get_num(0,uid,1)  #物品ID初始值读取
            gun_csgo_num += 100000000000
            sc._set_num(uid,gun_csgo_num,0,1) #设置为存在物品
            sc._set_num(uid,gun_csgo_num,2,gun_name_id) #写入武器识别ID
            sc._set_num(uid,gun_csgo_num,3,gun_stattrak) #写入武器是否是ST
            sc._set_num(uid,gun_csgo_num,4,gun_use_time) #写入武器磨损数据
            sc._set_num(uid,gun_csgo_num,5,gun_use_time_id) #写入武器磨损ID
            sc._set_num(uid,gun_csgo_num,6,level_num) #写入武器稀有度
            #4、判定是否是全新获取  num = csgo._get_num(gid,uid,c)
            c = str(gun_use_time_id)+str(gun_stattrak)+str(gun_name_id)
            c = int(c)
            new = csgo._get_num(gid,uid,c)
            csgo._add_num(gid,uid,c,1)
            #4.1、判定稀有度和新获取
            get_level_4 += 1
            if new == 0:
                    get_level_4_new +=1    
            print(f'4新获取判定完成 {z}')
    csgo._set_num(0,0,0,0)
    await bot.finish(ev,f'炼金结果：\n紫 +{get_level_2}(new+{get_level_2_new})\n粉 +{get_level_3}(new+{get_level_3_new})\n红 +{get_level_4}(new+{get_level_4_new})',at_sender=True)

@sv.on_fullmatch(('go仓库'))
async def shouji(bot,ev:CQEvent):
    uid = ev.user_id
    gid = ev.group_id
    csgo = getcsgo()
    #检索已载入武器
    num_have = 0
    num_have_max = 0
    gun_list = [] #空列表
    data_all = []
    have_all = []
    xy_z = {1001:'蓝',2001:'紫',3001:'粉',4001:'红'}
    for x in [1001,2001,3001,4001]:
        gun_name_id = x #检索武器初始值
        try:
            while True:  #利用检索字典报错的方法检测有多少武器
                look_list = gun_id[gun_name_id]
                gun_list.append(gun_name_id) #一旦上面那行报错就不会运行这一条了，完全可以放心使用
                gun_name_id += 1  #如果无报错会运行到这里+1
        except:
            pass
        num11 = 0 #已获取计数
        num12 = 0 #总武器计数
        data ={
                "type": "node",
                "data": {
                    "name": '龙酱',
                    "uin": 2570830652,
                    "content": f'---{xy_z[x]}稀有度列表---'
                        }
                  }
        data_all.append(data)
        for a in gun_list:  #循环列表
            msg = ''
            num1 = 0 #已获取计数
            num2 = 0 #总武器计数
            msg += f'{gun_id[a]}\n'
            for b in [100000,110000,200000,210000,300000,310000,400000,410000,500000,510000]: #磨损和ST的分类
                c = a+b
                num2 += 1
                num12 += 1
                num_have_max +=1
                num = csgo._get_num(gid,uid,c)
                if num != 0:
                    num1 += 1
                    num11 += 1
                    num_have += 1
                msg += f'{have_id[b]} {num}个\n'
            msg += f'收集进度：{num1}/{num2}\n'
            data ={
                "type": "node",
                "data": {
                    "name": '龙酱',
                    "uin": 2570830652,
                    "content": msg
                        }
                  }
            data_all.append(data)

        have ={
                "type": "node",
                "data": {
                    "name": '龙酱',
                    "uin": 2570830652,
                    "content": f'{xy_z[x]}稀有度收集进度：{num11}/{num12}'
                        }
                  }
        data ={
                "type": "node",
                "data": {
                    "name": '龙酱',
                    "uin": 2570830652,
                    "content": f'---{xy_z[x]}稀有度列表---'
                        }
                  }
        data_all.append(data)
        have_all.append(have)
        gun_list = [] #空列表
    have ={
                "type": "node",
                "data": {
                    "name": '龙酱',
                    "uin": 2570830652,
                    "content": f'go总图鉴完成度：{num_have}/{num_have_max}\n注意：图鉴记录的是获得过的数量，并非仓库持有数量！'
                        }
                  }
    have_all.append(have)
    have_all.reverse()
    have_all += data_all
    await bot.send_group_forward_msg(group_id=ev['group_id'], messages=have_all)

@sv.on_fullmatch(('强制解锁'))
async def unlock(bot,ev:CQEvent):
    uid = ev.user_id
    gid = ev.group_id
    csgo = getcsgo()
    if priv.check_priv(ev, priv.SUPERUSER):
        csgo._set_num(0,0,0,0)
        csgo._set_num(0,0,1,0)
        await bot.finish(ev,'强制解锁完成')
    
@sv.on_fullmatch(('go新手礼包'))
async def newlibao(bot,ev:CQEvent):
    uid = ev.user_id
    gid = ev.group_id
    csgo = getcsgo()
    shop = shopnew()
    if csgo._get_num(gid,uid,2) ==1:
        await bot.finish(ev,'你已经领取过啦！不能贪心',at_sender=True)
    shop._add_num(0,uid,100000001000,50)
    shop._add_num(0,uid,100000001001,15)
    shop._add_num(0,uid,100000001002,15)
    csgo._set_num(gid,uid,2,1)
    await bot.send(ev,'领取完了！可以使用<娱乐背包>查看道具')
