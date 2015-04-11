# -*- coding: utf-8 -*-
import tornado.gen
import tornado.web
from sempagar.handlers import Handler
from sempagar.models import users
import sys
sys.dont_write_bytecode = True

class Users(Handler):
	def prepare(self):
		super(Users, self).prepare()
		self.model = users.User()
	@tornado.gen.coroutine
	def post(self):
		data = self.model.create(self.data)
		self.render(data)

class UserProfile(Handler):
	def prepare(self):
		super(UserProfile, self).prepare()
		self.model = users.User(self.access_token)
	@tornado.gen.coroutine
	def put(self):
		data = self.model.update_profile(self.data)
		self.render(data)
	@tornado.gen.coroutine
	def get(self):
		data = self.model.get_profile()
		self.render(data)

class UserSession(Handler):
	def prepare(self):
		super(UserSession, self).prepare()
		self.model = users.User(self.access_token)
	def post(self):
		data = self.model.login(self.data)
		self.render(data)
	def delete(self):
		data = self.model.logout()
		self.render(data)
