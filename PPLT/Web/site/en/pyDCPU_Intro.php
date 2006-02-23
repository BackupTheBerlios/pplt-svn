<div class="TextBody">
    <div class="Text">
        <p>In this page I will give you a (really) short intoduction into the pyDCPU concept,
        if you want ot know more, please follow the links in this text.
        </p>
    </div>


    <div class="Head">Main Goals</div>
    <div class="Text">
        The main goal was to have a flexible, modular and platform-independent system,
        that graps information from many different systems over different interfaces
        meaning controlers and <i>intelligent</i> sensors and manage them together in one,
        so called, <i>Symbol-Tree</i>.

        <p>The second goal was to have an own user and group management to control the
        access to this central Symbol-Tree.</p>

        <p>At least it should be able to export this symbols to other systems by
        modules. So it is not bound to a single visualiziation.</p>
    </div>



    <div class="Head">Design</div>
    <div class="Text">
    You can split the pyDCPU system into 3 parts.

    <p style="text-align:center"><img src="/img/BasicConcept.png" alt="" title="Basic Concept"></p>
    <p>One part imports information and data from systems for example from controlers
    or sensors. This part is a little bit difficult to use because you have to handle
    with a lot of modules to get information from a controler. You need for example
    a module for the interface, the BUS protocol and one for the command-messageformat
    to read out values of a markers in a controller. But this is a main goal of this
    project because you only need to replace the interface and protocol modules to
    talk to the same controller over an other BUS-system. This makes this system very
    flexible.</p>

    <p>The other part manage this imported information into a file-system like
    <i>Symbol-Tree</i>. Imagine this Tree as a small file-system with folders and files.
    Each file (called <i>symbol</i>) represent for example a marker into a controller or
    the actual value of a sensor. To manage them better, if you have many of them, there are
    folders. This Symbol-Tree have also (like file-systems) a right-managment. This means
    you can define permissions to a spezific symbol or folder for other users and groups.</p>


    <p>The last part exports this symboltree to other systems, like visualisations or
    databases. This export-part also works with modules, so it is possible to process
    the information in the symbol-tree in many applications (if there are implemented
    with a module). For example there is a module which uses <a href="/en/SimpleExport.html">XML-RPC</a>
    to export this symbols for other applications.</p>

    But the best of all is, it was written in Python.


    <div class="Head">Future</div>
    <div class="Text">
        At first I planed to reach the stabile state.

        <p>But to reach this I need <u>help</u>. I am studying physics at the university
        of Potsdam. It is hard to do booth, studying physics and developing
        open source software at the same time. So if you are interested contact
        me. (please)</p>
    </div>
</div>
