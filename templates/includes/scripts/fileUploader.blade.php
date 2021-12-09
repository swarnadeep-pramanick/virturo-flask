<script id="dropify_script"  async=false defer=false src="{{ asset("assets/libs/dropify/js/dropify.min.js") }}"></script>
<script>
    let Upload = function (file, fileInput) {
        this.file = file;
        this.uploading = 0;
        let progress = fileInput.closest(".image-uploader").find(".upload.progress");
        progress.show();
        this.progressBar = progress.find(".progress-bar");
    };
    Upload.prototype.getType = function() {
        return this.file.type;
    };
    Upload.prototype.unlockForm = function(instance) {
        instance.progressBar.closest("form").find("button").prop("disabled", false);
    };
    Upload.prototype.lockForm = function() {
        this.progressBar.closest("form").find("button").prop("disabled", true);
    };
    Upload.prototype.getSize = function() {
        return this.file.size;
    };
    Upload.prototype.getName = function() {
        return this.file.name;
    };

    Upload.prototype.progressHandling = function (event, progressBar) {
        var percent = 0;
        var position = event.loaded || event.position;
        var total = event.total;
        if (event.lengthComputable) {
            percent = Math.ceil(position / total * 100);
        }
        progressBar.css("width", +percent + "%");
    };
    Upload.prototype.doUpload = function (callback) {
        if(typeof callback !== "function"){
            throw new Error("Supply a callback function to get the uploaded image path.");
        }
        var that = this;
        var formData = new FormData();
        formData.set("_token", "{{ csrf_token() }}");

        // add assoc key values, this will be posts values
        formData.append("file", this.file, this.getName());
        this.lockForm();

        $.ajax({
            type: "POST",
            url: "{{ route("cms.uploadFile") }}",
            xhr: function () {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    myXhr.upload.addEventListener('progress', e => that.progressHandling(e, that.progressBar), false);
                }
                return myXhr;
            },
            success: function (data) {
                that.unlockForm(that);
                if(data.success && data.path){
                    callback(data.path);
                }else{
                    showMessage("File Size Should not be greater than 12 MB", "error");
                    callback(false);
                }
                // your callback here
            },
            error: function (error) {
                // handle error
                that.unlockForm(that);
                callback(false);
                console.log(error)
            },
            async: true,
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
        });
    };
</script>
<script>
    function initializeFileUploads(){
        let fileInputs = $('[data-plugins="dropify"]');
        if (fileInputs.length > 0) {
            // Dropify
            fileInputs.each(function(){
                let fileInput = $(this);
                fileInput.closest(".image-uploader").append(`<div class="progress progress-sm upload mb-2"><div class="progress-bar progress-bar-striped bg-primary" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div></div>`);
                if(!fileInput.data("initdropify")){ //Only initialize if not already done so
                    fileInput.data("initdropify", true);
                    console.log(fileInput);
                    let dropifyInput = fileInput.dropify({
                        messages: {
                            'default': 'Drag and drop a file here or click',
                            'replace': 'Drag and drop or click to replace',
                            'remove': 'Remove',
                            'error': 'Ooops, something wrong appended.'
                        },
                    });
                    dropifyInput.on('dropify.afterClear', function(e, element){
                      let target = $(e.target);
                      let input = target.closest(".image-uploader").find(`.upload_input`).val("");
                    });

                    fileInput.on("change", function(e){
                        let target = $(e.target);
                        let type = target.data("type");
                        let input = target.closest(".image-uploader").find(`.upload_input`);
                        let files = e.target.files;
                        if(files.length){
                            let upload = new Upload(files[0], fileInput);
                            if(upload.getType().includes(type)){
                                upload.doUpload(function(path){
                                    if(path){
                                        input.val(path)
                                        input[0].dispatchEvent(new Event("uploaded"));
                                    }
                                });
                            }else{
                                setTimeout(() => target.parent().find(".dropify-clear").trigger("click"), 200);
                            }
                        }
                    });
                }
            })
        }
    }
    $(document).ready(
        $("#dropify_script").on("load",()=>{

            initializeFileUploads();
        })
        );
</script>
