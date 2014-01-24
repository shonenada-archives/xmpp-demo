import os, logging

import wsgiref.handlers

from google.appengine.ext import webapp, db
from google.appengine.api import xmpp, users, urlfetch
from google.appengine.ext.webapp.util import login_required


class BaseHandler(webapp.RequestHandler):
    server_jid = os.environ.get('APPLICATION_ID') + '@appspot.com'
    server_url = "http://%s.appspot.com" % os.environ.get('APPLICATION_ID')


class MainHandler(BaseHandler):
    def get(self):
        self.response.out.write('Hello~Please add <i>%s</i> to your contact list' % self.server_url)


class XMPPHandler(BaseHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        logging.info("XMPP Sender: %s - body: %s" % (message.sender, message.body))
        cmd = message.body.split(' ')[0].lower()
        body = message.body[len(cmd) + 1:]
        if cmd == 'echo':
            message.reply(body)
        elif cmd == 'sum':
            numbers = body.split(' ')
            total = 0
            try:
                for x in numbers:
                    total += int(x)
                text = "%s = %s" % (" + ".join(numbers), total)
            except:
                text = "Couldn't add these up!"
            message.reply(text)
        else:
            message.reply('I don\'t understand "%s"' % cmd)


app = webapp.WSGIApplication([('/', MainHandler),
                              ('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)
