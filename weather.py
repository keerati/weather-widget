from google.appengine.api import urlfetch
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

class IPMainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('ip/main.html')
        self.response.out.write( template.render({}) )

class IPYrNoPage(webapp2.RequestHandler):
    def get(self):
        # get city from ip locator api
        api_key = '704706f28ef70e7dd1950ede8dfcee1dcb1a11100585de1fdbbb0a1b659e84da'
        mock = self.request.GET.get('m')
        client_ip = mock if mock else self.request.remote_addr
        iplocator_url = "http://api.ipinfodb.com/v3/ip-city/?key=%s&ip=%s"%(api_key, client_ip)  
        iplocator_res = urlfetch.fetch(iplocator_url)
        # if service error, use oslo as default
        city = 'unknown'
        lat  = '59.9427'
        lng  = '10.7205'
        if iplocator_res.status_code == 200:
            res_array = iplocator_res.content.split(';')
            city = res_array[6] 
            lat  = res_array[8]
            lng  = res_array[9]

        render_data = {
            'content': iplocator_res.content,
            'city' : city,
            'lat'  : lat,
            'lng'  : lng,
        }
        template = jinja_environment.get_template('ip/yrno.html')
        self.response.out.write( template.render( render_data ) )


app = webapp2.WSGIApplication(
    [
        ( '/geo', GeoMainPage ), 
        ( '/geo/yrno', GeoYrNoPage ), 
        ( '/geo/wunderground', GeoWUndergroundPage ), 
        ( '/ip', IPMainPage ), 
        ( '/ip/yrno', IPYrNoPage ), 
    ],
    debug=True
)
