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

from poppy.manager.base import health


class DefaultHealthController(health.HealthControllerBase):

    def __init__(self, manager):
        super(DefaultHealthController, self).__init__(manager)

    def health(self):
        health_map = {}
        is_alive = True

        storage_name = self._storage.storage_name.lower()
        storage_alive = self._storage.is_alive()
        health_storage = {'storage_name': storage_name,
                          'is_alive': storage_alive}
        health_map['storage'] = health_storage
        if not storage_alive:
            is_alive = False

        health_map['providers'] = []
        for provider_ext in self._providers:
            provider = provider_ext.obj
            provider_name = provider.provider_name.lower()
            provider_alive = provider.is_alive()
            health_provider = {'provider_name': provider_name,
                               'is_alive': provider_alive}
            health_map['providers'].append(health_provider)
            if not provider_alive:
                is_alive = False

        return is_alive, health_map

    def is_provider_alive(self, provider_name):
        """Returns the health of provider."""

        return self._providers[provider_name].obj.is_alive()

    def is_storage_alive(self, storage_name):
        """Returns the health of storage."""

        if storage_name == self._storage.storage_name.lower():
            return self._storage.is_alive()
        else:
            raise KeyError
