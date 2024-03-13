import __main__


def LoginUI():
    username = input("Input your username : ")
    password = input("Input your password : ")
    __main__.LoginAPI(username, password)
