#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""    
.. module:: timeframe
   :platform: Unix, Windows, Mac OS X
   :synopsis: Module to manage timeframes \
(such as 'TF.M1', 'TF.M5', 'TF.H1', 'TF.D1'....).

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

import datetime

class TimeframeElement:
    """class to manage TimeframeElement such as 'M1', 'M5', 'H1', ..."""

    def __init__(self, name='M1', minute=1):
        self.__minute = minute
        self.__name = name
        
    def timedelta(self):
        """timedelta()

    Returns datetime.timedelta of TimeframeElement.

    Returns:
        A datetime.timedelta of TimeframeElement
        example for M15:

        datetime.timedelta(0, 900)
        """
        return(datetime.timedelta(minutes=self.__minute))

    def minutes(self):
        """minutes()

    Returns number of minutes for a TimeframeElement.

    Returns:
        integer
        example for M15:

        15
        """
        return(self.__minute)
        
    def name(self):
        """name()

    Returns name of a TimeframeElement.

    Returns:
        example for M15:

        M15
        """
        return(self.__name)

    def __repr__(self):
        return(self.__name)

    def __eq__(self, tf_elt):
        return(self.__minute == tf_elt.minutes())

    def __hash__(self):
        return(hash(self.__name))




    def floor(self, y):
        """floor(dt)

        Return the floor of dt as a datetime, the largest datetime according to this timeframe less than or equal to dt.
        
        NotImplemented
        """
        raise(NotImplementedError)

    def ceil(self, dt1):
        """ceil(dt)

        Return the ceiling of dt as a datetime, the smallest datetime according to this timeframe greater than or equal to dt.
        
        NotImplemented
        """
        raise(NotImplementedError)

    def round(self, dt1):
        """round(dt)

        Return the datetime rounded to nearest timeframe.
        
        NotImplemented
        """

class Timeframe:
    """class to manage Timeframes \
such as 'TF.M1', 'TF.M5', 'TF.H1', 'TF.D1'...."""

    def __init__(self):
        self.__periods_list = list()
        
        self.append_tf('M1', 1)
        self.append_tf('M5', 5)
        self.append_tf('M15', 15)
        self.append_tf('M30', 30)
        self.append_tf('H1', 60)
        self.append_tf('H2', 120) #?
        self.append_tf('H4', 240)
        self.append_tf('H6', 360) #?
        self.append_tf('H12', 720) #?
        self.append_tf('D1', 1440)
        self.append_tf('W1', 10080)
        self.append_tf('MN', 43200)
        
    def append_tf(self, name, minutes):
        """Append TimeframeElement to Timeframe.

        Args:
           name (str):  name of TimeframeElement.
           minutes (int):  delay (in minutes) of TimeframeElement.
        """
 
        self.__dict__[name] = TimeframeElement(name, minutes)
        self.__periods_list.append(name)
        
    def timeframes(self):
        """TimeframeElement generator

        Returns:
           generator of TimeframeElement in ascending order (if append_tf was called with ascending TF)
        """
        for timeframe in self.__periods_list:
            yield(timeframe)

    def from_string(self, name):
        """Append TimeframeElement to Timeframe.

        Args:
           name (str):  name of TimeframeElement.

        Returns:
           TimeframeElement 

        Raises:
           Exception when timeframe name doesn't exists
           
        """

        if name in self.__dict__:
            return(self.__dict__[name])
        else:
            raise(Exception("Timeframe doesn't exists"))

TF = Timeframe()