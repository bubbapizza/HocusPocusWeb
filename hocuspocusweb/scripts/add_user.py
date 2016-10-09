import sys
import transaction
import argparse

from sqlalchemy.orm.exc import NoResultFound
from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )
from hocuspocusweb.models.meta import (
    get_session,
    get_engine,
    get_dbmaker,
    )
from hocuspocusweb.models import User
from getpass import getpass


def main(settings):

    dbmaker = get_dbmaker(get_engine(settings))
    dbsession = get_session(transaction.manager, dbmaker)

    # needs: ip_address, name, email, password
    ip_address = input('ip address: ')
    try:
        dbsession.query(User).filter(
            User.ip_address == ip_address).one()
    except NoResultFound:
        pass
    else:
        print('ip_address already taken')
        sys.exit(1)

    name = input('name: ')

    email = input('email: ')
    try:
        dbsession.query(User).filter(User.email == email).one()
    except NoResultFound:
        pass
    else:
        print('email already taken')
        sys.exit(1)

    while True:
        mac_address = input('mac address(wifi): ')
        confirm_mac_address = input('Comfirm mac address: ')

        if mac_address != confirm_mac_address:
            print('Mac addresses don\'t match. Try again')
        else:
            break

    while True:
        password = getpass()
        comfirm_password = getpass(prompt='Confirm password: ')

        if password != comfirm_password:
            print('Passwords do not match! Try again.')
        else:
            break

    add_user(
        dbsession,
        ip_address=ip_address,
        mac_address=mac_address,
        name=name,
        email=email,
        password=password
    )


def add_user(dbsession, **kwargs):

    with transaction.manager:
        user = User(**kwargs)
        dbsession.add(user)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add user to database')
    parser.add_argument('config_uri', help='Pyramid config file')

    args = parser.parse_args()
    setup_logging(args.config_uri)
    settings = get_appsettings(args.config_uri)

    main(settings)
