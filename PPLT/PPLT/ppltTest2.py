#!/usr/bin/python
import pyDCPU;

core = pyDCPU.Core("/usr/PPLT/UserDB.xml");
core.ExporterAdd("Export.PPLTWeb",{'Address':'10.1.1.4','Port':'4711'},"admin");

