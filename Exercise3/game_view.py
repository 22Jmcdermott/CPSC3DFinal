from panda3d.core import Spotlight, VBase4, AmbientLight


class GameView:
    def __init__(self, render):
        self.render = render
        self.spotlightNP = None
        self.add_ambient_light()

    def add_ambient_light(self):
        ambient_light = AmbientLight("ambientLight")
        ambient_light.setColor(VBase4(0.5, 0.5, 0.5, 1))
        ambientNP = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambientNP)

    def add_spotlight(self, target):
        if self.spotlightNP:
            self.spotlightNP.removeNode()

        spotlight = Spotlight("Spotlight")
        spotlight.setColor(VBase4(1, 1, 1, 1))
        spotlight.setExponent(20)
        spotlight.setShadowCaster(True, 1024, 1024)

        self.spotlightNP = self.render.attachNewNode(spotlight)
        self.spotlightNP.setPos(5, 2, 5)
        self.spotlightNP.lookAt(target)

        self.render.setLight(self.spotlightNP)

    def remove_spotlight(self):
        if self.spotlightNP:
            self.render.clearLight(self.spotlightNP)
            self.spotlightNP.removeNode()
            self.spotlightNP = None
