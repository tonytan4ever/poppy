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

import abc

import six

from poppy.provider.base import controller
from poppy.provider.base import responder


@six.add_metaclass(abc.ABCMeta)
class ServicesControllerBase(controller.ProviderControllerBase):

    def __init__(self, driver):
        super(ServicesControllerBase, self).__init__(driver)

        self.responder = responder.Responder(driver.provider_name)

    @abc.abstractmethod
    def update(self, provider_service_id, service_json):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, service_name, service_json):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, provider_service_id):
        raise NotImplementedError

    @abc.abstractmethod
    def purge(self, provider_service_id, purge_urls=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, service_name):
        """Get details of the service, as stored by the provider."""
        raise NotImplementedError

    def _map_service_name(self, service_name):
        """Map poppy service name to provider's specific service name.

         Map a poppy service name to a provider's service name so it
         can comply provider's naming convention.
        """
        return service_name

    @abc.abstractmethod
    def current_customer(self):
        """Return the current customer for a provider.

        This will needed call each provider's customer API,
        useful for certain providers ( e.g fastly) and manage
        master-sub account
        """
        raise NotImplementedError
