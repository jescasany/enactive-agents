import model.world
import model.structure.structure
import model.agent.agent


class Experiment(object):
    def parse_world(self, world_repr, mapper=None):
        """
        Parse a representation of a world to a world.
        :param world_repr: A list of strings that represent a world.
        :param map: A function that maps symbols to objects.
        :return: The world.
        """
        if mapper is None:
            mapper = self.mapper

        world = model.world.World()

        max_y = 0
        max_x = 0
        y = 0
        for line in world_repr:
            x = 0
            for symbol in line:
                obj = mapper(symbol)
                if not obj is None:
                    obj.set_position((x,y))
                    world.add_entity(obj)
                x += 1
                max_x = max(max_x, x)
            y += 1
            max_y = max(max_y, y)

        world.set_width(max_x)
        world.set_height(max_y)

        return world

    def mapper(self, symbol):
        if symbol == "w":
            return model.structure.structure.Structure()
        elif symbol == "a":
            return model.agent.agent.Agent()
        else:
            return None