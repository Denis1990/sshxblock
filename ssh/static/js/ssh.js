/* Javascript for SshXBlock. */
function SshXBlock(runtime, element) {

    /**
     * This function is responsible for printing
     * the output of a command passed to server.
     */
    function printCommandOutput(result) {
        termObj.echo(JSON.parse(result)['response'])
    }

    function done(result) {
        alert(result.autho);
    }
    
    var sshCmd = runtime.handlerUrl(element, 'process_command');
    var authorizeUrl = runtime.handlerUrl(element, 'authorize');
    var termObj = $('#termDiv').terminal(
                function(command, term) {
                 
                }, {
            prompt: '>',
            name: 'test',
            enabled: true,
            greetings: 'Hello there. This is a terminal emulator!',
            keydown: function(e, term) {
                // keycode 13 --> enter keystroke
                if (e.which === 13) {
                    $.ajax({
                        type: "POST",
                        url: sshCmd,
                        data: JSON.stringify({"cmd": term.get_command()}),
                        success: printCommandOutput
                    });
                }
            }
        });
       
       //Function to make ssh connect with ssh.py  authorize function
       $('#btncon', element).click(function(eventObject) {
            //   var port = $("#portTxt").val();
            $.ajax({
                type: "POST",
                url: authorizeUrl,
                data: JSON.stringify({"host":$("#hostTxt").val(), "user": $("#usernameTxt").val(), "pass": $("#passwordTxt").val()}),
                success: done
            });
    });
       
       
       
}
