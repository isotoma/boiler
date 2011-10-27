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

from zope.interface import Interface

class ITask(Interface):

    """
    Actions performed by Yaybu Server are modelled as a Task. The act of
    deploying with Yaybu is decoupled from the Task management code to
    allow other tasks to be orchestrated by Yaybu.
    """

    def whenDone():
        """
        Returns a deferred that is fired when a task is completed, or when a
        task has failed
        """

    def start():
        """
        Actually execute a task. This only starts a task.
        """

    def stop():
        """
        Stop this task safely
        """

    def abort():
        """
        Stop this task immediately and aggressively
        """

