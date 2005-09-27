      <div class="TextBody">
		<div class="Head">Create a new <acronym>CoreInstance</acronym>.</div>
		<div class="Text">
			This call will create a new CoreInstance (CoreObject). This is the core
			of the pyDCPU(PPLT) system. All work will be done by calling methods of
			this object. Let's say it is important.
<pre>
import pyDCPU
Core = pyDCPU.Core(UserDBFile,
	           LogFile = None,
	           LogLevel = 'info',
	           SysLog = False)
</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>UserDBFile</b></td>
					<td>Path to the user/group database-file.</td></tr>
				<tr><td><b>LogFile</b></td>
					<td>Path to the logfile. If <i>None</i>(default) all messages will be written
						to the <i>stderr</i>.</td></tr>
				<tr><td><b>LogLevel</b></td>
					<td>The logging level. One of 'debug','info','error','fatal','off'. (default: 'info')</td></tr>
				<tr><td><b>SysLog</b></td>
					<td>If <i>True</i> all logging messages will be sent to the local SysLog daemon, even
						if a LogFile was specified.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return a Core instance. </td></tr>
			</table>
		</div>


		<div class="Head">Load a MasterModule</div>
		<div class="Text">
<pre>
ID = Core.MasterTreeAdd(ParentID,
			ModName,
			Address,
			Parameter);
</pre>
			It is like "Load Module <b>ModName</b>, setup with <b>Parameter</b>, connect it to
			<b>ParentID</b> with <b>Address</b>."
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>ParentID</b></td>
					<td>The module will be attached to the module pointed by <i>ParentID</i>.</td></tr>
				<tr><td><b>ModName</b></td>
					<td>Name of the Module to be loaded.</td></tr>
				<tr><td><b>Address</b></td>
					<td>Some modules need an address if a child is attached to it. Set to None if not
					needed.</td></tr>
				<tr><td><b>Parameter</b></td>
					<td>A <i>dict</i> of name,value pairs. Used to control the behavior of the module</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return a new ObjectID. This ID is used to attache other modules to it, to destroy it, etc.</td></tr>
			</table>
		</div>


		<div class="Head">Remove/Destroy a MasterModule.</div>
		<div class="Text">
<pre>
Core.MasterTreeDel(ObjectID);
</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>ObjectID</b></td>
					<td>Destroy the Module pointed by the <i>ObjectID</i>. Note: Only Modules
					without children can be destroyed</td></tr>
				</tr>
				<tr><td><b>RETURN</b></td>
					<td>Return True if the Object was sucessfully removed</td></tr>
			</table>
		</div>


		<div class="Head">Attach a SymbolSlot</div>
		<div class="Text">
<pre>
ObjectID = Core.MasterTreeAttachSymbolSlot(ParentID,
                                           Address,
                                           TypeName,
                                           TimeOut = 0.5);
</pre>
			Read it like: "Attach a SymbolSlot to <b>ParentID</b> with <b>Address</b> as <b>TypeName</b> and
			a <b>TimeOut</b> cache time."
			<table>
				<tr><th>Name</th><th>Description</th>
				<tr><td><b>ParentID</b></td>
					<td>The ID of the module the SymbolSlot will be attached to.</td></tr>
				<tr><td><b>Address</b></td>
					<td>Like Address in <i>MasterTreeAdd()</i>.</td></tr>
				<tr><td><b>TypeName</b></td>
					<td>Interpret the data of the parent module a this type.</td></tr>  <!--statt 'a', 'as'?//-->
				<tr><td><b>TimeOut</b></td>
					<td>Cache the value for this time. (default: 0.5s)</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return the ObjectID for the Slot. The slot will now be handled like a
						normal module.</td></tr>
			</table>
		</div>


		<div class="Head">List children of a MasterModule</div>
		<div class="Text">
			<pre>child_list = Core.MasterTreeList(ParentID);</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>ParentID</b></td>
					<td>The ID of the module that childen-IDs you will get back.</td></tr>
				<tr><td><b>RETURN</b>
					<td>Return a list of ObjectIDs.</td></tr>
			</table>
		</div>


		<div class="Head">Load a Export/Server Module</div>
		<div class="Text">
<pre>
ObjectID = Core.ExporterAdd(ExportModule,
                            Paramerters,
                            DefaultUser);
</pre>
			<table>
				<tr><th>Name</th><th>Description</th>
				<tr><td><b>ExportModule</b></td>
					<td>Name of the export module.</td></tr>
				<tr><td><b>Parameters</b></td>
					<td>Like <i>MasterTreeAdd()</i> these are the name, value pairs (dict)
						parameters to control the behavior of the module.</td></tr>
				<tr><td><b>DefaultUser</b></td>
					<td>Some Export/Server protocols have no auth. so this user will always be used.
					Note: Choose an user with less rights, else it would be a security problem.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return the new ObjectID of this loaded module</td></tr>
			</table>
		</div>


		<div class="Head">Unload/Stop a Export/Server Module</div>
		<div class="Text">
			<pre>Core.ExporterDel(ObjectID);</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>ObjectID</b>
					<td>The ObjectID of the Export/ServerModule you want to stop.</td></tr>
				<tr><td><b>RETURN</b>
					<td>Return <tt>True</tt> on sucess and <tt>False</tt> else.</td></tr>
			</table>
		</div>


		<div class="Head">List all runing Export/ServerModules</div>
		<div class="Text">
			<pre>exporter_list = Core.ExporterList()</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>RETURN</b></td>
					<td>List of all runing Export/Server Modules</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Create Folder</div>
		<div class="Text">
			<pre>Core.SymbolTreeCreateFolder(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path of the folder you want to create.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Retrun <tt>True</tt> on sucess.</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree Delete Folder</div>
		<div class="Text">
			<pre>Core.SymbolTreeDeleteFolder(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path of the folder you want to delete.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Retrun <tt>True</tt> on sucess.</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Create a Symbol</div>
		<div class="Text">
<pre>
Core.SymbolTreeCreateSymbol(Path,
                            SymbolSlotID);
</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the symbol you want to create</td></tr>
				<tr><td><b>SymbolSlotID</b></td>
					<td>ID of the SymbolSlot</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return <tt>True</tt> on sucess, <tt>False</tt> otherwise</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Delete a Symbol</div>
		<div class="Text">
			<pre>Core.SymbolTreeDeleteSymbol(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the symbol you want to delete</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return <tt>True</tt> on sucess</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: List Symbols</div>
		<div class="Text">
			<pre>symbol_list = Core.SymbolTreeListSymbols(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the folder you want to list.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return a list of all symbols in folder given by <tt>Path</tt></td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: List Folders</div>
		<div class="Text">
			<pre>symbol_list = Core.SymbolTreeListFolders(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the folder you want to list.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return a list of all folders in folder given by <tt>Path</tt></td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Get the permission</div>
		<div class="Text">
			<pre>(Owner, Group, Modus) = Core.SymbolTreeGetAccess(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td>Path</td>
					<td>The complete path to the symbol or folder</td></tr>
				<tr><td><b>Owner</b></td>
					<td>Username of the user who owns this symbol or folder</td></tr>
				<tr><td><b>Group</b></td>
					<td>Name of the group which the symbol or folder is attached to.</td></tr>
				<tr><td><b>Modus</b></td>
					<td>Integer like the Un*x file modus. Note: This integer has the base 10!</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Returns a tupel of (Owner, Group, Modus)</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Set the permission</div>
		<div class="Text">
			<pre>Core.SymbolTreeSetAccess(Path, Owner, Group, Modus)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td>Path</td>
					<td>The complete path to the symbol or folder</td></tr>
				<tr><td><b>Owner</b></td>
					<td>Username of the user who owns this symbol or folder</td></tr>
				<tr><td><b>Group</b></td>
					<td>Name of the group which the symbol or folder is attached to.</td></tr>
				<tr><td><b>Modus</b></td>
					<td>Integer like the Un*x file modus. Note: This integer has the base 10!</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Returns a tupel of (Owner, Group, Modus)</td></tr>
			</table>
		</div>


		<div class="Head">SymbolTree: Get value</div>
		<div class="Text">
			<pre> value = Core.SymbolTreeGetValue(Path)</pre>
			<table>
				<tr><th>Name</th><th>Description</th></tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the symbol</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return the value of the symbol or <tt>None</tt> on error.</td></tr>
			</table>
		</div>

		<div class="Head">SymbolTree: Set Value</div>
		<div class="Text">
<pre>
Core.SymbolTreeSetValue(Path,
                        Value)
</pre>
			<table>
				<tr><th>Name</th><th>Description</th><tr>
				<tr><td><b>Path</b></td>
					<td>The complete path to the symbol</td></tr>
				<tr><td><b>Value</b></td>
					<td>The value you want to set.</td></tr>
				<tr><td><b>RETURN</b></td>
					<td>Return <tt>True</tt> on success or <tt>False</tt> on error</td></tr>
			</table>
		</div>

      </div>
