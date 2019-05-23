from django.shortcuts import render,redirect
# from tourism.models import userInfo
# from tourism.models import attractionsInfo
from .models import attractionsInfo
from .models import userInfo
from django.contrib import messages
from django.shortcuts import render_to_response
# Create your views here.

def login(request):
    # 获取用户提交方法, request包含客户端所有信息
    # print request.method

    # 接收到的数据以字典形式接收
    if request.method == "POST":
        # 获取用户通过post提交的数据,request.POST看做一个字典
        # key不存在也不会报错
        username = request.POST.get('username', None)
        password = request.POST.get('pwd', None)
        #print(username,password)
        # 获取到值后，需要做判断。值正确跳转，不正确则有提示
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            username = int(username)
            print(username)
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                ################################下面有问题
                #user = userInfo.object.get(userId=int(username))
                user = userInfo.object.get(userId=username)

                print("user:",user)
                if user.password == password:
                    print("password:", user.password)
                    return redirect('/index/')
                else:
                    print("2")
                    print("密码不正确！")
            except:
                print("用户名不存在！")
        return render(request, 'login.html')
    return render(request, 'login.html',)

def register(request):
    pass
    return render(request,"register.html")

def index(request):
    pass
    return render(request,"index.html")

def query(request):
    query = request.GET['attrName']
    attrs = attractionsInfo.objects.filter(name__icontains = query)
    user = userInfo.objects.filter(name__icontains = query)
    # print(attrs)
    # print("")
    # print(user)
    return render_to_response('search_res.html', {'query':query, 'attrs': attrs})