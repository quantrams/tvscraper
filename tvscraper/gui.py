import attr
from typing import Callable
import logging
import PySimpleGUI as sg

logging.basicConfig(level=logging.WARNING)


@attr.s
class SGManager:
    ticker = attr.ib(type=str, default='AAPL')
    theme = attr.ib(type=str, default='DarkAmber')
    window_title = attr.ib(type=str, default='Tradingview Trainer')
    font = attr.ib(type=str, default='Courier 16')
    window_size = attr.ib(type=tuple, default=(500, 350))
    default_units = attr.ib(type=int, default=100000)
    element_padding = attr.ib(type=tuple, default=(5, 10))
    ohlc = attr.ib(type=dict, default={k: 0.0 for k in 'ohlc'})
    # Callback function invoked upon GUI-triggered events. Will be passed
    # args `event` and `value`.
    transaction_callback = attr.ib(type=Callable, default=print)
    ohlc_getter = attr.ib(default=lambda: dict(o=0., h=0., l=0., c=0.),
                          type=Callable)
    keybinds = attr.ib(type=dict, default={
        'b': 'Buy',
        's': 'Sell',
        'c': 'Close All',
        'n': 'Next Bar',
    })
    log_start_text = attr.ib(type=str, repr=False, default=str(
        '*********************************************\n' +
        '      Welcome to Tradingview Trainer\n' +
        'Logs such as transaction history appear here.\n' +
        '*********************************************\n'
    ))

    def run(self):
        """Main entrypoint"""
        self.get_window()
        # TODO: unhack this
        self.handle_transaction('Buy', 0, log=False)
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event in self.keybinds:
                self.handle_transaction(self.keybinds[event], values[0])
            elif event in self.keybinds.values():
                self.handle_transaction(event, values[0])
            else:
                # logging.debug(f'event: {event}')
                pass
        self.window.close()

    def handle_transaction(self, event, value, log=True):
        msg = f'{event} @ {self.last_price} ({value} units)'
        # logging.debug(msg)
        func = self.transaction_callback
        args = (self, event, value)
        if event == 'Buy':
            func(*args)
        elif event == 'Sell':
            func(*args)
        elif event == 'Close All':
            func(*args)
        elif event == 'Next Bar':
            func(*args)
            log = False
        else:
            raise NotImplementedError(event)
        if log is True:
            self.log(msg)

    def get_window(self):
        sg.theme(self.theme)
        sg.SetOptions(element_padding=self.element_padding)
        self.window = sg.Window(
            self.window_title, self.get_layout(), font=self.font,
            keep_on_top=True, size=self.window_size, finalize=True,
            return_keyboard_events=True, use_default_focus=False
        )
        return self.window

    def log(self, msg):
        """Appends `msg` to `log` element"""
        assert hasattr(self, 'window')
        cur = self.window['log'].Get()
        new = f"{cur}{msg}"
        self.window['log'].update(value=new)

    def set_ohlc(self, value, name='c'):
        assert isinstance(value, float)
        self.ohlc[name] = value
        self.window['ohlc'].update(self.get_ohlc_text())
        self.window.refresh()

    @property
    def last_price(self):
        return self.ohlc['c']

    def update_price_header(self):
        self.window['price_header'].update(self.get_price_header())

    def get_price_header(self, left_padding=2) -> str:
        return " " * left_padding + f"{self.ticker} @ {self.last_price}"

    def get_ohlc_text(self):
        lst = list()
        for k, v in self.ohlc.items():
            lst.append(f"{k.upper()}: {v}")
        return ", ".join(lst)

    def get_layout(self):
        return [
            # Ticker and current price
            [sg.Text(key='price_header', text=self.get_price_header(),
                     font='Arial 40', size=(30, 1))],
            [sg.Text(key='ohlc', text=self.get_ohlc_text(), size=(60, 1))],
            [sg.Text('_'*55)],
            # Number of units and transaction buttons
            [
                sg.Button('Buy', pad=(10, 0),
                          tooltip="Buy units (shortcut \'b\')"),
                sg.Button('Sell', pad=(0, 0),
                          tooltip="Sell units (shortcut \'s\'"),
                sg.Button('Close All', pad=(10, 0),
                          tooltip="Close all positions (shortcut \'c\'"),
                sg.Text(' ' * 5),
                sg.Text('Units:'),
                sg.InputText(default_text=self.default_units, size=(6, 1)),
            ],
            # Log
            [sg.Multiline(default_text=self.log_start_text, disabled=True,
                          key='log', autoscroll=True, size=(55, 30))],
        ]

