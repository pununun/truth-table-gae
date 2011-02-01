#!/user/bin/env python

import wsgiref.handlers
from propcalc_final import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MyHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('main.html', {}))
        self.response.out.write("""
        <br><div style="font-size:medium">-Alex Leutenegger 2011,
        <a href="http://code.google.com/p/truth-table-gae/">Source</a></div>
        </body></html>""")


    def post(self):
        formula = self.request.get("formula")
        self.response.out.write(template.render("main.html", {}))
        for line in truth_table(formula):
            self.response.out.write('<div>%s</div>' % line)
        self.response.out.write("""
        <br><div style="font-size:medium">Alex Leutenegger 2011
        <a href="http://code.google.com/p/truth-table-gae/">Source</a></div>
        </body></html>""")

def main():
    app = webapp.WSGIApplication([
        (r'.*', MyHandler), ], debug=True)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == '__main__':
    main()
    