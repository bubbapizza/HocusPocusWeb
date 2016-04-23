from pyramid.response import Response
from ..util.file_helpers import get_file_contents


def error_file_tween_factory(handler, registry):

    def tween(request):
        error_path = request.registry.settings.get(
            'door_controller_error_path',
            None
        )

        if not error_path:
            return Response('Error path not set in config',
                            content_type='text/plain',
                            status_int=500)

        error_file_contents = get_file_contents(error_path)

        if error_file_contents is not None:

            return Response(error_file_contents,
                            content_type='text/plain',
                            status_int=500)

        return handler(request)

    return tween
