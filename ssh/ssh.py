"""This XBlock is web base ssh terminal."""

import pkg_resources
import paramiko
import json

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String , List
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
    ssh_pwd = String(default='~', scope=Scope.user_state, help="With cd command the path you were before is stored here")
    ssh_hostnames = List(scope=Scope.user_state ,help="Editable property for studio version,defining machines to connect to.Field format :[hostname1,hostname2]")
    ssh_profiles = List(scope=Scope.user_state ,help="Editable property for studio version,defining login profiles for machines.Field format :[  [ [host1_user1,host1_user2] ,[host1_pass1,host1_pass2] ]  , [[..],[..]] <--host 2....]")
     

    def studio_view(self, context):
        """temporary for debug number of hosts=0"""
        print "------------------"
        for x in self.ssh_hostnames:
            print x
        print "------------------"    
        html = self.resource_string("static/html/ssh_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/ssh_edit.js"))
        frag.initialize_js('SshEditXBlock')
        return frag
    
    """Studio view uses this to remove a host machine by id """
    @XBlock.json_handler    
    def removeHost(self,data,suffix=''):
        host_id = int(data['host_id'])
        self.ssh_hostnames.pop(host_id)
        return {}
    
    
    """Studio view uses this to get all host machines """
    @XBlock.json_handler    
    def getHost(self,data,suffix=''):
        return json.dumps({'hosts': self.ssh_hostnames})
         
        
    """Studio view uses this to add new host machine""" 
    @XBlock.json_handler
    def addHost(self,data, suffix=''):
        new_host = data['new_machine']
        self.ssh_hostnames.append(new_host)         
        return {}
        
        
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
            port_num = int(self.ssh_port)
            ssh_connection.connect(hostname=self.ssh_host, port=port_num, username=self.ssh_user, password=self.ssh_pass)
            stdin, stdout, stderr = ssh_connection.exec_command('cd '+self.ssh_pwd)    
            test = data['cmd']      
            print test.split() 
            if test[0:3]=='cd ':
               """
               It seems that each exec_command is a seperate session so we have to run all commands combined
               http://www.vertigrated.com/blog/2010/02/python-remote-ssh-with-paramiko/
               http://stackoverflow.com/questions/8932862/how-do-i-change-directories-using-paramiko
               """
               stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';' +'cd ' +test[3:]+";pwd | tr -d '\n'")   
               self.ssh_pwd = stdout.readline()
               print self.ssh_pwd               
            stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';' + data['cmd'])
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
        self.ssh_port = data['port'];
        self.ssh_user = data['user'];
        self.ssh_pass = data['pass'];
        """"
        Because port is type <unicode> and not Integer and create a variable portnum for port which is int
        """
        port_num = int(self.ssh_port)
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.client.AutoAddPolicy());
        try:
            ssh_connection.connect(hostname=self.ssh_host,port=port_num,username=self.ssh_user,password=self.ssh_pass)
            stdin, stdout, stderr = ssh_connection.exec_command("cd ~ ;pwd | tr -d '\n'") 
            self.ssh_pwd = stdout.readline()       
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
            ("SshXBlock","""<ssh/>"""),
            ]

            
    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        return {
            'result': 'success',
        }
         