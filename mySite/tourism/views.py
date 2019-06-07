from django.shortcuts import render,redirect
# from tourism.models import userInfo
# from tourism.models import attractionsInfo
from .models import attractionsInfo
from .models import userInfo
from django.contrib import messages
from django.shortcuts import render_to_response
import sys
import logging
logging.basicConfig(level = logging.INFO)
# Create your views here.

def get_cur_info():
    # print sys._getframe().f_code.co_name # 当前函数名
    # print sys._getframe().f_lineno # 当前行号
    print("[文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno) )


def login(request):
    # 获取用户提交方法, request包含客户端所有信息
    # print request.method

    # 接收到的数据以字典形式接收
    if request.method == "POST":
        # 获取用户通过post提交的数据,request.POST看做一个字典
        # key不存在也不会报错
        username = request.POST.get('username', None)
        password = request.POST.get('pwd', None)
        message = "所有字段都必须填写！"
        logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
        logging.info(print("输入的用户名和密码为："))
        logging.info(print(username,password))
        # 获取到值后，需要做判断。值正确跳转，不正确则有提示
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()

            #可以添加try来检测用户名是否为int
            username = int(username)


            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                ################################下面有问题
                user = userInfo.objects.get(userid=username)

                logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
                logging.info(print("得到的user:", user))
                logging.info(print("数据库中 password:", user.password))

                if user.password == password:
                    # message = "登陆成功！"
                    # print("password:", user.password)
                    return redirect('/index/')
                else:
                    message = "用户名与密码不匹配！请重新输入！"
                    # print("2")
                    # print("密码不正确！")
            except:
                message = "用户名不存在！请重新输入！"
                # print("用户名不存在！")
        return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')

def register(request):
    pass
    return render(request,"register.html")

def index(request):
    pass
    return render(request,"index.html")

def query(request):
    query = request.GET['attrName']
    attrs = attractionsInfo.objects.filter(name__icontains = query)
    attrs = attrs.extra(select={'countid':'countid+0'})
    attrs = attrs.extra(order_by=["countid"])
    user = userInfo.objects.filter(name__icontains = query)
    # print(attrs)
    # print("")
    # print(user)
    return render_to_response('search_res.html', {'query':query, 'attrs': attrs})