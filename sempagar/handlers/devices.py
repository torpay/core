# -*- coding: utf-8 -*-
import tornado.gen
import tornado.web
from sempagar.handlers import Handler
from sempagar.models import devices
import sys
sys.dont_write_bytecode = True

class Devices(Handler):
	def prepare(self):
		super(Devices, self).prepare()
		self.model = devices.Device(self.access_token)
	@tornado.gen.coroutine
	def post(self):
		data = self.model.create(self.data)
		self.render(data)

class Device(Handler):
	def prepare(self):
		super(Device, self).prepare()
		self.model = devices.Device(self.access_token)
	@tornado.gen.coroutine
	def put(self, device_id):
		data = self.model.update(device_id, self.data)
		self.render(data)
