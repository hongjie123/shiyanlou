
from shiyanl.views import app
from shiyanl.models import db


if __name__ == '__main__':
    # 同步数据库
    db.create_all()
    app.run(host="127.0.0.1", port=8000, debug=True)

