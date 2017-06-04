This is a brief introduction about how to get access to wifind database.

**Sys**

```bash
uname -a
# Linux dj 4.8.0-52-generic #55~16.04.1-Ubuntu SMP 
```

**Install**

```bash
# Installing MySQL
sudo apt-get updat
sudo apt-get install mysql-server

# Configuring MySQL
sudo mysql_secure_installation

# Initialize MySQL data dir
mysqld --initialize  # mysql_install_db

# Test
## check status
systemctl status mysql.service # sudo systemctl mysql start
```

![](img/test)

```bash
## For an additional check, you can try connecting to the database using the mysqladmin tool, which is a client that lets you run administrative commands
mysqladmin -p -u root version  
```

![](img/version)

**Log in**

```bash
ssh netid@gw.cusp.nyu.edu
ssh compute
ssh wifind@wifind.cusp.nyu.edu
mysql -uroot -p
```

**To-Do**

- [ ] Export sample data
- [ ] Connect to GUI (Linux: Emma or MySQL workbench; MacOS: SQL Pro)



*Ref*

 [How To Install MySQL on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-16-04)

