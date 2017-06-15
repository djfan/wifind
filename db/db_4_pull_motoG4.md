```shell
mysql -uroot -p capstonemysql -e "select * from wifi_scan where device_model = 'Moto G (4)' " -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > motoG4_061511.csv
```

#### Free WIFI caps

```mysql
# linknyc free wi-fi
# DowntownBrooklynWiFi_Fon 
select distinct caps, ssid from wifi_scan where ssid = "linknyc free wi-fi" or ssid = "DowntownBrooklynWiFi_Fon";

+------------+--------------------------+
| caps       | ssid                     |
+------------+--------------------------+
| [ESS]      | DowntownBrooklynWiFi_Fon |
| [ess][ble] | downtownbrooklynwifi_fon |
| [wps][ess] | downtownbrooklynwifi_fon |
| [ess][ble] | linknyc free wi-fi       |
| [ess]      | linknyc free wi-fi       |
+------------+--------------------------+

# [ess]
# [ess][ble]
```

