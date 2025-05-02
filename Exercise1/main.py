from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight


class MyApp(ShowBase):
    def __init__(self):
        # Call the superclass constructor
        ShowBase.__init__(self)

        # This disables Panda3d's built in camera control
        self.objects = []
        base.disableMouse()

        #load pandas
        for i in range(3):
            obj = self.panda = self.loader.loadModel("Models/panda")
            obj.reparentTo(self.render)
            obj.setPos(i*4, 0, 0)
            obj.setScale(0.3)
            self.objects.append({"model": obj, "speed": 4 *-1})


        # Load the model
        self.environment = self.loader.loadModel("Models/environment")
        self.environment.reparentTo(self.render)
        self.environment.setPos(0, 0, 0)
        self.environment.setScale(0.1,0.1,0.1)



        # Initial camera setup
        self.camera.set_pos(-10, 14, 9)
        self.camera.look_at(0, 2, 5)

        self.taskMgr.add(self.rotate_panda, 'rotate_panda', sort=10)


    def rotate_panda(self, task):
        for obj_info in self.objects:
            obj = obj_info["model"]
            speed = obj_info["speed"]
            obj.setHpr(obj.getH() + speed, 0, 0)
        return Task.cont


app = MyApp()
app.run()

