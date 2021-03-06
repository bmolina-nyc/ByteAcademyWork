import os
import time
from app.orm import ORM
from app.account import Account 
from app.position import Position 
from app.trade import Trade

DIR = os.path.dirname(__file__)
DBFILENAME = 'ttrader.db'
DBPATH = os.path.join(DIR, DBFILENAME)

def seed(dbpath=DBPATH):
    ORM.dbpath = dbpath
    
    mike_bloom = Account(username='mike_bloom', balance=10000.00)
    mike_bloom.set_password('password')
    mike_bloom.save()

    # trade for a purchase of 10 shares yesterday
    # trade for a sell of 5 shares today

    buy_trade = Trade(accounts_pk = mike_bloom.pk, ticker='tsla', volume=10, price=100.0)
    sell_trade = Trade(accounts_pk=mike_bloom.pk, ticker='tsla', volume=5, price=200.0)
    buy_trade.save()
    sell_trade.save()

    tsla_position = Position(ticker='tsla', shares=5, accounts_pk=mike_bloom.pk)
    tsla_position.save()
