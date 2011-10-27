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

from twisted.application.internet import TimerService
from yaybu.boiler.service import BaseService

class TimedDeployment(BaseService):
    """
    Queues a deployment every 5 minutes, but only when the previous one has finished.
    """

    def __init__(self, step=5*60):
        BoilerService.__init__(self)
        TimerService(step, self.fire).setServiceParent(self)

    def fire(self):
        """ I am called every 5 minutes by TimerService and run some Yay """

        t = self.parent.execute_yay("""
            host: localhost
            port: 22
            config:
                resources:
                  - File:
                      name: /tmp/foo
            """)

        return t.whenDone()

