import abc
import model.world
import model.structure
import model.agent
import model.perceptionhandler

class Experiment(object):

    controller = None

    def parse_world(self, world_repr, mapper=None):
        """
        Parse a representation of a world to a world.
        :param world_repr: A list of strings that represent a world.
        :param map: A function that maps symbols to objects.
        :return: The world.
        :rtype: model.world.World
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
        """
        Parse a symbol to a world entity.
        :param symbol: The symbol to parse to an entity.
        :return: The entity to be placed in the world.
        :rtype: model.world.Entity
        """
        if symbol == "w":
            return model.structure.Wall()
        elif symbol == "b":
            return model.structure.Block()
        elif symbol == "a":
            return model.agent.ConstructiveAgent()
        elif symbol == "h":
            return model.agent.HomeostaticConstructiveAgent()
        elif symbol == "p":
            a = model.agent.ConstructiveAgent()
            a.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())
            return a
        else:
            return None

    @abc.abstractmethod
    def get_world(self):
        """
        Get the world generated by this experiment.
        :return: The world generator by this experiment.
        :rtype: model.world.World
        """
        raise NotImplementedError("Should be implemented by child")

    def has_controller(self):
        return self.controller != None

    def get_controller(self):
          return self.controller
        