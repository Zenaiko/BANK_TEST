import sqlite3
import random

try:
    conn = sqlite3.connect("bankInfo.db")
    cur = conn.cursor()

    cur.execute("CREATE TABLE Bank_Acc(UID int(10) primary key NOT NULL, USER_NAME varchar(100) , PIN varchar(50))")

    cur.close()

except:
    print("error")
    
class Users:
    def __init__(self, userName , password):
        self.userName = userName
        self.password = password

print("""Choose an action according to its corresponding number: \n
      1.) Withdraw \n 
      2.) Deposit \n 
      3.) Create an Account""")

userChoice = input("\n\t")

if int(userChoice) == 1:
    logCur = conn.cursor()
    print("Login")

    idLog = input("Bank ID: ")
    pinlog = input("Pin: ")

    logCur.execute("SELECT * FROM Bank_Acc WHERE  UID = (?) and PIN = (?)" , [idLog , pinlog])
    userLog = (logCur.fetchone())

    if userLog is not None:
        logCur.execute("SELECT USER_NAME FROM Bank_Acc")
        getUserName = (logCur.fetchone())
        print(getUserName)

        logCur.execute("SELECT UID FROM Bank_Acc")
        getID = (logCur.fetchone())
        print(getID)

elif int(userChoice) == 3:
    print("Fill up the following")
    newUserName = input("Name: ")
    newUserPass = input("Password: ")
    confirmPass = input("Confirm Password: ")
    userDataInp = (Users(newUserName , newUserPass))
        
    if newUserPass == confirmPass:
        insertCur = conn.cursor()

        insertCur.execute("SELECT * FROM Bank_Acc WHERE USER_NAME = (?)" , [newUserName])
        dupli = (insertCur.fetchone())

        if dupli is None:
            userID = (random.randrange(0, 9))
            insertCur.execute("INSERT INTO Bank_Acc values( ? , ? , ? )" , ( userID, userDataInp.userName , userDataInp.password))
            conn.commit()
            print("Account Successfully Created")

            insertCur.execute("SELECT * FROM Bank_Acc WHERE USER_NAME = (?)" , [newUserName])
            showAcc = (insertCur.fetchone())
            print(showAcc)
        else:
            print("Account Name is Already Taken")

        insertCur.close()
       
    else:
        print("Password does not match")


conn.close()