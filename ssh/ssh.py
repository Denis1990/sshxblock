"""This XBlock is web base ssh terminal."""

import pkg_resources
import paramiko
import json

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String , List,Dict
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
    ssh_hostnames = List(scope=Scope.settings ,help="Editable property for studio version,defining machines to connect to.Field format :[hostname1,hostname2,...]")
    ssh_portList = List(scope=Scope.settings ,help="Editable property for studio version,defining port to connect to.Field format :[hostname1-Port,hostname2-port,...]")
    ssh_profiles = Dict(scope=Scope.settings ,help="Editable property for studio version,defining login profiles for machines.Field format :[Hostname1:[[user1,pass1],[user2,pass2]],Hostname2:[[user1,pass2],[user2,pass2]]]")
         
        
    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")    
    
    #================student View========================    
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
        """These values will be reseted on each visit """
        self.ssh_host = ''
        self.ssh_user = '' 
        self.ssh_pass = ''
        self.ssh_port = ''
        self.ssh_pwd = ''
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
            if test[0:3]=='cd ':
               """
               It seems that each exec_command is a seperate session so we have to run all commands combined
               http://www.vertigrated.com/blog/2010/02/python-remote-ssh-with-paramiko/
               http://stackoverflow.com/questions/8932862/how-do-i-change-directories-using-paramiko
               """
               stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';' +'cd ' +test[3:]+";pwd | tr -d '\n'")   
               self.ssh_pwd = stdout.readline() 
               return json.dumps({'type':"cd",'response': self.ssh_user+"@"+self.ssh_host+":"+self.ssh_pwd+"$>"})               
            elif test[0:3]=="vi " or test[0:5]=="nano " or test[0:5]=="pico " or test[0:6]=="gedit "  or test[0:5]=="edit " :
               if test[0:3]=="vi ":
                   trimed = test[3:].strip()
               elif test[0:5]=="nano " or test[0:5]=="pico " or test[0:5]=="edit " :
                   trimed = test[5:].strip()
               else : 
                   trimed = test[6:].strip() 
               if '/' in trimed  :
                   print "\n Other Directory \n"
                   cutted = trimed.split('/')
                   lastPart = cutted[len(cutted)-1]
                   if cutted[0]=='':
                       cutted[0]=u'/'; 
                   firstPart = ""
                   for x in range(0, len(cutted)-1):
                       if x!=0:
                           firstPart += cutted[x]+"/"
                       else:  
                           firstPart += cutted[x]   
                   stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';find '+firstPart+' -name ' +'\''+lastPart+'\'' )                    
               else : 
                   stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';find . -name ' +'\''+trimed+'\'' ) 
               found = stdout.read();
               if found!='' :
                   stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ '; cat ' + trimed  );   
                   return json.dumps({'type':"editor",'response': stdout.readlines(),"title":trimed})                   
               return {'response': None}
            stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ ';' + data['cmd'])
            return json.dumps({'type':"command",'response': stdout.readlines()})
        except Exception:
            """
            print "Connection Failed"
            ssh_connection.close()
            """
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
            """
            print "Connection Failed"         
            self.ssh_connection.close()
            quit()
            """
            return {'autho':"Connection failed..."}           
        return {'autho': "Connected",'prefix':self.ssh_user+"@"+self.ssh_host+":"+self.ssh_pwd+"$>"}


    #function to edit texts         
    @XBlock.json_handler    
    def saveText(self,data,suffix=''):
        ssh_connection = paramiko.SSHClient()
        ssh_connection.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            port_num = int(self.ssh_port)
            ssh_connection.connect(hostname=self.ssh_host, port=port_num, username=self.ssh_user, password=self.ssh_pass)
            title = str(data["title"])
            newText = str(data["textArea"])       
            stdin, stdout, stderr = ssh_connection.exec_command('cd ' + self.ssh_pwd+ '; echo \"'+newText+'\" > '+title);        
            return {"response":""}
        except Exception:
             """
             print "Connection Failed"
             ssh_connection.close()
             """
             return {'response':"Not connected"}   
       
    
    
    @XBlock.json_handler    
    def getPort(self,data,suffix=''):
        selected_host = data["selectedHost"]
        x = 0
        for i in self.ssh_hostnames:
            if(i==selected_host):
                return {"port":self.ssh_portList[x]}
            x+=1    
        return {"port":""}
    
    def logout(self):
        self.channel.close()
        self.ssh_connection.close()

    #================studio View========================
    def studio_view(self, context):
        """temporary for debug number of hosts=0"""
        html = self.resource_string("static/html/ssh_edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/ssh_edit.js"))
        frag.initialize_js('SshEditXBlock')
        return frag
    
    #----------------------studio View-Hosts--------------
    """Studio view uses this to add new host machine""" 
    @XBlock.json_handler
    def addHost(self,data, suffix=''):
        new_host = data['new_machine']
        new_port = data['new_port']
        for i in self.ssh_hostnames:
          if (i==new_host): 
             return {"response":"false"}
        self.ssh_hostnames.append(new_host)  
        self.ssh_portList.append(new_port)        
        self.ssh_profiles.setdefault(new_host, [])
        return {"response":"true"}
    
    """Studio view uses this to remove a host machine by id """
    @XBlock.json_handler    
    def removeHost(self,data,suffix=''):
        host_id = int(data['host_id'])
        removed_host = self.ssh_hostnames[host_id]
        self.ssh_hostnames.pop(host_id)
        self.ssh_portList.pop(host_id)
        self.ssh_profiles.pop(removed_host)
        
        return {}
    
        """Studio view uses this to get all host machines """
    @XBlock.json_handler    
    def getHost(self,data,suffix=''):
        return json.dumps({'hosts': self.ssh_hostnames,'ports':self.ssh_portList})
    
        
    #----------------------studio View-Profiles--------------
    """Studio view uses this to add new profiles for a host""" 
    @XBlock.json_handler
    def addProfile(self,data, suffix=''):
        selected_host  = data['selected_host']
        new_user  = data['new_user']
        new_pass  = data['new_pass']
        for i in self.ssh_profiles[selected_host]:
            if (i[0]==new_user):
                return{"response":"false"}            
        self.ssh_profiles[selected_host].append([new_user,new_pass])
        return {"response":"true"} 
    
    """Studio view uses this to remove a profile for a selected machine by id """
    @XBlock.json_handler 
    def removeProfile(self,data,suffix=''):
        profile_id = int(data['profile_id'])
        selected_host = data['selected_host']
        self.ssh_profiles[selected_host].pop(profile_id)
        return {}
        
    """Studio view uses this to get all profiles for a specific machine """
    @XBlock.json_handler    
    def getProfile(self,data,suffix=''):
        selected = data['selectedHost']
        return json.dumps({'profiles': self.ssh_profiles[selected]})
               
    #===================================================
    
            
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
         
