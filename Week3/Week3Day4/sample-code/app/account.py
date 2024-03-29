import sqlite3
from app.orm import ORM
from app.util import hash_password
from app.position import Position
from app.util import hash_password
from app.trade import Trade

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance", "api_key"]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.get('pk')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.balance = kwargs.get('balance')
        self.api_key = kwargs.get('api_key')

    @classmethod
    def login(cls, username, password):
        """ login TODO: check password hash """
        return cls.select_one_where("WHERE username = ? AND password_hash = ?",
                                    (username, hash_password(password)))

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def get_positions(self):
        return Position.select_many_where("WHERE accounts_pk = ?", (self.pk, ))

    def get_position_for(self, ticker):
        """ return a specific Position object for the user. if the position does not
        exist, return a new Position with zero shares. Returns a Position object """
        position = Position.select_one_where(
            "WHERE ticker = ? AND accounts_pk = ?", (ticker, self.pk))
        if position is None:
            return Position(ticker=ticker, accounts_pk=self.pk, shares=0)
        return position

    def get_trades(self):
        """ return all of the user's trades ordered by time. returns a list of
        Trade objects """
        return Trade.select_many_where("WHERE accounts_pk =?", (self.pk,))

    def trades_for(self, ticker):
        """ return all of a user's trades for a given ticker """
        return Trade.select_many_where("WHERE ticker = ? AND accounts_pk=?",(ticker, self.pk))

    def buy(self, ticker, amount):
        """ make a purchase. raise KeyError for a non-existent stock and
        ValueError for insufficient funds. will create a new Trade and modify
        a Position and alters the user's balance. returns nothing """
        pass

    def sell(self, ticker, amount):
        """ make a sale. raise KeyErrror for a non-existent stock and
        ValueError for insufficient shares. will create a new Trade object,
        modify a Position, and alter the self.balance. returns nothing."""
        position = self.get_position_for(ticker)
        if amount > position.shares:
            raise.ValueError('insufficient shares')
        price = get_price(ticker)
        trade = Trade(accounts_pk = self.pk, ticker = ticker, price = price, volume=-amount)
        position.shares -= amount 
        self.balance += amount * price 
        position.save()
        trade.save()
        self.save()