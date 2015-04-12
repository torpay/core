
class PaymentError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)
class CreditCardError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)
