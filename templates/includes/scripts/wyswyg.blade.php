<script src="http://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.2/summernote.js"></script>
<script src="javascript/common.js" type="text/javascript"></script>

<script src={{ asset("../assets/libs/summernote-bs4.min.js"  )}} ></script>
<script type="text/javascript">
$('#summernote-basic').summernote({
    placeholder: 'Write something...',
    height: 230,
    maximumImageFileSize: 500*1024, // 500 KB
    callbacks: {
        // fix broken checkbox on link modal
        onInit: function onInit(e) {
            var editor = $(e.editor);
            editor.find('.custom-control-description').addClass('custom-control-label').parent().removeAttr('for');
        }
    },
    toolbar: [['style', ['style']],['font', ['bold', 'underline', 'clear']],['fontname', ['fontname']],['color', ['color']],['para', ['ul', 'ol', 'paragraph']],['table', ['table']],['insert', ['link', 'picture', 'video']],['view', ['fullscreen', 'codeview', 'help']],],
});
$('#summernote-basic-2').summernote({
    placeholder: 'Write something...',
    height: 230,
    maximumImageFileSize: 500*1024, // 500 KB
    callbacks: {
        // fix broken checkbox on link modal
        onInit: function onInit(e) {
            var editor = $(e.editor);
            editor.find('.custom-control-description').addClass('custom-control-label').parent().removeAttr('for');
        }
    }
});
</script>
