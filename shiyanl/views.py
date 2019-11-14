"""
视图文件
"""
import os
import random
from shiyanl import app
from flask import render_template
from flask import request,Response,session
from sqlalchemy import or_,and_

from shiyanl.models import *


# 首页
@app.route("/index/")
def index():
    return render_template("index.html")


# 实现检索功能的视图
@app.route("/courses/")
def courses():
    # cc_type=int(url_arg)
    label_list=Labels.query.all() #返回标签
    search_key=request.args.get("search") #获取get请求的参数
#     if cc_type == 3:
#         course_list = Course.query.all()  # 所有课程
#     else:
#         course_list = Course.query.filter_by(c_type=cc_type)
    if search_key:
        course_list=Course.query.filter(
            Course.name.like("%{}%".format(search_key))
        ).all() #模糊查询
    return render_template("course.html",**locals())

@app.route("/course/<path:url_arg>/")
def course(url_arg):
    label_list = Labels.query.all()  # 返回标签
    args = url_arg.split("/") #获取url上匹配的过滤条件，并且使用/对过滤条件进行切分
    len_arg = len(args)
    # 如果参数的个数是两个，那么安照参数1是类型 参数2是标签进行查询
    # 设置全局参数，防止在判断的时候有条件分支缺失导致变量不存在
    c_type = "" #url传递过来的课程类型
    label = "" #url传递过来的课程标签
    referer_url="" #提供lable重新定位的参数
    referer_urll="" #提供给c_type重新定位的参数
    if len_arg == 2:
        c_type, label = args #分解参数
        if int(c_type)==3:
            referer_urll = label + "/"  # 定义课程类型的链接
            label_id = Labels.query.filter_by(l_name=label).first().id #获取对应的标签
            course_list=Course.query.filter_by(label_id=label_id)
        else:
            referer_url = "%s/" % c_type  # 定义lable标签的链接
            referer_urll = label + "/"  # 定义课程类型的链接
            label_id = Labels.query.filter_by(l_name=label).first().id
            course_list = Course.query.filter(
                and_(
                    Course.c_type == c_type,
                    Course.label_id == label_id
                )
            ) #多条件查询所对应的多个课程（例：免费的Python课程）
    elif len_arg == 1:
        arg, = args
        if arg.isdigit():
            c_type = arg
            if int(c_type) == 3:
                course_list = Course.query.all()
            else:
                referer_url = "%s/" % c_type  # 定义lable标签的链接,渲染到前端
                course_list = Course.query.filter_by(c_type=c_type)
        else:
            label = arg
            referer_urll=label+"/" #定义课程类型的链接
            lab=Labels.query.filter_by(l_name=label).first().id
            course_list=Course.query.filter_by(label_id=lab)

    print("c_type:%s" % c_type)
    print("label:%s" % label)
    # 如果参数的个数是一个，那么需要检查是类型还是标签
    # 参数是类型，就查询当前类型的多有商品
    # 参数是标签，查询所有当前标签的课程
    return render_template("course.html", **locals())


# 添加课程
@app.route("/add_course/")
def add_course():
    result = [
        {'src': 'https://dn-simplecloud.shiyanlou.com/ncn63.jpg', 'alt': '新手指南之玩转实验楼'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/ncn1.jpg', 'alt': 'Linux 基础入门（新版）'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1480389303324.png', 'alt': 'Kali 渗透测试 - 后门技术实战（10个实验）'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1480389165511.png', 'alt': 'Kali 渗透测试 - Web 应用攻击实战'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482113947345.png', 'alt': '使用OpenCV进行图片平滑处理打造模糊效果'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482807365470.png', 'alt': '使用 Python 解数学方程'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482215587606.png', 'alt': '跟我一起来玩转Makefile'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1480386391850.png', 'alt': 'Kali 渗透测试 - 服务器攻击实战（20个实验）'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482113981000.png', 'alt': '手把手教你实现 Google 拓展插件'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482113522578.png', 'alt': 'DVWA之暴力破解攻击'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1482113485097.png', 'alt': 'Python3实现简单的FTP认证服务器'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1481689616072.png', 'alt': 'SQLAlchemy 基础教程'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1481511769551.png', 'alt': '使用OpenCV&&C++进行模板匹配'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1481512189119.png', 'alt': 'Metasploit实现木马生成、捆绑及免杀'},
        {'src': 'https://dn-simplecloud.shiyanlou.com/1480644410422.png', 'alt': 'Python 3 实现 Markdown 解析器'}
    ]

    for i in range(20):
        for j in range(len(result)):
            c = Course()
            c.name = result[j]["alt"]
            c.description = "%s课啊，真滴好啊" % result[j]["alt"]
            c.picture = result[j]["src"]
            c.show_number = random.randint(23210, 88932)
            c.c_time_number = random.randint(15, 30)
            c.labels = random.choice(Labels.query.all())
            c.save()

    return "添加成功"


@app.route("/course_show/")
def course_show():
    return render_template("course_show.html")


@app.route("/course_show2/")
def course_show2():
    return render_template("course_show2.html")


@app.route("/reports/")
def reports():
    return render_template("reports.html")


@app.route("/developer/")
def developer():
    return render_template("developer.html")


@app.route("/get_page/",methods=["GET","POST"])
def get_page():
    """
    page:当前页
    page_size:一页5个数据
    :return:
    """
    # modths=dir(request)
    # page=int(request.args.get("page",1))
    # page_size=5
    # course_list=Course.query.offset(page).limit(page_size).all()
    label_list=Labels.query.all()
    if request.method=="POST":
        data=request.form #form用于获取form表单中的内容
        c_name=data.get("c_name")
        description=data.get("description")
        show_number=data.get("show_number")
        c_time_number=data.get("c_time_number")
        label=data.get("label")
        logo = request.files.get("logo")
        #文件保存分两步
        #文件保存到服务器
        # file_path=os.path.join(
        #     os.path.dirname(os.path.abspath(__file__)),"static\img\%s"%logo.filename
        # )
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "static\img\%s" % logo.filename
        )

        logo.save(file_path)
        #文件路径保存到数据中
        c=Course()
        c.name=c_name
        c.description=description
        c.picture="img\%s"%logo.filename #保存图片的路径
        c.show_number=show_number
        c.c_time_number=c_time_number
        c.labels=Labels.query.get(int(label))
        c.save()

    return render_template("request_template.html",**locals())

@app.route("/cookie/")
def cookie():

    return render_template("1.html")