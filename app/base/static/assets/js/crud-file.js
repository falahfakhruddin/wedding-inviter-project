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
      });