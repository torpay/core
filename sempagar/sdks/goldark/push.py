# -*- coding: utf-8 -*-
from sempagar.utils import request
import config
import json
import copy
import sys
sys.dont_write_bytecode = True

def send(user_id, msg):
	url = '%s/push/users/%s/messages' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data={'message': msg})

def create_device(data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/push/devices' % (config.host)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data=_data)

def update_device(device_id, data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/push/devices/%s' % (config.host, device_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data=_data)