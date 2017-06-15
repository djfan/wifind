### [QGIS](https://gis.stackexchange.com/questions/133033/installing-the-latest-qgis-version-on-ubuntu)

```shell
# Ubuntu 16.04

sudo sh -c 'echo "deb http://qgis.org/debian xenial main" >> /etc/apt/sources.list'  

sudo sh -c 'echo "deb-src http://qgis.org/debian xenial main " >> /etc/apt/sources.list'  

wget -O - http://qgis.org/downloads/qgis-2016.gpg.key | gpg --import

gpg --fingerprint 073D307A618E5811

gpg --export --armor 073D307A618E5811 | sudo apt-key add -

sudo apt-get update && sudo apt-get install qgis python-qgis  
```

### [PostGIS](https://wiki.postgresql.org/wiki/Apt)

```shell
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository key from https://www.postgresql.org/media/keys/ACCC4CF8.asc, update the package lists, and start installing packages:

sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-9.5 pgadmin3
```

ref:

https://gis.stackexchange.com/questions/133033/installing-the-latest-qgis-version-on-ubuntu

https://wiki.postgresql.org/wiki/Apt