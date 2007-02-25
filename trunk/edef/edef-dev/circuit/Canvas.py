import sys
import Events
from SimpleCanvas import SimpleCanvas
from Costmap import CanvasCostmap
from SimpleCanvasObjects import gModule, gPin
from CanvasObjects import coConnection


class InsortList:
    _list = None 
    def __init__(self):
        self._list = []

    def insert(self, cost, item):
        for i in range(len(self._list)):
            (icost, iitem) = self._list[i]
            if icost > cost:
                self._list.insert( i, (cost,item) )
                return
        self._list.append( (cost, item) )

    def pop(self):
        return self._list.pop(0)

    def __len__(self): return len(self._list)


class Canvas(SimpleCanvas):
    
    def __init__(self, parent, ID):
        SimpleCanvas.__init__(self, parent, ID)
        self._cost_map = CanvasCostmap( (0,0) )
        self._corner_cost = 5
        self.Bind(Events.EVT_CAN_CONNECT, self._c_OnConnect)


    def _route(self, frm, to, gc=None):
        self._cost_map.setTarget(to)
        todo_stack = InsortList()
        back_track = CanvasCostmap( (0,0) )
       
        mod_list = self.getObjects(gModule)
        def pinHit( coord ):
            if coord == frm or coord == to:
                print "hit but start/end"
                return False
            for mod in mod_list:
                if isinstance(mod.hitTest( coord ), gPin):
                    print "PinHit! at %s (%s<->%s)"%(coord, frm, to)
                    return True
            return False

        todo_stack.insert( self._cost_map.get(frm), (frm, frm, self._cost_map.get(frm)) )
        back_track.add( frm, self._cost_map.get(frm))
        
        while True:
            (ccost, (cur, prev, csum)) = todo_stack.pop()
            cx,cy = cur
            px,py = prev
            
            # SOUTH
            if cx+1 <= 1000 and back_track.getPure( (cx+1,cy) )==0:      # FIXME cx+1<=max_x
                if px == cx: cost = self._cost_map.get((cx+1,cy))+self._corner_cost
                elif pinHit( (cx+1,cy) ): cost = sys.maxint
                else: cost = self._cost_map.get((cx+1,cy))
                todo_stack.insert(cost, ((cx+1,cy), cur, csum+cost))
                back_track.add( (cx+1, cy), cost+csum )
            # NORTH
            if cx-1 >= 0 and back_track.getPure( (cx-1,cy) )==0:
                if px == cx: cost = self._cost_map.get((cx-1,cy))+self._corner_cost
                elif pinHit( (cx-1,cy) ): cost = sys.maxint
                else: cost = self._cost_map.get((cx-1,cy))
                todo_stack.insert(cost, ((cx-1,cy), cur, csum+cost))
                back_track.add( (cx-1, cy), cost+csum )
            # EAST
            if cy+1 <= 1000 and back_track.getPure( (cx,cy+1) )==0:    # FIXME
                if py == cy: cost = self._cost_map.get((cx,cy+1))+self._corner_cost
                elif pinHit( (cx,cy+1) ): cost = sys.maxint
                else: cost = self._cost_map.get((cx,cy+1))
                todo_stack.insert(cost, ((cx,cy+1), cur, csum+cost) )
                back_track.add( (cx,cy+1), cost+csum )
            # WEST
            if cy-1 >= 0 and back_track.getPure( (cx,cy-1) )==0:
                if py == cy: cost = self._cost_map.get((cx,cy-1))+self._corner_cost
                elif pinHit( (cx,cy-1) ): cost = sys.maxint
                else: cost = self._cost_map.get((cx,cy-1))
                todo_stack.insert(cost, ((cx,cy-1), cur, csum+cost))
                back_track.add( (cx,cy-1), cost+csum )
            
            if cur == to: break # yeah found!
            if len(todo_stack)==0:
                raise Exception("No route found from %s to %s"%(frm,to))

        #print "found -> calling back_track"
        return self._back_route(frm, to, back_track, gc)


    def _back_route(self, frm, to, back_track, gc):
        if gc: back_track.draw(gc)
        #return [frm, to]
        route = [to]
        cx,cy = to
        #cost = back_track.getPure( (cx,cy) )
        
        while True:
            best_dir = None
            cost = sys.maxint
            # SOUTH
            if cx+1 <= 1000 and cost > back_track.getPure((cx+1,cy)):
                cost = back_track.getPure((cx+1,cy))
                best_dir = (cx+1,cy)
            # NORTH    
            if cx-1 >= 0 and cost > back_track.getPure( (cx-1,cy) ):
                cost = back_track.getPure((cx-1,cy))
                best_dir = (cx-1,cy)
            # EAST               
            if cy+1 >= 0 and cost > back_track.getPure( (cx,cy+1) ):
                cost = back_track.getPure((cx,cy+1))
                best_dir = (cx,cy+1)
            # WEST                
            if cy-1 >= 0 and cost > back_track.getPure( (cx,cy-1) ):
                cost = back_track.getPure((cx,cy-1))
                best_dir = (cx,cy-1)
            
            if (cx, cy) == frm: break 
            if best_dir == None: raise Exception("Opps")
            route.insert(0, best_dir)
            (cx, cy) = best_dir
        
        return route


    def addConnection(self, frm, to, auto_redraw=False):
        if self.isConnection(frm, to): return
        print "Add connection %s -> %s"%(frm,to)
        con = coConnection(frm, to)
        if auto_redraw: self.redraw()


    def isConnection(self, frm, to):
        connections = self.getObjects( coConnection )
        for con in connections:
            if (frm, to) == (con.getFrom(), con.getTo()):
                return True
        return False

    def getConnectionsFrom(self, obj):
        lst = []
        connections = self.getObjects( coConnection )
        for con in connections:
            if obj == con.getFrom().getModule(): lst.append(con)
        return lst

    def getConnectionsTo(self, obj):
        lst = []
        connections = self.getObjects( coConnection )
        for con in connections:
            if obj == con.getTo().getModule(): lst.append(con)
        return lst


    def draw(self, dc):
        self._cost_map = CanvasCostmap()
        for mod in self.getObjects(gModule):
            self._cost_map.addModule( mod.getPosition(), mod.getSize() )
        
        connections = self.getObjects( coConnection )
        for con in connections:
            route = self._route( con.getFromPos(), con.getToPos(), dc)
            con.setNodes( route[1:-1] )
            self._cost_map.addWire( con )
        
        #self._cost_map.draw(dc)
        SimpleCanvas.draw(self, dc)


    def _c_OnConnect(self, evt):
        frm = evt.GetFrom()
        to  = evt.GetTo()

        if not self.isConnection( frm, to ):
            self.addConnection( frm, to )
        self.redraw()


