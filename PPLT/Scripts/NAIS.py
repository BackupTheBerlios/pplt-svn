import Tkinter;
import Tix;


class SetupPage(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self);
        self.title('JVisuServer for NAIS FP-0/2');


        self.PARAFRM = Tkinter.Frame(self);
        self.PARAFRM.pack(expand = 0);
        self.COM = Tkinter.StringVar(self.PARAFRM);
        self.COM.set('COM1');
        self.COMMENU = Tkinter.OptionMenu(self.PARAFRM,
                                          self.COM,
                                          'COM1',
                                          'COM2',
                                          'COM3');
        self.COMMENU['width'] = 6;
        self.COMMENU.pack(side=Tkinter.LEFT);

        self.SPEED = Tkinter.StringVar(self.PARAFRM);
        self.SPEED.set('19200');
        self.SPEEDMENU = Tkinter.OptionMenu(self.PARAFRM,
                                            self.SPEED,
                                            '9600',
                                            '19200');
        self.SPEEDMENU['width'] = 6;
        self.SPEEDMENU.pack(side=Tkinter.LEFT);

        self.PARITY = Tkinter.StringVar(self.PARAFRM);
        self.PARITY.set('Even');
        self.PARITYMENU = Tkinter.OptionMenu(self.PARAFRM,
                                             self.PARITY,
                                             'None',
                                             'Even',
                                             'Odd');
        self.PARITYMENU['width'] = 6;
        self.PARITYMENU.pack(side=Tkinter.RIGHT);

        self.SERVERFRM = Tkinter.Frame(self);
        self.SERVERFRM.pack(expand = 1, fill='x');
        self.ADDRENTRY = Tkinter.Entry(self.SERVERFRM);
        self.ADDRENTRY.insert(0,'127.0.0.1');
        self.ADDRENTRY.pack(side=Tkinter.LEFT,
                            expand = 1,
                            fill = 'x');
        self.PORTENTRY = Tkinter.Entry(self.SERVERFRM);
        self.PORTENTRY.insert(0,'2200');
        self.PORTENTRY.pack(side = Tkinter.RIGHT,
                            expand = 0);

#        self.SYMBOLTREE = Tix.Tree(self);
#        self.SYMBOLTREE[hlist] = [];
#        self.SYMBOLTRRE.pack();




setup = SetupPage();
setup.mainloop();
        
