# Copyright (c) 2014 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Default manager driver implementation."""

import mock

from poppy.common import decorators
from poppy.manager import base
from poppy.manager.delegate import controllers
from poppy.manager.delegate import manager_daemon


class DelegateManagerDriver(base.Driver):

    def __init__(self, conf, storage, providers, dns):
        super(DelegateManagerDriver, self).__init__(
            conf, storage, providers, dns)
        self._queue = mock.Mock()

    @property
    def queue(self):
        return self._queue

    @decorators.lazy_property(write=False)
    def services_controller(self):
        return controllers.Services(self)

    @decorators.lazy_property(write=False)
    def home_controller(self):
        return controllers.Home(self)

    @decorators.lazy_property(write=False)
    def flavors_controller(self):
        return controllers.Flavors(self)

    @decorators.lazy_property(write=False)
    def health_controller(self):
        return controllers.Health(self)

    def run_delegate_daemon(self):
        manager_daemon.manager_daemon(self)
