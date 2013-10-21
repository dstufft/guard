import functools


class ContentSecurityPolicy(object):

    DEFAULT_POLICY = {
        "default-src": ["self"],
    }

    def __init__(self, application, policy=None, report_uri=None,
                 report_only=False):
        self.application = application

        # Merge the provided policy with the default policy
        merged_policy = self.DEFAULT_POLICY.copy()
        merged_policy.update(policy if policy is not None else {})

        # Turn into a policy dictionary into a policy string
        directives = [
            [name] + values
            for name, values in merged_policy.items()
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
