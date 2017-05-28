This is a brief introduction about how to install and set up dev env of wifimapping application `wifind` (*Andorid*) by `phonegap` and `ripple`.



**System**

```bash
uname -a
# Linux dj 4.8.0-52-generic #55~16.04.1-Ubuntu
# x86_64 GNU/Linux
```

**Installation of Java :**

```bash
# Check if Java is not already installed on your system.
java -version
```

```bash
# Return Java version if available java in your system. Otherwise install java.
sudo apt-get install default-jre
sudo apt-get install default-jdk
```

**Installation of nodejs and npm :**

```bash
sudo apt-get install nodejs
sudo apt-get install npm
```

```bash
# The NodeJS is installed & named as nodejs. But PhoneGap, always execute using the name node. So create a symlink named node that points to nodejs for fix this inconsistency.

sudo ln -s /usr/bin/nodejs /usr/bin/node
```

**Installation of Ant :**

```bash
sudo apt-get install ant
```

**Install PhoneGap and depending libraries of PhoneGap :**

```bash
sudo npm install -g phonegap
sudo apt-get install lib32z1 lib32ncurses5 lib32bz2-1.0 lib32stdc++6

# base on Readme.md in wifimapping/app, also install following:
sudo npm install -g cordova ionic bower
#or npm install -g phonegap cordova ionic bower
```

**Download [Android SDK](http://dl.google.com/android/android-sdk_r24.3.3-linux.tgz) : **  

```bash
# Extract to /usr/local/. Give the executable permission for path/android-sdk-linux/tools/android.
sudo tar -zxvf ~/Downloads/android-sdk_r24.0.2-linux.tgz -C /usr/local/
sudo chmod a+x /usr/local/android-sdk-linux/tools/android
```

**Add Path : **

```bash
# Then add the following lines to the end part of the file.
subl ~/.bashrc
export PATH=$PATH:/usr/local/android-sdk-linux/
export PATH=$PATH:/usr/local/android-sdk-linux/tools
export PATH=$PATH:/usr/local/android-sdk-linux/platform-tools
export PATH=$PATH:/usr/local/android-sdk-linux/build-tools
source ~/.bashrc
```

```bash
# If EACCES: permission denied .config/configstore/...
sudo chown -R $USER:$GROUP ~/.npm
sudo chown -R $USER:$GROUP ~/.config
```

**Test the app locally : ** 

```bash
git clone `project`
cd `project`
# Install bower packages:
bower install
# test
phonegap serve
```

**Download Emulator**

```bash
# Chrome Extention - Ripple
# `Enable`
# `Apache Cordova (1.0.0)`
```

![](ripple1)

![](ripple2)



**To-Do:**

- [ ] Setup the app's platforms and plugins:

```
ionic state restore
```

- [ ] Run in Android phone instead of emulator.