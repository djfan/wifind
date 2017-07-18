import pandas as pd
import pipeline
from pipeline import onlyFree, bssidPoint, grid, spatialJoin, dataPlot, updateCarto, urlAPI, rm, addMaxMin
import etl
import requests
import time


# API 1
# data = urlAPI(starttime = '06/20/2017', batch = '3000')
# df = pd.read_json(data)

# API 2
# url = '?' 
# df = pd.read_json(requests.get(url).text)

# DataFrame: Extracted from Datebase
df = pd.read_csv('~/Desktop/motoG4_0629.csv') # motoG4_062212.csv

print 1
df2 = bssidPoint(df)
print 12
grid(50, df2, 'polygon_grid.shp')
print 13
df3 = spatialJoin('polygon_grid.shp', df2)
print 14
unimin, unimax = dataPlot(df3, "grid_plot.csv")
print 15

f = onlyFree(df)
if len(f) != 0:
	f2 = bssidPoint(f)
	print 22
	# grid(50, df2, 'polygon_grid.shp')
	print 23
	f3 = spatialJoin('polygon_grid.shp', f2)
	print 24
	unimin2, unimax2 = dataPlot(f3, "grid_plot_free.csv")
	print 25
	updateCarto('freewifi', "grid_plot_free.csv")
	print 20
	unimin = min(unimin, unimin2)
	unimax = max(unimax, unimax2)
	time.sleep(20)
	print 26
	addMaxMin('grid_plot.csv', "grid_plot.csv", unimin, None)
print unimin, unimax

updateCarto('allwifi', "grid_plot.csv")
time.sleep(60)
print 16

if len(f) != 0:
	addMaxMin('grid_plot_free.csv', "grid_plot_free_same_color_range.csv", None, unimax)
	updateCarto('freewifi_same_color_range', "grid_plot_free_same_color_range.csv")
	time.sleep(30)
	print 36
else:
	etl.ClearContent('freewifi_same_color_range')
	time.sleep(30)
	etl.ClearContent('freewifi')
	print 'No Free WiFi! Clean Up!'

updateCarto('allwifi', "grid_plot.csv")
time.sleep(60)
print 16

#rm(['polygon_grid.*', 'unique_bssid.p', 'grid_plot.csv', 'grid_plot_free.csv', 'grid_plot_free_same_color_range.csv'])





