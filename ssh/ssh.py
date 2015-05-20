"""This XBlock is web base ssh terminal."""

import pkg_resources
import paramiko

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class SshXBlock(XBlock):
    """
    Make an ssh connection with a remote machine.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    host_name = String(default='', scope=Scope.user_state, help="The hostname of the machine to connect to")
    host_ip = String(default='', scope=Scope.user_state, help="The hosts ip address")
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
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'
        print "incread"
        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def process_command(self, data, suffix=''):
        if self.ssh_connection != None:
            self.channel = self.ssh_connection.invoke_shell()
            buff = ''
            self.chan.send(data['cmd'])
            while not self.channel.recv_ready():
                continue
            command_output = self.channel.recv()
            return {'response', command_output}
        print 'return null'
        command_output = None
        return {'response': command_output}

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
            self.vari = 98
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
