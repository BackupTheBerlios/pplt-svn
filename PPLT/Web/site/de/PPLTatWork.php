<div class="Head">PPLT at Work</div>
<div class="Text">
	In diesem Dokument m&ouml;chte ein paar Beispiele zeigen und diese kurz 
	erleutern. In dem ersten Beispiel habe ich eine Siemens SIMATIC S7-200
	Steuerung an die zweite serielle Schnittstelle angeschlossen. Es werden
	dann die Merker SMB28(ein Byte) und SM0.5(ein Bit) ausgelesen. Des weiteren
	habe ich an die erste serielle Schnitstelle mein Siemens Handy (S55) mit 
	einen sog. Datenkabel angeschlossen. Von diesem Telefon lasse ich dann
	den Battriestaus, die Signalqualit&auml;t, der Modellname und den
	Herstellernamen aus lesen.  
	
	<p>Um diese Daten darstellen zu k&ouml;nnen, habe ich die Server
	<i>PPLTWebServer</i> und <i>JVisuServer</i> benutzt. Der erste 
	Server ist ein einfacher Web-Server mit dessen Hilfe man mit
	einem Browser (hier Firefox) durch den Symbolbaum
	browsen kann. Der zweite Server stellt den Symbolbaum der
	in Java geschriebenen Visualisierung JVisu bereit.<p>

<pre>
import PPLT;

psys = PPLT.System();
psys.LoadDevice("Mobile.GSMMobilePhone", "handy", {"Port":"0","Speed":"115200"});
psys.LoadDevice("PLC.S7-200", "s7", {"Port":"1","PCAddr":"0","S7Addr":"2"});

psys.CreateFolder("/handy");
psys.CreateSymbol("/handy/battery", "handy::GSM::battery", "DWord");
psys.CreateSymbol("/handy/signal", "handy::GSM::quality", "DWord");
psys.CreateSymbol("/handy/manufacturer", "handy::GSM::manufacturer", "String");
psys.CreateSymbol("/handy/model", "handy::GSM::model", "String");

psys.CreateFolder("/simatic");
psys.CreateSymbol("/simatic/SMB28", "s7::Marker::SMB28", "Byte");
psys.CreateSymbol("/simatic/SM0.5", "s7::Marker::SM0.5", "Bool");

psys.LoadServer("Web.PPLTWebServer", "web", "admin", {"Address":"10.1.1.4","Port":"4711"});
psys.LoadServer("Visu.JVisuServer", "jvisu", "admin", {"Address":"10.1.1.4","Port":"2200"});

while True:
    pass;
</pre>

	<p>Dieses Script l&auml;d also all die Ger&auml;te, erzeugt die Symbole und startet zum Schluss
	die Server. Wenn sie nun mit ihrem Browser auf die Addresse "http://10.1.1.4:4711" gehen,
	dann werden sie in etwa folgendes sehen:

	<table style="border:none;" align="center">
	<tr>
	<td>
		<a href="/img/PPLTWeb02.png">
			<img src="/img/pPPLTWeb02.png" alt="Screenshot der Seite" title="PPLTWebServer">
		</a>
	</td>
	<td>
		<a href="/img/PPLTWeb01.png">
			<img src="/img/pPPLTWeb01.png" alt="Screenshot der Seite" title="PPLTWebServer">
		</a>
	</td>
	</tr></table>

	Wenn sie hingegen die Visualisierung JVisu verwenden wollen, kommt auf sie 
	ein wenig Konfigurationsarbeit zu. Wenn sie JVisu gestartet haben, 
	m&uuml;ssen sie zun&auml;chst einmal ein sog. Panel zusammen stellen.
	So ein Panel umfasst ein oder mehrere Anzeigeelemente, die jeweis mit einem
	Symbol aus dem Symbolbam verbunden werden. das Ergebnis k&ouml;nnte dann
	so aussehen:
	<p align="center">
		<a href="/img/JVisu01.png">
			<img src="/img/pJVisu01.png" alt="Screenshot von einem JVisuPanel" title="JVisu">
		</a>
	</p>
	</p>

	<p>Im folgenden m&ouml;chte ich kurz den Quelltext diskutieren.<br>
	In der ersten Zeile wird mit <i>import PPLT</i> die PPLT-Bibliothek 
	eingebunden. Und in der 3. Zeile wird mit dem aufruf 
	<i>psys = PPLT.System()</i> ein PPLT-System Objekt erzeugt und
	initialisiert. Bei der Initialisierung werden die Module, Ger&auml;te,
	und Server gesucht und die Benutzerdatenbank (auf die ich hier nicht
	weiter eingehen m&ouml;chte) geladen. Alle darauf folgenden Aktionen
	werden durch den Aufruf einer Methode dieses Objektes veranlasst.</p>

	<p>Die beiden Aufrufe von <i>psys.LoadDevice</i>, veranlassen das System
	,wie der Name schon sagt, die entsprechenden Ger&auml;te zu laden. Um
	so ein Ger&auml;t korrekt zu laden ben&ouml;tigt das System genaue
	Informationen. Wie zum Beispiel, welches ger&auml;t zu laden ist,
	unter welchen Alias (Namen) es sp&auml;ter zu verwalten ist und
	mit welchen Parametern das Ger&auml;t initialisiert werden soll. 
	Der Names des Ger&auml;tes, das zu laden ist wird als erster Parameter
	der Methode &uuml;bergen gefolgt von dem Alias, mit dem das erzeugte
	Ger&auml;t dann identifiziert werden kann. Als letzten Parameter
	kommt ein sog. Dictionary, das die Parameter f&uuml;r das initialisieren
	des Ger&auml;tes. (So ein <i>Dictionary</i> wird in anderen Sprachen
	auch als <i>Hash</i> oder <i>assoziatives Array</i> bezeichnet.)</p>

	<p>Das Mobiltelefon wird mit den Parametern <i>Port=0</i> und 
	<i>Speed=115200</i> geladen, was so viel bedeutet, das das
	Handy an der ersten serielle Schnitstelle (0=COM1, 1=COM2,...)
	angeschlossen ist und diese mit einer &Uuml;bertragungsgeschwindigkeit von
	115200 Baud arbeiten soll.<br>
	Die Parameter f&uuml;r die SIMATIC sind hingegen komplizierter. Diese
	wird &uuml;ber die zweite serielle Schnitstelle (<i>Port=1</i>)
	angesprochen. Da es sich bei dem &Uuml;bertragungsprotokoll
	um PPI handelt, welches ein (echtes) BUS-Protokoll ist, 
	m&uuml;ssen beide BUS-Teilnehmer eine Adresse besitzen.
	F&uuml;r den PC w&auml;re das die 0 (<i>PCAddr=0</i>) und
	f&uuml;r die Steuerung die 2 (<i>S7Addr=2</i>).</p>

	<p>Wenn w&auml;rend der initialisierung ein Fehler auftritt und
	das Ger&auml;t nicht geladen werden kann, gibt die Methode
	<i>False</i> zur&uuml;ck. Dies kann man dann mit einer einfachen
	<i>if</i>-Anweisung abfragen. Darauf habe ich bei diesem
	Beispiel aus Gr&uuml;den der &Uuml;bersicht verzichtet.</p>

	<p>[Symbole][Symbolbaum]</p>
	<p>[Server]</p>
	<p>[Endlosschleife]</p>
	 	

</div>
