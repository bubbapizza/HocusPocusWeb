def logging_tween_factory(handler, registry):

    def tween(request):
        return handler(request)

    return tween
