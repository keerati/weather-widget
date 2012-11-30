from google.appengine.api import urlfetch
import webapp2
import jinja2
import os
import httplib
from datetime import datetime
from datetime import timedelta

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

        mock = self.request.GET.get('m')
        cookie_city = self.request.cookies.get('city', '')
        cookie_lat  = self.request.cookies.get('lat', '')
        cookie_lng  = self.request.cookies.get('lng', '')

        if not mock and cookie_city and cookie_lat and cookie_lng:
             render_data = {
                'city' : cookie_city,
                'lat'  : cookie_lat,
                'lng'  : cookie_lng,
                'from_cookie_text' : 'Location data is get from cookie',
            }
        else:
            # get city from ip locator api
            api_key = '704706f28ef70e7dd1950ede8dfcee1dcb1a11100585de1fdbbb0a1b659e84da'
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

            render_data = { 'city' : city, 'lat'  : lat, 'lng'  : lng }
            # set cookies
            for s in self.get_cookie_string(render_data):
                self.response.headers.add_header('Set-Cookie', s)

        template = jinja_environment.get_template('ip/yrno.html')
        self.response.out.write( template.render( render_data ) )

    def get_cookie_string(self, data):
        cookie_expire = self.get_cookie_expire()
        return [ '%s=%s; expires=%s'%(key, value, cookie_expire) for key, value in data.items() ] 

    def get_cookie_expire( self ):
        # Wdy, DD Mon YYYY HH:MM:SS GMT
        date = datetime.now() + timedelta(hours = 1)
        return date.strftime('%a %d %b %Y %H:%M%:%S GMT')


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
