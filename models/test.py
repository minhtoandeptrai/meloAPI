import mysql.connector
class Test():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host = "localhost", user = "root", password= "123123", database= "melospace")
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print('okk')
        except:
            print('fault')