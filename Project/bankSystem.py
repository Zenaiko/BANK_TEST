import sqlite3
import random

try:
    conn = sqlite3.connect("bankInfo.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE Bank_Acc(UID int(10) primary key NOT NULL,
                USER_NAME varchar(100) ,
                PIN varchar(50) ,
                BALANCE DECIMAL (10,2))""")
    cur.close()

except:
    print("error")
    
class Users:
    def __init__(self, userName , password):
        self.userName = userName
        self.password = password

def IDgenerator():
    numGenCur = conn.cursor()
    num = (random.randrange(0, 9**8))

    numGenCur.execute("SELECT * FROM Bank_Acc WHERE UID = (?)" , [num])
    dupliID = (numGenCur.fetchone())

    if dupliID is not None:
        IDgenerator()
    elif dupliID is None:
        return num
    
def login():
    logCur = conn.cursor()
    print("Login")

    idLog = input("Bank ID: ")
    pinlog = input("Pin: ")

    logCur.execute("SELECT * FROM Bank_Acc WHERE UID = (?)" , [idLog])
    userLog = (logCur.fetchone())

    if userLog is not None:
        logCur.execute("SELECT * FROM Bank_Acc WHERE PIN = (?)" , [pinlog])
        passLog = (logCur.fetchone())
        
        if passLog is not None:

            logCur.execute("SELECT USER_NAME FROM Bank_Acc")
            getUserName = (logCur.fetchone())
            print("Account Name: " , getUserName)

            logCur.execute("SELECT UID FROM Bank_Acc")
            getID = (logCur.fetchone())
            print("Account ID: " , getID)

            logCur.execute("SELECT BALANCE FROM Bank_Acc")
            getBalance = (logCur.fetchone())
            print("Balance: " , getBalance)
            logCur.close()

        else:
            print("Pin Incorrect")
            return False
            
    else:
        print("Account does not Exist")
        return False
    

print("""Choose an action according to its corresponding number: \n
      1.) Deposit \n 
      2.) Withdraw \n 
      3.) Create an Account""")
41959411
userChoice = input("\n\t")

if int(userChoice) == 1:
   if login() is not False:
        depCur = conn.cursor()
        userDep = input("Deposit Amount: ")
        depCur.execute("UPDATE Bank_Acc SET BALANCE = BALANCE + (?)" , [float(userDep)])
   
if int(userChoice) == 2:
    login()

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
            userID =  IDgenerator()
            insertCur.execute("INSERT INTO Bank_Acc values( ? , ? , ? , NULL)" , ([userID, userDataInp.userName , userDataInp.password]))
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