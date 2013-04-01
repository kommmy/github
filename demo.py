import math
import web
import model

urls = (
        '/title/(\d+)','Content'
)
app = web.application(urls,globals())
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['timeout'] = 3600 #24 * 60 * 60, # 24 hours   in seconds
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'auth':''})
    web.config._session = session
    print web.config
else:
    session = web.config._session


t_globals={
    'cookie':web.cookies,
    'session':session
}
render = web.template.render('templates',base='base',globals=t_globals)
class Content:
    def GET(self,num):
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

# <!--$if int(num) ==1:-->
# <!--$pass-->
# <!--<a href="/title/$(int(num))">prve</a>-->
# <!--$else:-->
# <!--<a href="/title/$(int(num)-1)">prve</a>-->
# <!--<form style="display: inline-block;" action="" method="POST">-->
# <!--<input type="text" name="fname" size='1' />$num/$total-->
# <!--<input type="submit" value="GO"/>-->
# <!--</form>-->
# <!--$if int(num) == int(total):-->
# <!--$pass-->
# <!--$else:-->
# <!--<a href="/title/$(int(num)+1)">next</a>-->
if __name__=='__main__':

    app.run()