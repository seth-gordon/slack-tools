# coding:utf-8
# Copyright 2017 Scout Exchange, LLC. All Rights Reserved.
"""DEPLOYMENT NOTE: This code must be run with the milton-ops virtual environment
active, and the user must be able to run the appriate fab commands from the command
line without having to enter a password (you may need to invoke ssh-agent)."""
import os, subprocess

class FabricRuntimeError(RuntimeError):
    def __init__(self, returncode, stdout, stderr):
        self.msg = "Running fab failed with return code {}".format(returncode)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class CommonFabric(object):
    """
    Base class to define the required fabric commands.  TPX and Connect will
    derive their own class as the commands are different per application.
    """

    def __init__(self, fab_file, fab_executable=None):
        """@:param fab_executable: The path to the fab program itself.
           @:param fab_file: The path to the `fabfile.py` configuration file
                             (there are different files for TPX and Connect)."""
        if not os.access(fab_file, os.R_OK):
            raise ValueError('Fabfile at {} not readable'.format(fab_file))
        self.fab_file = fab_file
        homedir = os.environ['HOME']
        if not fab_executable:
            fab_executable = os.path.join(homedir, 'milton-ops', 'virtualenv', 'bin', 'fab')
        if not os.access(fab_executable, os.X_OK):
            raise ValueError('Fab program at {} not executable'.format(fab_executable))
        self.fab_executable = fab_executable

    def _invoke(self, *args):
        """Run fab with the given arguments. If the command terminates successfully,
        return the output; otherwise, raise an exception. This does not have to run
        in any particular directory, but the milton-ops virtualenv must be active."""
        arglist = [self.fab_executable, '-f', self.fab_file] + list(args)
        pipe = subprocess.Popen(arglist,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        stdout, stderr = pipe.communicate()
        if pipe.returncode != 0:
            raise FabricRuntimeError(pipe.returncode, stdout, stderr)
        return stdout

    def deploy(self, target, build):
        """
        TPX:     fab -R <target> deploy:milton-tpx,<build>
        Connect: cd scout-connect
                 fab <target> deploy:scout-app,<build>
        """
        raise NotImplemented('Implementation in derived class.')

    def rollforward(self, target, build):
        """
        TPX:     fab -R <target> rollforward:milton-tpx,<build>
        Connect: cd scout-connect
                 fab <target> rollforward:scout-app,<build>
        """
        raise NotImplemented('Implementation in derived class.')

    def reload(self, target):
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
    def __init__(self, fab_file=None, fab_executable=None):
        if not fab_file:
            fab_file = os.path.join(os.environ['HOME'], 'milton-ops', 'fabfile.py')
        super(TPXFabric, self).__init__(fab_file, fab_executable)

    def deploy(self, target, build):
        """
        TPX: fab -R <target> deploy:milton-tpx,<build>
        """
        return self._invoke('-R', target, 'deploy:milton-tpx,{}'.format(build))

    def rollforward(self, target, build):
        """
        TPX: fab -R <target> rollforward:milton-tpx,<build>
        """
        return self._invoke('-R', target, 'rollforward:milton-tpx,{}'.format(build))

    def reload(self, target):
        """
        This should be on web nodes only.

        TPX: fab -R <target> reload:milton-tpx
        """
        return self._invoke('-R', target, 'reload:milton-tpx')

    def stop_scheduler(self, target):
        """
        TPX: fab -R <target> stop_scheduler
        """
        return self._invoke('-R', target, 'stop_scheduler')


    def start_scheduler(self, target):
        """
        TPX: fab -R <target> start_scheduler
        """
        return self._invoke('-R', target, 'start_scheduler')


    def stop_worker(self, target):
        """
        TPX: fab -R <target> stop_worker
        """
        return self._invoke('-R', target, 'stop_worker')

    def start_worker(self, target):
        """
        TPX: fab -R <target> start_worker
        """
        return self._invoke('-R', target, 'start_worker')


class ConnectFabric(CommonFabric):
    """
    Call the fabric commands specific to Connect.
    """
    def __init__(self, fab_file=None, fab_executable=None):
        if not fab_file:
            fab_file = os.path.join(os.environ['HOME'], 'milton-ops',
                                    'scout-connect', 'fabfile.py')
        super(ConnectFabric, self).__init__(fab_file, fab_executable)

    def deploy(self, target, build):
        """
        Connect: cd scout-connect
                 fab <target> deploy:scout-app,<build>
        """
        return self._invoke(target, 'deploy:scout-app,{}'.format(build))

    def rollforward(self, target, build):
        """
        Connect: cd scout-connect
                 fab <target> rollforward:scout-app,<build>
        """
        return self._invoke(target, 'rollforward:scout-app,{}'.format(build))

    def reload(self, app, target):
        """
        This should be on web nodes only.

        Connect: cd scout-connect
                 fab <target> restart_uwsgi
        """
        return self._invoke(target, 'restart_uwsgi')


if __name__ == '__main__':
    f = TPXFabric()
    print f.reload('environment:blackops')
