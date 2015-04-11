# -*- coding: utf-8 -*-
import sempagar
from sempagar.utils import Response
import json
import sys
sys.dont_write_bytecode = True

class Model(object):
	def __init__(self, *args, **kwargs):
		self.session_instance = sempagar.application.settings['redis']
		self.access_token = None
		if len(args) > 0:
			self.access_token = args[0]
		if 'access_token' in kwargs:
			self.access_token = kwargs['access_token']
	def get_user(self):
		if self.access_token is None:
			return None
		user = self.session_instance.get('session/%s' % self.access_token)
		return json.loads(user)
	def render(self, status, contents, **kwargs):
		mimetype = kwargs.get('mimetype')
		if mimetype is None:
			mimetype = 'json'
		charset = kwargs.get('charset')
		if charset is None:
			charset = 'utf8'
		response = Response()
		response.set_content_type(mimetype)
		response.set_charset(charset)
		response.status = status
		response.response = contents
		return response
