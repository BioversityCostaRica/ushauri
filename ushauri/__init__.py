import sys

if sys.version_info[0] == 3 and sys.version_info[1] >= 6:
    import gevent.monkey

    gevent.monkey.patch_all()

from ushauri.config.environment import load_environment
from pyramid.config import Configurator
import os

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""

    authn_policy = AuthTktAuthenticationPolicy(
        settings["auth.secret"],
        cookie_name="ushauri_" + settings["country"] + "_auth_tkt",
    )

    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
    )

    apppath = os.path.dirname(os.path.abspath(__file__))

    config.include(".models")
    # Load and configure the host application
    load_environment(settings, config, apppath)
    return config.make_wsgi_app()
