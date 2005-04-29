<div class="TextBody">
	<div class="Text">
		In this document, i'll give you a short reference for the PPLT library. This library is a python package
		so you can use it in you own scripts. The PPLT is build on the top of pyDCPU.  
	</div>
	
	<div class="Head">Start the System</div>
	<div class="Text">
		This class will create a new PPLTSystem object. All work will be done by calling methods of 
		this object.

<pre>
import PPLT;
psys = = PPLT.System();
</pre>

		You see, the creation of the PPLTSystem needs no parameters.
	</div>

	<div class="Head">Load a Device</div>
	<div class="Text">
		To load a divice you need to know it's name and the parameters.
<pre>
if not psys.LoadDevice(DeviceName, Alias, Parameters):
	print "Error while load Device";
</pre>
		<p>
		The <i>LoadDevice</i> method will load the device named <i>DeviceName</i> as 
		<i>Alias</i> with the parameters <i>Parameters</i>. That means, that the device
		if it could be loaded, will have the "Name" you set in <i>Alias</i>. Later you
		can access the device over this alias. For example if you want to attach a Symbol
		to this device.</p>
		
		<p>
		The method will return <i>True</i> if the device was sucessfully loaded and <i>Flase</i>
		otherwise.
		</p>
	</div>

	<div class="Head">Unload a device.</div>
	<div class="Text">
		To unload a device simply call:
<pre>
if not psys.UnLoadDevice(Alias):
	print "Error while unload device";
</pre>
		The parameter <i>Alias</i> is the "Name" of the device you specified in the <i>LoadDevice()</i> call.
		The method will return <i>True</i> if the device was successfully unloaded and <i>False</i> otherwise. 
	</div>		

	<div class="Head">List loaded devices.</div>
	<div class="Text">
		To list all loaded devices try:
<pre>
dev_list = psys.ListDevices();
</pre>		
	</div>

	
</div>
