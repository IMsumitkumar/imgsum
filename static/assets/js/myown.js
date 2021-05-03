$('.like-form').submit(function(e) {
    e.preventDefault();

    const post_id = $(this).attr('id')
    const like_icon = $.trim($(`.like-btn-${post_id}`).text())
    const url = $(this).attr('action')

    let res;
    const likes = $.trim($(`.like-count-${post_id}`).text())
    const trimCount = parseInt(likes);
    console.log(like_icon);


    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'post_id': post_id,
        },
        success: function(response) {
            console.log(response);

            if (like_icon === 'UnLike') {
                $(`.like-btn-${post_id}`).html('<i class="fa fa-heart-o m-2" aria-hidden="true"></i>'+'<p hidden>Like</p>');
                res = trimCount - 1;
            } else {
                $(`.like-btn-${post_id}`).html('<i class="fa fa-heart m-2" aria-hidden="true"></i>'+'<p hidden>UnLike</p>');
                res = trimCount + 1;
            }

            $(`.like-count-${post_id}`).html("<b>"+res+"</b>"+"<b> likes </b>")
        },
        error: function(response) {
            console.log(url),
            console.log('error', response)
        }
    })
});

$('#addPostModal').on('shown.bs.modal', function () {
    $('#addPostModal').trigger('focus')
})

$('#EmbedCode').on('shown.bs.modal', function () {
    $('#EmbedCode').trigger('focus')
})



$('.widget-content .mixin').on('click', function () {
    const toast = swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000,
      padding: '2em'
    });
  
    toast({
      type: 'success',
      title: 'Signed in successfully',
      padding: '2em',
    })
  
})

setTimeout(function (){
    if ($('#msg').length > 0) {
        $('#msg').remove();
    }
}, 4000 )

document.getElementById("copy-link-button-1").onclick = function() {
    inputField = document.getElementById('copy-input-link-1');
    inputField.select();
    document.execCommand('copy');
    document.getElementById('copy-link-button-1').innerHTML = "Copied";
}

document.getElementById("copy-link-button-2").onclick = function() {
    inputField = document.getElementById('copy-input-link-2');
    inputField.select();
    document.execCommand('copy');
    document.getElementById('copy-link-button-2').innerHTML = "Copied";
}

document.getElementById("copy-link-button-3").onclick = function() {
    inputField = document.getElementById('copy-input-link-3');
    inputField.select();
    document.execCommand('copy');
    document.getElementById('copy-link-button-3').innerHTML = "Copied";
}


Filevalidation = () => {
    const fi = document.getElementById('uploadimage');
    const upload_button = document.getElementById('uploadformbutton');

    var supported_ext = ['image/jpeg', 'image/jpg', 'image/png'];
    // Check if any file is selected.   size-alert
    if (fi.files.length > 0) {
        for (const i = 0; i <= fi.files.length - 1; i++) {

            const fsize = fi.files.item(i).size;
            // console.log(fext);
            const file = Math.round((fsize / 1024));
            // The size of the file.
            if (!supported_ext.includes(fi.files.item(i).type)){
                upload_button.disabled = true
                document.getElementById('size-alert').innerHTML = '<div class="alert alert-danger m-2" role="alert">We dont support this file format <a href="#">know more</a></div>';
            } else if (file >= 4096) {
                upload_button.disabled = true
                document.getElementById('size-alert').innerHTML = '<div class="alert alert-danger m-2" role="alert">File too Big, please select a file less than 4mb</div>';
            } else if (file < 10) {
                upload_button.disabled = true
                document.getElementById('size-alert').innerHTML = '<div class="alert alert-danger m-2" role="alert">File too small, please select a file greater than 128kb</div>';
            } else {
                document.getElementById('size').innerHTML = '<b>'
                + file + '</b> KB';
            }
        }
    }
}