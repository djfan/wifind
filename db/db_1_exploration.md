```mysql
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| capstonemysql      |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

```mysql
use capstonemysql;
show tables;
+----------------------------+
| Tables_in_capstonemysql    |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_content_type        |
| django_migrations          |
| django_site                |
| gpsq                       |
| ingestion_scan             |
| test_unique_locations      |
| wifi_scan                  |
| wifi_scan_orig             |
| wifi_scan_temp             |
+----------------------------+
```

```mysql
describe wifi_scan;
+---------------+---------------+------+-----+---------+----------------+
| Field         | Type          | Null | Key | Default | Extra          |
+---------------+---------------+------+-----+---------+----------------+
| idx           | bigint(20)    | NO   | PRI | NULL    | auto_increment |
| lat           | double        | NO   |     | NULL    |                |
| lng           | double        | NO   |     | NULL    |                |
| acc           | float         | NO   |     | NULL    |                |
| altitude      | double        | NO   |     | NULL    |                |
| time          | decimal(15,0) | NO   |     | NULL    |                |
| device_mac    | varchar(20)   | NO   |     | NULL    |                |
| app_version   | varchar(10)   | NO   |     | NULL    |                |
| droid_version | varchar(10)   | NO   |     | NULL    |                |
| device_model  | varchar(50)   | NO   |     | NULL    |                |
| ssid          | varchar(100)  | YES  | MUL | NULL    |                |
| bssid         | varchar(20)   | YES  |     | NULL    |                |
| caps          | varchar(100)  | YES  |     | NULL    |                |
| level         | float         | YES  |     | NULL    |                |
| freq          | float         | YES  |     | NULL    |                |
+---------------+---------------+------+-----+---------+----------------+

select count(*) from wifi_scan;
+----------+
| count(*) |
+----------+
| 44233832 |
+----------+

select * from wifi_scan limit 1 \G;
*************************** 1. row ***************************
          idx: 1
          lat: 40.6927366
          lng: -73.9862345
          acc: 24.948
     altitude: 0
         time: 1416428624717
   device_mac: 40:b0:fa:c4:5d:5f
  app_version: 0.5
droid_version: 4.2.2
 device_model: Nexus 4
         ssid: nyupda
        bssid: cc:d5:39:27:ec:9c
         caps: [ESS]
        level: -72
         freq: 5180
*************************** 2. row ***************************
          idx: 2
          lat: 40.6927366
          lng: -73.9862345
          acc: 24.948
     altitude: 0
         time: 1416428624717
   device_mac: 40:b0:fa:c4:5d:5f
  app_version: 0.5
droid_version: 4.2.2
 device_model: Nexus 4
         ssid: nyu
        bssid: cc:d5:39:27:f0:bf
         caps: [WPA-EAP-TKIP][WPA2-EAP-CCMP][ESS]
        level: -49
         freq: 5240

select count(*) from wifi_scan where altitude != 0;
+----------+
| count(*) |
+----------+
| 42886102 |
+----------+

select count(distinct time) from wifi_scan;
+----------------------+
| count(distinct time) |
+----------------------+
|               828582 |
+----------------------+

select count(distinct ssid) from wifi_scan;
+----------------------+
| count(distinct ssid) |
+----------------------+
|               330214 |
+----------------------+
select ssid, count(*) from wifi_scan group by ssid order by count desc limit 25;
+--------------------------+---------+
| ssid                     | count   |
+--------------------------+---------+
|                          | 4350276 |
| optimumwifi              | 1730520 |
| CableWiFi                | 1713510 |
| TWCWiFi                  | 1681210 |
| TWCWiFi-Passpoint        | 1397019 |
| DowntownBrooklynWiFi_Fon |  695657 |
| xfinitywifi              |  572289 |
| nyuguest                 |  454613 |
| nyu                      |  429604 |
| eduroam                  |  394809 |
| attwifi                  |  183145 |
| @smartfi-open            |  159776 |
| @smartfi-passpoint       |  152517 |
| ncpsp                    |  137223 |
| NYU-ROAM3                |  112403 |
| DG1670A52-5G             |  109861 |
| DG1670A72-5G             |   95182 |
| DG1670A62-5G             |   95022 |
| TG1672G32-5G             |   94402 |
| DG1670A42-5G             |   92877 |
| DG1670A82-5G             |   92702 |
| nyu-legacy               |   91970 |
| TG1672GD2-5G             |   89655 |
| linknyc free wi-fi       |   89048 |
| DG1670AD2-5G             |   87775 |
+--------------------------+---------+

select lat, lng, count(*) as count from wifi_scan group by lat, lng order by count desc limit 10;
+-------------+--------------+-------+
| lat         | lng          | count |
+-------------+--------------+-------+
|  40.6309443 |   -73.958346 | 18747 |
| 40.68915057 | -73.98213411 |  7696 |
| 40.68915846 | -73.98214533 |  7592 |
| 40.68916575 | -73.98215932 |  7488 |
| 40.68917316 | -73.98217332 |  7171 |
| 40.68921591 | -73.98225352 |  7102 |
| 40.68918125 | -73.98219047 |  7070 |
| 40.68922664 | -73.98227507 |  6996 |
| 40.68919011 | -73.98220913 |  6969 |
| 40.68795626 |  -73.9818954 |  6916 |
+-------------+--------------+-------+

select caps, count(*) as count, 100.0*count(*)/44233832 as percent from wifi_scan group by caps order by count desc limit 10;
+---------------------------------------------------+---------+----------+
| caps                                              | count   | percent  |
+---------------------------------------------------+---------+----------+
| [wpa2-psk-ccmp][wps][ess][ble]                    | 7809530 | 17.65511 |
| [ESS]                                             | 7617670 | 17.22137 |
| [WPA2-PSK-CCMP][ESS]                              | 5678430 | 12.83730 |
| [WPA2-PSK-CCMP][WPS][ESS]                         | 5355782 | 12.10789 |
| [ess][ble]                                        | 2449495 |  5.53761 |
| [WPA-PSK-CCMP+TKIP][WPA2-PSK-CCMP+TKIP][WPS][ESS] | 1869310 |  4.22597 |
| [wpa2-psk-ccmp][ess][ble]                         | 1619854 |  3.66203 |
| [WPA-PSK-CCMP+TKIP][WPA2-PSK-CCMP+TKIP][ESS]      | 1229621 |  2.77982 |
| [WPA2-EAP-CCMP][ESS]                              |  890183 |  2.01245 |
| [WEP][ESS]                                        |  837604 |  1.89358 |
+---------------------------------------------------+---------+----------+

```



```mysql
describe gpsq;
+-------------------+---------------+------+-----+---------+-------+
| Field             | Type          | Null | Key | Default | Extra |
+-------------------+---------------+------+-----+---------+-------+
| ROUND(time*0.001) | decimal(17,0) | NO   |     | 0       |       |
| FORMAT(lat, 5)    | varchar(62)   | YES  |     | NULL    |       |
| FORMAT(lng, 5)    | varchar(62)   | YES  |     | NULL    |       |
| level             | float         | YES  |     | NULL    |       |
| bssid             | varchar(20)   | YES  |     | NULL    |       |
+-------------------+---------------+------+-----+---------+-------+

select count(*) from gpsq;
+----------+
| count(*) |
+----------+
|   429604 |
+----------+

select * from gpsq limit 2;
+-------------------+----------------+----------------+-------+-------------------+
| ROUND(time*0.001) | FORMAT(lat, 5) | FORMAT(lng, 5) | level | bssid             |
+-------------------+----------------+----------------+-------+-------------------+
|        1416428625 | 40.69274       | -73.98623      |   -49 | cc:d5:39:27:f0:bf |
|        1416428625 | 40.69274       | -73.98623      |   -64 | cc:d5:39:27:f2:40 |
+-------------------+----------------+----------------+-------+-------------------+

```



```mysql
SELECT * FROM gpsq INTO OUTFILE 'GPSQ.CSV' FIELDS ENCLOSED BY '"' TERMINATED BY ';' ESCAPED BY '"' LINES TERMINATED BY '\r\n';
```

