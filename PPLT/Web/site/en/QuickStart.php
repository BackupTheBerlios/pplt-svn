<div class="TextBody">
	<p>In this document I will describe how to install the PPLT and how to
	do the first steps. If you have any questions to this document
	feel free to send me an <a href="/en/Contact.html">e-mail</a>.
	I used a lot of PPLT specific terms in this text, so you may want to 
	look at the <a href="/en/Terms.html">explanation of terms</a>.</p>

	<div class="Head">Requirements</div>
	<div class="Text">
	To install the PPLT you need to have done some preparation. You need to 
	install first the <b>Python interperter</b> version 2.3.0 or higher. You 
	can get it from <a href="http://www.python.org">python.org</a>.

	<p>The next is the grafic-library used by the PPLT tools like <i>PPLT Center</i>
	called <b>wxPython</b>. You need wxPython version 2.5.0 or higher. You can
	download this from <a href="http://www.wxpython.org">wxpython.org</a>. If you 
	only want to use the PPLT library in your own scripts then you may don't need it.</p>

	<p>If you want to use the PPLT under Windows you need to install the <b>pywin32</b>
	extention version 208. You can get it from 
	<a href="http://pywin32.sourceforge.net">pywin32.sourceforge.net</a>. If you use a 
	POSIX like system, for example Linux or BSD you don't need it.</p>

	<p>Some plugins need also some Python-extentions. To find out what extentions are
	needed look at the documentaion of the single plugin. For the GSM, Simatic S7-200,
	Agilent and NAiS modules you will need the <b>pyserial</b> extention from
	<a href="http://pyserial.sourceforge.net">pyserial.sourceforge.net</a>.</b> 
	</div>

	<div class="Head">Install</div>
	<div class="Text">
	To be sure that all will be fine, please install the packages in following order:
	<ol>
		<li><b>Python</b> interpreter</li>
		<li><b>pywin32 (*)</b></li>
		<li><b>wxPython (*)</b></li>
		<li><b>pyserial</b></li>
		<li><b>PPLT</b></li>
	</ol>

	<p>The procedure to install the single packages depends on the System you 
	use. For Windows you will have an executabe installer so it should not be
	a problem.<br>
	Under Linux you should get the source pakages, unpack and complile it. How 
	to do this, please read the README or INSTALL files inside the packages.
	</p>
	</div>

	<div class="Head">Starting the PPLT Center</div>
	<div class="Text">
	With the version 0.3.1 you find the folder <i>PPLT</i> inside you 
	<i>Programs</i> submenu of the start-menu, where you should find
	two shortcuts to the PPLT Center. The <i>PPLTCenter-debug</i> 
	shortcut starts the PPLTCenter in debug-mode. If something was wrong
	with the installation of PPLT you could find the PPLT Center in the
	folder where python installs all scripts. This should be something
	like <b>C:\Python23\Scripts</b>. There you find the files PPLTC.bat and
	PPLTC.py. The PPLTC.bat starts the PPLT Center application.
	If all is right you should see now something
	like this:
	<div style="text-align:center">
		<a href="/img/PPLTC01.png">
		<img 	src="/img/pPPLTC01.png"
				alt="The PPLT Center fornt-end."
				title="PPLT Center"></a>
	</div>

	Under Linux you should simply type <b>PPLTC.py</b> at a open terminal. Because Python copy all scripts into 
	<i>/usr/bin</i> or <i>/usr/local/bin</i>. 
	</div>

	<div class="Head">Install Modules</div>
	<div class="Text">
	Now if the Center is running, you can install the Modules. So get the module-package and unpack the ZIP into 
	a folder. The will be a lot of files in it. One called <b>Setup.idf</b>. Now start the PPLT-Center and click 
	on the left menu at the icon labled <i>Module install</i>. You will see a file section dialog. Change to 
	the folder where you unpacked the modules an select the Setup.idf. Now all modules will be installed. 
	</div>

	<div class="Head">The PPLT Center frontend</div>
	<div class="Text">
	The PPLT Center has a realy strange concept of use. You will not find so much buttons like in
	other GUI applications. Because the most actions you will do are in context with a specific item
	of a list or tree. So try to right-click everything you see. If you want to select a item, 
	try a double click (instead of selecting it with a single-click and then click the OK button).

	<p>For example: If you want to load a device, make a right-klick on the empty list of devices.
	In the context-menu select <i>Add device</i>. Now you will see a list off devices; Select 
	the device you want to load with a double-click.</p>

	<p>At the beginning it will be a little bit starange handleing. But later it is quiet fast.</p>
	</div>


	<div class="Head">PPLT Center working circle</div>
	<div class="Text">
		A normal woking circle will be to load at first the devices you want to access. Then you
		create the symbols and connect them to the devices. The last step should be to load 
		the servers.  

		<p>To load a device you right-click at the tab <i>Devices</i> or at an empty space
		inside the device-list. Select <i>Load device</i> at the context-menu. Now you see
		the device selection dialog. There are all devices listed, ordered by there class.
		Select now the device you want to load with a double-click. A single click at a
		device will show a short help text at the buttom of the dialog. Now you should 
		see the setup-dialog for the device you selected. Fill up the form an click 
		<i>OK</i>. If you need help for the parameters you have to set, keep with the
		mouse over the entry-feeld of the parameter an a tool-tip will be shown or
		take a look at the <a href="/en/Devices.html">device-reference</a>. 
		<b>Note:</b> you allways have to set an alias. This alias will be used to
		identify the the device later. If all parameters were right, the device 
		will be shown now at the device-list.</p>

		<p>Now, if you loaded all devices you need, you can start to fill up the
		symbol tree. To create a symbol or folder at the root of the symbol-tree,
		please right-click at a empty space inside the symbol-tree or at the
		tab <i>SymbolTree</i>. To create a symbol inside a existing folder, please
		right click the folder where the new symbol or folder should be created.<br>
		If you selected <i>Create symbol</i> at the context-menu, where all loaded 
		devices are listed. If you double click the device you'll see all
		namespaces that the device provide. If you double-click a namespace
		you'll see all slot that are in this namespace. At this moment, please
		don't care about the namespaces and what there are, you do not need to know
		what there are and what they do. You should need to care about the slots or
		slotranges. A simple slot has the singe plug as icon the slot range the 
		double-plug. <br>
		Now you setup the connection between the symbol and the device.
		A simple symbol represents a single value, while the slotranges represents
		a wide range of values. If you select a slot almost every thing is done you 
		will now see the symbol-property-dialog where you can set the owner, group,
		rights, etc. Else if you select a slot range the system will ask you for 
		a specific address or name before continueing the setup of the symbol.<br>
		For example: You want to access the markers of a PLC. Of course not all 
		markers can be shown at the dialog. So a placeholder (slotrange) will
		be used and the system will ask for the marker-address you want to use.
		The system also can't determ what type the marker is. So you'll need to set
		it at the symbol-property-dialog at the combo-box <i>Type</i>.</p>

		<p>Starting a server is quiet similar to loading a devic. You right-click
		at a empty space in the serverlist or at the tab <i>Servers</i> then
		you select the server you want to start with a double click. Like 
		loding a device you'll see now the setup-dialog for the server. Fill
		up the form and click <i>OK</i>. You'll allways have to set an alias,
		a default user and a server-root. The alias will be used to identify
		the server later (like the alias for devices). The default user is 
		necessary for servers, that do not know something like authentification
		so every client that connects the server will have the rights of this
		user. Servers that use authentification will ignore it or use it like
		a fallback. So please use only users with less rights for the default
		user. Server-root means that the server will only export the given
		folder and all it's subfolders. To leave here the slash means to 
		export the whole symboltree. Also like at the setup-dialog of devices
		you'll get tool-tips if you stay with you mous over an entry. If all
		parameters where ok, the server will be started and shown at the 
		list.</p>
	<div>


	<p><b>If you want to know more, or if you have problems; Feel free to <a href="/en/Contact.html">contact</a>
	me.</b></p>
</div>
