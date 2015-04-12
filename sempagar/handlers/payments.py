# -*- coding: utf-8 -*-
import tornado.gen
import tornado.web
from sempagar.handlers import Handler
from sempagar.models import payments
import sys
sys.dont_write_bytecode = True

class Payment(Handler):
	def prepare(self):
		super(Payment, self).prepare()
		self.model = payments.Payment(self.access_token)
	@tornado.gen.coroutine
	def post(self):
		data = self.model.create(self.data)
		self.render(data)

class PaymentAccept(Handler):
	def prepare(self):
		super(PaymentAccept, self).prepare()
		self.model = payments.Payment()
	@tornado.gen.coroutine
	def post(self):
		data = self.model.accept_payment(self.data)
		self.render(data)