if(window.location.pathname.toLowerCase() == "/searching/"){
   const urlParams = new URLSearchParams(window.location.search);
   const locationParam = urlParams.get('location');
   const bloodParam = urlParams.get('blood');
   const diseaseParam = urlParams.get('disease');

   if(locationParam != null) $("#location").value = locationParam;
   if(bloodParam != null) $("#blood").value = bloodParam;
   if(diseaseParam != null) $("#disease").value = diseaseParam;
}
if(window.location.pathname.toLowerCase() == "/donation_list/"){
   $(".review-btn").on('click', function (){
      var id = $(this).attr('data-bs-donation-id');
      $('#donation_id').val(id).change();
   });
}