"""This XBlock is web base ssh terminal."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment


class SshXBlock(XBlock):
    """
    Make an ssh connection with a remote machine.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )

    host_name = String(default='', scope=Scope.user_state, help="The hostname of the machine to connect to")
    host_ip = String(default='', scope=Scope.user_state, help="The hosts ip address")

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
        print "-----------"
        print "Count is %i" % (self.count)
        print "-----------"
        self.count += 1
        return {"count": self.count}

    @XBlock.json_handler
    def process_command(self, data, suffix=''):
        print 'received command ', data['cmd']
        print 'returning ...'
        return {'response': ['.', '..']}

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
