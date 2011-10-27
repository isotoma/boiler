# Copyright 2011 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.application.service import MultiService

import yay
from yaybu.boiler.task import Tasks, ParallelTask, TaskType


class Boiler(MultiService):

    """
    Orchestrate multiple deployments
    """

    def __init__(self, config=None):
        MultiService.__init__(self)
        self.config = config

        # Create a tasks queue
        self.tasks = Tasks()
        self.tasks.setServiceParent(self)

    def execute_yay(self, stream):
        """
        Takes a stream containing tasks encoded as Yay and executes them.

        Returns an object implementing ITask for tracking execution of
        the tasks.
        """
        d = yay.load(stream)
        p = ParallelTask(TaskType.create_all(d['tasks']))
        self.tasks.add(p)
        return p


