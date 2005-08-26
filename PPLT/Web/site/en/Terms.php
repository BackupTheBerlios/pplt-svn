<div class="TextBody">
	<div class="Head">Explanation of Terms</div>
	<div class="Text">
		<table align="center">
			<tr>
				<td>
					<ul>
						<li><a href="#CoreModule">Core-Module</a></li>
						<li><a href="#Device">Device</a></li>
						<li><a href="#Group">Group</a></li>
					</ul>
				</td>
				<td>
					<ul>				
						<li><a href="#Namespace">Namespace</a></li>
						<li><a href="#PPLTC">PPLT Center</a></li>
						<li><a href="#Server">Server</a></li>
					</ul>
				</td>
				<td>
					<ul>
						<li><a href="#Slot">Slot/Slotrange</a></li>
						<li><a href="#Symbol">Symbol</a></li>
						<li><a href="#Symboltree">SymbolTree</a></li>
					</ul>
				</td>
				<td>
					<ul>
						<li><a href="#User">User</a></li>
					</ul>
				</td>
			</tr>
		</table>
	</div>
	

	<div class="Head"><a name="CoreModule">Core-Module</a></div>
	<div class="Text">
		A Core-Module is a piece of python source ziped into
		an archive. Such a core-module implements mostly a 
		layer of the communication between the PC and the 
		hardware. So it implements for example the interface
		used or the transmission protocol.

		<p>A <a href="#Device">device</a> or a 
		<a href="#Server">server</a> consists of one ore more core modules.
		so it is possible to reuse parts of other devices to create a new.
		This concept of reuseable parts is the main design idea of the
		PPLT system. But because of the core modules are hidden into 
		abstract devices, the usability of the system keeps quied easy.</p> 
	</div>


	<div class="Head"><a name="Device">Device</a></div>
	<div class="Text">
		The device is one of the 3 main parts of the PPLT system (beside
		the <a href="#Symboltree">symboltree</a> and the 
		<a href="#Server">servers</a>). Devices a grouped in classes to 
		keep the overview. A full qualified devicename consists of the
		whole class-path and the device name divided by a single dot.
		For example <i>PLC.S7-200</i>. Please take a look into the
		<a href="/en/Devices.html">device reference</a> to get an 
		overview about all aviable devices. 

		<p>A device is the repesentation of a piece of hardware. You may think 
		of it as a driver for this hardware. Each device provides one ore more
		<a href="#Slot">slots</a>. Over such a slot a 
		<a href="#Symbol">symbol</a> (which ist connected to a slot) can read 
		out or write in values. So the device is the interface between the 
		<a href="#Symboltree">symbols</a> and the real existing hardware.</p>

		<p>A main design idea is that a device is not a single module. A device
		consists of some so called <a href="CoreModule">core modules</a>. Each
		core module implements a layer of the communication with the hardware.
		So you will have a module for the interface used, one for the 
		transmission protocol and one for the command messages of the specific 
		device. So it is possible to reuse parts of other devices when a new
		device is written.<br>
		Because of that there have to be a <a href="Namespace">namespace</a>
		concept to keep the slot-names unique.</p>
		
		<p>To load a device in the <a href="PPLTC">PPLT Center</a> application
		right-click at the tab <i>Devices</i> or at a empty area of the
		device list. Select the option <i>Load device</i> in the context menu.
		Select the device you want to load and do the setup. If you want help
		for the setup dialog keep with the mouse a while over an entry feeld
		of the setup dialog, a tool-tip will be showed. Or take a look at the
		<a href="/en/Devices.html">device-reference</a>.</p>

		<p>If you use the PPLT library you should call something like:
<pre>
import PPLT;
system = PPLT.System();
system.LoadDevice("Class.DeviceName", "Alias", {"Parameter":"Value",...});
</pre>
		The first parameter of the LoadDevice() call is the full qualified 
		device name. The second should be a unique alias for the device you
		will load to identify it later. The last is a dictionary with the 
		parameter&lt;-&gt;value pairs for setup. Note: The parameter name and
		also the values have to be strings.</p>  
	</div>




	<div class="Head"><a name="Group">Group</a></div>
	<div class="Text">
		All <a href="#User">users</a> are orgenised in groups. Each
		user have to be member of a group. A peculiarity is that
		a group can have sub-groups. That means that a member of a
		group is allways member of <u>all</u> sub-groups.
	</div>




	<div class="Head"><a name="Namespace">Namespace</a></div>
	<div class="Text">
		It is a main design feature that a 
		<a href="#Device">device</a> is not a single 
		module. It consists of a list of so called 
		<a href="#CoreModule">core modules</a>.<br> Each core module
		implements a layer of the communication with the
		device. So you will have one module for the interface, one
		for the transport protocol and one for the command messages
		of the specific device. But all of these modules are hidden
		into one device and each of this may provide values you may 
		interested in.

		<p>But if a device consist of may modules you can't be
		sure that the <a href="#Slot">slotnames</a> of the modules are unique. 
		So you'll need namespaces to seperate the core modules inside
		the device.</p> 
	</div>


	<div class="Head"><a name="PPLTC">PPLT Center</a></div>
	<div class="Text">
		The PPLT Center is a GUI application to show the functionality of
		the PPLT library. You can load <a href="#Device">devices</a>,
		manipulate the <a href="#Symboltree">symboltree</a>, load
		<a href="#Server">servers</a>, manage <a href="#User">users</a>
		and <a href="#Group">groups</a> and (un)install the modules.

		<p>The PPLT Center has a realy strange usability. Almost everything 
		will be done over context-menus. To get the context-menu you have to
		right-click something. It has two major advantages. At first the 
		front end keeps clean and the second is that you will work realy 
		fast if you get used to.</p>

		<div style="text-align:center">
			<a href="/img/PPLTC01.png">
			<img	src="/img/pPPLTC01.png"
					alt="The PPLT Center application at work."
					title="The PPLT Center.">
			</a>
		</div>

		<p>Note: The PPLT Center uses the wxPython widgets, so please be sure
		to have <a href="http://www.wxpython.org">wxPython</a> installed.</p>
	</div>


	<div class="Head"><a name="Server">Server</a></div>
	<div class="Text">
		The server is beside the <a href="#Device">devices</a> and the
		<a href="#Symboltree">symboltree</a> one of the 3 main parts of the
		PPLT system. Servers are grouped into classes to keep the overview.
		A full qualified server name consists of the whole class-path and
		the server name divided by a single dot. For example: 
		<i>Web.PPLTWebServer</i>. Please take a look at the 
		<a href="/en/Servers.html">server reference</a> to get an overview
		about aviable servers.

		<p>A server can export the <a href="Symboltree">symboltree</a>
		or parts of it to other applications like a webbrowser or 
		visualisiation. Also the server have to care about the 
		authentification against the <a href="#User">user database</a>.
		If a protocol don't know authentification, you can set a 
		default user at the loading of the server. Normaly this should be
		a user with less rights. So the server is the interface between
		the <a href="#Symbol">symbols</a> and the rest of the wolrd.</p>

		<p>If you want to load a server at the <a href="PPLTC">PPLT Center</a>
		application. Right-click the tab <i>Servers</i> or a empty space	
		at the server list. Select the option <i>Load server</i> in the
		context menu and select the server you want to load.
		Now setup it, if you need help for a parameter of the
		setup dialog, keep a with the mouse over the entryfeeld
		and a tooltip will be showed. Or take a look at the 
		<a href="/en/Servers.html">server-reference</a>.</p>

		<p>If you use the PPLT library in your own application, you should 
		type something like:
<pre>
import PPLT;
system = PPLT.System();
syste.LoadServer("Class.ServerName", "Alias", "DefaultUser", {"Parameter":"Value",...}, "/SrvRoot");
</pre>
		The first parameter of the LoadServer() call should be the full 
		qualified server name of the server you want to load. With the second 
		you give the server an unique alias to identify it later. <i>DefualtUser</i>
		should be replaced by a user name you want to set to the default user. 
		The dictionary as the 4-th parameter contains the parameter&lt;-&gt;value
		pairs for setup the server. The last (optional) parameter defines the
		so called server-root. If you missed this the whole symboltree will
		be exported by the server else the given folder with all subfolders
		will be exported.</p>
	</div>



	<div class="Head"><a name="Slot">Slot/SlotRange</a></div>
	<div class="Text">
		Each <a href="#Device">device</a> provides slots and/or slotranges grouped
		into so called <a href="#Namespace">namespaces</a>.

		<p>A slot is a kind of a socket where <a href="#Symbol">symbols</a> can 
		attach to. Also many symbols can attach to one singe slot. The slot is 
		the source here symbols get there values from and write there values to.
		So it is the interface between the <a href="#Symboltree">symboltree</a>
		and the devices.</p>

		<p>At the <a href="#PPLTC">PPLT Center</a> application the slots and
		slotranges were litsted if you want to create a new symbol. You 
		select the one your symbol should be connected to and set some 
		properties like <a href="#RefreshRate">refresh rate</a> etc.<br>
		If you use the PPLT as a Python library you have to know the 
		name of the slots/slotranges, namespace and 
		<a href="#Alias">device alias</a> to create a new symbol. To do so
		call:
<pre>
import PPLT;
system = PPLT.System();
[...]
system.CreateSymbol("/PathToSymbol", "ALIAS::NAMESPACE::SLOT", "Type");
</pre>
	
		<i>/PathToSymbol</i> is the complete path to the symbol you want to 
		create. Note: The path allways begins with a slash.<br>
		<i>ALIAS::NAMESPACE::SLOT</i> is the full qualified name of a slot, where
		<i>ALIAS</i> is the device alias of the device you want to use, 
		<i>NAMESPACE</i> is the Namespace and <i>SLOT</i> is the slot you want 
		to connect your symbol to. You see, that you need to know the 
		<a href="#Types">type</a> of the values you can get from the specific 
		slot</p>

		<p>A slotrange is a kind of a placeholder for a complete list of slots.
		For example if you want do connect a new symbol to a marker of a PLC.
		The device that represents the PLC can't have all Markers implemented
		each as a single Slot so the device gives you a slotrange for all 
		markers.</p>

		<p>At the PPLT Center application, the program will ask you for a
		specific marker-address if you select the slotrange for the markers.
		If you use the PPLT library you will have to replace the name of the
		slot in the full qualified slotname with the marker address. Meaning:
		instead of <i>ALIAS::NAMESPACE::SLOT</i> you will use 
		<i>ALIAS::NAMESPACE::MARKERADDR</i>.
	</div>

	<div class="Head"><a name="Symbol">Symbol</a></div>
	<div class="Text">
		A symbol represent a value of a specific source like a marker of a
		PLC or a sensor. It is owned like <a href="#Folder">folders</a> by
		a <a href="#User">user</a> and a <a href="#Group">group</a>. So
		you have the possibility to control who has access to this value.</a>

		<p>The rights you can distribute are distinguished between reading and
		writing. Also you can set different rights for the owner of the symbol
		and for the group.</p>

		<p>Symbols are connected to a determ <a href="#Slot">slot</a> of a 
		<a href="#Device">device</a>. If a <a href="#Server">server</a> wants
		to read from a symbol, the symbol gets its data from the specified
		slot and convert it into a usabe value.</p>

		<p>If you want to create a symbol in the <a href="#PPLTC">PPLT Center</a>
		application, you have to right-click the folder where you want to create
		the symbol and select in the context-menu the option <i>create symbol</i>.
 		Then you'll need to select the slot which the sysmbol shoulb be connected
		to. And finally you'll set the permission rights for the symbol.</p>

		<p>Else, if you use the PPLT library direct into you own application you
		should do something like:
<pre>
import PPLT;
system = PPLT.System();
[...]
system.CreateSymbol("/PathToSymbol", "ALIAS::NAMESPACE::SLOT", "Type");
</pre>
		Substitute <i>/PathToSymbol</i> with the complete (including the slash) 
		path to the symbol you want to create. <i>ALIAS::NAMESPACE::SLOT</i>
		is the full qualified slotname of the slot the symbol will be connected to.
		Where <i>ALIAS</i> will be the <a href="#Alias">device-alias</a>, 
		<i>NAMESPACE</i> the <a href="#Namespace">Namespace</a> of the slot you
		want to use. Please see at the 
		<a href="/en/Devices.html">device-reference</a> to find out what slots are
		provieded by the devices.</p>
	</div>

	<div class="Head"><a name="Symboltree">Symboltree</a></div>
	<div class="Text">
		The symboltree is beside the <a href="#Server">Servers</a> and 
		<a href="#Device">Devices</a> the third main part of the PPLT system.

		<p>The symboltree looks like a filesystem. It has 
		<a href="#Folder">folders</a> and <a href="#Symbol">symbols</a> to
		orgenize the values you may want to observe.
		</p>

		<p>Servers can export the symboltree (or parts of it) to other systems
		like to a webbrowser or a visualization. Also the symbols inside the
		symboltree are connected to <a href="#Slot">slots</a> of devices. So
		the symboltree is the interface between the servers and the devices.
		At this possition it is usefull to controll who has access to the 
		symbols and so control the access to the devices.<br>
		So the symboltree has its own right-management. With 
		<a href="#User">users</a> and <a href="#Group">groups</a>.
	</div>	


	<div class="Head"><a name="User">User</a></div>
	<div class="Text">
		The most systems for industrial communication do not have there 
		own (or better any) user/group system. There believe that it will
		be sufficient to handle security related things at the network level
		(For example VPN etc.).
		But that means that everybody who has access to the network as 
		full access to all. So you can't decide who can access the 
		different devices if the one has access to the network even
		if he has the right to access the network. So I decided to
		implement a right-management to the system to prevent such
		situations.

		<p>The user- and <a href="#Group">group</a>-system does not realy 
		differ from other systems like your operating-system. But there are 
		some small differences. For example that every user can become the 
		super user (or may be admin) and there is also a peculiarity with
		the heritage of <a href="#Group">group</a> membership. </p> 
	</div>



</div>
