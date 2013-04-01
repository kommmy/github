#coding=utf-8
import math
import web
import model
from crypt import crypt,KEY
from form import myform,register_form,login_form
import markdown
##AES
aes = crypt(KEY)


##Url mapping
urls = ('/','Index',
        '/del/(\d+)','Delete',
        '/register','Register',
        '/login','Login',
        '/logout','Logout',
        '/mark','MarkDown',
        '/title/(\d+)',"Content",
        '/title/',"Content",
)

##session
app = web.application(urls, globals())
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['timeout'] = 3600 #24 * 60 * 60, # 24 hours   in seconds
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'auth': 0 })
    web.config._session = session
    print web.config
else:
    session = web.config._session


##Template
t_globals={
    'session': session,
    'cookie':web.cookies,
    'markdown': markdown.markdown
}
render = web.template.render('templates',base='base',globals=t_globals)


##视图函数

class Login():

    def GET(self):
        login = login_form()
        cur_user = session.get('register')
        if cur_user:
            session.pop('register')
            return render.login(login,cur_user=cur_user)
        else:
            return render.login(login,cur_user=None)

    def POST(self):
        login = login_form()
        data= web.input()
        if login.validates():
            session.auth = login.d.name
            if data.get('autoLogin'):
                token = login.d.name+';'+login.d.password
                token = token.encode('utf-8')
                # web.setcookie('autologin',1,3600)
                # web.setcookie('name',login.d.name,3600)
                # web.setcookie('password',aes.encrypt(login.d.password),36000)
                web.setcookie('token',aes.encrypt(token),3600)
                print web.cookies()
            return web.seeother('/')
        return render.login(login,cur_user=None)

class Register():

    def GET(self):
        register = register_form()
        return render.register(register)

    def POST(self):
        register = register_form()
        if register.validates():
            model.insert_user(register.d.user,register.d.password1,register.d.email)
            session.register = register.d.user
            raise web.seeother('/login')
        else:
            return render.register(register)

class Logout:
    def GET(self):
        if 'token' in web.cookies():
            web.setcookie('token',0,0)
        session.auth = 0
        print session.auth
        raise web.seeother('/login')

class Index():
    myform = myform()

    def GET(self):
        print session.get('auth')
        print bool(session.get('auth') ==0)
        if ('token' not in web.cookies()) and \
           ('auth' not in session or session.get('auth')==0):
            raise web.seeother('/login')
        elif 'token' in web.cookies():
            userinfo = aes.decrypt(web.cookies().get('token')).split(';')
            username = userinfo[0].strip()
            password = userinfo[1].strip()
            if password != model.db.select(
               'user',what = 'password',where = 'name=$name',vars={'name':username})[0].password:
                raise web.seeother('/login')


        mydb = model.get_mydb()  #获得数据库内容
        myform = self.myform()
        return render.index(mydb,myform)  #将数据库，表单传给模板

    def POST(self):
        if ('token' not in web.cookies()) and \
            ('auth' not in session or session.get('auth')==0):
            raise web.seeother('/login')
        myform = self.myform()
        if not myform.validates():
            mydb = model.get_mydb()
            return render.index(mydb,myform)
        else:
            model.insert_mydb(myform['title'].value)  #插入一条新数据
            raise web.seeother('/')


class Delete():
    def POST(self,id):
        id = int(id)
        model.del_mydb(id)
        raise web.seeother('/')


class MarkDown():

    def GET(self):
        print web.input()
        return render.mark('test')

    def POST(self):
        data = web.input()
        if data.textedit != '0':
            return render.mark('test',error=u'不正确')
        return render.mark('test',error=None)


class Content:

    def GET(self,num=1):
        if ('token' not in web.cookies()) and \
                ('auth' not in session or session.get('auth')==0):
            raise web.seeother('/login')
        total = model.getAllTitle()
        page = float(total)/float(5)
        apage=math.ceil(page)

        if int(num) > apage or int(num) ==0:
            raise web.notfound()
        titles=model.db.select('mydb',what='title',limit = 5,offset= 5*(int(num)-1))
        pagination =ProbbsPage(total,5)
        url = '/title/%s'
        page_html = pagination.set_url(url).set_page(num).show()
        return render.test(num=num,total=total,html=page_html,titles=titles)

    def POST(self):
        pass

class ProbbsPage:
    def __init__(self, total, per = 10):
        self.total = total
        self.per = per
        self.url = ''
        self.page = 1

    def set_url(self,url):
        self.url = url
        return self

    def set_page(self,page):
        self.page = int(page)
        return self

    def show(self):
        if self.total%self.per == 0:
            pages = self.total/self.per
        else:
            pages = self.total/self.per+1
            #if self.page < 6:
        limit_s = 1
        #else:
        #    limit_s = self.page

        if pages < (limit_s+10):
            limit_e = pages
        else:
            limit_e = limit_s+10

        pagination = '<span>%s/%s pages </span>'%(self.page,pages)
        for i in range(limit_s,limit_e+1):
            if i == self.page:
                pagination += '<a class="cur" style="border:1px solid red;margin-right:5px;" href="javascript:void(0);">%s</a>'%(i,)
            else:
                pagination += '<a  style="margin-right:5px" href="%s">%s</a>'%(self.url%i,i)

        return pagination
if __name__=='__main__':
    app.run()

