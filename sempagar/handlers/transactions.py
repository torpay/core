# -*- coding: utf-8 -*-
import tornado.gen
import tornado.web
from sempagar.handlers import Handler
from sempagar.models import payments
import sys
sys.dont_write_bytecode = True

class Transactions(Handler):
	def prepare(self):
		super(Transactions, self).prepare()
		self.model = payments.Payment(self.access_token)
	@tornado.gen.coroutine
	def get(self):
		data = self.model.search()
		self.render(data)

class Transaction(Handler):
	def prepare(self):
		super(Transaction, self).prepare()
		self.model = payments.Payment(self.access_token)
	@tornado.gen.coroutine
	def get(self, transaction_id):
		data = self.model.get_one(transaction_id)
		self.render(data)
