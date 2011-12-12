from urlparse import urlparse
from flask import Flask, request, make_response, redirect
from urllib2 import Request, urlopen, HTTPError, URLError

app = Flask(__name__)
H2H_Headers = ["connection", "keep-alive", "proxy-authenticate", \
			"proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"]

REC_ADD = ('0.facebook.com','fb.me','live.airtelworld.com')

def prox():
	return 'Prox Work in Progress'

@app.route('/')
def visible_index():
	return "<strong>Houston We Hava A Problem Here</strong>"


@app.route('/<path:loc>')
def index(loc):
#	url = 'http://122.170.122.191.mirrorrr.appspot.com/%s' \
#		% urlparse.urlparse(loc).netloc
	url = loc
	if urlparse(url).netloc == '' or urlparse(url).netloc.find('.') == -1:
		return "Invalid Address"
	
	if urlparse(url).netloc in REC_ADD:
		return prox()
	(content, headers) = urlfetch(url, request.headers)
	resp = make_response(content)
	resp.headers = headers
	return resp

def urlfetch(url, headers):
	''' Small urllib2 implementation 
		returns (content, headers)
			header -> dictonary 
			content-> plain response
	'''
	try:
		req = Request(url)
		for key,val in tuple(headers):
			req.add_header(key.strip(),val.strip())
		try:
			r = urlopen(req)
		except HTTPError, e:
			return ('HTTP Error %s' % e.code, dict(r.info))
		except URLError, e:
			return ('URL Error %s' % e.reason,dict(r.info))
		
		return (r.read(), dict(r.info))
	except Exception, e:
		return ('','')

if __name__ == "__main__":
	app.run(debug=True,port=5000)
