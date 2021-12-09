//Get Added Custom Fields for Second Slide
var event_id = $('#event_id').val();
var dataId = [];
var checkboxes = [];
let customFieldUrl = "http://localhost:8000/Eventee/Form/CustomFields";
let SaveFieldUrl = "http://localhost:8000/Eventee/Form/SaveField";
let CustomSaveField = "http://localhost:8000/Eventee/Form/SaveCustomFields";
let FinalPreview = "http://localhost:8000/Eventee/Form/preview";
let deleteUrl = "http://localhost:8000/Eventee/Form/Delete";
function customField(){
    // var weburl = "{{route('eventee.form.custom'),:id}}";
    // weburl.replace(':id',event_id);
    $.ajax({
        url:customFieldUrl,
        method:'post',
        data:{'event_id':event_id},
        success:function(fields){
           if(fields.code == 200){
            $('#second-tbody').empty();
            //    console.log(fields.field);
               $.each(fields.field,function(index,value){
                   $('#second-tbody').append('<tr><td><input onclick="getSecondID(this)" class="checkNotDone" type="checkbox" data-id="'+ value.id +'" value="0" >&nbsp; '+value.label+' </td><td><input type="text" class="placeholder2 placeholder form-control" placeholder="Enter The placeholder name" required></td><td>'+value.type+' </td><td><input type="checkbox" name="'+value.label +' " onclick="Check2(this)" ></td></tr>');
               });
           }
           else{
                $('#second-tbody').append('<tr><td colspan="4">There Are No Custom Field Available</td></tr>')
           }
        },
        error:function(message){
            alert('Not connected');
        }
    });
}
//CheckBox Of Custom Fields
function getSecondID(e){
    if(e.value == 0){
        var id = e.getAttribute('data-id');
        dataId.push(id);
        e.setAttribute('class','CheckDone');
        e.value = 1;
    }
   else{
        e.value = 0;
        e.setAttribute('class','CheckNotDone');
        var index = dataId.indexOf(fieldId);
        if(index >= 0){
            ids.splice(index,1);
        }   
   }
}

function check2(e){
    if(e.value == 0){
        e.value = 1;
        checkboxes.push(1);
    }
    else{
        e.value = 0;
        checkboxes.pop();
    }
}

function submitForm2(){
    if(dataId.length === 0){
        alert("Please Select Fields First");
    }
    else{
        var field = document.getElementsByClassName('placeholder2');
        var checkbox = document.getElementsByClassName('check');
        var form_id = $('#form_id').val();
        var placeholder = [];

        if((field) != "" && $('.CheckDone').prop("checked", true)){
            $('.placeholder2').each(function(){
               
                 if($(this).val() != "" ){
                 placeholder.push($(this).val());
                 $('#place-error').removeClass('errors');
                 $('#place-error').addClass('notshow');
               }
               
               
            });

            $.ajax({
                url:CustomSaveField,
                method:"POST",
                data:{'event_id':event_id,"fields":dataId,'placeholder':placeholder,'required':required,'form_id':form_id},
                success:function(response){
                    if(response.code ===200){
                        $('#form_id').val(response.form_id);
                        AllFields();
                        $('#second-box').fadeOut('fast');
                        $('#third-box').fadeIn('fast');
                    }
                    else if(response.code == 403){
                        alert(response.message);
                        window.location.reload();
                    }
                    else{
                        alert(response.message);
                    }
                }
            });
        }


    }
}


function SaveCustomField(){
    let label = $('#label').val();
    let type = $('#type').val();
    $.ajax({
        url:SaveFieldUrl,
        method:"POST",
        data:{'event_id':event_id,'label':label,'type':type},
        success:function(response){
            if(response.code == 200){
                customField();
                $('#exampleModal').modal('toggle');
                // alert("Field Added Successfully");
            }
            else{
                alert("Something Went Wrong");
            }
            
        }
    });
}


//Third Wizard
function AllFields(){
    $.ajax({
        url:FinalPreview,
        method:"POST",
        data:{'event_id':event_id},
        success:function(res){
            $('#third-tbody').empty();
            if(res.code == 200){
                $.each(res.fields,function(index,value){
                    if(value.required == 1){
                        $('#third-tbody').append('<tr><td>'+ value.label+'</td><td colspan = "4"><center><input class="form-control" type="'+ value.type +'" placeholder="'+value.placeholder+'" required></center></td></tr>');
                    }
                    else{
                        $('#third-tbody').append('<tr><td>'+ value.label+'</td><td colspan = "4"><center><input class="form-control" type="'+ value.type +'" placeholder="'+value.placeholder+'"></center></td></tr>');
                    }
                });
            }
            else{
                $('#third-tbody').append('<tr><td colspan = "4"><center>Sorry No Field Found</center></td></tr>')
            }
        }
    });

}

function confiemDelete(e){
    let formId = e.getAttribute('data-id');
    confirmDelete("Are you sure you want to DELETE Form?","Confirm Form Delete").then(confirmation=>{
        if(confirmation){
            $.ajax({
                url:deleteUrl,
                data: {
                    "form_id":formId
                },
                method:"POST",
                success: function(res){
                    if(res.code ==200){
                        e.closest("tr").remove();
                    }
                    else{
                        alert("Something went wrong");
                    }
                    
                }
            })
        }
    });
}