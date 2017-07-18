import pandas as pd
import pipline
from pipline import onlyFree, bssidPoint, grid, spatialJoin, dataPlot, updateCarto, urlAPI
import etl
import time


# API
# data = urlAPI(starttime = '06/20/2017', batch = '3000')
# df = pd.read_json(data)
# DataFrame from Datebase
# df = pd.read_csv('./motoG4_062212.csv')
df = pd.read_csv('~/Desktop/motoG4_0629.csv')
print 1

df2 = bssidPoint(df)
print 12
grid(50, df2, 'polygon_grid.shp')
print 13
df3 = spatialJoin('polygon_grid.shp', df2)
print 14
unimin1, unimax1 = dataPlot(df3, "grid_plot.csv")
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
	time.sleep(20)
	print 26



try:
	unimin = min(unimin1, unimin2)
	unimax = max(unimax1, unimax2)
except:
	unimin = unimin1
	unimax = unimax1
print unimin, unimax

a = 'POLYGON ((0 0, 0 0, 0 0, 0 0, 0 0))'
b = 'POLYGON ((0.1 0.1, 0.1 0.1, 0.1 0.1, 0.1 0.1, 0.1 0.1))'
maxpoly = [-1, a, unimax]
minpoly = [-1, b, unimin]
tmp = pd.read_csv("grid_plot.csv", index_col=0)
# tmp = tmp.append(pd.DataFrame([maxpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
tmp = tmp.append(pd.DataFrame([minpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
print tmp.uni.max(), tmp.uni.min()
tmp.to_csv("grid_plot.csv")

updateCarto('allwifi', "grid_plot.csv")
time.sleep(20)
print 16

if len(f) != 0:
	tmp = pd.read_csv("grid_plot_free.csv", index_col=0)
	tmp = tmp.append(pd.DataFrame([maxpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
	tmp = tmp.append(pd.DataFrame([minpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
	tmp.to_csv("grid_plot_free_same_color_range.csv")
	updateCarto('freewifi_same_color_range', "grid_plot_free_same_color_range.csv")
	print 36
else:
	etl.ClearContent('freewifi_same_color_range')
	print 'No Free WiFi! Clean Up!'