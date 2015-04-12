import simplify
import config
import exceptions
import creditcard as creditcard

simplify.public_key = config.simplify_access['public_key']
simplify.private_key = config.simplify_access['private_key']

def tokenify(card):
	obj = {
		"card" : card
	}
	try:
		cardToken = simplify.CardToken.create(obj)
		token_id = cardToken.id if cardToken else None
	except: 
		token_id = None

	return token_id

def charge_with_token( token, currency, amount, description=None):

	obj = {
		"token" : token,
		"amount" : amount,
		"description" : description,
		"currency" : currency
	}
	if description:
		obj['description'] = description

	payment = simplify.Payment.create( obj )

	if payment.paymentStatus == 'APPROVED':
		print "Payment approved"

	return payment

def charge_with_card_details(card, currency, amount, description=None):
	if (int(amount) < 50 or int(amount) > 9999900 ):
		raise exceptions.PaymentError('transation amount out of range')
	if (len(currency) != 3 ):
		raise exceptions.PaymentError('invalid transation currency')
	if ( len(description) > 1024):
		raise exceptions.PaymentError('The description of the transation is too long')

	obj = {
		"card" : card,
		"amount" : amount,
		"description" : description,
		"currency" : currency
	}

	if description:
		obj['description'] = description

	payment = simplify.Payment.create( obj )

	if payment.paymentStatus == 'APPROVED':
		print "Payment approved"

	return payment


def test_charge_with_card():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	receipt = charge_with_card_details(amount = 100, description = "shipment of two eggs in a glass bottle" , currency = "USD", card=card.to_simplify_obj())
	print "Callback returned: %s" % receipt

def test_tokenify():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	token = tokenify( card.to_simplify_obj() )
	print " Token returned: %s" % token

def test_charge_with_token():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	token = tokenify( card.to_simplify_obj() )
	receipt = charge_with_token(token=token, currency="USD", amount="1000")
	print "Callback returned: %s " % receipt


if __name__ == "__main__":
	test_tokenify()
	test_charge_with_token()
	test_charge_with_card()