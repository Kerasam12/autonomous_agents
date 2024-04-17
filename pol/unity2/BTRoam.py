import asyncio
import random
import time
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import statistics


class BN_DoNothing(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing BN_DoNothing")
        super(BN_DoNothing, self).__init__("BN_DoNothing")

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.DoNothing(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                print("BN_DoNothing completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_DoNothing completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.my_goal.cancel()


class BN_ForwardRandom(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_ForwardRandom")
        super(BN_ForwardRandom, self).__init__("BN_ForwardRandom")
        self.logger.debug("Initializing BN_ForwardRandom")
        self.my_agent = aagent

    def initialise(self):
        self.logger.debug("Create Goals_BT.ForwardDist task")
        self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, 1, 5).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_ForwardRandom completed with SUCCESS")
                print("BN_ForwardRandom completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_ForwardRandom completed with FAILURE")
                print("BN_ForwardRandom completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_ForwardRandom")
        self.my_goal.cancel()


class BN_TurnRandom(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_TurnRandom")
        super(BN_TurnRandom, self).__init__("BN_TurnRandom")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_Turn completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_Turn completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_TurnRandom")
        self.my_goal.cancel()


class BN_DetectFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectFlower")
        super(BN_DetectFlower, self).__init__("BN_DetectFlower")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Flower":  # If it is a flower
                    # print("Flower detected!")
                    print("BN_DetectFlower completed with SUCCESS")
                    return pt.common.Status.SUCCESS
        # print("No flower...")
        # print("BN_DetectFlower completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


class BN_EatFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_EatFlower")
        super(BN_EatFlower, self).__init__("BN_EatFlower")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.EatFlower(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_EatFlower completed with SUCCESS")
                # self.my_agent.i_state.update_hunger(False)
                # self.my_agent.i_state.update_lunch_time(time.time())
                return pt.common.Status.SUCCESS
            else:
                print("BN_EatFlower completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_EatFlower")
        self.my_goal.cancel()


class BN_CheckIfHungry(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_CheckIfHungry")
        super(BN_CheckIfHungry, self).__init__("BN_CheckIfHungry")
        self.my_agent = aagent
        self.previous_hungry_state = None

    def initialise(self):
        pass

    def update(self):
        current_hungry_state = self.my_agent.i_state.hungry

        if self.my_agent.i_state.hungry:
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with SUCCESS")
                self.previous_hungry_state = current_hungry_state
            return pt.common.Status.SUCCESS
        elif time.time() - self.my_agent.i_state.last_lunch_time() >= 15:
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with SUCCESS")
                self.previous_hungry_state = current_hungry_state
            self.my_agent.i_state.update_hunger(True)
            return pt.common.Status.SUCCESS
        else:
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with FAILURE")
                self.previous_hungry_state = current_hungry_state
            return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


class BN_DetectCollision(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectCollision")
        super(BN_DetectCollision, self).__init__("BN_DetectCollision")
        self.my_agent = aagent
        self.previous_obstacle_state = None

    def initialise(self):
        pass

    def update(self):
        current_obstacle_state = self.my_agent.i_state.get_obstacle_location()

        self.sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        
        left_threshold = list(range(9))
        right_threshold = list(range(15, 22))
        only_flowers_range = left_threshold + right_threshold

        degrees_negative = list(range(-10, -91, -180 // 21))
        degrees_positive = list(range(10, 91, 180 // 21))
        degrees_positive.reverse()  # Reversing positive part to have smaller numbers on the edges
        degrees = degrees_negative + [-90] + degrees_positive

        detection_indexes = [i for i, obj in enumerate(self.sensor_obj_info) if obj is not None]
        detection_indexes = [i for i in detection_indexes if self.sensor_obj_info[i]['tag'] != "Astronaut"]

        if detection_indexes:
            obstacle_index = int(statistics.median(detection_indexes))
            if obstacle_index not in only_flowers_range:
                if current_obstacle_state != self.previous_obstacle_state:
                    print("BN_DetectCollision completed with SUCCESS")
                    self.previous_obstacle_state = current_obstacle_state
                self.my_agent.i_state.locate_obstacle(degrees[obstacle_index])
                # print("BN_DetectCollision completed with SUCCESS")
                return pt.common.Status.SUCCESS
            
        if current_obstacle_state != self.previous_obstacle_state:
            print("BN_DetectCollision completed with FAILURE")
            self.previous_obstacle_state = current_obstacle_state
        # print("BN_DetectCollision completed with FAILURE")
        return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


class BN_AvoidCollision(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_AvoidCollision")
        super(BN_AvoidCollision, self).__init__("BN_AvoidCollision")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.AvoidCollision(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_AvoidCollision completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_AvoidCollision completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_AvoidCollision")
        self.my_goal.cancel()


class BN_DetectAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectAstronaut")
        super(BN_DetectAstronaut, self).__init__("BN_DetectAstronaut")
        self.my_agent = aagent
        self.previous_astronaut_state = None

    def initialise(self):
        pass

    def update(self):
        current_astronaut_state = self.my_agent.i_state.get_astronaut_location()

        self.sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        
        left_threshold = list(range(9))
        right_threshold = list(range(15, 22))
        only_flowers_range = left_threshold + right_threshold

        degrees = list(range(-90, 90, 180 // 21))

        detection_indexes = [i for i, obj in enumerate(self.sensor_obj_info) if obj is not None]
        detection_indexes = [i for i in detection_indexes if self.sensor_obj_info[i]['tag'] == "Astronaut"]

        if detection_indexes:
            astronaut_index = int(statistics.median(detection_indexes))
            if current_astronaut_state != self.previous_astronaut_state:
                print("BN_DetectAstronaut completed with SUCCESS")
                self.previous_astronaut_state = current_astronaut_state
            self.my_agent.i_state.locate_astronaut(degrees[astronaut_index])
            # print("BN_DetectCollision completed with SUCCESS")
            return pt.common.Status.SUCCESS
            
        if current_astronaut_state != self.previous_astronaut_state:
            print("BN_DetectAstronaut completed with FAILURE")
            self.previous_astronaut_state = current_astronaut_state
        # print("BN_DetectCollision completed with FAILURE")
        self.my_agent.i_state.locate_astronaut(None)
        return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


class BN_TurnAlongAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_TurnAlongAstronaut")
        super(BN_TurnAlongAstronaut, self).__init__("BN_TurnAlongAstronaut")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.TurnAlongAstronaut(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_TurnAlongAstronaut completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_TurnAlongAstronaut completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_TurnAlongAstronaut")
        self.my_goal.cancel()


class BN_WalkTowardsAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_WalkTowardsAstronaut")
        super(BN_WalkTowardsAstronaut, self).__init__("BN_WalkTowardsAstronaut")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.BN_WalkTowardsAstronaut(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_WalkTowardsAstronaut completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_WalkTowardsAstronaut completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_WalkTowardsAstronaut")
        self.my_goal.cancel()


class BTRoam:
    def __init__(self, aagent):
        # py_trees.logging.level = py_trees.logging.Level.DEBUG

        self.aagent = aagent

        detection = pt.composites.Sequence(name="DetectFlower", memory=True)
        detection.add_children([BN_CheckIfHungry(aagent), BN_DetectFlower(aagent), BN_EatFlower(aagent)])

        avoid_obstacle = pt.composites.Sequence(name="AvoidObstacle", memory=True)
        avoid_obstacle.add_children([BN_DetectCollision(aagent), BN_AvoidCollision(aagent)])
        
        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        intelligent_roaming = pt.composites.Selector(name="IntelligentRoaming", memory=False)
        intelligent_roaming.add_children([avoid_obstacle, roaming])

        track_astronaut = pt.composites.Parallel(name="TrackAstronaut", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        track_astronaut.add_children([BN_WalkTowardsAstronaut(aagent), BN_TurnAlongAstronaut(aagent)])

        stalk_astronaut = pt.composites.Sequence(name="FollowAstronaut", memory=True)
        stalk_astronaut.add_children([BN_DetectAstronaut(aagent), track_astronaut])

        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([detection, stalk_astronaut, intelligent_roaming])

        self.behaviour_tree = pt.trees.BehaviourTree(self.root)

    # Function to set invalid state for a node and its children recursively
    def set_invalid_state(self, node):
        node.status = pt.common.Status.INVALID
        for child in node.children:
            self.set_invalid_state(child)

    def stop_behaviour_tree(self):
        # Setting all the nodes to invalid, we force the associated asyncio tasks to be cancelled
        self.set_invalid_state(self.root)

    async def tick(self):
        self.behaviour_tree.tick()
        await asyncio.sleep(0)
