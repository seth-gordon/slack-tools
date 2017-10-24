# coding:utf-8
# Copyright 2017 Scout Exchange, LLC. All Rights Reserved.

class CommonFabric(object):
    """
    Base class to define the required fabric commands.  TPX and Connect will
    derive their own class as the commands are different per application.
    """
    # we want the slack commands to be simple and as short as possible.  Map
    # the simple commands to the git repo fabric needs.
    repo_map = {
        'tpx': 'milton-tpx',
        'connect': 'scout-app'
    }

    def deploy(self, app, target, build):
        """
        TPX:     fab -R <target> deploy:milton-tpx,<build>
        Connect: cd scout-connect
                 fab <target> deploy:scout-app,<build>
        """
        raise NotImplemented('Implementation in derived class.')

    def rollforward(self, app, target, build):
        """
        TPX:     fab -R <target> rollforward:milton-tpx,<build>
        Connect: cd scout-connect
                 fab <target> rollforward:scout-app,<build>
        """
        raise NotImplemented('Implementation in derived class.')

    def reload(self, app, target):
        """
        This should be on web nodes only.

        TPX:     fab -R <target> reload:milton-tpx
        Connect: cd scout-connect
                 fab <target> restart_uwsgi
        """
        raise NotImplemented('Implementation in derived class.')


class TPXFabric(CommonFabric):
    """
    Call the fabric commands specific to TPX.
    """
    def __init__(self):
        super(TPXFabric, self).__init__()

    def deploy(self, app, target, build):
        """
        TPX: fab -R <target> deploy:milton-tpx,<build>
        """
        raise NotImplemented('Needs code.')

    def rollforward(self, app, target, build):
        """
        TPX: fab -R <target> rollforward:milton-tpx,<build>
        """
        raise NotImplemented('Needs code.')

    def reload(self, app, target):
        """
        This should be on web nodes only.

        TPX: fab -R <target> reload:milton-tpx
        """
        raise NotImplemented('Needs code.')

    def stop_scheduler(self, target):
        """
        TPX: fab -R <target> stop_scheduler
        """
        raise NotImplemented('Is Nice-to-Have.')

    def start_scheduler(self, target):
        """
        TPX: fab -R <target> start_scheduler
        """
        raise NotImplemented('Is Nice-to-Have.')

    def stop_worker(self, target):
        """
        TPX: fab -R <target> stop_worker
        """
        raise NotImplemented('Is Nice-to-Have.')

    def start_worker(self, target):
        """
        TPX: fab -R <target> start_worker
        """
        raise NotImplemented('Is Nice-to-Have.')


class ConnectFabric(CommonFabric):
    """
    Call the fabric commands specific to Connect.
    """
    def __init__(self):
        super(ConnectFabric, self).__init__()

    def deploy(self, app, target, build):
        """
        Connect: cd scout-connect
                 fab <target> deploy:scout-app,<build>
        """
        raise NotImplemented('Needs code.')

    def rollforward(self, app, target, build):
        """
        Connect: cd scout-connect
                 fab <target> rollforward:scout-app,<build>
        """
        raise NotImplemented('Needs code.')

    def reload(self, app, target):
        """
        This should be on web nodes only.

        Connect: cd scout-connect
                 fab <target> restart_uwsgi
        """
        raise NotImplemented('Needs code.')