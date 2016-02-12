import os
from pyramid.response import Response


def get_pid_file_contents(path):
    if os.path.exists(path):
        with open(path, 'r') as pid:
            contents = pid.read()
            return contents if contents else ''
    return None


def pid_tween_factory(handler, registry):

    def tween(request):
        pid_path = request.registry.settings.get(
            'door_controller_pid_path',
            None
        )

        if not pid_path:
            return Response('pid path not set in config',
                            content_type='text/plain',
                            status_int=500)

        pid_contents = get_pid_file_contents(pid_path)

        if pid_contents is not None:
            if len(pid_contents) > 0:
                message = pid_contents
                status_int = 500
            else:
                message = 'Door is already unlocked'
                status_int = 200

            return Response(message,
                            content_type='text/plain',
                            status_int=status_int)

        return handler(request)

    return tween
