import pytest
import transaction

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class DataBase():

    def __init__(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('hocuspocusweb.models.meta')
        settings = self.config.get_settings()

        from hocuspocusweb.models.meta import (
            get_session,
            get_engine,
            get_dbmaker,
            )

        self.engine = get_engine(settings)
        dbmaker = get_dbmaker(self.engine)

        self.session = get_session(transaction.manager, dbmaker)

    def init_database(self):
        from hocuspocusweb.models.meta import Base
        Base.metadata.create_all(self.engine)

    def rollback(self):
        from hocuspocusweb.models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.create_all(self.engine)


@pytest.fixture(scope='module')
def db():
    return DataBase()


class TestMyView():

    @pytest.fixture(autouse=True)
    def transaction(self, request, db):
        db.init_database()
        request.addfinalizer(db.rollback)

    def test_failing_view(self, db):
        from hocuspocusweb.views.default import Index

        index = Index(dummy_request(db.session))
        index.request.client_addr = ''
        info = index.post()

        assert info.status_int == 404

    def test_passing_view(self, db):
        from hocuspocusweb.models.user import User
        from hocuspocusweb.views.default import Index

        user = User(
            ip_address='192.168.1.111',
            name='Randy',
            password='somepassword',
            email='fake@fake.com'
        )
        db.session.add(user)

        index = Index(dummy_request(db.session))
        index.request.client_addr = '192.168.1.111'
        index.request.POST = {'password': 'somepassword'}

        info = index.post()

        assert info['name'] == 'Randy'
