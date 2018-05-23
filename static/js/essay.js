
$(document).ready(function(){
 $('#notice').hide();  
 $('#submit').attr("disabled");
$('#all').prop("checked", true);
});
$('#repeater').focusout(function(){
    
    input1=$('#tel').val();
    input2=$('#repeater').val();
    if(input1!=input2){
        $('#submit').attr("disabled");
        $('#notice').show();
    }
    else{
        $('#notice').hide();
        $('#submit').removeAttr("disabled");
    }
});
$('#myTabs a').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
});
$('input:radio[name="usage"]').change(function(){
        if($(this).val() == 'email') {
          $('#email').show();
          $('#tel').hide();
          $('#repeater').hide();
        }
        if($(this).val() == 'tel'){
          $('#email').hide();
          $('#tel').show();
          $('#repeater').show();
        }
        if($(this).val() == 'all'){
          $('#email').show();
          $('#tel').show();
          $('#repeater').show();
        }
        
    });
