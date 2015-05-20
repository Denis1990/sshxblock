"""This XBlock is web base ssh terminal."""

import pkg_resources
import paramiko
import json

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class SshXBlock(XBlock):
    """
    Make an ssh connection with a remote machine.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    ssh_host = String(default='', scope=Scope.user_state, help="The hosts ip address or name")
    ssh_user = String(default='', scope=Scope.user_state, help="The username for ssh connection")
    ssh_pass = String(default='', scope=Scope.user_state, help="The password for ssh connection")
    ssh_port = Integer(default=22, scope=Scope.user_state, help="The port for ssh connection")
    
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the SshXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/ssh.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/ssh.css"))
        frag.add_css(self.resource_string("static/css/jqueryterm.css"))
        frag.add_javascript(self.resource_string("static/js/ssh.js"))
        frag.add_javascript(self.resource_string("static/js/jqueryterm.js"))
        frag.initialize_js('SshXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.

    @XBlock.json_handler
    def process_command(self, data, suffix=''):
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            ssh_connection.connect(hostname=self.ssh_host, port=9022, username=self.ssh_user, password=self.ssh_pass)
            stdin, stdout, stderr = ssh_connection.exec_command(data['cmd'])
            return json.dumps({'response': stdout.readlines()})
        except Exception:
            print "Connection Failed"
            ssh_connection.close()
            return {'autho':"Not connected"}
        return {'response': None}

    # TO-DO: exceptions dont work well with some cases :eg Uknown host
    # Need to make safe ssh with keys 
    # Need to be done with jqueryterm and not text fields    
    @XBlock.json_handler
    def authorize(self, data, suffix=''):
        self.ssh_host = data['host'];
        self.ssh_user = data['user'];
        self.ssh_pass = data['pass'];
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(paramiko.client.AutoAddPolicy());
        try:
            self.ssh_connection.connect(hostname=self.ssh_host,port=9022,username=self.ssh_user,password=self.ssh_pass)
        except paramiko.SSHException:
            print "Connection Failed"
            self.ssh_connection.close()
            """"quit()"""
            return {'autho':"Not connected"}
        return {'autho': "Connected"}

    def logout(self):
        self.channel.close()
        self.ssh_connection.close()

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("SshXBlock",
             """<vertical_demo>
                <ssh/>
                </vertical_demo>
             """),
            ]
