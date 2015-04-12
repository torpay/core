# -*- coding: utf-8 -*-
from sempagar.utils import request
import config
import json
import copy
import sys
sys.dont_write_bytecode = True

def from_consumer(user_id):

	url = '%s/creditcards?user=%s' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)


