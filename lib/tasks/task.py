"""
The task class.
"""


class Task:
    """
    Base class for all built-in Tasks.
    """
    
    def set_task_type(self, taskType):
        """
        sets the type of this task.
        
        Be aware! this method can only get called once!
        
        :param taskType: the type of this task
        """
        if hasattr(self, "_taskType"):
            raise Exception("taskType is only allowed to set once!")
        self.taskType = taskType  
    
    def get_task_type(self):
        """
        :return: the type set by set_type_task
        """
        return self._taskType
    
    def execute_task(self, msg):
        """
        this is the method tasks usually override. 
        It gets called anytime the task should get executed
        
        default does nothing
        
        :param msg: the msg for this task
        """
        pass
    
    def _execute(self, taskType, msg):
        """
        internal method which gets called for any member in a hostgroup.
        It determines if it has an appropriate type by comparing taskType with get_task_type().
        Calls execute_task() if the type matches
        
        :param taskType: the type of the fail which is compared with get_task_type()
        :param msg: the error message
            
        :return: True if execute_task() is called succesfully, else False
        """
        if self.get_task_type() == taskType:
            self.execute_task(msg)
            return True
        return False