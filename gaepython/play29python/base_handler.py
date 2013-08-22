import facebook
import jinja2
import os
import webapp2
from webapp2_extras import sessions

FACEBOOK_APP_ID = "326517067460642"
FACEBOOK_APP_SECRET = "eaf5a4e2ae9bec1f6dcfc3a2b92e6ee5"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/tmpls"),
    extensions=['jinja2.ext.autoescape'])

def pluralize(count, singular, plural):
    phrase = singular if count == 1 else plural
    return "%d %s" % (count, phrase)


class BasePage(webapp2.RequestHandler):
    
    def renderTemplate(self, template_path, template_values):
        template = JINJA_ENVIRONMENT.get_template(template_path)
        self.response.write(template.render(template_values))
        
    @webapp2.cached_property
    def current_user(self):
        user = self.session.get("user")
        fbCookie = self.request.cookies.get("fbsr_" + FACEBOOK_APP_ID, "")
        
        if user and user["fb_cookie"] == fbCookie:
            # User is logged in
            return user
            
        else:
            # Either used just logged in or just saw the first page
            # We'll see here
            cookie = facebook.get_user_from_cookie(fbCookie,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:
                self.session["user"] = {
                    "uid" : cookie["uid"],
                    "access_token" : cookie["access_token"],
                    "fb_cookie" : fbCookie
                }
                    
                return self.session.get("user")
            elif not(user is None) :
                del self.session["user"]
        return None
    
    def dispatch(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        return self.session_store.get_session()
                
    def get(self):
        self.ensureLoginGet()

    def post(self):
        self.ensureLoginGet()

    def put(self):
        if self.current_user is None:
            template_values = self.getBaseTemplateVals()
            self.renderTemplate('auth.html', template_values)
        else :
            self.Put()
    
    def ensureLoginGet(self):
        if self.current_user is None:
            template_values = self.getBaseTemplateVals()
            self.renderTemplate('auth.html', template_values)
        else :
            self.Get()
    
    def Get(self):
        pass
            
    def getBaseTemplateVals(self):
        template_values = {
                           'facebook_app_id': FACEBOOK_APP_ID, 
                           'current_user' : self.current_user,
                           'channel_path' : self.request.host_url + "/channel.html"
                           }
        
        return template_values
    