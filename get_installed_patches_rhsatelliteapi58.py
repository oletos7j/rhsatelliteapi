#!/usr/bin/python
import xmlrpc.client
import os, ssl
from datetime import datetime, timedelta
import settings
import pytz
from pytz import timezone

#reads credentials from the settings.py file
uri = settings.URI
login = settings.USER_NAME
password = settings.USER_PASSWORD

#parameters to use
origTZ = 'America/Chicago' #timezone of your satellite server
myTZ = 'America/New York' #your timezone
n = 21 #how long back should the report be generated, in days

e = datetime.now()
end_date = e.strftime('%Y%m%d' + 'T' + '%H:%M:%S')

s = datetime.now() - timedelta(days=n)
start_date = s.strftime('%Y%m%d' + 'T' + '%H:%M:%S')

#ignores ssl cert issues
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
    client = xmlrpc.client.Server(uri, verbose=0)
    key = client.auth.login(login, password)
    result = client.system.listActiveSystems(key)

for info in result:
    serverid = (info['id'])
    print("")
    print("Installed on server %s:" % (info['name']))
    print("")
    pkgs = client.system.listPackages(key, serverid)

    for pkg in pkgs:
        try:
            if pkg['installtime'] >= start_date and pkg['installtime'] <= end_date:
                cst = pytz.timezone(origTZ).localize(datetime.strptime(pkg['installtime'].value, "%Y%m%dT%H:%M:%S"))
                ast = cst.astimezone(timezone(myTZ))
                print(f"Date/Time: {ast} - Package: {pkg['name']}, Version: {pkg['version']}, Release: {pkg['release']}, Arch: {pkg['arch']}")
        except:
            continue
