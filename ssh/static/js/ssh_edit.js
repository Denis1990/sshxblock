function SshEditXBlock(runtime, element) {
    
     var addHostUrl = runtime.handlerUrl(element, 'addHost');
     var getHostUrl = runtime.handlerUrl(element, 'getHost');
     var removeHostUrl = runtime.handlerUrl(element, 'removeHost');
 
//This function will be used each time the table is changed and on 
//page load to draw the table 
/*http://www.learnfast.ninja/posts/53cce9e28a04fffc0c29147b*/    
    function drawHostTable(result)
    {     
       $('#hosts-table').find("tr:gt(0)").remove();
       var array  = JSON.parse(result)['hosts']
       for (var i in array)       
         $('#hosts-table').append('<tr><td>'+i+'</td><td>'+array[i]+'</td><td><input type="button" value="remove"  ></td></tr>');
    }
     
     //We created remove buttons for each id on the table this is the listener
     $("#hosts-table").on("click", "tr td:nth-child(3)", function(event){
         var tr = $(this).closest("tr")
         var col_id = $(tr).find('td:eq(0)').text()
          $.ajax({
                type: "POST",
                url: removeHostUrl,
                data: JSON.
                stringify({"host_id":col_id}),
                success: getHost
            });  
      });
     
     //We want to return all hosts from our db
     function getHost() 
    {
              $.ajax({
                type: "POST",
                url: getHostUrl,
                data: JSON.
                stringify({"null":null}),
                success: drawHostTable
            });  
    }
         
     //Adding a new host    
     $('#new-host-button', element).click(function(eventObject) {
            $.ajax({
                type: "POST",
                url: addHostUrl,
                data: JSON.
                stringify({"new_machine":$("#new-machine").val()}),
                success: getHost
            });            
    });
 
    //on page load
    $(function ($) {
        //We draw the host table for the first time
        getHost()
    });
}
