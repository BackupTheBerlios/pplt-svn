import sys
import wx
import Events
from SimpleCanvas import SimpleCanvas
from Costmap import CanvasCostmap
from SimpleCanvasObjects import gModule, gPin, gWire



class Canvas(SimpleCanvas):
    
    def __init__(self, parent, ID):
        SimpleCanvas.__init__(self, parent, ID)
        self._cost_map = None #CanvasCostmap( (0,0) )
        self._corner_cost = 5


    def route(self, frm_pin, to_pin, gc=None):
        self._logger.debug("Begin routing. Set cursor")
        wx.BusyCursor()

        frm = frm_pin.getPosition()
        to  = to_pin.getPosition()

        self._cost_map.setTarget(to)
        todo_stack = InsortList()
        back_track = CanvasCostmap( (0,0) )
       
        mod_list = self.getObjects(gModule)
        def pinHit( coord ):
            if coord == frm or coord == to:
                self._logger.debug("hit but start/end")
                return False
            for mod in mod_list:
                if isinstance(mod.hitTest( coord ), gPin):
                    self._logger.debug("PinHit! at %s (%s<->%s)"%(coord, frm, to))
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

        return self._back_route(frm, to, back_track, gc)


    def _back_route(self, frm, to, back_track, gc):
        if gc: back_track.draw(gc)
        
        route = [to]
        cx,cy = to
        
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
            if best_dir == None: raise Exception("Oops")
            route.insert(0, best_dir)
            (cx, cy) = best_dir
        
        return route


    def draw(self, dc):
        self._cost_map = CanvasCostmap()
        for mod in self.getObjects(gModule):
            self._cost_map.addModule( mod.getPosition(), mod.getSize() )
        
        connections = self.getObjects( coConnection )
        for con in connections:
            con.reroute(dc)
            self._cost_map.addWire( con )
        
        SimpleCanvas.draw(self, dc)

       


class coConnection (gWire):
    """ Extends the L{gWire} class to use the routing algorithm of the 
        L{Canvas} class to find it's way throught the canvas. """

    def __init__(self, frm, to):
        """ Constructor needs the start and end "pin". """
        can = frm.getCanvas()
        if not isinstance(can, Canvas):
          raise Exception("coConnection needs a Canvas instance as canvas")
        gWire.__init__(self, frm, to, [])


    def reroute(self, dc=None):
        """ Will be called by the redraw() method of Canvas to reroute the 
            wire. """
        can = self.getCanvas()
        route = can.route( self.getFrom(), self.getTo())#, dc )
        self.setNodes(route[1:-1])



class InsortList:
    """ Internal used I{insort}-sorted lis}. """
    _list = None 
    def __init__(self):
        self._list = []

    def insert(self, cost, item):
        for i in range(len(self._list)):
            (icost, iitem) = self._list[i]
            if icost >= cost:
                self._list.insert( i, (cost,item) )
                return
        self._list.append( (cost, item) )

    def pop(self):
        return self._list.pop(0)

    def __len__(self): return len(self._list)


       
