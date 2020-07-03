class UserDAO:

    def get_users(self):
        raise Exception("Must be imlemented")

    def delete_user(self, username):
        raise Exception("Must be implemented")

    def select_user(self, username):
        raise Exception("must be implemented")

    def add_user(self, username, password, full_name):
        raise Exception("must be implemented")
