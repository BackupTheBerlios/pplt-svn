#!/usr/bin/python
import urllib;
import zipfile;

SRV_URL	= "ftp://10.1.1.4";
MOD_DIR	= "Mdules"

f = urllib.urlopen("ftp://10.1.1.4/Modules/PPLTWeb.zip");
z = zipfile.ZipFile(f);
print z.read("meta.xml")
