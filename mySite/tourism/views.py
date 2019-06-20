from django.shortcuts import render,redirect
# from tourism.models import userInfo
# from tourism.models import attractionsInfo
from .models import attractionsInfo
from .models import userInfo
from django.contrib import messages
from django.shortcuts import render_to_response
import sys
sys.path.append('G:/1/Python/GraduationProject/getData') 
import decisionTrees
import treePlotter
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

    #不允许重复登录
    if request.session.get('is_login',None):
        return redirect('/index/')

    # 接收到的数据以字典形式接收
    if request.method == "POST":
        # 获取用户通过post提交的数据,request.POST看做一个字典
        # key不存在也不会报错
        username = request.POST.get('username', None)
        password = request.POST.get('pwd', None)
        message = "请检查填写的内容！"
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

                    request.session.set_expiry(0)  #设置cookie的有效期。可以传递不同类型的参数值：• 如果为0，在用户关闭浏览器后失效 • 如果为None，则将使用全局会话失效策略
                    #往session字典内写入用户状态和数据：
                    request.session['is_login'] = True

                    logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
                    logging.info(print("userid为:", user.userid))
                    logging.info(print("name为:", user.name))

                    request.session['userId'] = user.userid
                    request.session['name'] = user.name
                    request.session['address'] = user.address
                    request.session['tree'] = user.tree
                    return redirect('/index/')
                else:
                    message = "用户名与密码不匹配！请重新输入！"
                    # print("2")
                    # print("密码不正确！")
            except:
                message = "用户名不存在！请重新输入！"
                # print("用户名不存在！")
        logging.info(print("locals():", locals()))
        return render(request, 'login.html', locals())  #{"message": message}  
    return render(request, 'login.html', locals())  #Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()  #flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def register(request):
    if request.method == "POST":
        user = request.POST.get('user', None)  #id
        try:
            user = int(user)
        except:
            message = '用户名应只含数字！'
            return render(request, 'register.html', locals())
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        username = request.POST.get('username', None)
        sex = request.POST.get('sex', None)
        age = request.POST.get('age', None)
        try:
            age = int(age)
        except:
            message = '年龄应只含数字！'
            return render(request, 'register.html', locals())
        address = request.POST.get('address', None)
        tel = request.POST.get('tel', None)
        s1 = request.POST.get('select1', None)
        s2 = request.POST.get('select2', None)
        s3 = request.POST.get('select3', None)
        s4 = request.POST.get('select4', None)
        s5 = request.POST.get('select5', None)
        s6 = request.POST.get('select6', None)
        s7 = request.POST.get('select7', None)
        s8 = request.POST.get('select8', None)
        s9 = request.POST.get('select9', None)
        s10 = request.POST.get('select10', None)
        logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
        logging.info(print(locals()))
        same_name_user = userInfo.objects.filter(userid=user)
        if same_name_user:  # 用户名唯一
            message = '用户已经存在，请重新选择用户名！'
            logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
            logging.info(print(message))
            return render(request, 'register.html', locals())
        
        # 当一切都OK的情况下，创建新用户
        preference = {'1':s1,'1183':s6,'1047':s2,'1461':s7,'2808':s3,'2283':s8,'3274':s4,'2330':s9,'8918':s5,'6251':s10}
        dataset1 = [[0, 0, 0, 1, 2,s1],
                    [0, 3, 2, 1, 1,s2],
                    [2, 3, 2, 1, 2,s3],
                    [2, 3, 1, 1, 0,s4],
                    [7, 3, 2, 0, 2,s5],
                    [0, 3, 0, 1, 1,s6],
                    [1, 1, 1, 1, 2,s7],
                    [1, 1, 2, 1, 2,s8],
                    [3, 3, 1, 1, 2,s9],
                    [5, 3, 2, 1, 2,s10]]
        logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
        logging.info(print(dataset1))
        dataSet_now = decisionTrees.get_a_dataSet(dataset1)  #传入评分信息
        logging.info(print(dataSet_now))
        dataSet, labels = decisionTrees.createDataSet(dataSet_now)
        logging.info(print(dataSet, labels))
        labels_tmp = labels[:]
        logging.info(print(labels_tmp))
        desicionTree = decisionTrees.createTree(dataSet, labels_tmp)
        logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
        logging.info(print(preference))
        logging.info(print("desicionTree:",desicionTree))
        #  treePlotter.createPlot(desicionTree) 可视化决策树
        new_user = userInfo.objects.create(userid = user,password = password,name = username,sex = sex,age = age,address = address,tel = tel,preference = preference,tree = desicionTree)
        # new_user.userId = user
        # new_user.password = password
        # new_user.name = username
        # new_user.sex = sex
        # new_user.age = age
        # new_user.address = address
        # new_user.tel = tel
        # new_user.preference = {'1':s1,'1183':s6,'1047':s2,'1461':s7,'2808':s3,'2283':s8,'3274':s4,'2330':s9,'8918':s5,'6251':s10}
        # new_user.tree = 1
        logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
        logging.info(print(new_user))
        new_user.save()

        return redirect('/login/')  # 自动跳转到登录页面
    return render(request, 'register.html', locals())


def index(request):
    pass
    return render(request,"index.html")

def query(request):
    query = request.GET['attrName']
    attrs = attractionsInfo.objects.filter(name__icontains = query)  #  模糊搜索
    
    pass #筛选
    
    tree = request.session.get('tree',None)
    logging.info(print("\n[调试处文件：%s @ 函数：%s @ 行数：%s]" % (__file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)))
    logging.info(print('tree:',tree))
    logging.info(print('attrs:',attrs))
    
    test_set = get_set(attrs)

    attrs = attrs.extra(select={'countid':'countid+0'})
    attrs = attrs.extra(order_by=["countid"])  #  人气排序
    user = userInfo.objects.filter(name__icontains = query)
    # print(attrs)
    # print("")
    # print(user)
    return render_to_response('search_res.html', {'query':query, 'attrs': attrs})

def get_set(attrsInfo):
    for attr in attrsInfo:
        #主题-> "文化古迹-0","自然风光-1","展馆-2","公园-3","农家度假-4","游乐场-5","城市观光-6","运动健身-7"
        if attr.theme == "文化古迹"：
            s1 = 0
        elif attr.theme == "自然风光"：
            s1 = 1
        elif attr.theme == "展馆"：
            s1 = 2
        elif attr.theme == "公园"：
            s1 = 3
        elif attr.theme == "农家度假"：
            s1 = 4
        elif attr.theme == "游乐场"：
            s1 = 5
        elif attr.theme == "城市观光"：
            s1 = 6
        else ：
            s1 = 7
        
        #级别-> 0：5A景区 | 1：4A景区 | 2：3A景区 | 3：其他
        if attr.level == "5A景区":
            s2 = 0
        elif attr.level == "4A景区":
            s2 = 1
        elif attr.level == "3A景区":
            s2 = 2
        else:
            s2 = 3
        
        #热度-> 0： 1.0 | 1： 0.7 - 0.99 | 2：0.7以下
        if attr.productstarlevel == "热度 1.0":
            s3 = 0
        elif attr.productstarlevel >= "热度 0.7":
            s3 = 1
        else:
            s3 = 2

        #地址-> 0：在本省 | 1： 不在本省
        hisaddress = request.session.get(address)
        if attr.address
        #价格-> 0：免费 | 1：0.1-50元 起 | 2：50-500元  | 3：500元及以上 | 4：未知
