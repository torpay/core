# -*- coding: utf-8 -*-
from sempagar.models import Model
from sempagar.sdks import goldark
import json
import sys
sys.dont_write_bytecode = True

class Device(Model):
	def create(self, data):
		user = self.get_user()
		if user:
			if not 'user_id' in data:
				data['user_id'] = user['id']
		(response, code, mimetype) = goldark.push.create_device(data)
		return self.render(code, json.loads(response))
	def update(self, device_id, data):
		(response, code, mimetype) = goldark.push.update_device(device_id, data)
		return self.render(code, json.loads(response))
