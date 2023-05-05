class Users:
    def __init__(self , userName , pin):
        self.userName = userName
        self.pin = pin

newUserName = input("Name: ")
newUserPass = input("pin: ")
confirmPass = input("Confirm pin: ")

studentInfo = (Users(newUserName , newUserPass))