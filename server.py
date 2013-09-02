#!/usr/bin/env python

from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log
import sys
log.startLogging(sys.stdout)

import twilio

from auth import ACCOUNT_SID, ACCOUNT_TOKEN

API_VERSION = '2010-04-01'
utils = twilio.Utils(ACCOUNT_SID, ACCOUNT_TOKEN)
validate = utils.validateRequest

def response(*items):
    item = ' '.join(str(item) for item in items)
    return "<Response>%s</Response>" % item

def redirect(action, method="POST"):
    return '<Redirect method="%s">%s</Redirect>' % (method, action)

def say(item, voice="man", language="en"):
    return '<Say voice="%s" language="%s">%s</Say>' % (voice, language, item    ) 

class MyRequest(http.Request):

    def process(self):
        headers = self.received_headers
        path = self.uri
        args = self.args

        base = 'http://%s' % headers['host']
        url = base + (path if path != '/' else '')
        data = dict((key, value[0]) for (key, value) in args.items())
        signature = headers.get('x-twilio-signature', "???")
        valid = validate(url, data, signature)
        valid = valid or validate(url+"/", data, signature) # hmm, not sure what i'm doing here.

        print "url:", url
        print data

        if not valid:
            body = response(say("could not validate"))
        elif path == '/':
            body = response(redirect("/foo"))
        else:
            body = response(say("hello monkey"))

        self.setHeader('content-type',"text/xml")
        self.setHeader('content-length', str(len(body)))
        print
        print body
        print
        self.write(body)
        self.finish()

class MyHTTPChannel(http.HTTPChannel):
    requestFactory = MyRequest

class MyHTTPFactory(http.HTTPFactory):
    protocol = MyHTTPChannel

reactor.listenTCP(8080, MyHTTPFactory())
reactor.run()


