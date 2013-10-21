Guard
=====

.. image:: https://travis-ci.org/dstufft/guard.png?branch=master
   :target: https://travis-ci.org/dstufft/guard

.. image:: https://coveralls.io/repos/dstufft/guard/badge.png?branch=master
   :target: https://coveralls.io/r/dstufft/guard?branch=master


Guard is a collection of generic WSGI middlewares and utilities for improving
the security of a web application.


Content Security Policy
-----------------------

``guard.ContentSecurityPolicy`` provides a WSGI middleware that can be used
to provide a content security policy for a web application.

Usage
~~~~~

.. code:: python

    import guard, wsgi_app

    # Default Policy
    app = guard.ContentSecurityPolicy(wsgi_app.application)

    # Custom Directives
    app = guard.ContentSecurityPolicy(wsgi_app.application, {"img-src": ["*"]})

    # Report Only
    app = guard.ContentSecurityPolicy(wsgi_app.application, report_only=True)
