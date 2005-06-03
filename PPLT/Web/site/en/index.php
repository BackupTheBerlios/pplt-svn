<div class="TextBody">
    <div class="Head">News
		<a style="font-size:0.5em;" href="/en/NewsHistory.html">[History]</a>
	</div>
    <div class="NewsItem">
	<b>2005-06-03 - Release of PPLT Version 0.2.2</b><br>
	I've added some features to the library and the PPLTC application.
	You can now save a session and load it later. Also I've fixed
	some bugs and the german translation of PPLTC.<br><br>
	<b>2005-05-28 - Bugfix Release for PPLT (0.2.1)</b><br>
	I've fixed some annoying bugs in libraries and in the application.
	I recommend you to <u>update</u>.<br><br>
	<b>2005-05-27 - 2nd Alpharelease of PPLT (0.2.0)</b><br>
	I've released the 2nd alpha version of PPLT. The major change is the new
	GUI application PPLT Center (PPLTC.py) that shows the functionality of
	the library. Also some bugs are fixed.
    </div>

    <div class="Head">What is PPLT</div>
    <div class="Text">
    PPLT is an open framework for industrial communication. It was writen in
    Python and it is licensed under the GNU LGPL. It is designed as a Python
    library, so you can use it in your own applications. It is modular, that
    means the number of divices supported by the PPLT-System depends on the
    modules you are useing.

    <p>The main targets are to import data from different systems like controllers,
    manage them into a single filesystem like symboltree and export them to
    other systems like visualisations. So you can use it for data-invention etc.
    </p>

    <p>On the other hand it is still a library. So you can use it to access data
    from systems that are supported. Until now there are modules for some PLCs,
    Mobilephones, etc. So it makes no difference to access status information from
    a mobilephone like battery-level or the current status of the output-coils of
    an industry controller (<span title="Programable Logic Controller">PLC</span>).</p>
    </div>

    <div class="Head">Design</div>
    <div class="Text">
    The PPLT system consists of two parts. The first is the core library called
    <span title="PYthon Data Collect and Process Unit">pyDCPU</span>. This unit
    load and unload the modules, cares about the central symbol-tree and handle
    users/groups. If you want to know more about the core library, please look
    at the pyDCPU
    <a href="/en/pyDCPU_Intro.html"
        title="Intoduction into the pyDCPU Core library.">introduction</a>.

    <p>The second part is called PPLT-Library. This library is build on the top
    of pyDCPU. It is an abstraction-layer. This is necessary for providing a simple
    to use interface to the pyDCPU core library. This layer do not handle with
    modules but with abstract devices. </p>
    </div>
    
    <div class="Head">Supported Hardware/Sofware</div>
    <div class="Text">
    <ul>
        <li><b>NAIS FP0/FP2</b> - I tested them over the ToolPort. It was
        also possible to access them over the tunneled ToolPort of an
        <b>NAIS Web-Server</b>.

        <li><b>NAIS A200</b> - This is an industrial image-checker. To
        access it i used the build in RS232 port.

        <li><b>Siemens SIMATIC S7-200</b> - I used the PPI-Cable in
        <i>FreePort</i> mode.

        <li><b>Siemens S55</b> mobile phone. I am sure that other GSM
        compatible mobile phones will also work fine.</li>
		
		<li><b>Agilent 5462X</b> Oscilloscopes. You can measure frequency,
		aplitude, etc. of signals.</li>

		<li><b>JVisu 1.0</b> This is a open visualisation written in Java.
		There is a server module to export the symboltree to this application.</li>

		<li>A <b>simple HTTP</b> webserver is also aviable as a server module.
		So you can browse the symboltree with FireFox or other webbrowser.</li>

		<li>A <b>XML-RPC</b> server module called <i>SimpleExport</i> serves
		you the symboltree for nearly every programing language on every platform.</li>
    </ul>
    </div>
</div>
