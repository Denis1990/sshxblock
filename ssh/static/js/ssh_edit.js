function SshEditXBlock(runtime, element) {
     var selectedHost = "NO HOST SELECTED"
     var addHostUrl = runtime.handlerUrl(element, 'addHost');
     var getHostUrl = runtime.handlerUrl(element, 'getHost');
     var removeHostUrl = runtime.handlerUrl(element, 'removeHost');
     var addProfileUrl = runtime.handlerUrl(element, 'addProfile');
     var getProfileUrl = runtime.handlerUrl(element, 'getProfile');
     var removeProfileUrl = runtime.handlerUrl(element, 'removeProfile');

//Regex to check if one or more spaces on start
function check(item){return  /^[ ]+/.test(item)}     
//Regex to check if a number(valid port 22 or 4digit number)
function checkNumber(item){return  /^((22)|([1-9][0-9]{3,}))/.test(item)}           
      
//============================HOST TABLE=============================
     
//This function will be used each time the table is changed and on 
//page load to draw the table 
/*http://www.learnfast.ninja/posts/53cce9e28a04fffc0c29147b*/    
    function drawHostTable(result)
    {     
       $('#hosts-table').find("tr:gt(0)").remove();
       var hosts  = JSON.parse(result)['hosts']
       var ports = JSON.parse(result)['ports']
       for (var i in hosts)       
         $('#hosts-table').append('<tr><td>'+i+'</td><td>'+hosts[i]+'</td><td>'+ports[i]+'</td><td><input type="button" value="select"  ></td><td><input type="button" value="remove"  ></td></tr>');
    }
    
         //Adding a new host    
     $('#new-host-button', element).click(function(eventObject) {
         new_machine = $("#new-machine").val()
         new_port = $("#new-port").val()
         if(!(check(new_machine) || new_machine==="" || new_port==="" || !checkNumber(new_port)))
         {
            $.ajax({
                type: "POST",
                url: addHostUrl,
                data: JSON.
                stringify({"new_machine":new_machine,"new_port":new_port}),
                success: responseHost
            }); 
            $("#new-machine").val('')
            $("#new-port").val('')
         }
         else alert("Please give a valid hostname/ip and port!!!")             
    });
    
   //When we add a host we check if already exists 
   function responseHost(result)
    {
      if (result.response=="false")
         alert("Hostname already exists on the table")
      else
      getHost()     
    }
     
    //We created select buttons for each id on the host table this is the listener
      $("#hosts-table").on("click", "tr td:nth-child(4)", function(event){
         var tr = $(this).closest("tr")
         var col_hostname = $(tr).find('td:eq(1)').text()
         $('#select-host').html(col_hostname)  
         selectedHost =   $('#select-host').text()
         getProfile()         
      });
     
     
     //We created remove buttons for each id on the host table this is the listener
     $("#hosts-table").on("click", "tr td:nth-child(5)", function(event){
         var tr = $(this).closest("tr")
         var col_id = $(tr).find('td:eq(0)').text()
          $.ajax({
                type: "POST",
                url: removeHostUrl,
                data: JSON.
                stringify({"host_id":col_id}),
                success: getHost
            });  
         if($(tr).find('td:eq(1)').text()==selectedHost)
         {
             selectedHost = "NO HOST SELECTED" 
             $('#select-host').html(selectedHost)  
             $('#profile-table').find("tr:gt(1)").remove();
         }
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
    
     //When we add a profile we check if already exists
     function responseProfile(result)
    {
      if (result.response=="false")
         alert("Username already exists on the table")
      else
      getProfile()     
    }
     
     //Adding a new profile
     $('#new-profile-button', element).click(function(eventObject) {
        new_user = $("#new-username").val()
        new_pass = $("#new-password").val()
        if(selectedHost!="NO HOST SELECTED")
        {
            if(!(check(new_user) || new_user==="" || check(new_pass) || new_pass=="" ))
            {
             if($("#new-password").val()==$("#new-password-2").val())
             {                 
                $.ajax({
                    type: "POST",
                    url: addProfileUrl,
                    data: JSON.
                    stringify({"new_user":new_user,"new_pass":new_pass,"selected_host":selectedHost}),
                    success: responseProfile
                }); 
                $("#new-username").val('')
                $("#new-password").val('')
                $("#new-password-2").val('')  
            }
            else alert("Passwords not matching!!!!")            
           }
           else alert("Please fill the fields username and password with valid values!!!")
        }
        else alert("Please choose a Host first!!!")        
    });
    
//==========================ON PAGE LOAD==================================
    $(function ($) {
        //We draw the host table for the first time
        getHost()
    });
}
