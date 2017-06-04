```mysql
select count(*) from wifi_scan where ssid ='linknyc free wi-fi';
+----------+
| count(*) |
+----------+
|    89048 |
+----------+
```

```mysql
select caps, count(*) as count from wifi_scan where ssid ='linknyc free wi-fi' group by caps order by count desc;
+------------+-------+
| caps       | count |
+------------+-------+
| [ess][ble] | 73103 |
| [ess]      | 15945 |
+------------+-------+
```

```mysql
select lat, lng, count(*) as count from wifi_scan where ssid = 'linknyc free wi-fi' group by lat, lng order by count desc limit 10;
+-------------+--------------+-------+
| lat         | lng          | count |
+-------------+--------------+-------+
| 40.76235602 | -73.98621634 |    23 |
|  40.7624268 | -73.98625099 |    23 |
| 40.76487743 | -73.98365371 |    22 |
| 40.76031231 | -73.96807937 |    20 |
| 40.76297625 | -73.98628633 |    20 |
| 40.76035636 | -73.96795155 |    20 |
| 40.75972293 | -73.96799121 |    20 |
| 40.76504517 | -73.98354649 |    20 |
| 40.76504742 | -73.98361578 |    20 |
| 40.76476604 | -73.98360358 |    20 |
+-------------+--------------+-------+
```

```mysql
select lat, lng, count(*) as count, max(level) as max_level from wifi_scan where ssid = 'linknyc free wi-fi' group by lat, lng order by max_level desc limit 20;
+-------------+--------------+-------+-----------+
| lat         | lng          | count | max_level |
+-------------+--------------+-------+-----------+
| 40.73570802 | -73.98533739 |     7 |       -29 |
| 40.74009644 | -73.98198972 |     4 |       -30 |
| 40.71964298 | -73.99418821 |     1 |       -30 |
| 40.71965103 | -73.99416537 |     1 |       -30 |
| 40.71965956 | -73.99415686 |     1 |       -30 |
| 40.74457577 | -73.99916136 |    10 |       -31 |
| 40.74457161 | -73.99917257 |    10 |       -31 |
| 40.74455356 | -73.99919137 |    10 |       -31 |
| 40.74452877 | -73.99920246 |    10 |       -31 |
| 40.74010753 | -73.98198012 |     4 |       -31 |
| 40.74008716 | -73.98199937 |     3 |       -32 |
| 40.74005644 | -73.98202472 |     3 |       -32 |
| 40.74041871 | -73.98200599 |     5 |       -32 |
| 40.74006551 |  -73.9820163 |     3 |       -32 |
| 40.72137994 | -73.99343059 |     4 |       -32 |
| 40.73997224 | -74.00234404 |     7 |       -32 |
|  40.7399634 | -74.00235832 |     7 |       -32 |
| 40.72141302 | -73.99342472 |     4 |       -33 |
| 40.73615772 |  -73.9849797 |     5 |       -33 |
|  40.7646891 | -73.98406031 |     6 |       -33 |
+-------------+--------------+-------+-----------+
```

```mysql
select lat, lng, max(level) as max_level, min(level) as min_level, avg(level) as mean_level from wifi_scan where ssid = 'linknyc free wi-fi' group by lat, lng order by max_level desc limit 20;
+-------------+--------------+-----------+-----------+---------------------+
| lat         | lng          | max_level | min_level | mean_level          |
+-------------+--------------+-----------+-----------+---------------------+
| 40.73570802 | -73.98533739 |       -29 |       -74 |  -60.57142857142857 |
| 40.71964298 | -73.99418821 |       -30 |       -30 |                 -30 |
| 40.71965103 | -73.99416537 |       -30 |       -30 |                 -30 |
| 40.71965956 | -73.99415686 |       -30 |       -30 |                 -30 |
| 40.74009644 | -73.98198972 |       -30 |       -83 |              -53.25 |
| 40.74452877 | -73.99920246 |       -31 |       -81 |               -55.2 |
| 40.74010753 | -73.98198012 |       -31 |       -81 |               -56.5 |
| 40.74457577 | -73.99916136 |       -31 |       -81 |               -55.2 |
| 40.74457161 | -73.99917257 |       -31 |       -81 |               -55.2 |
| 40.74455356 | -73.99919137 |       -31 |       -81 |               -55.2 |
|  40.7399634 | -74.00235832 |       -32 |       -76 | -57.285714285714285 |
| 40.74005644 | -73.98202472 |       -32 |       -81 | -53.666666666666664 |
| 40.74041871 | -73.98200599 |       -32 |       -66 |               -55.6 |
| 40.72137994 | -73.99343059 |       -32 |       -53 |               -42.5 |
| 40.74006551 |  -73.9820163 |       -32 |       -84 | -57.666666666666664 |
| 40.74008716 | -73.98199937 |       -32 |       -83 | -54.666666666666664 |
| 40.73997224 | -74.00234404 |       -32 |       -76 | -57.285714285714285 |
|  40.7646891 | -73.98406031 |       -33 |       -73 | -54.666666666666664 |
| 40.72141302 | -73.99342472 |       -33 |       -53 |                 -43 |
| 40.74425914 | -73.99940626 |       -33 |       -70 |              -53.25 |
+-------------+--------------+-----------+-----------+---------------------+
```

```mysql
select * from (select lat, lng, max(level) as max_level, min(level) as min_level, avg(level) as mean_level, count(*) as count from wifi_scan where ssid = 'linknyc free wi-fi' group by lat, lng order by mean_level desc) as A where A.count>5 limit 20;

+-------------+--------------+-----------+-----------+---------------------+-------+
| lat         | lng          | max_level | min_level | mean_level          | count |
+-------------+--------------+-----------+-----------+---------------------+-------+
| 40.73628911 | -73.98488113 |       -43 |       -62 | -51.333333333333336 |     6 |
| 40.73621884 | -73.98495749 |       -44 |       -58 |               -51.5 |     6 |
| 40.73620295 | -73.98496547 |       -43 |       -65 | -52.333333333333336 |     6 |
|  40.7646794 | -73.98416713 |       -44 |       -60 | -54.166666666666664 |     6 |
|  40.7362987 | -73.98488344 |       -48 |       -60 | -54.166666666666664 |     6 |
|  40.7363085 | -73.98488297 |       -49 |       -64 | -54.333333333333336 |     6 |
| 40.73631708 | -73.98487827 |       -49 |       -64 |               -54.5 |     6 |
| 40.76283854 | -73.98560134 |       -46 |       -68 |               -54.5 |     8 |
|  40.7646891 | -73.98406031 |       -33 |       -73 | -54.666666666666664 |     6 |
| 40.74450756 | -73.99916098 |       -42 |       -68 | -54.833333333333336 |     6 |
|  40.7646202 | -73.98431501 |       -45 |       -63 |                 -55 |     6 |
| 40.76459831 | -73.98435869 |       -47 |       -64 |                 -55 |     6 |
| 40.76465311 | -73.98420285 |       -43 |       -61 |                 -55 |     6 |
| 40.74452877 | -73.99920246 |       -31 |       -81 |               -55.2 |    10 |
| 40.74457577 | -73.99916136 |       -31 |       -81 |               -55.2 |    10 |
| 40.74457161 | -73.99917257 |       -31 |       -81 |               -55.2 |    10 |
| 40.74455356 | -73.99919137 |       -31 |       -81 |               -55.2 |    10 |
| 40.76465014 | -73.98424041 |       -45 |       -63 |               -55.5 |     6 |
| 40.76474402 | -73.98365786 |       -38 |       -70 |  -55.57142857142857 |     7 |
| 40.76453052 | -73.98446466 |       -45 |       -63 | -55.666666666666664 |     6 |
+-------------+--------------+-----------+-----------+---------------------+-------+

```
