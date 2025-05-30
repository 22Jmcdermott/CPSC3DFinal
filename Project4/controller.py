from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys

from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser, \
    WindowProperties, Quat
from pubsub import pub

from game_logic import GameLogic
from player_view import PlayerView

controls = {
    'w': 'forward',
    'a': 'left',
    's': 'backward',
    'd': 'right',
    'w-repeat': 'forward',
    'a-repeat': 'left',
    's-repeat': 'backward',
    'd-repeat': 'right',
    'q': 'toggleTexture',
    'escape': 'toggleMouseMove',
    'mouse1': 'click',
}

class Main(ShowBase):
    def go(self):
        pub.subscribe(self.new_player_object, 'create')
        pub.subscribe(self.new_collider, 'collider')

        self.player = None

        self.cTrav = CollisionTraverser()
        self.collision_queue = CollisionHandlerQueue()
        #COMMENT LINE BELOW TO TURN OF SHOWING COLLISIONS
        #self.cTrav.show_collisions(self.render)

        # load the world
        self.game_logic.load_world()
        self.sky = base.loader.loadModel("Models/verycloudy")
        self.sky.reparentTo(base.render)
        self.sky.setPos(0,0,-50)
        self.sky_texture = base.loader.loadTexture("Textures/maps/SKY.tif")
        self.sky.setTexture(self.sky_texture)

        self.map = base.loader.loadModel("Models/cornfield")
        self.map.reparentTo(base.render)
        self.map.setPos(0, 0, -5)
        self.map_texture = base.loader.loadTexture("Textures/maps/cornfieldTEXTURE01.tif")
        self.map.setTexture(self.map_texture)

        self.camera.set_pos(0, -20, 0)
        self.camera.look_at(0, 0, 0)
        self.taskMgr.add(self.tick)

        picker_node = CollisionNode('mouseRay')
        picker_node.set_into_collide_mask(0)
        picker_np = self.camera.attachNewNode(picker_node)
        picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        picker_node.addSolid(self.pickerRay)
        picker_np.show()
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(picker_np, self.rayQueue)


        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        self.SpeedRot = 0.05
        self.CursorOffOn = 'Off'
        self.props = WindowProperties()
        self.props.setCursorHidden(True)
        self.win.requestProperties(self.props)
        self.run()

    def new_collider(self, collider):
        self.cTrav.addCollider(collider, self.collision_queue)

    def new_player_object(self, game_object):
        if game_object.kind != "player":
            return
        self.player = game_object


    def get_nearest_object(self):
        self.pickerRay.setFromLens(self.camNode, 0, 0)
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            entry = self.rayQueue.getEntry(0)
            picked_np = entry.getIntoNodePath()
            picked_np = picked_np.findNetTag('selectable')

            if not picked_np.isEmpty() and picked_np.getPythonTag("owner"):
                return picked_np.getPythonTag("owner")

        return None

    def input_event(self, event):
        self.input_events[event] = True

    def tick(self, task):
        for entry in self.collision_queue.entries:
            into_go = entry.into_node.get_python_tag('game_object')
            from_go = entry.from_node.get_python_tag('game_object')
            into_go.collision(from_go)
            from_go.collision(into_go)

        if 'click' in self.input_events and base.mouseWatcherNode.hasMouse():
            picked_object = self.get_nearest_object()
            if picked_object and hasattr(picked_object, 'game_object') and picked_object.game_object.kind == "button":
                self.game_logic.destroy_world()

        if 'toggleMouseMove' in self.input_events:
            if self.CursorOffOn == 'Off':
                self.CursorOffOn = 'On'
                self.props.setCursorHidden(False)
            else:
                self.CursorOffOn = 'Off'
                self.props.setCursorHidden(True)

            self.win.requestProperties(self.props)

        if self.input_events:
            pub.sendMessage('input', events=self.input_events)



        if self.CursorOffOn == 'Off':
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            if self.win.movePointer(0, base.win.getXSize() // 2, self.win.getYSize() // 2):
                self.player.z_rotation = self.camera.getH() - (x - self.win.getXSize() / 2) * self.SpeedRot
                self.player.x_rotation = self.camera.getP() - (y - self.win.getYSize() / 2) * self.SpeedRot

                if self.player.x_rotation <= -90.1:
                    self.player.x_rotation = -90
                if self.player.x_rotation >= 90.1:
                    self.player.x_rotation = 90

        h = self.player.z_rotation
        p = self.player.x_rotation
        r = self.player.y_rotation
        self.camera.setHpr(h, p, r)

        q = Quat()
        q.setHpr((h, p, r))
        forward = q.getForward()
        delta_x = -forward[0]
        delta_y = -forward[1]
        delta_z = -forward[2]
        x, y, z = self.player.position
        distance_factor = 0.5
        self.camera.set_pos(x + delta_x * distance_factor, y +
                            delta_y * distance_factor, z + delta_z * distance_factor)

        # give the model and view a chance to do something
        self.game_logic.tick()
        self.player_view.tick()

        if self.game_logic.get_property("quit"):
            sys.exit()

        self.input_events.clear()
        return Task.cont

    def __init__(self):
        ShowBase.__init__(self)
        self.sky_texture = None
        self.sky = None
        self.input_events = None
        self.pickerRay = None
        self.collision_queue = None
        self.props = None
        self.SpeedRot = None
        self.player = None
        self.CursorOffOn = None
        self.disableMouse()
        self.render.setShaderAuto()
        # create the model and view
        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic)

if __name__ == '__main__':
    main = Main()
    main.go()