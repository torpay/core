# -*- coding: utf-8 -*-
from sempagar.models import Model
from sempagar.sdks import goldark
import json
import sys
sys.dont_write_bytecode = True

class User(Model):
	def create(self, data):
		if 'username' in data:
			if not '+55' in data['username']:
				data['username'] = '+55%s' % data['username']
			data['phone'] = data['username']
		if not 'user_type' in data:
			data['user_type'] = 'merchant'
		(response, code, mimetype) = goldark.users.signup(data)
		return self.render(code, json.loads(response))
	def update_profile(self, data):
		user = self.get_user()
		if user is None:
			return self.render(404, {'error': 'token.not_found'})
		(response, code, mimetype) = goldark.users.update_profile(user['id'], data)
		return self.render(code, json.loads(response))
	def get_profile(self):
		user = self.get_user()
		if user is None:
			return self.render(404, {'error': 'token.not_found'})
		(response, code, mimetype) = goldark.users.get_profile(user['id'])
		return self.render(code, json.loads(response))
	def login(self, data):
		(response, code, mimetype) = goldark.users.login(data)
		parsed_response = json.loads(response)
		session = {}
		if code == 201:
			session['token'] = parsed_response['token']
			if 'user' in parsed_response:
				session['user'] = parsed_response['user']
		if 'user' in session and 'token' in session:
			self.session_instance.set('session/%s' % session['token'], json.dumps(session['user']))
		return self.render(code, parsed_response)
	def logout(self):
		user = self.get_user()
		if user is None:
			return self.render(404, {'error': 'token.not_found'})
		(response, code, mimetype) = goldark.users.logout(self.access_token)
		if code == 200:
			self.session_instance.delete('session/%s' % self.access_token)
		return self.render(code, json.loads(response))
