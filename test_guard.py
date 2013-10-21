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
import pretend

from guard import ContentSecurityPolicy


class TestContentSecurityPolicy:

    def test_instance_creation(self):
        app = pretend.stub()
        assert ContentSecurityPolicy(app).application is app

    def test_default_policy(self):
        app = lambda e, s: s(200, [])
        csp = ContentSecurityPolicy(app)

        resp = pretend.stub()

        environ = {}
        start_response = pretend.call_recorder(lambda status, headers: resp)

        assert csp(environ, start_response) is resp
        assert start_response.calls == [
            pretend.call(
                200,
                [("Content-Security-Policy", "default-src self")],
            ),
        ]

    def test_default_report_only(self):
        app = lambda e, s: s(200, [])
        csp = ContentSecurityPolicy(app, report_only=True)

        resp = pretend.stub()

        environ = {}
        start_response = pretend.call_recorder(lambda status, headers: resp)

        assert csp(environ, start_response) is resp
        assert start_response.calls == [
            pretend.call(
                200,
                [("Content-Security-Policy-Report-Only", "default-src self")],
            ),
        ]

    def test_configured_policy(self):
        app = lambda e, s: s(200, [])
        csp = ContentSecurityPolicy(app, {"img-src": ["*"]})

        resp = pretend.stub()

        environ = {}
        start_response = pretend.call_recorder(lambda status, headers: resp)

        assert csp(environ, start_response) is resp
        assert start_response.calls == [
            pretend.call(
                200,
                [("Content-Security-Policy", "default-src self; img-src *")],
            ),
        ]
