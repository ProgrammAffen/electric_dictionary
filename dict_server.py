'''
电子词典服务端
'''
import socket
import signal,sys
from multiprocessing import Process
import pymysql
# 定义全局变量
HOST = '0.0.0.0'
PORT = 6666
ADDR = (HOST,PORT)
#链接数据库
db = pymysql.connect(host = 'localhost',port = 3306,user = 'root',password = 'Aa136549.',database = 'client_info',charset = 'utf8')
cur = db.cursor()

#确定协议
'''
R register
LI log in
LO log out
C check up
H history
Q quit client
'''

# 创建套接字
s = socket.socket()

# 设置端口复用
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#绑定地址
s.bind(ADDR)
s.listen(5)

# 回收僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

#处理客户端请求
def handle_request(c):
    while True:
        data = c.recv(1024)
        judge_request = data.decode().split(' ')[0]
        if not data or judge_request == 'Q':
            #若客户端强制退出或从一级界面退出 则关闭监听套接字 子进程也退出
            break
        if judge_request== 'R':
            do_register(data.decode())
        elif judge_request == 'LI':
            do_log_in(data.decode())
        elif judge_request == 'C':
            do_check_up(data.decode())
        elif judge_request == 'H':
            do_history(data.decode())
        else:
            continue
    c.close()

#处理用户登录 如果用户名存在发送‘username exists’，不存在则加入数据库 并创建该用户的单词查询table
def do_register(data):
    msg = data.split(' ')
    sql = 'select * from client where username="%s";'
    cur.execute(sql, [msg[1]])
    data = cur.fetchone()
    if data:
        c.send('Username exists'.encode())
    else:
        c.send('Register suceeded'.encode())
        try:
            sql1 = 'insert into client values ("%s","%s");'
            sql2 = 'create table %s (word varchar(31) not null,time datetime not null);'
            cur.execute(sql1,[msg[1],msg[2]])
            cur.execute(sql2,[msg[1]])
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

#处理用户登录 若用户名密码不存在 则返回登录失败 否则成功
def do_log_in(data):
    msg = data.split(' ')
    sql = 'select * from client where username="%s" and password="%s";'
    if cur.execute(sql,[msg[1],msg[2]]):
        c.send('Log in suceeded'.encode())
    else:
        c.send('Log in failed'.encode())

#处理用户查单词的请求
def do_check_up(data):
    msg = data.split(' ')
    f = open('dict.txt','r')
    while True:
        word_list = f.readline()
        word = word_list.split(' ')[0]
        if msg[2] == word:
            sql = 'insert into %s values ("%s",now());'
            cur.execute(sql,[msg[2]])
            db.commit()
            c.send(word_list.encode())
            f.close()
            return
        elif not word_list:
            c.send(b'not find')
            f.close()
            return

#处理客户端查询历史记录的请求
def do_history(data):
    msg = data.split(' ')
    sql = 'select * from %s;'
    if cur.execute(sql,[msg[1]]):
        history_list = str(cur.fetchmany(10))
        c.send(history_list.encode())
    else:
        c.send(b'Unknown Error')

#循环接收客户端请求
while True:
    #除非服务端主动退出 否则一直保持服务端运行
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        sys.exit('Server exits')
    except Exception as others:
        print(others)
        continue
    print('Connect from:',addr)
    # 创建子进程处理客户端请求
    p = Process(target=handle_request,args = (c,))
    # 主进程退出客户端随之退出
    p.daemon = True
    p.start()