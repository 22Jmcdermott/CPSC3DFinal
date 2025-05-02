from panda3d.core import CollisionNode, GeomNode, CollisionRay, CollisionHandlerQueue, CollisionTraverser


class GameObject:
    def __init__(self, loader, render, camera):
        self.pickerRay = None
        self.cTrav = None
        self.rayQueue = None
        self.render = render
        self.loader = loader
        self.camera = camera

        self.panda = self.load_panda()
        self.environment = self.load_environment()
        self.sky = self.load_sky()

        self.spinning = False
        self.spotlightNP = None

        self.setup_collision()

    def load_panda(self):
        panda = self.loader.loadModel("Models/panda")
        panda.reparentTo(self.render)
        panda.setPos(0, 40, -3)
        panda.setScale(1)
        panda.setTag("selectable", "")
        return panda

    def load_environment(self):
        environment = self.loader.loadModel("Models/BeachTerrain")
        environment.reparentTo(self.render)
        environment.setPos(0, 0, 0)
        environment.setScale(1, 1, 1)
        environment.setTexture(self.loader.loadTexture("Textures/Material_#4_CL.tif"))
        return environment

    def load_sky(self):
        sky = self.loader.loadModel("Models/blue_sky_sphere")
        sky.reparentTo(self.render)
        sky.setPos(0, 0, 0)
        sky.setScale(1, 1, 1)
        sky.setTexture(self.loader.loadTexture("Textures/sky_Material_#24_CL.tif"))
        return sky

    def setup_collision(self):
        pickerNode = CollisionNode('mouseRay')
        pickerNP = self.camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)

        self.rayQueue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(pickerNP, self.rayQueue)

    def get_nearest_object(self, x, y):
        self.pickerRay.setFromLens(self.camera.node(), x, y)
        self.cTrav.traverse(self.render)
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            entry = self.rayQueue.getEntry(0)
            pickedNP = entry.getIntoNodePath()
            pickedNP = pickedNP.findNetTag('selectable')
            if not pickedNP.isEmpty():
                return pickedNP
        return None
