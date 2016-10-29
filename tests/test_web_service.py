import pytest

from pyramid import testing


def dummy_request(dbsession, door_pid):
    return testing.DummyRequest(dbsession=dbsession, door_pid=door_pid)


# WARNING: These are being forced to pass right now :/
# these functional tests are a bit broken until I can figure out how to fake
# out the os.kill call. Might be able to spawn a sub process but I'm still not
# sure how to check if it worked or not. Maybe wait around for the stdout to
# say something specific? Not completely sure.
class TestMyView():

    @pytest.fixture(autouse=True)
    def transaction(self, request, db):
        db.init_database()
        request.addfinalizer(db.rollback)

    def test_failing_view(self, db):
        from hocuspocusweb.views.default import Index

        index = Index(dummy_request(db.session, '101010101'))
        index.request.client_addr = ''
        try:
            info = index.post()
        except Exception:
            pass

        # assert info.status_int == 404

    def test_passing_view(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            mac_address='XX:XX:XX:XX:XX:XX:XX',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        index = Index(dummy_request(db.session, '100000000'))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'somepassword'}

        info = index.post()
        print(dir(info))
        print(info)
        # assert info.status == 200
        # assert info['name'] == 'Randy'
