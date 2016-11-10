"""
Module to build experiments (worlds, agents, etc.).
"""

import model.interaction
import model.agent
import experiment
import pygame

class BasicExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w.............w",
        "w.wwwwwww.....w",
        "w.......wwwww.w",
        "w.wwwww.......w",
        "w.w.......w...w",
        "w.w.wwwww.w...w",
        "w.w.w...w.ww..w",
        "w.www.....w...w",
        "w.....wwwww.a.w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        feel = model.interaction.PrimitiveInteraction("Feel", "Succeed")
        feel_fail = model.interaction.PrimitiveInteraction("Feel", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return feel_fail
            else:
                return feel

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[feel.get_name()] = _feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(feel_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 1
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[feel_fail] = -1
        
        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

class BasicHomeostaticExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w.............w",
        "w.wwwwwww.....w",
        "w.......wwwww.w",
        "w.wwwww.......w",
        "w.w.......w...w",
        "w.w.wwwww.w...w",
        "w.w.w...w.ww.ww",
        "w.www.....w...w",
        "w.....wwwww.h.w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicHomeostaticExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        feel = model.interaction.PrimitiveInteraction("Feel", "Succeed")
        feel_fail = model.interaction.PrimitiveInteraction("Feel", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                agent.add_to_homeostatic_value("energy", -0.1)
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return feel_fail
            else:
                return feel

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[feel.get_name()] = _feel

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(feel_fail)

        # Set intrinsic homeostatic motivation values.
        motivation = {}
        motivation[step] = lambda agent: agent.get_homeostatic_value("energy") * 0.1
        motivation[step_fail] = lambda agent: -10
        motivation[turn_right] = lambda agent: -2
        motivation[turn_left] = lambda agent: -2
        motivation[feel] = lambda agent: 0
        motivation[feel_fail] = lambda agent: -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)
                if isinstance(entity, model.agent.HomeostaticConstructiveAgent):
                    entity.set_homeostatic_value("energy", 100)


    def get_world(self):
        return self.world

class BasicCoexsistenceExperiment(experiment.Experiment):
    world_representation = [
        "wwwww",
        "w..aw",
        "w.w.w",
        "w.w.w",
        "wa..w",
        "wwwww"
        ]

    def __init__(self):
        super(BasicCoexsistenceExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        feel = model.interaction.PrimitiveInteraction("Feel", "Succeed")
        feel_fail = model.interaction.PrimitiveInteraction("Feel", "Fail")
        cuddle = model.interaction.PrimitiveInteraction("Cuddle", "Succeed")
        cuddle_fail = model.interaction.PrimitiveInteraction("Cuddle", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _feel(world, agent, interaction):
            if world.can_step(agent):
                return feel_fail
            else:
                return feel

        def _cuddle(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if entity != agent and isinstance(entity, model.agent.Agent):
                    return cuddle
            
            return cuddle_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[feel.get_name()] = _feel
        enact_logic[cuddle.get_name()] = _cuddle

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(feel)
        primitives.append(feel_fail)
        primitives.append(cuddle)
        primitives.append(cuddle_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 1
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[feel] = 0
        motivation[feel_fail] = -1
        motivation[cuddle] = 50
        motivation[cuddle_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

class BasicVisionExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w....p........w",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 25
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

class BasicHomeostaticVisionExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwww",
        "w......w",
        "w...w..w",
        "w...w..w",
        "w...w..w",
        "w...w..w",
        "w..ww..w",
        "w..w...w",
        "w.....hw",
        "wwwwwwww",
        ]

    def __init__(self):
        super(BasicHomeostaticVisionExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        eat = model.interaction.PrimitiveInteraction("Eat", "Succeed")
        eat_fail = model.interaction.PrimitiveInteraction("Eat", "Fail")
        destroy = model.interaction.PrimitiveInteraction("Destroy", "Succeed")
        destroy_fail = model.interaction.PrimitiveInteraction("Destroy", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                agent.add_to_homeostatic_value("energy", -0.1)
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _eat(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if isinstance(entity, model.structure.Food):
                    world.remove_entity(entity)
                    agent.add_to_homeostatic_value("energy", 10)
                    return eat
            
            return eat_fail

        def _destroy(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if isinstance(entity, model.structure.Block):
                    world.remove_entity(entity)
                    food = model.structure.Food()
                    food.set_position(entity.get_position())
                    self.world.add_entity(food)
                    return destroy
            
            return destroy_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[eat.get_name()] = _eat
        enact_logic[destroy.get_name()] = _destroy

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(eat)
        primitives.append(eat_fail)
        primitives.append(destroy)
        primitives.append(destroy_fail)

        # Set intrinsic homeostatic motivation values.
        motivation = {}
        motivation[step] = lambda agent: agent.get_homeostatic_value("energy") * 0.1
        motivation[step_fail] = lambda agent: -10
        motivation[turn_right] = lambda agent: -2
        motivation[turn_left] = lambda agent: -2
        motivation[eat] = lambda agent: 10 - agent.get_homeostatic_value("energy") * 0.1
        motivation[eat_fail] = lambda agent: -20
        motivation[destroy] = lambda agent: 30
        motivation[destroy_fail] = lambda agent: -2

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)
                if isinstance(entity, model.agent.HomeostaticConstructiveAgent):
                    entity.set_homeostatic_value("energy", 100)
                    entity.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())


    def get_world(self):
        return self.world

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
            elif event.key == pygame.K_b:
                block = model.structure.Block()
                block.set_position(coords)
                self.world.add_entity(block)

class BasicVisionPushExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwwwwww",
        "w............pw",
        "wwwwwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionPushExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        push = model.interaction.PrimitiveInteraction("Push", "Succeed")
        push_fail = model.interaction.PrimitiveInteraction("Push", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different from the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _push(world, agent, interaction):
            if world.can_step(agent):
                pos = agent.get_position()
                entities = world.get_entities_at(pos)
                for entity in entities:
                    if isinstance(entity, model.structure.Block):
                        entity.position.add(agent.get_move_delta(1))
                        return push
            return push_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[push.get_name()] = _push

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(push)
        primitives.append(push_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = -1
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[push] = 500
        motivation[push_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world


class BasicVisionCoexsistenceExperiment(experiment.Experiment):
    world_representation = [
        "wwwww",
        "w..pw",
        "w.w.w",
        "w.w.w",
        "wp..w",
        "wwwww"
        ]

    def __init__(self):
        super(BasicVisionCoexsistenceExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        cuddle = model.interaction.PrimitiveInteraction("Cuddle", "Succeed")
        cuddle_fail = model.interaction.PrimitiveInteraction("Cuddle", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _cuddle(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if entity != agent and isinstance(entity, model.agent.Agent):
                    return cuddle
            
            return cuddle_fail

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[cuddle.get_name()] = _cuddle

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(cuddle)
        primitives.append(cuddle_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = 1
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[cuddle] = 50
        motivation[cuddle_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

class BasicVisionCoexsistenceDestroyExperiment(experiment.Experiment):
    world_representation = [
        "wwwwwwwwwwww",
        "wp.........w",
        "wp.........w",
        "wwwwwwwwwwww"
        ]

    def __init__(self):
        super(BasicVisionCoexsistenceDestroyExperiment, self).__init__()

        # Parse world
        self.world = self.parse_world(self.world_representation)

        # Set up primitives
        step = model.interaction.PrimitiveInteraction("Step", "Succeed")
        step_fail = model.interaction.PrimitiveInteraction("Step", "Fail")
        turn_right = model.interaction.PrimitiveInteraction("Turn Right", "Succeed")
        turn_left = model.interaction.PrimitiveInteraction("Turn Left", "Succeed")
        eat = model.interaction.PrimitiveInteraction("Eat", "Succeed")
        eat_fail = model.interaction.PrimitiveInteraction("Eat", "Fail")
        collaborative_destroy = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Succeed")
        collaborative_destroy_fail = model.interaction.PrimitiveInteraction("Collaborative Destroy", "Fail")

        # Define environment logic for primitives, these functions will be
        # registered to the primitive interactions and will be called once
        # the agent attempts to enact the primitive interaction. 
        # The function can manipulate the world and the agents.
        # The return value is the actual enacted interaction (i.e., can be 
        # different form the attempted interaction).
        def _step(world, agent, interaction):
            if world.can_step(agent):
                agent.step()
                return step
            else:
                return step_fail

        def _turn_right(world, agent, interaction):
            agent.add_rotation(-90)
            return turn_right
        
        def _turn_left(world, agent, interaction):
            agent.add_rotation(90)
            return turn_left

        def _eat(world, agent, interaction):
            entities = world.get_entities_at(agent.get_position())
            for entity in entities:
                if isinstance(entity, model.structure.Food):
                    world.remove_entity(entity)
                    return eat
            
            return eat_fail

        def _collaborative_destroy(world, agents_interactions):
            enacted = {}

            for agent_1, interaction_1 in agents_interactions.iteritems():
                if agent_1 in enacted:
                    continue
                else:
                    enacted[agent_1] = collaborative_destroy_fail # Set fail as default, we will now see whether it succeeded

                    entities = world.get_entities_at(agent_1.get_position())
                    for entity in entities:
                        if isinstance(entity, model.structure.Block):
                            # There is a block at agent 1's position, try to find a second agent attempting to destroy the same block:
                            for agent_2, interaction_2 in agents_interactions.iteritems():
                                if agent_1 == agent_2:
                                    continue

                                if agent_2.get_position() == agent_1.get_position():
                                    # The agents are at the same position, so the action fails
                                    continue

                                if entity in world.get_entities_at(agent_2.get_position()):
                                    # Agent 2 is enacting on the same block as agent 1, so the action succeeded
                                    world.remove_entity(entity)
                                    pos = entity.get_position()
                                    pos_2 = (pos.get_x(), pos.get_y() + 1)

                                    food_1 = model.structure.Food()
                                    food_2 = model.structure.Food()
                                    food_1.set_position(pos)
                                    food_2.set_position(pos_2)

                                    self.world.add_entity(food_1)
                                    self.world.add_entity(food_2)
                                        
                                    enacted[agent_1] = collaborative_destroy
                                    enacted[agent_2] = collaborative_destroy
            return enacted

        # Register the previously defined functions.
        enact_logic = {}
        enact_logic[step.get_name()] = _step
        enact_logic[turn_right.get_name()] = _turn_right
        enact_logic[turn_left.get_name()] = _turn_left
        enact_logic[eat.get_name()] = _eat

        self.world.add_complex_enact_logic(_collaborative_destroy, collaborative_destroy.get_name())

        # Set primitives known/enactable by the agents.
        primitives = []
        primitives.append(step)
        primitives.append(step_fail)
        primitives.append(turn_right)
        primitives.append(turn_left)
        primitives.append(eat)
        primitives.append(eat_fail)
        primitives.append(collaborative_destroy)
        primitives.append(collaborative_destroy_fail)

        # Set intrinsic motivation values.
        motivation = {}
        motivation[step] = -1
        motivation[step_fail] = -10
        motivation[turn_right] = -2
        motivation[turn_left] = -2
        motivation[eat] = 20
        motivation[eat_fail] = -2
        motivation[collaborative_destroy] = 50
        motivation[collaborative_destroy_fail] = -1

        for entity in self.world.get_entities():
            if isinstance(entity, model.agent.Agent):
                self.world.add_enact_logic(entity, enact_logic)
                entity.set_primitives(primitives)
                entity.set_motivation(motivation)


    def get_world(self):
        return self.world

    def controller(self, event, coords):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                food = model.structure.Food()
                food.set_position(coords)
                self.world.add_entity(food)
            elif event.key == pygame.K_b:
                block = model.structure.Block()
                block.set_position(coords)
                block.height = 2
                self.world.add_entity(block)