# -*- coding: utf-8 -*-
import os.path
import os
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import redis
import utils
import sdks
import config
import handlers
import sys
sys.dont_write_bytecode = True

define('port', default=5000, help='run on the given port', type=int)

#redis = redis.StrictRedis(host='cobia.redistogo.com', port='9608', password='742b9896c3849731f37ad20b60a49310', db='redistogo')
redis = redis.StrictRedis()

routes = []
#users
routes.append((r'/users', handlers.Users))
routes.append((r'/users/login', handlers.UserSession))
routes.append((r'/users/logout', handlers.UserSession))
routes.append((r'/users/profile', handlers.UserProfile))
#payments
routes.append((r'/payments', handlers.Payment))
routes.append((r'/payments/accept', handlers.PaymentAccept))
#devices
routes.append((r'/devices', handlers.Devices))
routes.append((r'/devices/([0-9a-fA-F]{24})', handlers.Device))
#transactions
routes.append((r'/transactions', handlers.Transactions))
routes.append((r'/transactions/([0-9a-fA-F]{24})', handlers.Transaction))

application = tornado.web.Application(routes, redis=redis, debug=True)

def run(port=5000):
	tornado.options.parse_command_line()
	print 'Starting ark server....'
	application.listen(os.environ.get('PORT', 5000))
	print 'Running on port %s' % port
	tornado.ioloop.IOLoop.instance().start()
