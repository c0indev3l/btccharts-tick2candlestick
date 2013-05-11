#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""    
.. module:: symbol
   :platform: Unix, Windows, Mac OS X
   :synopsis: Module to download tick data from BitcoinCharts
   
   http://api.bitcoincharts.com/v1/csv/

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

import os
import argparse
from symbol import Symbol
from timeframe import TF

import urllib2
from urlparse import urljoin

import datetime
import dateutil.parser

import pandas as pd

class ApiRequestBitcoinchartsGetTicks:
    """"Class to download (or read) tick data from BitcoinCharts
    using http://api.bitcoincharts.com/v1/csv/{symbol}.csv
    with {symbol}=mtgoxUSD
    """
    
    filename = ''
    data = ''
    dataframe = None
    dataframe_out = None
    
    def __init__(self, args):
        self.args = args
        
        self.basepath = ARGS.basepath
        self.symbol = ARGS.symbol
        self.dt1 = ARGS.dt1
        self.dt2 = ARGS.dt2
        self.timeframe = ARGS.tf
        self.flag_download_overwrite = ARGS.downloadagain

        self.api_url = self.symbol.shortname()+'.csv'
        self.api_base_url = "http://api.bitcoincharts.com/v1/csv/"
        self.url = urljoin(self.api_base_url, self.api_url)        

    def update(self):
        """Update data (get, convert to DataFrame, print, resample..."""
        self.get_data()
        #self.pretty_print_data()
        self.convert_to_dataframe()
        self.pretty_print_dataframe(self.dataframe)
        self.calculate()

    def get_data(self):
        """Get data (download and write or read from file)"""
        self.filename = os.path.join(self.basepath,
            "data_in/ticks_{api_url}".format(
                api_url=self.api_url,
            )
        )
        
        file_not_exists = not os.path.exists(self.filename)
        
        if self.flag_download_overwrite or file_not_exists:
            self.download()
            self.write_data()
        else:
            self.read_data()

    def download(self):
        """Download data"""
        print("Downloading using url {url} (please wait)".format(url=self.url))
        response = urllib2.urlopen(self.url)        
        self.data = response.read()
        
    def write_data(self):
        """Write data to file"""
        print("Writing {api_url} to {filename}"\
            .format(api_url=self.api_url, filename=self.filename))
        my_file = open(self.filename, 'w')
        my_file.write(self.data)
        my_file.close()

    def read_data(self):
        """Display read data from file message"""
        print("Reading {api_url} from {filename}"\
            .format(api_url=self.api_url, filename=self.filename))
        print("    instead of downloading using url {url}".format(url=self.url))

    def pretty_print_data(self):
        """Print raw data (CSV here)"""
        print(self.data)

    def pretty_print_dataframe(self, dataframe):
        """Print DataFrame (head, ... tail, dtypes)"""
        print(dataframe.head())
        print(dataframe)
        print(dataframe.tail())
        print(dataframe.dtypes)

    #def conv_timestamp_to_datetime(x):
    #    return(datetime.datetime.fromtimestamp(x, dateutil.tz.tzutc()))
    
    def convert_to_dataframe(self):
        """Convert raw data to a Python Pandas DataFrame"""
        self.dataframe = pd.read_csv(self.filename,
            names=['TIMESTAMP', 'PRICE', 'VOL'])

    def calculate(self):
        """Convert data to appropriate type, calculate, resample"""

        print("Convert data type")

        self.dataframe['TIMESTAMP'] = \
            pd.to_datetime(self.dataframe['TIMESTAMP']*int(1e9))
        #print(self.dataframe.dtypes)
        self.dataframe = \
            self.dataframe.set_index('TIMESTAMP').astype('float64')
            
        self.dataframe['TICK_VOL'] = 1

        #self.dataframe = self.dataframe.set_index('TIMESTAMP')
        #self.dataframe['TIMESTAMP'] = pd.DatetimeIndex(
        #self.dataframe['TIMESTAMP'])
        
        price_digits = 5
        vol_digits = 8
        self.dataframe['PRICE'] = self.dataframe['PRICE'].map(
            lambda x: int(x * 10**price_digits))
        
        self.dataframe['VOL'] = self.dataframe['VOL'].map(
            lambda x: int(x * 10**vol_digits))

        if self.dt1 != None:
            self.dataframe = self.dataframe[self.dataframe.index >= self.dt1]
        
        if self.dt2 != None:
            self.dataframe = self.dataframe[self.dataframe.index <= self.dt2]
                
        print("="*100)
        print("Tick data")
        self.pretty_print_dataframe(self.dataframe)
        print("="*100)            
        
        #self.dataframe_out = self.dataframe.resample('15Min', how='ohlc')

        print("Resample ticks data to OHLC candlesticks {tf} (please wait)"\
            .format(tf=self.timeframe))
        
        timeframes_pandas_names = {
            TF.M1: '1min',
            TF.M5: '5min',
            TF.M15: '15min',
            TF.M30: '30min',
            TF.H1: 'H1',
            TF.H2: 'H2',
            TF.H4: 'H4',
            TF.H6: 'H6',
            TF.H12: 'H12',
            TF.D1: 'D1',
            TF.W1: 'W1',
            TF.MN: 'M',
        }
        
        timeframe_pd = timeframes_pandas_names[self.timeframe]
                
        self.dataframe_out = self.dataframe['PRICE']\
            .resample(timeframe_pd, how='ohlc')
        
        self.dataframe_out['VOL'] = self.dataframe['VOL']\
            .resample(timeframe_pd, how='sum')
        
        self.dataframe_out['TICK_VOL'] = self.dataframe['TICK_VOL']\
            .resample(timeframe_pd, how='sum')
        self.dataframe_out['TICK_VOL'] = self.dataframe_out['TICK_VOL'].fillna(0)
        # or .fillna(1)
        
        self.dataframe_out = self.dataframe_out.rename(
            columns={
                'open': 'OPEN',
                'high': 'HIGH',
                'low': 'LOW',
                'close': 'CLOSE',
            }
        )
        
        print("Fill NaN (VOLUME=0 and OPEN=HIGH=LOW=CLOSE=CLOSE_PREVIOUS)")
        #self.dataframe_out['MISSING'] = self.dataframe_out['VOL'].isnull()
        self.dataframe_out['VOL'] = self.dataframe_out['VOL'].fillna(0)
        self.dataframe_out['CLOSE'] = self.dataframe_out['CLOSE'].fillna()
        self.dataframe_out['OPEN'] = self.dataframe_out['OPEN']\
            .fillna(self.dataframe_out['CLOSE'])
        self.dataframe_out['LOW'] = self.dataframe_out['LOW']\
            .fillna(self.dataframe_out['CLOSE'])
        self.dataframe_out['HIGH'] = self.dataframe_out['HIGH']\
            .fillna(self.dataframe_out['CLOSE'])

        for col in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL', 'TICK_VOL']:
            self.dataframe_out[col] = self.dataframe_out[col].map(int)
        
        #self.dataframe_out.index = self.dataframe_out.index.map(lambda x: (x.to_pydatetime()))
        self.dataframe_out['TIMESTAMP'] = self.dataframe_out.index
        self.dataframe_out['TIMESTAMP'] = self.dataframe_out.index.map(lambda x: int(x.to_pydatetime().strftime('%s')))

        print("Reorder columns")
        self.dataframe_out = self.dataframe_out.reindex_axis(['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL', 'TICK_VOL'], axis=1)
        
        print("="*100)
        print("Candlestick data")
        self.pretty_print_dataframe(self.dataframe_out)
        print("="*100)
        
        self.output_file()
        
    def output_file(self):
        for to_format in ARGS.to.split(','):
            to_format = to_format.lower()
            
            if to_format == 'csv':
                self.to_csv()
            elif to_format == 'xls':
                self.to_xls()
            elif to_format == 'hdf5':
                self.to_hdf5()
            else:
                print("File format '{to_format}' is not supported".format(to_format=to_format))
                
    def output_filename(self, ext):
        dt_format = '%Y%m%d%H%M'
        dt1_str = self.dataframe_out.index[0]\
            .to_pydatetime().strftime(dt_format)
        dt2_str = self.dataframe_out.index[-1]\
            .to_pydatetime().strftime(dt_format)
        filename = os.path.join(self.basepath,
            "data_out/{symbol}-{timeframe}-{dt1}-{dt2}.{ext}".format(
            symbol = self.symbol.longname(),
            timeframe = self.timeframe.name(),
            dt1 = dt1_str,
            dt2 = dt2_str,
            ext = ext))
        return(filename)        

    def to_xls(self):
        """Output excel file"""
        filename = self.output_filename('xls')
        print("Save to Excel file as {filename}".format(filename=filename))
        self.dataframe_out.to_excel(filename, index=False)

    def to_csv(self):
        """Output CSV file"""
        filename = self.output_filename('xls')
        print("Save to CSV file as {filename}".format(filename=self.output_filename('csv')))
        self.dataframe_out.to_csv(filename, index=False)

    def to_hdf5(self):
        """Output HDF5 file"""
        filename = self.output_filename('h5')
        print("Save to HDF5 file as {filename}".format(filename=filename))
        try:
            os.remove(filename) # remove h5 file to avoid it to inflate
        except:
            print("Can't remove {filename} (maybe this file doesn't exist)".format(filename=filename))
        store = pd.HDFStore(filename, complevel=9, complib='blosc')
        store.append('df', self.dataframe_out)
        store.close()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Use the following parameters')
    
    PARSER.add_argument('--downloadagain', action="store_true",
        help="use this flag to overwrite data (downloading them again...)\n\
please don't use this too often!")

    PARSER.add_argument('--dt1', action="store",
        help="use this flag to set datetime from (2012-01-01T00:00Z)",
        default=None)
        
    PARSER.add_argument('--dt2', action="store",
        help="use this flag to set datetime to (2013-12-31T00:00Z)",
        default=None)
        
    PARSER.add_argument('--tf', action="store",
        help="use this flag to set timeframe \
(M1, M5, M15, M30, H1, H4, D1, W1, MN, YR)",
        default='M15')
        
    PARSER.add_argument('--symbol', action="store",
        help="use this flag to set market symbol (mtgox|BTC/USD)",
        default='mtgox|BTC/USD')

    PARSER.add_argument('--to', action="store",
        help="use this flag to set output file ('csv', 'xls', 'hdf5', 'csv,hdf5')")

        
    ARGS = PARSER.parse_args()

    ARGS.basepath = os.path.dirname(__file__)

    ARGS.symbol = Symbol(ARGS.symbol)

    ARGS.tf = TF.from_string(ARGS.tf)
    
    if ARGS.dt1 != None:
        ARGS.dt1 = dateutil.parser.parse(ARGS.dt1)
    
    if ARGS.dt2 != None:
        ARGS.dt2 = dateutil.parser.parse(ARGS.dt2)
        if ARGS.dt2 < ARGS.dt1:
            raise(Exception('dt2 < dt1 !'))
            
    #print(ARGS.dt1)
    
    DATATICKS = ApiRequestBitcoinchartsGetTicks(ARGS)
    DATATICKS.update()

