/* Javascript for SshXBlock. */
function SshXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    function done(result) {
        alert(result.autho);
    }
    
    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var sshCmd = runtime.handlerUrl(element, 'process_command');
    var authorizeUrl = runtime.handlerUrl(element, 'authorize');
    
    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $('#termDiv').terminal(
        function(command, term) {
            if (command == 'test') {
                term.echo("you just typed 'test'");
            }
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
                        success: function() {
                            term.echo('.\n..\nDocuments\n');
                            return true;
                        }
                    });
                }
            }
        });
       
       //Function to make ssh connect with ssh.py  authorize function
       $('#btncon', element).click(function(eventObject) {
               var host =  $("#hostTxt").val();
               var user =  $("#usernameTxt").val();
               var pass = $("#passwordTxt").val();
            //   var port = $("#portTxt").val();
               console.log("Host = "+host+"\nUsername = "+user+"\nPassword ="+pass);
         $.ajax({
            type: "POST",
            url: authorizeUrl,
            data: JSON.stringify({"host":host,"user": user,"pass": pass}),
            success: done
        });
    });
       
       
       
}
