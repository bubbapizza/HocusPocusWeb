from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from sqlalchemy.orm.exc import NoResultFound


from ..models.user import User


@view_defaults(route_name='index')
class Index:

    def __init__(self, request):
        self.request = request

    @view_config(context=NoResultFound)
    def user_not_found(self):
        return Response('User not found',
                        content_type='text/plain',
                        status_int=403)


    @view_config(renderer='../templates/index.jinja2',
                 attr='get',
                 request_method='GET')
    def get(self):
        return {}

    @view_config(renderer='../templates/unlock.jinja2',
                 attr='post',
                 request_method='POST')
    def post(self):

        ip_address = self.request.client_addr
        query = self.request.dbsession.query(User)
        print(ip_address)
        # will throw NoResultFound which will be handled in an Exception view
        user = query.filter(User.ip_address == ip_address).one()

        print(self.request.POST)
        password = self.request.POST['password']

        if user.check_password(password):
            return {'name': user.name}

        return Response('Password is not correct',
                        content_type='text/plain',
                        status_int=401)
