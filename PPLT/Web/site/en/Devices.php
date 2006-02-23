<div class="TextBody">
	<div class="Head"><b>Devices</b> - Overview</div>
	<div class="Text">
	<ul>
		<li><b>Debug</b>
		<ul>
			<li><b><a href="#rand">RandomGenerator</a></b>
				 - Generates random values of different types.
			</li>
		</ul></li>

		<li><b>PLC</b>
		<ul>
			<li><b><a href="#FPX">Panasonic-FPX</a></b> - Access to the values of the Markers
			of a Panasonic FP0 or FP2.</li>
			<li><b><a href="#FPWEB">Panasonic-FPWEB</a></b> - Accesses a Panasonic FP0 via a connected
			Panasonic FPWEB server.</li>
			<li><b><a href="#S7-200">S7-200</a></b> - Access to 
			the values of the Markers of a Siemens SIMATIC S7-200.</li>
		</ul>

		<li><b>Measure</b>
		<ul>
			<li><b><a href="#AGI">Agilent 5462x</a></b> - Measures while using the oscilloscopes
			of the 5462x series by Agilent.</li>
		</ul>
		</li>

		<li><b>Mobile</b>
		<ul>
			<li><b><a href="#GSM">GSM</a></b> - Reads values like battery-level or
			signal-quality out of a GSM compatible mobile phone.</li>
		</ul>
		</li>
	</ul>
	</div>






	<div class="Head"><a name="rand">RandomGenerator</a></div>
	<div class="Text">
	This device generates random values of different types. It doesn't need any specific hard-
	or software, so it is pretty useful for testing the PPLT system. 

	<p>This device also doesn't need any parameters, so you only need to set an alias for the device
	to setup.
	<div style="text-align:center">
		<img 	src="/img/RandomGenerator01.png"
				alt="The RandomGenerator setup dialog.">
	</div>
	</p>
	
	<p>If you use the PPLT library in a Python-script instead of the PPLT Center, the
	setup call should look like this:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("Debug.RandomGenerator", "alias", {});
</pre>
	Note: Replace <i>alias</i> with the alias you want to use for the RandomGenerator.
	</p> 

	
	<p>This device provide one Namespace <i>Generator</i> with 6 slots in it. Each
	slot holds the random numbers for a defined type. So the slot holds
	<i>Byte</i> random values of the type byte, etc. 
	<table align="center">
		<tr><th>Slot</th><th>Meaning</th></tr>
		<tr>
			<td>Bool</td>
			<td>Randomly True or False.</td>
		</tr>
		<tr>
			<td>Byte</td>
			<td>byte</td>
			<td>An integer value between 0 and 100.</td>
		</tr>
		<tr>
			<td>Word</td>
			<td>word</td>
			<td>An integer value between 0 and 100.</td>
		</tr>
		<tr>
			<td>DWord</td>
			<td>double word</td>
			<td>An integer value between 0 and 100.</td>
		</tr>
		<tr>
			<td>Float</td>
			<td>float</td>
			<td>A floating point value between 0 and 1.</td>
		</tr>
		<tr>
			<td>Double</td>
			<td>double</td>
			<td>A floating point value between 0 and 1.</td>
		</tr>
	</table>
	</p>
	</div>	





	<div class="Head"><a name="S7-200">Simatic S7-200</a></div>
	<div class="Text">
	This device gives you access to the values of the markers of a Siemens SIMATIC S7-200
	connected to the PC by a PPI cable.
	

	<p><b>Note:</b>This device uses the <i>UniSerial</i> core-module. This module needs the
	<i>pyserial</i> Python library. Be sure to have it installed before using this Device.</p> 	

	<p>This device needs 3 parameters to setup. At first the <i>Port</i>. This
	is the number of the serial interface, the PPI cable is connected to.
	<b>Note</b>: The number for the first port (COM1) is 0!<br>
	The other parameters are the PPI-addresses for the PC: <i>PCAddr</i> 
	(in most cases 0) and the PPI-address of the PLC: <i>S7Addr</i>.
	<div style="text-align:center">
		<img	src="/img/SimaticS7-200.png"
				alt="Setup dialog for the S7-200 device.">
	</div></p>

	<p>
	The library call should look like this:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("PLC.S7-200", "alias", {"Port":"0", "PCAddr":"0", "S7Addr":"2"});
</pre>
	</p>

	<p>The <i>S7-200</i> device provides 2 namespaces. At first the namespace 
	<i>Marker</i>. This namespace holds only one slot-range in it named 
	<i>Markers</i>. The slotrange is a placeholder for a number of slots. In 
	this case it is a placeholder for all markers of the PLC. If you select the 
	Slotrange in the PPLT-Center application the program will ask for a
	specific makername. Because the program can't determ the type of the
	marker you need to set it in the symbol-property-dialog.<br>
	If you use PPLT as a Python library, simply type:

<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("PLC.S7200", "s7-200", {"Port":"0", "PCAddr":"0", "S7Addr":"2"});
system.CreateSymbol("/PathToSymbol", "s7-200::Markers::SMB28", "Byte");
</pre>
	</p>

	<p>The second namespace called <i>PPIStatistic</i> holds 5 Slots. Each slot
	holds a statistic value about the data going through the PPI kable. For example the <i>read_data</i> slot 
	holds the number of bytes readed back from the PLC.
	<table align="center">
		<tr><th>Slot</th><th>Type</th><th>Meaning</th></tr>
		<tr>
			<td>read_data</td>
			<td>double word</td>
			<td>Number of bytes recived from the PLC.</td>
		</td>
		<tr>
			<td>write_data</td>
			<td>double word</td>
			<td>Number of bytes send to the PLC.</td>
		</tr>
		<tr>
			<td>read_speed</td>
			<td>double</td>
			<td>Bytes per second received.</td>
		</tr>
		<tr>
			<td>write_speed</td>
			<td>double</td>
			<td>Bytes per second send.</td>
		</tr>
		<tr>
			<td>error</td>
			<td>double word</td>
			<td>Number of transmission errors occured.</td>
		</tr>
	</table></p>
	</div>



	
	
	<div class="Head"><a name="FPX">Panasonic FP0/2</a></div>
	<div class="Text">
	With this device you can access all markers of a Panasonic FP0 or FP2
	via the so called <i>ToolPort</i>. The ToolPort is connected via
	an simple cable to a serial interface of the PC.</p> 
	
	<p><b>Note:</b> Because of that this device uses the core module
	<i>UniSerial</i> and this modules uses the Python library 
	<i>pyserial</i> you need to have this installed. 
	So please be sure to have this library installed 
	before loading this device.</b>

	<p>To load this device only 2 Parameters are needed. <i>Port</i>
	is the number of the serial interface.<br>
	<b>Note:</b> The number of the first serial interface 
	(COM1) is 0!<br>
	The second parameter is the address of the PLC. Only if you
	want to access the PLC over a MEWTOCOL-COM bus you need to
	set this field. Otherwise you can set this to any number between   
	1 and 254 (because the PLC ignores the destinationfield in the
	message if you use the ToolPort).
 	<div style="text-align:center">
		<img	src="/img/FPX01.png"
				alt="Setup dialog for the Panasonic FP0 or FP2 device.">
	</div>
	</p>
	
	<p>If you use the PPLT as a Python library type:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("PLC.Panasonic-FPX", "alias", {"Port":"0", "Address":"1"});
</pre>
	Substitute <i>alias</i> with the alias you want to give the device.</p>

	<p>
	The Panasonic-FPX device provides only one namespace (<i>Marker</i>). In 
	this namespace there are one Slot named <i>STATUS</i> and a slotrange 
	named (<i>Marker</i>) available. <br>
	The slotrange is a placeholder for all markers of the
	PLC. If you select this slotrange in the PPLT-Center an application
	will ask you for a specific marker address.<br>
	<b>Note:</b> You will need to set a type for the symbol at the 
	property-dialog.<br>
	But if you want to use the PPLT just as a library you can ignore the
	existence of this placeholder and simply use the marker address
	as a name of a slot. For example (to access the first input bit):
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("PLC.Panasonic-FPX", "fp0", {"Port":"0", "Address":"1"});
system.CreateSymbol("/PathToSymbol", "fp0::Marker::Y0", "Bool");
</pre> 

	The slot <i>STATUS</i> is read- and writable and controls the status
	of the PLC. If this Slot is True, the PLC is in the <i>RUN</i>
	mode else it is in the <i>STOP</i> mode. So you can also control
	the mode of the PLC.
	</p>
	</div>






	<div class="Head"><a name="FPWEB">Panasonic FP-WEB server</a></div>
	<div class="Text">
	The <i>Panasonic-FPWEB</i> device is almost the same like the <i>Panasonic-FPX</i>.
	But with this device you access the PLC trough the tunneled ToolPort
	by the Panasonic FPWEB server. If you config the FPWEB server, it will
	tunnel the toolport transparent to a TCP/IP port and so this device
	can access the PLC by this port.</p>

	<p>To load this device you need (like the Panasonic-FPX device) only 
	2 parameters. The first <i>NetAddr</i> is the network address
	of the Panasonic-FPWEB server in the format ADDRESS:PORT (for
	example 10.1.1.10:9094 or www.yoursite.com:9094). The second 
	Parameter is the MEWTOCOL address of the PLC connected to
	the webserver. Because the ToolPort will often be tunneled
	it could be any number between 1 and 254.
	<div style="text-align:center">
		<img	src="/img/FPWEB01.png"
				alt="The setup dialog of the Panasonic-FPWEB device.">
	</div></p>
	
	<p>If you want to use the PPLT as a Python library type:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("PLC.Panasonic-FPWEB", "alias", {"NetAddr":"10.1.1.10:9094", "MEWAddr":"1"});
</pre></p>
	
	<p>This device provides the same namespace, slot and slot-range like the 
	<a href="#FPX">Panasonic-FPX</a> device. So take a look at the description
	of this device to find out more.</p> 
	</div>







	<div class="Head"><a name="GSM">GSM mobile phone</a></div>
	<div class="Text">
	With this device you can access some status information of a GSM
	compatible mobile phone like battery-level or signal-quality.

	<p><b>Note:</b> Because this device uses the <i>UniSerial</i> core
	module to access the serial interface, you have to have installed
	the <i>pyserial</i> Python library before you can use this device.</p>
	
	<p>To load this device you need to set two parameters. The first
	<i>Port</i> sets the number of the serial interface you'll use.
	<br><b>Note:</b>The number of the first serial interface is 0!<br>
	The second parameter sets the speed in baud. 9600 baud 
	should be a useable value.
	<div style="text-align:center">
		<img	src="/img/GSMDev01.png"
				alt="Setup dialog of the GSMMobilePhone device.">
	</div></p>

	<p>If you will use PPLT as a Python library type:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("Mobile.GSMMobilePhone", "alias", {"Port":"0", "Speed":"9600"});
</pre></p>

	<p>This device provides only one namespace named <i>GSM</i> with 4 slots in it.
	<table align="center">
		<tr><th>Slot</th> <th>Type</th> <th>Meaning</th></tr>
		<tr>
			<td>battery</td>
			<td>double word</td>
			<td>The battary-level in percent.</td>
		</tr>
		<tr>
			<td>quality</td>
			<td>double word</td>
			<td>The signal quality in dB.</td>
		</tr>
		<tr>
			<td>manufacturer</td>
			<td>string</td>
			<td>The name of the manufacturer.</td>
		</tr>
		<tr>
			<td>model</td>
			<td>string</td>
			<td>The model-name of the mobile phone.</td>
		</tr>
	</table></p>
	</div>




	<div class="Head"><a name="AGI">Agilent oscilloscope 5462x</a></div>
	<div class="Text">
	<p>With this device you can control and get back the results of the measurement
	of an oscilloscope of the 5462x series by Agilent. This device uses the serial
	interface to connect the oscilloscope.</p>
	
	<p><b>Note:</b> This device uses the <i>UniSerial</i> core module. The module
	needs the <i>pyserial</i> Python extension. So be sure to have it installed 
	before using this device.</p>

	<p>This device needs 3 parameters to setup. The first parameter <i>Port</i>
	is the number of the serial interface which you use.<br> 
	<b>Note:</b> The first serial interface has the number 0!<br>
	The next parameter is the primary signal source <i>Primary</i> and
	the last is the secondary signal source <i>Secondary</i>. You need
	to set booth signal sources if you want to do measurements that
	compares two signals like the phase-difference. Else you only need 
	to set the primary. (Set the secondary to the same value.)
	<div style="text-align:center">
		<img 	src="/img/Agilent-5462X01.png"
				alt="The setup dialog of the Agilent 5460x device.">
	</div></p>
	<p>If you want to use the PPLT as a Python library type:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("Measue.AGILENT-5462X", "alias",{"Port":"0", "Primary":"A1", "Secondary":"A2"});
</pre></p>	

	<p>This device provides only one namespace (<i>Values</i>).
    All slots in this namespace measure a specific value.
	<table align="center">
		<tr><th>Slot</th> <th>Type</th> <th>Meaning</th></tr>
		<tr>
			<td>amp</td>
			<td>double</td>
			<td>Amplitude</td>
		</tr>
		<tr>
			<td>freq</td>
			<td>double</td>
			<td>Fequency</td>
		</tr>
		<tr>
			<td>phase</td>
			<td>double</td>
			<td>Phasedifference</td>
		</tr>
		<tr>
			<td>max</td>
			<td>double</td>
			<td>Maximum</td>
		</tr>
		<tr>
			<td>min</td>
			<td>double</td>
			<td>Minimum</td>
		</tr>
		<tr>
			<td>pp</td>
			<td>double</td>
			<td>Peak-Peak value</td>
		</tr>
		<tr>
			<td>top</td>
			<td>double</td>
			<td>see <i>max</i></td>
		</tr>
		<tr>
			<td>base</td>
			<td>double</td>
			<td>see <i>min</i></td>
		</tr>
		<tr>
			<td>width</td>
			<td>double</td>
			<td>Pulse width</td>
		</tr>
	</table></p>
			
	</div>	
</div>
