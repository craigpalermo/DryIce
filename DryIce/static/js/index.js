$( document ).ready(function() {
    resetTimers();    

    $(document).bind('drop dragover', function(e) {
        e.preventDefault(); 
    });
    
    $("#dropbox").on("click", function() {
        $("#uploadFile").trigger('click');
    });

    $("#dropbox").bind('fileuploaddragover', function(e) {
        alert('bla');
    });

    $("#clear_session").on("click", function() {
        deleteFiles();
    });

    $("#link_table").on("click", ".trashcan", function() {
        var filename = $(this).data('filename');
        deleteFiles(filename);
    });

    $(function() {
        // Setup drop down menu
        $('.dropdown-toggle').dropdown();

        // Fix input element click problem
        $('.dropdown input, .dropdown label').click(function(e) {
            e.stopPropagation();
        });
    });
});

function deleteFiles(filename) {
    $('#spinner-container').css('z-index', '1000');
    $('#refresh-spinner').css({'visibility':'visible', 'z-index':'1000'});
   
    url = typeof filename !== 'undefined' ? '/delete/'+filename : 'clear_session';

    $.ajax({
        type: "GET",
        url: url,
        success: function() {
            reloadLinkTable();
        },
        error: function() {
            $('#link_table').html("<div id='message'></div>");
            $('#message').html("<h2>There was a problem loading your files... Try refreshing the page.</h2>");
        }
    });    
}


function resetTimers() {
    $(".file_row").each(function(i, x) {
        var end = moment($(x).data('file_expire_time'));
        var unixtime = new Date(end).getTime() / 1000;
        var spanName = "#" + (i+1) + "_timeRemaining";
        $(spanName).scojs_countdown({until:unixtime});
    });
}

function reloadLinkTable() {
    $('#link_table').load('/api/load_link_table', function() {
        resetTimers(); 
        $('#refresh-spinner').css({'visibility':'hidden'});
        $('#spinner-container').css('z-index', '-1');
    });
}

$(function() {
  $('input[type=file]').bootstrapFileInput();
  $('.file-inputs').bootstrapFileInput();

  var progressbar   = $("#progressbar"),
      progressLabel = $("#progress-label");

  progressbar.progressbar({
    value: false,
    change: function() {
      progressLabel.text(progressbar.progressbar("value") + "%");
    },
    complete: function() {
      progressLabel.text("Upload complete!");
    }
  });

  $("#uploadFile").fileupload({
    dataType: "xml",
    replaceFileInput: true,
    autoUpload: true,
    add: function (e, data) {
      $("#uploadButton").unbind("click").click(function () {
      });
        $("#uploadKey").val(window.SESSION_ID+'/${filename}');
        data.submit();
        $("#uploadButton").text("Uploading...").attr("disabled", "disabled");
    },
    done: function (e, data) {
        /* make the refresh spinner appear */
        $('#no_files').css('visibility', 'hidden');
        $('#spinner-container').css('z-index', '1000');
        $('#refresh-spinner').css({'visibility':'visible', 'z-index':'1000'});
    

        /* submit form with file info */
        var hidden_filename = $('input[type=file]').val().split('\\').pop(); 
        var expiration = $('[name="expiration"]').val();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        var dataString = 'hidden-filename='+ hidden_filename + '&expiration=' + expiration
                         + '&csrftoken=' + csrftoken;
        $.ajax({
            type: "POST",
            beforeSend: function(request)
            {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/add_file_info/",
            data: dataString,
            success: function() {
                reloadLinkTable();
                
            },
            error: function() {
                $('#link_table').html("<div id='message'></div>");
                $('#message').html("<h2>There was a problem loading your files... Try refreshing the page.</h2>");
            }
        });    
    },
    fail: function(e, data) {
    },
    always: function(e, data) {
      $("#uploadButton").text("Upload").removeAttr("disabled");
    },
    progress: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      progressbar.progressbar("value", progress + 1);
    }
  });

  $('#upload-button').prop('disabled', true);

  // FIXME
  var size_limit = window.SIZE_LIMIT / 1024 / 1024;

  $('#upload-button').click(function() {
    document.getElementById("upload-form").submit();
  });

  $("#file-input").change(function (e) {
    var files = e.currentTarget.files;
    var filesize = ((files[0].size/1024)/1024).toFixed(4); //MB
    if (filesize > size_limit) {
      alert("Selected file is larger than the " +
        size_limit + "MB limit.");
      $('#upload-button').prop('disabled', true);
    } else {
      $('#upload-button').prop('disabled', false);
    }
  });

});
