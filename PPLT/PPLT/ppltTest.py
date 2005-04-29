#!/usr/bin/python

import PPLTSystem;


system = PPLTSystem.System();
system.LoadDevice('Debug.RandomGenerator',
					'rand',
					{});
system.LoadServer('Web.PPLTWebServer',
					'web',
					'admin',
					{'Address':'10.1.1.4', 'Port':'4711'});

if not system.CreateSymbol('/test','rand::Generator::DWord','DWord'):
	print "error while create Symbol /test";

print system.GetValue('/test');

while True:
	pass;
