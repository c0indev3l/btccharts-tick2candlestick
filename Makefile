all:
	python tick2candlestick.py --symbol "mtgox|BTC/USD" --tocsv --tf M30 --dt1 2013-01-01T00:00

.PHONY: clean

clean:
	$(RM) data_in/*
	$(RM) data_out/*
	$(RM) *.pyc