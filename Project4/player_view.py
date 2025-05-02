from pubsub import pub

from view_object import ViewObject


class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}

        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.del_game_object, 'delete')

    def new_game_object(self, game_object):
        view_object = ViewObject(game_object)
        self.view_objects[game_object.id] = view_object
    def del_game_object(self, game_object):
        self.view_objects[game_object.id].deleted()
        del self.view_objects[game_object.id]
    def tick(self):
        for key in self.view_objects:
            self.view_objects[key].tick()