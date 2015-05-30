function SshEditXBlock(runtime, element) {
    
     var addHostUrl = runtime.handlerUrl(element, 'addHost');
     
     /*http://www.learnfast.ninja/posts/53cce9e28a04fffc0c29147b*/
      function addRow(result) {
          alert(result.id+"\n"+result.host)
        $('#hosts-table').append('<tr><td>'+result.id+'</td><td>'+result.host+'</td></tr>');
    }
     
     $('#new-host-button', element).click(function(eventObject) {
            $.ajax({
                type: "POST",
                url: addHostUrl,
                data: JSON.stringify({"new_machine":$("#new-machine").val()}),
                success: addRow
            });            
    });
 
    /* 
    On next version this should redraw the Hosts table
    This function will be called on each update
    */
    function drawHostsTable()
    {}
 
    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}