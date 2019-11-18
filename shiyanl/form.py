from flask_wtf import FlaskForm
import wtforms
from wtforms import validators
from wtforms import ValidationError
from shiyanl.models import User

class OurError(object):
    def __init__(self,message=None):
        """
        :param message: 错误提示信息
        """
        self.message=message
    def __call__(self, form,field):
        """
        :param form: 固定参数，代表form表单 <TestLou.form.UserForm object at 0x00000000046C6E80>
        :param field: 固定参数，字段本身 <input id="username" name="username" type="text" value="dhj">
        :return:
        """
        print(form)
        print(field)

        validata=field.data #字段数据 dhj
        db_user=User.query.filter_by(user_name=validata).first()
        if db_user:
            self.message+=":用户名重复"
            raise ValidationError(self.message)
        pool=["dhj"]
        if validata in pool:
            self.message+=":敏感词"
            raise ValidationError(self.message) #错误回收


class UserForm(FlaskForm):
    username=wtforms.StringField("用户名",validators=[OurError("违法命名")])
    email=wtforms.StringField("邮箱",validators=[validators.Email("邮箱格式错误")])
    password=wtforms.PasswordField("密码")




