class UserDAO:

    def get_users(self):
        raise Exception("Must be imlemented")

    def delete_user(self, username):
        raise Exception("Must be implemented")

    def select_user(self, username):
        raise Exception("must be implemented")

    def add_user(self, username, password, full_name):
        raise Exception("must be implemented")

    def edit_user(self, username, password, full_name):
        raise Exception("must be implemented")



    def add_image(self, username, filename):
        raise Exception("must be implemented")

    def get_images(self, username):
        raise Exception("must be implemented")

    def get_image_names(self, username):
        raise Exception("must be implemented")


    def delete_image(self, filename):
        raise Exception("must be implemented")
