#!/usr/bin/python
import PPLT;

psys = PPLT.System();

info = psys.GetDeviceInfo("PLC.NAiS-FPX");
nslst = info.GetNameSpaces();
for ns in nslst:
	slotlst = info.GetSlots(ns);
	for slot in slotlst:
		print "%s::%s \"%s\""%(ns,slot,info.GetSlotDescription(ns,slot));
	slotlst = info.GetSlotRanges(ns);
	for slot in slotlst:
		print "%s::%s \"%s\""%(ns,slot,info.GetSlotRangeDescription(ns,slot));
		

