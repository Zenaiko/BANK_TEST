import sqlite3
from sqlite3 import Error
import random

try:
    conn = sqlite3.connect("bankInfo.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE USER
                (UID INTEGER PRIMARY KEY NOT NULL,
                FIRST_NAME varchar(100) NOT NULL,
                LAST_NAME varchar(100) NOT NULL,
                PIN INT(6) NOT NULL,
                BANK_ACC_NO INT(8) NOT NULL)""")
    
    cur.execute(""" CREATE TABLE BANK_ACCOUNT
                (ACCOUNT_NO PRIMARY KEY,
                BALANCE DECIMAL (10,2),
                FOREIGN KEY(ACCOUNT_NO) REFERENCES USER(BANK_ACC_NO))""")
    cur.close()
except Error as e:
    print(e)

 # TESTS
# testCur = conn.cursor()
# codea = """INSERT INTO USER (FIRST_NAME , LAST_NAME , PIN , BANK_ACC_NO) VALUES ("Maki" , "SecAd" , 1 , 15)"""
# balAd = """ INSERT INTO BANK_ACCOUNT VALUES ( 15 , 200.00)"""
# testCur.execute(codea)
# testCur.execute(balAd)
# conn.commit()


    
class Users:
    def __init__(self, firstName , lastName ,pin):
        self.firstName = firstName
        self.lastName = lastName
        self.pin = pin

def IDgenerator():
    numGenCur = conn.cursor()
    num = (random.randrange(0, 9**8))

    numGenCur.execute("SELECT * FROM USER WHERE BANK_ACC_NO = (?)" , [num])
    dupliID = (numGenCur.fetchone())

    if dupliID is not None:
        IDgenerator()
    elif dupliID is None:
        return num
    
def login():
    logCur = conn.cursor()
    print("Login")

    bankAccbIDLog = input("Bank ID: ")
    pinLog = input("Pin: ")

    logCur.execute("SELECT * FROM USER WHERE BANK_ACC_NO = (?)" , [bankAccbIDLog])
    bankAccID = (logCur.fetchone())

    if bankAccID is not None:
        logCur.execute("SELECT * FROM USER WHERE BANK_ACC_NO = (?) AND PIN = (?) " ,[bankAccbIDLog, pinLog])
        passLog = (logCur.fetchone())
        
        if passLog is not None:
            logCur.execute("SELECT BANK_ACC_NO FROM USER WHERE BANK_ACC_NO = (?) AND PIN = (?) " ,[bankAccbIDLog, pinLog])
            getID = (logCur.fetchone())

            logCur.execute("SELECT FIRST_NAME FROM USER WHERE BANK_ACC_NO = (?)" , getID)
            getfirstName = (logCur.fetchone())
            print("Account Name: " , getfirstName)

            logCur.execute("SELECT LAST_NAME FROM USER WHERE BANK_ACC_NO = (?)" , getID)
            getlastName = (logCur.fetchone())
            print("Bank Account ID: " , getlastName)
       
            print("Bank Account ID: " , getID)

            logCur.execute("SELECT BALANCE FROM BANK_ACCOUNT WHERE ACCOUNT_NO = (?)" , getID)
            getBalance = (logCur.fetchone())
            print("Balance: " , getBalance)
            logCur.close()

            return getID[0]
        
        else:
            print("Incorrect Pin")
            return False
            
    else:
        print("Account does not Exist")
        return False
    

print("""Choose an action according to its corresponding number: \n
      1.) Deposit \n 
      2.) Withdraw \n 
      3.) Transfer \n
      4.) Create an Account""")
userChoice = input("\n\t")

if int(userChoice) == 1:
   userID = login()
   if userID is not False:
        depCur = conn.cursor()
        userDep = input("Deposit Amount: ")

        depCur.execute("SELECT BALANCE FROM BANK_ACCOUNT WHERE ACCOUNT_NO = (?)" , userID)
        userBal = (depCur.fetchone())
        newUserBal = float(userBal[0]) + float(userDep)
        
        depCur.execute("UPDATE BANK_ACCOUNT SET BALANCE = (?) WHERE ACCOUNT_NO = (?)" , [newUserBal , userID])
        conn.commit()
        depCur.close()
   
elif int(userChoice) == 2:
    if login() is not False:
        withCur = conn.cursor()
        userWith = input("Withdraw Amount: ")


elif int(userChoice) == 3:
    if login() is not False:
        print

elif int(userChoice) == 4:
    print("Fill up the following")
    newFirstName = input("First Name: ")
    newLastName = input("Last Name: ")
    newUserPass = input("Pin: ")
    confirmPass = input("Confirm pin: ")
    userDataInp = (Users(newFirstName , newLastName ,newUserPass))
        
    if newUserPass == confirmPass:
        insertCur = conn.cursor()

        bankAccNO =  IDgenerator()
        insertCur.execute("INSERT INTO USER(FIRST_NAME , LAST_NAME , PIN , BANK_ACC_NO) VALUES( ? , ? , ? , ?)"
                        ,([userDataInp.firstName , userDataInp.lastName, userDataInp.pin , bankAccNO]))
        conn.commit()
        print("Account Successfully Created")

        insertCur.execute("SELECT * FROM USER WHERE FIRST_NAME = (?)" , [newFirstName])
        showAcc = (insertCur.fetchone())
        print(showAcc)

        insertCur.close()
       
    else:
        print("pin does not match")


conn.close()