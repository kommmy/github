#coding=utf-8
import web

db = web.database(dbn='mysql',user='root',pw='xj198898',db='mydb')

def get_mydb():
    return db.select('mydb',order='id')

def insert_mydb(text):
    return db.insert('mydb',title = text)

def del_mydb(id):
    return db.delete('mydb',where='id=$id', vars=locals())

def insert_user(name,password,email):
    return db.insert('user',name=name,password=password,email=email)

def getAllTitle():
    result = db.query('select count(title) from mydb')
    for i in result:
        result = i.get('count(title)')
    return result
if __name__=='__main__':
    result = db.query('select count(title) from mydb')
    for i in result:
        print i.get('count(title)')