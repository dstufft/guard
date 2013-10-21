# Copyright 2013 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import functools


__title__ = "guard"
__version__ = "1.0.1"
__summary__ = "WSGI Middlewares for Web Application Security"
__license__ = "Apache License v2.0"
__uri__ = "https://github.com/dstufft/guard"
__author__ = "Donald Stufft"
__email__ = "donald@stufft.io"


class ContentSecurityPolicy(object):

    DEFAULT_POLICY = {
        "default-src": ["self"],
    }

    def __init__(self, application, policy=None, report_only=False):
        self.application = application

        # Merge the provided policy with the default policy
        merged_policy = self.DEFAULT_POLICY.copy()
        merged_policy.update(policy if policy is not None else {})

        # Turn into a policy dictionary into a policy string
        directives = [
            [name] + values
            for name, values in sorted(list(merged_policy.items()))
        ]
        self.policy = "; ".join(" ".join(d) for d in directives)

        # Should we enforce this policy or should it be read only
        self.report_only = report_only

    def __call__(self, environ, start_response):
        @functools.wraps(start_response)
        def _start_response(status, headers, *args, **kwargs):
            if self.report_only:
                headers.append((
                    "Content-Security-Policy-Report-Only",
                    self.policy,
                ))
            else:
                headers.append(("Content-Security-Policy", self.policy))

            return start_response(status, headers, *args, **kwargs)

        return self.application(environ, _start_response)
