#coding:utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
import time
from . import models

# Create your views here.

# USER_LIST = [
#     {'username':'chinablue','email':'124@126.com','gender':'man'}
# ]
# for index in range(20):
#     tmp = {'username':'chinablue'+str(index),'email':'124@126.com','gender':'man'}
#     USER_LIST.append(tmp)

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    #注册
    return render(request, 'register.html')

""" def register(request):
    a = 1
    if request.method=='POST':
        userId=request.POST.get('user','')
        password=request.POST.get('password','')
        repassword=request.POST.get('repassword','')
        username=request.POST.get('username','')
        sex=request.POST.get('sex','')
        age=request.POST.get('age','')
        address=request.POST.get('address','')
        tel=request.POST.get('tel','')
        preference=request.POST.get('preference','')
        errors=[]

        #添加到数据库
        registAdd = User.objects.create_user(id=userId, password=password,name=username,sex=sex,age=age,address=address,tel=tel,preference=preference)
        if registAdd == False:
            return render(request,'register.html', {'registAdd': registAdd, 'userId': userId})

        else:
            # return HttpResponse('ok')
            return render(request,'register.html', {'registAdd': registAdd}) 


    return render(request, "register.html")"""

def preference(request):
    return render(request,"preference.html")

def login(request):
    # 获取用户提交方法, request包含客户端所有信息
    # print request.method

    # 接收到的数据以字典形式接收
    if request.method == "POST":
        # 获取用户通过post提交的数据,request.POST看做一个字典
        # key不存在也不会报错
        username = request.POST.get('username',None)
        password = request.POST.get('pwd', None)
        print(username,password)
        # 获取到值后，需要做判断。值正确跳转，不正确则有提示
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            print(username)
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                ################################下面有问题
                user = models.userInfo.objects.get(name=username)
                print("1")
                print ("user:",user)
                if user.password == password:
                    print ("password:",user.password)
                    return redirect('/index/')
                else:
                    print("2")
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login.html')
    return render(request, 'login.html')


def index(request):
    pass
    return render(request,"index.html")

def home(request):
    if request.method == "POST":
        # 获取用户提交的数据
        u = request.POST.get('username')
        e = request.POST.get('email')
        g = request.POST.get('gender')
        tmp = {'username': u, 'email': e, 'gender': g}
        USER_LIST.append(tmp)
    return render(request,'home.html',{'user_list':USER_LIST})

def query(request):
   query = request.GET['attrName']
   attrs = models.Attractionsinfo.objects.filter(name__icontains = query)
   books1 = Userinfo.objects.filter(name__icontains = query)
   return render_to_response('search_res.html', {'query':query, 'attrs': books1})