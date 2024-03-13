'''
Created on Mar 5, 2024

@author: Dave
'''

from time import sleep
from py_trees.composites import Selector
from py_trees.behaviour import Behaviour
from py_trees.composites import Sequence
from py_trees.common import Status
from py_trees import logging as log_tree
from py_trees.display import render_dot_tree



    

class AlwaysSuccess(Behaviour):
    def __init__(self, name):
        super(AlwaysSuccess, self).__init__(name)
        """ The constructor of this class """

        
    def setup(self):
        self.logger.debug(f"AlwaysSuccess::setup {self.name}")
        """ This mehod Allows you to do some more initialization later, which cannot yet be done yet at the time of construction 
            (e.g. after the node has been added to the tree). 
            If you want to use this method you need to write the code that calls it yourself.
            However, you can probably ignore this method.
        """
        
    def initialise(self):
        self.logger.debug(f"AlwaysSuccess::initialise {self.name}")
        """
            This method is called whenever a new execution of the action corresponding to this node must be started.
            That is, it is called when the node is ticked and:
                - This node has not been ticked before, or
                - After the previous tick, this node returned SUCCES or FAILURE
            So, if this node is ticked, and on the previous tick it returned RUNNING, then this method will *not* be called.
        """

    def update(self):
        self.logger.debug(f"AlwaysSuccess::update {self.name}")
        """
            This method is called every time the node is ticked.
            It must return SUCCESS, FAILURE, or RUNNING.
        """
        return Status.SUCCESS
    
    def terminate(self, new_status:Status):
        self.logger.debug(f"AlwaysSuccess::terminate {self.name}. Terminated with status {new_status}")
        """
            This method is called whenever the action corresponding to this node has finished its execution.
            That is, if the update() method has returned either SUCCESS or FAILURE.
        """
        
        



    