#!/usr/bin/python

import PPLTSystem;


system = PPLTSystem.System();
system.LoadDevice('Mobile.GSMMobilePhone',
					'handy',
					{'Port':'0','Speed':'115200'});
#system.LoadServer('RPC.SimpleExport',
#					'test',
#					'admin',
#					{'Address':'10.1.1.4', 'Port':'4711'});
if not system.CreateSymbol('/test','handy::GSM::model','String'):
	print "error while create Symbol /test";

print system.GetValue('/test');
