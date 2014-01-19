$( document ).ready(function() {
    $(".file_row").each(function(i, x) {
    	var end = moment($(x).data('file_expire_time'));
    	startCountdown(new Date(end), i+1);
    });
});

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
    replaceFileInput: false,
    add: function (e, data) {
      $("#uploadButton").unbind("click").click(function () {
        $("#uploadKey").val(window.SESSION_ID+'/${filename}');
        data.submit();
        $("#uploadButton").text("Uploading...").attr("disabled", "disabled");
      });
    },
    done: function (e, data) {
        $('#no_files').css('visibility', 'hidden');
        $('#spinner-container').css('z-index', '1000');
        $('#refresh-spinner').css({'visibility':'visible', 'z-index':'1000'});
        setTimeout(function() { location.reload(); }, 800);
    },
    fail: function(e, data) {
      console.log(e);
      console.log(data);
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
