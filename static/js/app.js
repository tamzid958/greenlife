if(window.location.pathname.toLowerCase() == "/searching/"){
   const urlParams = new URLSearchParams(window.location.search);
   const locationParam = urlParams.get('location');
   const bloodParam = urlParams.get('blood');
   const diseaseParam = urlParams.get('disease');

   if(locationParam != null) document.getElementById('location').value = locationParam;
   if(bloodParam != null) document.getElementById('blood').value = bloodParam;
   if(diseaseParam != null) document.getElementById('disease').value = diseaseParam;
}