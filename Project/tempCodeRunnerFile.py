codea = """INSERT INTO USER (FIRST_NAME , LAST_NAME , PIN , BANK_ACC_NO) VALUES ("Aki" , "Admin" , 1 , 1)"""
cur.execute(codea)
conn.commit()

cur.close()