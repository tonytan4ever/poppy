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

try:
    import ordereddict as collections
except ImportError:
    import collections

from poppy.transport.pecan.models.response import link


class StorageModel(collections.OrderedDict):
    def __init__(self, is_alive):
        super(StorageModel, self).__init__()

        if is_alive:
            self['online'] = 'true'
        else:
            self['online'] = 'false'


class ProviderModel(collections.OrderedDict):
    def __init__(self, is_alive):
        super(ProviderModel, self).__init__()

        if is_alive:
            self['online'] = 'true'
        else:
            self['online'] = 'false'


class HealthModel(collections.OrderedDict):

    def __init__(self, request, health_map):
        super(HealthModel, self).__init__()

        health_storage = collections.OrderedDict()
        if health_map['storage']['is_alive']:
            health_storage['online'] = 'true'
        else:
            health_storage['online'] = 'false'

        health_storage['links'] = link.Model(
            u'{0}/v1.0/health/storage/{1}'.format(
                request.host_url, health_map['storage']['storage_name']),
            'self')

        self['storage'] = {
            health_map['storage']['storage_name']: health_storage}

        self['providers'] = {}
        for provider in health_map['providers']:
            health_provider = collections.OrderedDict()
            if provider['is_alive']:
                health_provider['online'] = 'true'
            else:
                health_provider['online'] = 'false'

            health_provider['links'] = link.Model(
                u'{0}/v1.0/health/provider/{1}'.format(
                    request.host_url, provider['provider_name']),
                'self')

            self['providers'][provider['provider_name']] = health_provider
