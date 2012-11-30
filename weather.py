import webapp2
import jinja2
import os
import httplib

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader( os.path.join( os.path.dirname(__file__), 'template') )
)

class GeoMainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('geo/main.html')
        self.response.out.write( template.render({}) )

class GeoYrNoPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('geo/yrno.html')
        self.response.out.write( template.render({}) )

class GeoWUndergroundPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('geo/wunderground.html')
        self.response.out.write( template.render({}) )

app = webapp2.WSGIApplication(
    [
        ( '/geo', GeoMainPage ), 
        ( '/geo/yrno', GeoYrNoPage ), 
        ( '/geo/wunderground', GeoWUndergroundPage ), 
    ],
    debug=True
)
