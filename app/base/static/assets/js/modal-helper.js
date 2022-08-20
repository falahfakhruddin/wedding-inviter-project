    /*
    upload guest
    */

    $('#uploadGuest').submit(function(event) {
      // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var formData = new FormData();

        formData.append('file', $('input[type=file]')[0].files[0]);

        console.log($SCRIPT_ROOT)
        console.log(formData);

        // process the form
        $.ajax({
          method: 'POST',
          url: $SCRIPT_ROOT + 'api/backend/guest-list/_upload',
          processData : false,
          mimeType : "multipart/form-data",
          contentType: false,
          cache : false,
          data: formData
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages

                $('form').html('<div class="alert alert-success">' + data.message + '</div>');

            })

            // using the fail promise callback
            .fail(function(data) {

              // log data to the console so we can see
              console.log(data);

              //Server failed to respond - Show an error message
              $('form').html('<div class="alert alert-danger">Could not reach server, please try again later and refresh the page.</div>');
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();

        setTimeout(function(){// wait for 5 secs(2)
                    location.reload(); // then reload the page.(3)
                 }, 500);
      });

      /*
      delete guest
      */

      $('#deleteGuest').submit(function(event) {

        // process the form
        $.ajax({
          method: 'DELETE',
          url: $SCRIPT_ROOT + 'api/backend/guest-list/_delete'
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages

                $('form').html('<div class="alert alert-success">' + data.message + '</div>');
            })

            // using the fail promise callback
            .fail(function(data) {

              // log data to the console so we can see
              console.log(data);

              //Server failed to respond - Show an error message
              $('form').html('<div class="alert alert-danger">Could not reach server, please try again later and refresh the page.</div>');
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();

        setTimeout(function(){// wait for 5 secs(2)
            location.reload(); // then reload the page.(3)
         }, 500);

      });


      /*
      share invitation to guest
      */

      $('#inviteGuest').submit(function(event) {

        var str = $("textarea[id=messageForm]").val();
        var name = $("label[id=guestName]").val();

        let message = encodeURIComponent(str);

        console.log(message)

        var url = `whatsapp://send?text=${message}`;

        console.log(url);

        var formData = {
            'name' : name,
        };

        // process the form
        $.ajax({
          method: 'POST',
          url: $SCRIPT_ROOT + 'api/backend/guest/_update_shared_at',
          contentType: "application/json",
          dataType: "json",
          accepts: "application/json",
          data: JSON.stringify(formData)
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages

                var win = window.open(url, '_blank');

                if (win) {
                    //Browser has allowed it to be opened
                    win.focus();
                } else {
                    //Browser has blocked it
                    alert('Please allow popups for this website');
                }

            })

            // using the fail promise callback
            .fail(function(data) {

              // log data to the console so we can see
              console.log(data);

              //Server failed to respond - Show an error message
              $('form').html('<div class="alert alert-danger">Could not reach server, please try again later and refresh the page.</div>');
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();

        setTimeout(function(){// wait for 5 secs(2)
                    location.reload(); // then reload the page.(3)
                 }, 500);

      });


      /*
      generate message
      */

      $('.open-shareButton').click(function(event) {

        var name = $(this).data('guest');
        var group = $(this).data('group');

        var formData = {
            'group' : group,
        };

        console.log(name);
        console.log(formData)

        $.getJSON({
            url: $SCRIPT_ROOT + "api/backend/_message/" + name ,
            data: formData,
            success: function(data){
                $("textarea").html(data.template_message);
            }
        });

        var guestName = document.getElementById("guestName")
        guestName.innerHTML = name;
        guestName.value = name;

      });

       /*
      get template message
      */

      $('.open-editButton').click(function(event) {
        var template = $(this).data('template');
        var group = $(this).data('group');
        $("textarea").html(template);
        var groupTemplate = document.getElementById("groupTemplate")
        groupTemplate.innerHTML = group;
        groupTemplate.value = group;


      });

      /*
      edit template message
      */

      $('#editTemplateMessage').submit(function(event) {

        let message = $("textarea[id=templateMessageForm]").val();
        let group = $("label[id=groupTemplate]").val();

        var formData = {
            "template_message": message,
            "group": group
        }
        console.log(formData)

        // process the form
        $.ajax({
          method: 'POST',
          url: $SCRIPT_ROOT + 'api/backend/message/_edit',
          contentType: "application/json",
          dataType: "json",
          accepts: "application/json",
          data: JSON.stringify(formData)
        })
            // using the done promise callback
            .done(function(data) {

                // log data to the console so we can see
                console.log(data);

                // here we will handle errors and validation messages

                $('form').html('<div class="alert alert-success">' + data.message + '</div>');

            })

            // using the fail promise callback
            .fail(function(data) {

              // log data to the console so we can see
              console.log(data);

              //Server failed to respond - Show an error message
              $('form').html('<div class="alert alert-danger">Could not reach server, please try again later and refresh the page.</div>');
            });

        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();

        setTimeout(function(){// wait for 5 secs(2)
                    location.reload(); // then reload the page.(3)
                 }, 500);

      });