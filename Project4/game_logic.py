from panda3d.core import CollisionNode, CollisionBox, Point3, BitMask32

from game_object import GameObject
from pubsub import pub

from player_object import PlayerObject

class GameLogic:


    def __init__(self):
        self.render = None
        self.collision_ray = None
        self.button = None
        self.properties = {}
        self.game_objects = {}
        self.next_id = 0

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, position, kind, size):
        if kind == "player":
            obj = PlayerObject(position, kind, self.next_id, size)
        else:
            obj = GameObject(position, kind, self.next_id, size)

        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def load_world(self):
        self.create_object([0, -10, -1.8], "crate", (8.9, 8.9, 1))
        self.create_object([0, -10, 2.0], "crate", (8.9, 8.9, 1))
        self.create_object([0, -5, 0], "crate", (9, 1, 3))
        self.create_object([-5, -10, 0], "crate", (1, 9, 3))
        self.create_object([5, -10, 0], "crate", (1, 9, 3))
        self.create_object([0, -15, 0], "crate", (9, 1, 3))
        self.create_object([0, -14, 0], "button", (1, 1, 1))
        self.create_object([0, -10, 0], "player", (1, 1, 1))

    def destroy_world(self):
        print("boom")
        ids_to_remove = list(self.game_objects.keys())
        print(len(ids_to_remove))
        for obj_id in ids_to_remove:
            pub.sendMessage('delete', game_object=self.game_objects[obj_id])

            del self.game_objects[obj_id]


    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value