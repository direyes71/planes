
$(document).ready(function(e){



    function onPopupDragStart(e) { 			

 			
 	}
 	
if (typeof onMapClick  !=  "undefined")
 	miObjeto.map.on('click', onMapClick);
});


function Planes(container){
	this.container =  container;
 	//this.map = L.map(container).setView([0, 0], 1);
 	this.pos_x = 0.5440;
 	this.pos_y = 0.5440;
 	this.popup = L.popup();
 	this.map  = L.map(this.container).setView([0, 0], 2);

	
 	this.setMap =  function (fotos,_minZoom,_maxZoom){
 		L.tileLayer(fotos+'/{z}/{x}/{y}.jpg', {
 			minZoom: parseInt(_minZoom),
 			maxZoom: parseInt(_maxZoom),
            noWrap: true
 		}).addTo(this.map);
 	}

 	this.getX = function (){
 		return this.pos_x;
 	}

 	this.getY =  function(){
 		return this.getY;
 	}

 	this.createMarker =  function (pos_x,pos_y,messaje,link,titleLink,id,details,tMarker){
 		
 		tMarker = tMarker || 0;

 		var iconURL = '/static/planes/icons/icon1.png';
 		var shadowUrl = '/static/planes/icons/leaf-shadow.png';
 		
 		if (tMarker == 1){
			iconURL = "/static/planes/icons/icon1.png";
 			shadowUrl = "/static/planes/icons/icon1s.png";
 		};

 		if (tMarker == 2){
			iconURL = "/static/planes/icons/icon2.png";
 			shadowUrl = "/static/planes/icons/icon2s.png";
 		};

 		if (tMarker == 3){
			iconURL = "/static/planes/icons/icon3.png";
 			shadowUrl = "/static/planes/icons/icon3s.png";
 		};

 		if (tMarker == 4){
			iconURL = "/static/planes/icons/icon4.png";
 			shadowUrl = "/static/planes/icons/icon4s.png";
 		};

 		if (tMarker == 5){
			iconURL = "/static/planes/icons/icon5.png";
 			shadowUrl = "/static/planes/icons/icon5s.png";
 		};

 		if (tMarker == 6){
			iconURL = "/static/planes/icons/icon6.png";
 			shadowUrl = "/static/planes/icons/icon6s.png";
 		};

 		if (tMarker == 7){
			iconURL = "/static/planes/icons/icon7.png";
 			shadowUrl = "/static/planes/icons/icon7s.png";
 		};

 		if (tMarker == 8){
			iconURL = "/static/planes/icons/icon8.png"; 			
 		};

 		if (tMarker == 9){
			iconURL = "/static/planes/icons/icon9.png"; 			
 		};


 		var icon = L.icon({
		    iconUrl: iconURL,		    
		    iconSize:     [24, 24], // size of the icon		    
		    iconAnchor:   [5, 17], // point of the icon which will correspond to marker's location		    
		    popupAnchor:  [5, -27] // point from which the popup should open relative to the iconAnchor
		});


         details.seeMore = details.seeMore || 0;
         details.delete = details.delete || 0;
         
         var marker = L.marker([parseFloat(pos_x),parseFloat(pos_y)],{icon: icon});
         var content = "";
         content = "<div style='text-align: center; width: 100%; font-weight: 900;'>"+messaje+"! <br>";
         if (details.see_more == 1){
             content += "<a href=\""+link+"\"> "+titleLink+"</a>";
         }

         // To remove marker
         marker.id = id;
         marker.label = messaje;
         if (details.delete == 1){
             content += "<a href=# id=\"point_"+id+"\" class='delete_marker'> Eliminar</a>";
         }
         content += "</div>";
         marker.addTo(this.map).bindPopup(content);
 	}

 	this.loadPoint = function(service){
	    var miFunction = this.createMarker;
 	}

 	this.getPoints = function (){
 	}


    
	
}