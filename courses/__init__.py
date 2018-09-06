from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    
    # setup session factory
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    config.set_session_factory(my_session_factory)

    return config.make_wsgi_app()
    
