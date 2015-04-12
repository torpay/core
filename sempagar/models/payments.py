# -*- coding: utf-8 -*-
from sempagar.models import Model
from sempagar.sdks import goldark, channel, payment
import json
import sys
import urlparse, urllib
sys.dont_write_bytecode = True

class Payment(Model):
	def check_acceptance(self, data):
		#  this is the callback of the consumer SMS response
		# 1. tries to find the active invoice of the consumer 
		# 2. updates the invoice status
		# 3. iniciates payment transation
		# 4. updates the invoice status
		# 5. notifies to consumer and merchand of the transation result

		parsed = urlparse.parse_qs(data)
		sender =parsed['To'][0]
		receiver =parsed['From'][0]
		message =parsed['Body'][0]
		# 1.
		# getting the consumer, who is the receiver of the message
		(user, code, mimetype) = goldark.users.find_by_phone( urllib.quote(sender) )
		_user = json.loads(user) if type(user) != dict else user
		user_id = _user['data'][0]['id']

		# getting the valid invoice of the consumer
		(invoice, code, mimetype) = goldark.invoices.find_by_consumer( user_id )
		_invoice = json.loads(invoice) if type(invoice) != dict else invoice
		invoice_id = _invoice['data'][0]['id']
		invoice_description = _invoice['data'][0]['description']
		invoice_amount = _invoice['data'][0]['total_value']
		invoice_currency = _invoice['data'][0]['currency']

		# 2. 
		# getting the status, based on the consumer response
		status = self.get_status_from_consumer( channel.response.process_message(message) )
		(status_response, code, mimetype) = goldark.invoices.update_status( invoice_id, status)

		# 3. 
		(creditcard, code, mimetype) = goldark.creditcards.from_consumer( user_id )
		_creditcard = json.loads(creditcard) if type(creditcard) != dict else creditcard
		card_number = _creditcard['data'][0]['number']
		card_year = _creditcard['data'][0]['year']
		card_month = _creditcard['data'][0]['month']
		card_cvc = _creditcard['data'][0]['cvc']
		
		card = payment.creditcard.CreditCard(number = card_number, exp_month=card_month, exp_year=card_year, cvc=card_cvc)
		receipt = payment.simplifyservice.charge_with_card_details(amount = invoice_amount, description = invoice_description , currency = invoice_currency, card=card.to_simplify_obj() )
		# print receipt
		# 4. 
		status = self.get_status_from_transation(payment.response.process_message(receipt))
		(status_response, code, mimetype) = goldark.invoices.update_status( invoice_id, status)

		# 5.
		# print urllib.urlencode(status_response)	
		

		return self.render(code, urllib.urlencode(json.loads(status_response ) ), mimetype='text/plain')

	def get_status_from_consumer(self, response ):
		if response:
			return { "status": u"Approved", "status_message": u"Transation sucessfully approved" }
		else:
			return { "status": u"Failed", "status_message": u"Transation not approved by consumer" }

	def get_status_from_transation(self, response):
		if response:
			return { "status": u"Approved", "status_message": u"Transation sucessfully approved" }
		else:
			return { "status": u"Failed", "status_message": u"Transation not approved by credit card operator"}
