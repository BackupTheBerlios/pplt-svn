<div class="TextBody">
    <div class="Head">News</div>
    <div class="NewsItem">
    <b>2005-04-28 - Release PPLT version 0.1pre3</b><br>
	This release is nearly the same like <i>0.1pre2</i>
	but I've removed some ugly bugs.<br><br>
	<b>2005-04-25 - Release PPLT version 0.1pre2</b><br>
	I've released a second prealpha version of the PPLT library.
	The new feature is an abstraction layer. Now it is quiet simple
	to load and manage devices and servers.<br><br> 
	<b>2005-03-31 - Release PPLT version 0.1pre</b><br>
    I've <a href="http://developer.berlios.de/project/showfiles.php?group_id=3237"
            title="Link to released files.">released</a>
    a prealpha version of the PPLT library. The
    <span title="This core library is called pyDCPU">Core-Library</span> is
    quite useable but the abstraction-layer is completely missing.
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
    <a href="/doc/pyDCPU_Intro.html"
        title="Intoduction into the pyDCPU Core library.">introduction</a>.

    <p>The second part is called PPLT-Library. This library is build on the top
    of pyDCPU. It is an abstraction-layer. This is necessary for providing a simple
    to use interface to the pyDCPU core library. This layer do not handle with
    modules but with abstract devices. </p>
    </div>
    
    <div class="Head">Supported Hardware</div>
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
    </ul>
    </div>
</div>
