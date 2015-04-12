# -*- coding: utf-8 -*-
import tornado.gen
import tornado.web
from sempagar.handlers import Handler
from sempagar.models import payments, users
import sys
sys.dont_write_bytecode = True

class PaymentsAccept(Handler):
	def prepare(self):
		super(PaymentsAccept, self).prepare()
		self.model = payments.Payment()
	@tornado.gen.coroutine
	def post(self):
		data = self.model.check_acceptance(self.data)
		self.render(data)