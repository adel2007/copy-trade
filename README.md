# copy-trade
you need a copy trading between your mt5 account well this well help you!😉

at the first you need do 3 thing

1:installing python on your system from below link : https://www.python.org/downloads/

2:install metatrader5 with pip , first press windows+r , type CMD and press enter now pase this on yor terminal "pip install MetaTrader5"

after installing the requirements your ready to do the next step

open server.py whit notepad and pute your secound account information on it for example :

account = 123456

password = "passwoard"

server = "metatrader_server"

next step :

paste the server.py on your destination metatrader (the second account on which you intend to copy trades) data folder

paste the copy_trading.ex5 on your first metatrader data folder

if you dont now the location of your data folder reade this : https://www.mql5.com/en/blogs/post/751359

on the first terminal :

open open options from tools menu (ctrl+o)


1:go to expert advisors tab

2:enable allow webrequest for listed url

3:click on add new url and enter following url : 127.0.0.1

4:press ok and close

![expert](https://github.com/adel2007/copy-trade/assets/75173278/0960e6a1-c120-4005-920d-b9a1934771a5)


now you just need to drag the server.py file in secound terminal in a chart windows

and drag the copy_trading file in first(main) terminal in a chart windows

thats done enjoy!
