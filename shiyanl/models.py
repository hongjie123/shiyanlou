from  shiyanl import db

class Model(db.Model): #用于定义id
    __abstract__=True #代表当前类为抽象类，不会再继承过程当中执行
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def save(self):
        session=db.session()
        session.add(self)
        session.commit()

    def delete(self):
        session=db.session()
        session.delete(self)
        session.commit()


#身份表
class Role(Model):
    name=db.Column(db.String(32))
    description=db.Column(db.Text)
    user_role=db.relationship("User",backref="role") #反向映射到多表
    def __repr__(self):
        return self.name

#多对多;映射表，中间表
user_course=db.Table(
    'user_course', #表名
    #可以在关系表中加上自己的路由
    # db.Column("id",db.Integer,primary_key=True,autoincrement=True),
    db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
    db.Column("course_id",db.Integer,db.ForeignKey("course.id")),
) #这种搭建方式，只用于关系表

#定义数据库模型
class User(Model):
    user_name=db.Column(db.String(32))
    email=db.Column(db.String(32))
    password=db.Column(db.String(32))
    role_id=db.Column(db.Integer,db.ForeignKey("role.id")) #映射到一表（外键）
    #反向映射到课程表，关系在user_course表中
    course=db.relationship("Course",secondary=user_course,backref="c_user")
    def __repr__(self):
        return self.name

#课程表
class Course(Model):
    name=db.Column(db.String(32))  #课程名称
    description=db.Column(db.Text) #课程描述
    picture = db.Column(db.String(32)) #课程图片
    show_number=db.Column(db.Integer) #观看人数
    c_time_number=db.Column(db.Integer) #课时
    state=db.Column(db.Integer,default=1) #课程状态，0即将上线，1上线
    c_type=db.Column(db.Integer,default=0) #课程类型，0免费，1限时免费，2VIP会员
#外键:在多表当中创建一个字段，定义为int类型，用来存储一表的id,一表表名小写

    label_id=db.Column(db.Integer,db.ForeignKey("labels.id"))

    def __repr__(self):
        return self.name


#课程标签
class Labels(Model):
    l_name=db.Column(db.String(32))
    l_description=db.Column(db.Text)
    # course_label = db.relationship("Course", backref="labels",uselist=False) #一对一关系需要uselist参数

    #在一表当中，创建字段反向映射向多表。
    # backref是在多表当中调用一表整条数据的字段。
    course_label=db.relationship("Course",backref="labels")
    def __repr__(self):
        return self.l_name





