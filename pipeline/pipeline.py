import pandas as pd
from shapely.geometry import Point
import datetime as dt
import geopandas as gpd
from fiona.crs import from_epsg
import os
#import etl
import py_compile
import math
import shapefile as shp
import requests

# old
# free_wifi = ['#flatiron free wifi', 'freewifibysurface', 'bryantpark.org', \
# 'DowntownBrooklynWiFi_Fon', \
# 'linknyc free wi-fi', 'Metrotech', \
# 'usp park wifi', 'Red Hook Wifi']

# new
free_wifi = ["flatiron free wifi","flatiron","freewifibysurface","bryantpark.org","bryantpark",\
"downtownbrooklynwifi_fon","downtownbrooklyn","linknyc free wi-fi","linknyc","metrotech",\
"usp park wifi","usppark","red hook wifi","redhook","attwifi","guestwifi","guest", "unionsquarewifi"]


def urlAPI(starttime = '06/20/2017', batch = '3000'):
	#starttime = '06/20/2017'
	#batch = '3000' # how many records you want to fetch 
	url = 'http://wifindproject.com/wifipulling/?columns=lat%7Clng%7Cssid%7Cbssid%7Ctime&startdate='+starttime+'&batch='+batch+'&timeformat=1'
	resp = requests.get(url)
	print url
	return resp.text

def onlyFree(df):
	s1 = set(df.ssid)
	s2 = set(free_wifi)
	free_wifi_intersection = list(s1.intersection(s2))
	tmp = df[df['ssid'].isin(free_wifi_intersection)]
	return tmp

def datetime(df):
	df['time2'] = pd.to_datetime(df.time)
	df['month'] = map(lambda x: x.month, df['time2'])
	df['day'] = map(lambda x: x.day, df['time2'])
	df['hour'] = map(lambda x: x.hour, df['time2'])
	df['minute'] = map(lambda x: x.minute, df['time2'])
	df['sec'] = map(lambda x: x.second, df['time2'])
	return df

def bssidPoint(df, fromEPSG=4326, toEPSG=2263, acc_threshold=None):
	if acc_threshold:
		df = df[df.acc <= acc_threshold]
	# return geo dataframe (Point) with unique bssid
	df['geo'] = zip(df.lng, df.lat)
	access_count = df.groupby(df.geo).apply(lambda x: len(x.bssid.unique()))
	access_bssidList = df.groupby(df.geo).apply(lambda x: list(x.bssid.unique()))
	df = pd.DataFrame(map(lambda x: Point(x), access_count.index), columns=['geometry'])
	df['unique_bssid_count'] = access_count.values
	df['unique_bssid_list'] = access_bssidList.values
	df= gpd.GeoDataFrame(df)
	df.crs = from_epsg(fromEPSG)
	df.to_crs(epsg=toEPSG, inplace=True)
	df.to_pickle('unique_bssid.p')
	return df

def grid(cell_length, df, output='polygon_grid', MINx=None, MAXx=None, MINy=None, MAXy=None):
	# grid boundry
	if (MINx and MAXx and MINy and MINx):
		minx, maxx, miny, maxy = MINx, MAXx, MINy, MAXy
	else:
		all_x = map(lambda p: p.x, df.geometry)
		all_y = map(lambda p: p.y, df.geometry)
		minx, maxx, miny, maxy = min(all_x), max(all_x), min(all_y), max(all_y) 
	# grid length
	dx = cell_length
	dy = cell_length
	nx = int(math.ceil(abs(maxx - minx)/dx))
	ny = int(math.ceil(abs(maxy - miny)/dy))
	# grid plotting
	g = shp.Writer(shp.POLYGON)
	g.autoBalance = 1
	g.field("ID")
	id=0
	for i in range(ny):
		for j in range(nx):
			id+=1
			vertices = []
			parts = []
			vertices.append([min(minx+dx*j,maxx),max(maxy-dy*i,miny)])
			vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*i,miny)])
			vertices.append([min(minx+dx*(j+1),maxx),max(maxy-dy*(i+1),miny)])
			vertices.append([min(minx+dx*j,maxx),max(maxy-dy*(i+1),miny)])
			parts.append(vertices)
			g.poly(parts)
			g.record(id)
	g.save(output)
	# return g

def spatialJoin(grid, bssid, toEPSG=2263):
	# Both grid and uni_bssid should be GeoDataFrame.
	grid = gpd.read_file(grid)
	grid.crs = from_epsg(toEPSG)
	# print 'g',grid.crs
	uni_bssid = bssid
	uni_bssid.to_crs(epsg=2263, inplace=True)
	# print 'u',uni_bssid.crs 
	# which cell does the Point intersect with?
	PointInPoly = gpd.sjoin(uni_bssid, grid, how='left', op='intersects')
	PointInPoly.dropna(subset=['ID'], inplace=True)
	# groupby cell.ID to get list of bssid (with duplications) for each cell
	# then calculate length of unique bssid "uni"
	grouped = PointInPoly.groupby('ID').apply(lambda x: reduce(lambda x,y: x+y, x.unique_bssid_list))
	bssidInPoly = pd.DataFrame(grouped, columns=['all_bssid_list']) 
	bssidInPoly['uni'] = map(lambda x: len(set(x)), grouped)
	bssidInPoly['ID'] = bssidInPoly.index
	bssidInPoly.reset_index(drop=True, inplace=True)
	grid_bssid = pd.merge(grid, bssidInPoly, how='left', on='ID')
	grid_bssid.to_crs(epsg=toEPSG, inplace=True)
	return grid_bssid

def dataPlot(df, output):
	# input df should be a GeoDataFrame
	# return length of grid_plot
	grid_plot = df.loc[:, ['ID', 'uni', 'geometry']]
	grid_plot.dropna(subset=['uni'], inplace=True) 
	grid_plot.to_csv(output)
	return grid_plot.uni.min(), grid_plot.uni.max()
	# return len(grid_plot)

def etlConfig(table, csv, account, api):
	import os
	os.system("rm " + "./etl.conf")
	with open("./etl.conf", 'w') as f:
		f.write("[carto]\nbase_url=https://{}.carto.com/\n".format(account))
		f.write("api_key={}\n".format(api)) 
		f.write("table_name={tbname}\n".format(tbname=table))
		f.write("columns=uni,ID\n")
		f.write("[etl]\nchunk_size={l}\n".format(l=pd.read_csv(csv).shape[0]+50))
		f.write("max_attempts=3\n")
		f.write("[log]\nfile=etl.log\nlevel=debug")



def updateCarto(table, csv, cartoAPI="myAPI.txt", fromEPSG=2263):
	with open(cartoAPI, 'r') as f:
		myAPI = f.read().splitlines()
	etlConfig(table, csv, myAPI[0], myAPI[1])
	py_compile.compile("etl.py")
	import etl
	etl.table_name = table
	etl.chunk_size = pd.read_csv(csv).shape[0]
	etl.ClearContent(table)
	job = etl.InsertJob(csv_file_path=csv, srid=fromEPSG, table=table)
	log = job.run()
	return log

def addMaxMin(input_csv, output_csv, unimin=None, unimax=None):
	tmp = pd.read_csv(input_csv, index_col=0)
	maxpoly = [-1, 'POLYGON ((0 0, 0 0, 0 0, 0 0, 0 0))', unimax]
	minpoly = [-1, 'POLYGON ((0.1 0.1, 0.1 0.1, 0.1 0.1, 0.1 0.1, 0.1 0.1))', unimin]
	print len(tmp)
	if unimax:
		tmp = tmp.append(pd.DataFrame([maxpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
	if unimin:
		tmp = tmp.append(pd.DataFrame([minpoly], columns=['ID', 'geometry', 'uni']),ignore_index=True)
	print len(tmp)
	tmp.to_csv(output_csv)

def rm(list_of_files):
	import os
	for file in list_of_files:
		try:
			os.system("rm " + file)
			print "\rremove {}".format(file),
		except:
			print "\r{} not exist".format(file),