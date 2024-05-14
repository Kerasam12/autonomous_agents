import asyncio
import random
import time
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import statistics
from py_trees.display import render_dot_tree


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
                    location = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.ANGLE][index]                    
                    self.my_agent.i_state.update_flower_distance(value["distance"])
                    self.my_agent.i_state.update_flower_location(location)
                    print("BN_DetectFlower completed with SUCCESS")
                    return pt.common.Status.SUCCESS
        # print("No flower...")
        # print("BN_DetectFlower completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


class BN_FaceFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_FaceFlower")
        super(BN_FaceFlower, self).__init__("BN_FaceFlower")
        self.logger.debug("Initializing BN_FaceFlower")
        self.my_agent = aagent

    def initialise(self):
        self.logger.debug("Create Goals_BT.ForwardDist task")
        self.my_goal = asyncio.create_task(Goals_BT.TurnToFlower(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_FaceFlower completed with SUCCESS")
                print("BN_FaceFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_FaceFlower completed with FAILURE")
                print("BN_FaceFlower completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_FaceFlower")
        self.my_goal.cancel()


class BN_MoveToFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_MoveToFlower")
        super(BN_MoveToFlower, self).__init__("BN_MoveToFlower")
        self.logger.debug("Initializing BN_MoveToFlower")
        self.my_agent = aagent

    def initialise(self):
        self.logger.debug("Create Goals_BT.ForwardDist task")
        self.my_goal = asyncio.create_task(Goals_BT.MoveToFlower(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_MoveToFlower completed with SUCCESS")
                print("BN_MoveToFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_MoveToFlower completed with FAILURE")
                print("BN_MoveToFlower completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_MoveToFlower")
        self.my_goal.cancel()


# This node triggers the EatFlower goal.
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
                return pt.common.Status.SUCCESS
            else:
                print("BN_EatFlower completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_EatFlower")
        self.my_goal.cancel()


# This node handles the Hungry Flag.
class BN_CheckIfHungry(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_CheckIfHungry")
        super(BN_CheckIfHungry, self).__init__("BN_CheckIfHungry")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_hungry_state = None

    def initialise(self):
        pass

    def update(self):
        current_hungry_state = self.my_agent.i_state.hungry

        if self.my_agent.i_state.hungry:
            # Only print the output if the state has changed.
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with SUCCESS")
                self.previous_hungry_state = current_hungry_state
            return pt.common.Status.SUCCESS

            # If 15 seconds have past, update hunger flag.
        elif time.time() - self.my_agent.i_state.last_lunch_time() >= 15:
            # Only print the output if the state has changed.
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with SUCCESS")
                self.previous_hungry_state = current_hungry_state
            self.my_agent.i_state.update_hunger(True)
            return pt.common.Status.SUCCESS
        
        else: # If agent is not hungry    
            # Only print the output if the state has changed.
            if current_hungry_state != self.previous_hungry_state:
                print("BN_CheckIfHungry completed with FAILURE")
                self.previous_hungry_state = current_hungry_state
            return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass


# This node detects obstacles in the Agent's sight.
class BN_DetectCollision(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectCollision")
        super(BN_DetectCollision, self).__init__("BN_DetectCollision")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_obstacle_state = None

    def initialise(self):
        pass

    def update(self):
        # Get in which direction the obstacle was found
        current_obstacle_state = self.my_agent.i_state.get_obstacle_location()

        # Obtain all information that my sensors detect.
        self.sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        
        # Store the range that the agent only uses for flower and astronaut detection
        # left_threshold = list(range(9))
        # right_threshold = list(range(15, 22))
        # only_flowers_range = left_threshold + right_threshold

        # Create a list of degrees [-10, -20, ..., 90, ..., 20, 10]
        # This is the degrees the agent will turn. The more in the middle the
        # obstacle is, the more the agent will have to turn
        degrees_negative = list(range(-10, -91, -180 // len(self.sensor_obj_info)))
        degrees_positive = list(range(10, 91, 180 // len(self.sensor_obj_info)))
        degrees_positive.reverse()  # Reversing positive part to have smaller numbers on the edges
        degrees = degrees_negative + [-90] + degrees_positive

        # If my agent is hungry, dont avoid Flowers
        if self.my_agent.i_state.is_hungry():
            do_not_avoid = ["Astronaut", "CritterMantaRay", "Flower"]
        else:
            do_not_avoid = ["Astronaut", "CritterMantaRay"]

        # Store indexes of sensor where I detect obstacles
        detection_indexes = [i for i, obj in enumerate(self.sensor_obj_info) if obj is not None]
        detection_indexes = [i for i in detection_indexes if self.sensor_obj_info[i]['tag'] not in do_not_avoid]

        # If i have detected something
        if detection_indexes:
            # Take as location the median of all detections
            obstacle_index = int(statistics.median(detection_indexes))
            # if obstacle_index not in only_flowers_range:
                # Only print the output if the state has changed.
            if current_obstacle_state != self.previous_obstacle_state:
                print("BN_DetectCollision completed with SUCCESS")
                self.previous_obstacle_state = current_obstacle_state

            # Store the direction where I found my obstacle.
            self.my_agent.i_state.locate_obstacle(degrees[obstacle_index])
            return pt.common.Status.SUCCESS
            
        # Only print the output if the state has changed.  
        if current_obstacle_state != self.previous_obstacle_state:
            print("BN_DetectCollision completed with FAILURE")
            self.previous_obstacle_state = current_obstacle_state

        return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


# This node avoids collisions with obstacles in the path.
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


# This node detects the astronaut if it appears in front of the agent.
class BN_DetectAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectAstronaut")
        super(BN_DetectAstronaut, self).__init__("BN_DetectAstronaut")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_astronaut_state = None

    def initialise(self):
        pass

    def update(self):
        # Only print the output if the state has changed.
        current_astronaut_state = bool(self.my_agent.i_state.get_astronaut_location())

        # Store sensor's information
        self.sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]

        # Store the degrees of each sensor location.
        degrees = list(range(-90, 90, 180 // len(self.sensor_obj_info)))

        # Store the indexes where I found an astronaut.
        detection_indexes = [i for i, obj in enumerate(self.sensor_obj_info) if obj is not None]
        detection_indexes = [i for i in detection_indexes if self.sensor_obj_info[i]['tag'] == "Astronaut"]

        if detection_indexes:
            # Take the degree most aligned with the astronaut.
            astronaut_index = int(statistics.median(detection_indexes))

            # Only print the output if the state has changed.
            if current_astronaut_state != self.previous_astronaut_state:
                print("BN_DetectAstronaut completed with SUCCESS")
                self.previous_astronaut_state = current_astronaut_state

            # Store where has the agent seen the astronaut.
            self.my_agent.i_state.locate_astronaut(degrees[astronaut_index])
            # Store the distance in which the astronaut is w.r.t the agent.
            self.my_agent.i_state.update_astronaut_distance(self.sensor_obj_info[astronaut_index]['distance'])
            self.my_agent.i_state.update_last_astronaut_direction(degrees[astronaut_index])
            return pt.common.Status.SUCCESS
        
        # Only print the output if the state has changed.
        if current_astronaut_state != self.previous_astronaut_state:
            print("BN_DetectAstronaut completed with FAILURE")
            self.previous_astronaut_state = current_astronaut_state
        
        # Store in agents internal state that there is not an astronaut in sight.
        self.my_agent.i_state.locate_astronaut(None)
        return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


# This node makes that the agent is always facing the astronaut.
class BN_TurnAlongAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_TurnAlongAstronaut")
        super(BN_TurnAlongAstronaut, self).__init__("BN_TurnAlongAstronaut")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_astronaut_state = None

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.TurnAlongAstronaut(self.my_agent).run())

    def update(self):
        # Variable that will be used for a cleaner debugging.
        current_astronaut_state = True

        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        
        else:
            res = self.my_goal.result()

            if res:
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_WalkTowardsAstronaut completed with SUCCESS")
                    self.previous_astronaut_state = res
                return pt.common.Status.SUCCESS
            
            else:
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_WalkTowardsAstronaut completed with FAILURE")
                    self.previous_astronaut_state = res

                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_TurnAlongAstronaut")
        self.my_goal.cancel()


# This node makes that the agent is always behind the astronaut.
class BN_WalkTowardsAstronaut(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_WalkTowardsAstronaut")
        super(BN_WalkTowardsAstronaut, self).__init__("BN_WalkTowardsAstronaut")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.                
        self.previous_astronaut_state = None

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.WalkTowardsAstronaut(self.my_agent).run())

    def update(self):
        # Variable that will be used for a cleaner debugging.                
        current_astronaut_state = True

        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            
            if res:
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_WalkTowardsAstronaut completed with SUCCESS")
                    self.previous_astronaut_state = res
                return pt.common.Status.SUCCESS
            
            else:
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_WalkTowardsAstronaut completed with FAILURE")
                    self.previous_astronaut_state = res
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_WalkTowardsAstronaut")
        self.my_goal.cancel()


"""
# When it losses contact with astronaut, it moves forward for 4 seconds.
class BN_MoveToAstronautTrail(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_MoveToAstronautTrail")
        super(BN_MoveToAstronautTrail, self).__init__("BN_MoveToAstronautTrail")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_astronaut_state = None

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.MoveToAstronautTrail(self.my_agent).run())

    def update(self):
        # Variable that will be used for a cleaner debugging.
        current_astronaut_state = True

        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()

            if res:        
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_MoveToAstronautTrail completed with SUCCESS")
                    self.previous_astronaut_state = res
                return pt.common.Status.SUCCESS
            
            else:
                # Only print the output if the state has changed.
                if current_astronaut_state != self.previous_astronaut_state:
                    print("BN_MoveToAstronautTrail completed with FAILURE")
                    self.previous_astronaut_state = res
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_MoveToAstronautTrail")
        self.my_goal.cancel()


# WHen it losses contact with astronaut, it turns to the direction 
# where the agent was last seen
class BN_DeduceAstronautTrail(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DeduceAstronautTrail")
        super(BN_DeduceAstronautTrail, self).__init__("BN_DeduceAstronautTrail")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_astronaut_state = None

    def initialise(self):
        pass

    def update(self):
        # Variable that will be used for a cleaner debugging.
        current_astronaut_state = bool(self.my_agent.i_state.get_astronaut_location())

        astronaut_trail = self.my_agent.i_state.get_last_astronaut_direction()
        if astronaut_trail[0] is not None:
            if astronaut_trail[0] > astronaut_trail[1]:
                self.my_agent.i_state.set_last_astronaut_direction("tl")
            elif astronaut_trail[0] < astronaut_trail[1]:
                self.my_agent.i_state.set_last_astronaut_direction("tr")
            else:
                self.my_agent.i_state.set_last_astronaut_direction("nt")

            print("BN_DeduceAstronautTrail completed with SUCCESS")
            return pt.common.Status.SUCCESS
        else:
            print("BN_DeduceAstronautTrail completed with FAILURE")
            return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


class BN_FaceAstronautTrail(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_FaceAstronautTrail")
        super(BN_FaceAstronautTrail, self).__init__("BN_FaceAstronautTrail")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.FollowAstronautTrail(self.my_agent).run())

    def update(self):

        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()

            if res:        
                print("BN_FaceAstronautTrail completed with SUCCESS")
                return pt.common.Status.SUCCESS
            
            else:
                # Only print the output if the state has changed.
                print("BN_FaceAstronautTrail completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_FaceAstronautTrail")
        self.my_goal.cancel()
"""


# This node detects other critters in the path.
class BN_DetectCritter(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectCritter")
        super(BN_DetectCritter, self).__init__("BN_DetectCritter")
        self.my_agent = aagent

        # Variable that will be used for a cleaner debugging.
        self.previous_critter_state = None

    def initialise(self):
        pass

    def update(self):
        # Variable that will be used for a cleaner debugging.
        current_critter_state = self.my_agent.i_state.get_critter_location()

        # Store all information from sensors
        self.sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]

        # Store the degrees of each sensor
        degrees = list(range(-90, 90, 180 // len(self.sensor_obj_info)))

        # Store the indexes in which a critter has been detected.
        detection_indexes = [i for i, obj in enumerate(self.sensor_obj_info) if obj is not None]
        detection_indexes = [i for i in detection_indexes if self.sensor_obj_info[i]['tag'] == "CritterMantaRay"]

        if detection_indexes:
            critter_index = int(statistics.median(detection_indexes))

            # Only print the output if the state has changed.
            if current_critter_state != self.previous_critter_state:
                print("BN_DetectCritter completed with SUCCESS")
                self.previous_critter_state = current_critter_state

            self.my_agent.i_state.locate_critter(degrees[critter_index])
            return pt.common.Status.SUCCESS
            
        # Only print the output if the state has changed.
        if current_critter_state != self.previous_critter_state:
            print("BN_DetectCritter completed with FAILURE")
            self.previous_critter_state = current_critter_state

        self.my_agent.i_state.locate_critter(None)
        return pt.common.Status.FAILURE                

    def terminate(self, new_status: common.Status):
        pass


# This node triggers the escape of another critter.
class BN_RunAwayFromCritter(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_RunAwayFromCritter")
        super(BN_RunAwayFromCritter, self).__init__("BN_RunAwayFromCritter")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.RunAwayFromCritter(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_RunAwayFromCritter completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_RunAwayFromCritter completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_RunAwayFromCritter")
        self.my_goal.cancel()


# This node makes the agent turn against the critter
class BN_TurnAwayFromCritter(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_TurnAwayFromCritter")
        super(BN_TurnAwayFromCritter, self).__init__("BN_TurnAwayFromCritter")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.TurnAwayFromCritter(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_TurnAwayFromCritter completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_TurnAwayFromCritter completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_TurnAwayFromCritter")
        self.my_goal.cancel()
    

# This class creates the final behavior tree.
class BTRoam:
    def __init__(self, aagent):
        # py_trees.logging.level = py_trees.logging.Level.DEBUG

        self.aagent = aagent

        approach_flower = pt.composites.Parallel(name="ApproachFlower", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        approach_flower.add_children([BN_FaceFlower(aagent), BN_MoveToFlower(aagent)])

        # Detect and eat flower behavior
        flower_detection = pt.composites.Sequence(name="DetectFlower", memory=True)
        flower_detection.add_children([BN_CheckIfHungry(aagent), BN_DetectFlower(aagent), 
                                       approach_flower, BN_EatFlower(aagent)])

        # Roam without colliding with obstacles
        avoid_obstacle = pt.composites.Sequence(name="AvoidObstacle", memory=True)
        avoid_obstacle.add_children([BN_DetectCollision(aagent), BN_AvoidCollision(aagent)])
        
        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        # Detect the astronaut and follow him
        move_behind_astronaut = pt.composites.Parallel(name="TrackAstronaut", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        move_behind_astronaut.add_children([BN_WalkTowardsAstronaut(aagent), BN_TurnAlongAstronaut(aagent)])

        detect_and_follow_astronaut = pt.composites.Sequence(name="FollowAstronaut", memory=True)
        detect_and_follow_astronaut.add_children([BN_DetectAstronaut(aagent), move_behind_astronaut])

        # follow_astronaut_trails = pt.composites.Parallel(name="SearchAstronautBack", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        # follow_astronaut_trails.add_children([BN_FaceAstronautTrail(aagent), BN_MoveToAstronautTrail(aagent)])

        # look_for_lost_astronaut = pt.composites.Sequence(name="SearchAstronaut", memory=True)
        # look_for_lost_astronaut.add_children([BN_DeduceAstronautTrail(aagent), follow_astronaut_trails])
        
        # astronaut_follower_behavior = pt.composites.Selector(name="AstronautFollower", memory=False)
        # astronaut_follower_behavior.add_children([detect_and_follow_astronaut, look_for_lost_astronaut]) # BN_LookForAstronaut(aagent)])


        #Detect other critters and avoid them
        move_away_from_critter = pt.composites.Parallel(name="RunAwayFromCritter", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        move_away_from_critter.add_children([BN_TurnAwayFromCritter(aagent), BN_RunAwayFromCritter(aagent)])

        detect_and_escape_critter = pt.composites.Sequence("AvoidCritter", memory=True)
        detect_and_escape_critter.add_children([BN_DetectCritter(aagent), move_away_from_critter])


        # ROOT: Main tree
        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([avoid_obstacle, flower_detection, detect_and_escape_critter, detect_and_follow_astronaut, roaming])

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