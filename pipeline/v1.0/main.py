import pandas as pd
import pipline
from pipline import onlyFree, bssidPoint, grid, spatialJoin, dataPlot, updateCarto, urlAPI
#from etl import ClearContent
import etl

# Example:
# l = updateCarto('dj_1', 'dj_all.csv')
# print l
# l2 = updateCarto('djnew', 'dj_f.csv')
# print l2

# API
data = urlAPI(starttime = '06/20/2017', batch = '3000')
df = pd.read_json(data)
# DataFrame from Datebase
# df = pd.read_csv('./motoG4_062212.csv')
# df = pd.read_csv('./motoG4_0629.csv')
print 1

df2 = bssidPoint(df)
print 2
grid(50, df2, 'polygon_grid.shp')
print 3
df3 = spatialJoin('polygon_grid.shp', df2)
print 4
dataPlot(df3, "grid_plot.csv")
print 5
updateCarto('dj_1', "grid_plot.csv")
print 6

f = onlyFree(df)
if len(f) != 0:
	f2 = bssidPoint(f)
	print 2
	# grid(50, df2, 'polygon_grid.shp')
	print 3
	f3 = spatialJoin('polygon_grid.shp', f2)
	print 4
	dataPlot(f3, "grid_plot.csv")
	print 5
	updateCarto('djnew', "grid_plot.csv")
	print 6
else:
	etl.ClearContent('djnew')
	print 'clean up'

