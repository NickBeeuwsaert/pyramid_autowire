====================
``pyramid_autowire``
====================

``pyramid_autowire`` is a package that allows your pyramid views to use pyramids registry for dependency injection.

.. code-block:: python

    from pyramid_autowire import autowired

    @view_defaults(route_name='test_route', mapper=autowired)
    class Posts:
        def __init__(
            # Standard pyramid (context, request) and (request,) arguments
            # are available through position-only args
            self, request, /,
            # the database and user objects will be injected from the registry
            database: IDatabase, active_user: IUser
        ):
            self.request = request
            self.database = database
            self.active_user = active_user
    
        @view_config()
        def view_post(
            self, *,
            # the matchdict is injected as keyword-only args
            post_id
        ):
            return self.database.query(Post, post_id)
    
    def includeme(config):
        registry = config.registry

        # pretend for the example that the database session is global
        registry.registerUtility(MyDatabase(), IDatabase)

        def get_active_user(request):
            # Fetch active user from the request data
            ...

        registry.registerAdapter(get_active_user, (IRequest, ), IUser)
