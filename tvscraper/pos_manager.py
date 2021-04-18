import attr
from attrdict import AttrDict


@attr.s
class PositionManager:
    ticker = attr.ib(type=str)
    cost_basis = attr.ib(type=float, default=0.)
    last = attr.ib(type=float, default=0.)
    units = attr.ib(type=int, default=0.)
    leverage = attr.ib(type=float, default=0.1)
    realized = attr.ib(type=float, default=0.)

    @property
    def pnl(self):
        return self.unrealized + self.realized

    @property
    def unrealized(self):
        return self.units * (self.last - self.cost_basis)

    def transact(self, action, units, price):
        if not units or not price:
            return
        if action == 'buy':
            pass
        elif action == 'sell':
            units *= -1
        else:
            raise NotImplementedError(action)
        if not (self.units + units):
            self.close_all()
            return
        self.units += units
        self.cost_basis = price

    def buy(self, *args, **kwargs):
        return self.transact('buy', *args, **kwargs)

    def sell(self, *args, **kwargs):
        return self.transact('sell', *args, **kwargs)

    def close_all(self):
        self.realized += self.unrealized
        self.cost_basis = self.units = 0
