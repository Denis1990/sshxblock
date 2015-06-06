function SshEditXBlock(runtime, element) {
     var selectedHost = null
     var addHostUrl = runtime.handlerUrl(element, 'addHost');
     var getHostUrl = runtime.handlerUrl(element, 'getHost');
     var removeHostUrl = runtime.handlerUrl(element, 'removeHost');
     var addProfileUrl = runtime.handlerUrl(element, 'addProfile');
     var getProfileUrl = runtime.handlerUrl(element, 'getProfile');
     var removeProfileUrl = runtime.handlerUrl(element, 'removeProfile');


//============================HOST TABLE=============================
     
//This function will be used each time the table is changed and on 
//page load to draw the table 
/*http://www.learnfast.ninja/posts/53cce9e28a04fffc0c29147b*/    
    function drawHostTable(result)
    {     
       $('#hosts-table').find("tr:gt(0)").remove();
       var array  = JSON.parse(result)['hosts']
       for (var i in array)       
         $('#hosts-table').append('<tr><td>'+i+'</td><td>'+array[i]+'</td><td><input type="button" value="select"  ></td><td><input type="button" value="remove"  ></td></tr>');
    }
    
    //We created select buttons for each id on the host table this is the listener
      $("#hosts-table").on("click", "tr td:nth-child(3)", function(event){
         var tr = $(this).closest("tr")
         var col_hostname = $(tr).find('td:eq(1)').text()
         $('#select-host').html(col_hostname)  
         selectedHost =   $('#select-host').text()
         getProfile()         
      });
     
     
     //We created remove buttons for each id on the host table this is the listener
     $("#hosts-table").on("click", "tr td:nth-child(4)", function(event){
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

//============================PROFILE TABLE=============================

    
    //This will be called each time a host is selected or a profile is added/removed
    function drawProfileTable(result)
    {     
       $('#profile-table').find("tr:gt(1)").remove();
       var array  = JSON.parse(result)['profiles']
       for (var i in array)
           $('#profile-table').append('<tr><td>'+i+'</td><td>'+array[i][0]+'</td><td>'+array[i][1]+'</td><td><input type="button" value="remove"></td></tr>')                     
    }
     
      //We created remove buttons for profile on the profie table this is the listener
      $("#profile-table").on("click", "tr td:nth-child(4)", function(event){
         var tr = $(this).closest("tr")
         var col_id = $(tr).find('td:eq(0)').text()         
         $.ajax({
                type: "POST",
                url: removeProfileUrl,
                data: JSON.
                stringify({"profile_id":col_id,"selected_host":selectedHost}),
                success: getProfile
            });  
      });
     
          
     //We want to return all profiles for a specific host from our db
     function getProfile() 
    {
              $.ajax({
                type: "POST",
                url: getProfileUrl,
                data: JSON.
                stringify({"selectedHost":selectedHost}),
                success: drawProfileTable
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
 
     //Adding a new profile
     $('#new-profile-button', element).click(function(eventObject) {
            $.ajax({
                type: "POST",
                url: addProfileUrl,
                data: JSON.
                stringify({"new_user":$("#new-username").val(),"new_pass":$("#new-password").val(),"selected_host":$('#select-host').text()}),
                success: getProfile
            });            
    });
    
//==========================ON PAGE LOAD==================================
    $(function ($) {
        //We draw the host table for the first time
        getHost()
    });
}
