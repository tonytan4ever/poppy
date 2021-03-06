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

import json
import logging

from pecan import hooks
import webob

from poppy.openstack.common import log as oslo_log

LOG = oslo_log.getLogger(__name__)


class ErrorHook(hooks.PecanHook):

    '''Intercepts all errors during request fulfillment and logs them.'''

    def on_error(self, state, exception):
        '''Fires off when an error happens during a request.

        :param state: The Pecan state for the current request.
        :type state: pecan.core.state
        :param exception: The exception that was raised.
        :type exception: Exception
        :returns: webob.Response -- JSON response with the error
            message.
        '''
        exception_payload = {
            'status': 500,
        }
        message = {
            'message': (
                'The server encountered an unexpected condition'
                ' which prevented it from fulfilling the request.'
            )
        }
        log_level = logging.ERROR

        # poppy does not have internal exception/eternal exceptions
        # yet, so just catch the HTTPException from pecan.abort
        # and send out a a json body
        message['message'] = str(exception)
        exception_payload['status'] = exception.status

        LOG.log(
            log_level,
            'Exception message: %s' % str(exception),
            exc_info=True,
            extra=exception_payload
        )

        return webob.Response(
            json.dumps(message),
            status=exception_payload['status'],
            content_type='application/json'
        )
