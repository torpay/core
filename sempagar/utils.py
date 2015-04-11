# -*- coding: utf-8 -*-
import json
from encodings.aliases import aliases
import urllib2
import sys
sys.dont_write_bytecode = True

class Response(object):
	def __init__(self):
		self.content_type = None
		self.status = None
		self.response = None
		self.charset = None
		self.charsets = {key.replace('_', ''):aliases.get(key).replace('_', '-') for key in aliases.keys()}
		self.types = {
			'json': 'application/json',
			'xml': 'application/xml',
			'soap': 'application/soap+xml'
		}
		self.transactions = None
	def set_content_type(self, t):
		if t in self.types:
			self.content_type = self.types[t]
		else:
			self.content_type = t
	def set_charset(self, c):
		if c in self.charsets:
			self.charset = self.charsets[c]
		else:
			self.charset = self.charsets['utf-8']
	def render_as_json(self):
		if self.response:
			return json.dumps(self.response)
		return None

def request(**kwargs):
	method = kwargs.get('method')
	data = kwargs.get('data')
	mimetype = kwargs.get('mimetype')
	url = kwargs.get('url')
	headers = kwargs.get('headers')
	if headers is None:
		headers = {}
	if mimetype == 'json' and type(data) != str:
		data = json.dumps(data)
		headers['Content-Type'] = 'application/json;charset=utf-8'
	else:
		headers['Content-Type'] = mimetype
	res = None
	code  = 0
	mime = None
	req = None
	if method == 'GET' or method == 'DELETE':
		req = urllib2.Request(url=url, headers=headers)
	else:
		req = urllib2.Request(url=url, data=data, headers=headers)
	req.get_method = lambda: method
	try:
		f = urllib2.urlopen(req)
		res = f.read()
		code = f.getcode()
		mime = f.headers.typeheader
	except urllib2.URLError as e:
		res = e.read()
		code = e.code
		mime = e.headers['content-type']
	except Exception as e:
		return (json.dumps({'error': 'internal error'}), 500, 'application/json;charset=utf-8')
	return (res, code, mime)