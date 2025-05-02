from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from game_object import GameObject
from game_view import GameView


class GameController(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Initialize Model and View
        self.model = GameObject(self.loader, self.render, self.camera)
        self.view = GameView(self.render)

        # Set up user interactions
        self.spinning = False
        self.accept("mouse1", self.on_mouse_click)

        self.setup_camera()

    def setup_camera(self):
        self.camera.set_pos(20, -50, -50)
        self.camera.look_at(self.model.panda)

    def rotate_panda(self, task):
        self.model.panda.setHpr(self.model.panda, 1, 0, 0)
        return Task.cont

    def on_mouse_click(self):
        if not self.mouseWatcherNode.hasMouse():
            return

        x = self.mouseWatcherNode.getMouseX()
        y = self.mouseWatcherNode.getMouseY()

        picked_object = self.model.get_nearest_object(x, y)
        if picked_object and picked_object.hasNetTag("selectable"):
            if self.spinning:
                self.taskMgr.remove("spinTask")
                self.view.remove_spotlight()
            else:
                self.taskMgr.add(self.rotate_panda, "spinTask")
                self.view.add_spotlight(self.model.panda)
            self.spinning = not self.spinning

    def run_app(self):
        self.run()
