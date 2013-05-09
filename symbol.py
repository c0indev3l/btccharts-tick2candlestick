#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""    
.. module:: symbol
   :platform: Unix, Windows, Mac OS X
   :synopsis: Module to manage Symbol \
(such as 'mtgox|BTC/USD', 'mtgox|BTC/EUR', ....).

.. moduleauthor:: Working4coins <working4coins@gmail.com>

    Copyright (C) 2013 "Working4coins" <working4coins@gmail.com>
    You can donate: https://sites.google.com/site/working4coins/donate

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class Symbol:
    """class to manage Symbol such as 'mtgox|BTC/USD'"""

    __exchange = '' # mtgox
    __symbol = '' # BTC/USD
    __cur1 = '' # BTC
    __cur2 = '' # USD

    def __init__(self, name = 'mtgox|BTC/USD'):
        """A class to manage Symbol such as 'mtgox|BTC/USD'

        Args:
           name (str): name of Symbol ('mtgox|BTC/USD').

        """
        # ToDo : RegExp
        self.__name = name
        self.update()

    def update(self):
        """update()

    Updates private attributes such as '__exchange', '__symbol', '__cur1', '__cur2'.

        Returns None
        """
        try:
            (self.__exchange, self.__symbol) = self.__name.split('|')
            (self.__cur1, self.__cur2) = self.__symbol.split('/')
        except:
            msg = "Symbol '{name}' is invalid \
(try something like 'mtgox|BTC/USD')".format(name=self.__name)
            raise(Exception(msg))

    def name(self):
        """name()

    Returns name of Symbol.

    Returns:
        A string which contains name
        example:

        mtgox|BTC/USD
        """
        return(self.__name) # ex mtgox|BTC/USD

    def exchange(self):
        """exchange()

    Returns exchange name of Symbol.

    Returns:
        A string which contains exchange name
        example:

        mtgox
        """
        return(self.__exchange)

    def cur1(self):
        """cur1()

    Returns cur1 name of Symbol.

    Returns:
        A string which contains cur1
        example:

        BTC
        """
        return(self.__cur1)

    def cur2(self):
        """cur2()

    Returns cur2 name of Symbol.

    Returns:
        A string which contains cur2
        example:

        USD
        """
        return(self.__cur2)

    def shortname(self):
        """shortname()

    Returns shortname of Symbol.

    Returns:
        A string which contains shortname
        example:

        mtgoxUSD
        """
        return(self.__exchange+self.__cur2)

    def longname(self):
        """longname()

    Returns longname of Symbol.

    Returns:
        A string which contains longname
        example:

        mtgoxBTCUSD
        """
        return(self.__exchange+self.__cur1+self.__cur2)

    def __eq__(self, symb2):
        return(self.__name == symb2.name())

    def __repr__(self):
        """__repr__()

        Return symbol as a printable string."""

        return(self.__name)
