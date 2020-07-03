from .. import db
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
        result = []
        cursor = db.execute("select username, password, full_name from users;")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result

    def delete_user(self, username):
        db.execute("delete from users where username=%s;",(username,))

    def select_user(self, username):
        cursor = db.execute("select * from users where username=%s;",(username,))
        res = cursor.fetchone();
        return User(res[0],res[1],res[2])

    def edit_user(self, username, password, full_name):
        db.execute("update users set password=%s, full_name=%s where username=%s;",(password,full_name,username))

    def add_user(self, username, password, full_name):
        db.execute("insert into users values (%s,%s,%s);",(username,password,full_name))
