import psycopg2

db_host = "image-gallery.cvst3zkdn4vk.us-west-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
    connection.set_session(autocommit=True)

def execute(query,args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def addUser():
    name = input("Username> ")
    passw = input("Password> ")
    fname = input("Full name> ")
    res = execute("Insert into users values (%s,%s,%s);",(name,passw,fname))

def editUser():
    name = input("Username to edit> ")
    passw = input("New password (press enter to keep current)> ")
    fname = input("New full name (press enter to keep current)> ")
    if passw == "" and fname != "":
        res = execute("update users set full_name=%s where username=%s;",(fname,name))
    elif passw != "" and fname == "":
        res = execute("update users set password=%s where username=%s;",(passw,name))
    elif passw != "" and fname != "":
        res = execute("update users set password=%s, full_name=%s where username=%s;",(passw,fname,name))


def deleteUser():
    yn = ""
    name = input("Enter username to delete> ")
    while yn != "Yes":
        yn = input("Are you sure that you want to delete " + name + "? ")
    if yn == "Yes":
        res = execute("delete from users where username=%s;", (name,))


def printUsers():
    res = execute('select * from users;')
    for row in res:
        print(row)


def main():
    choice = "10"
    connect()
    while choice != "5":
        print("\n1) List Users\n2) Add User\n3) Edit User\n4) Delete User\n5) Quit\n")
        choice = input("Enter command> ")
        if choice == "1":
           printUsers()
        if choice == "2":
            addUser()
        if choice == "3":
            editUser()
        if choice == "4":
            deleteUser()
    print("Bye.")

if __name__ == '__main__':
    main()

