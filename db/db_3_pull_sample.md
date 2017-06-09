

```shell
# Ref -> https://stackoverflow.com/questions/22783202/exporting-mysql-table-into-a-csv-file

# "mysql -uroot -p capstonemysql -e "select * from wifi_scan limit 10000" -B" for .tsv

# for .csv
mysql -uroot -p capstonemysql -e "select * from wifi_scan limit 10000" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > t10000.csv

scp wifind@wifind.cusp.nyu.edu:t10000.csv ./
```





