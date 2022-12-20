const homepageLikeBtns = document.querySelectorAll("[id^='home-like-button']")
for (const homepageLikeBtn of homepageLikeBtns){
    
    homepageLikeBtn.addEventListener('click', homepageLike)

function homepageLike(evt) {
    getPhotoId = evt.target.id.split("-");
    photoId=getPhotoId[3];
    el = document.getElementById(`home-like-button-${photoId}`)
    fetch(`/like/${photoId}`, { method: "POST" })
      .then((response) => response.text())
      .then((data) => {
        console.log(data)
        if (data["liked"] === "True") {
            el.className = "fa-solid fa-heart";
        }
        else  {
            el.className = "fa-regular fa-heart";
          }
})
}

}
const likeButton = document.querySelector('#like-button');


function like() {

    const likeCount = document.querySelectorAll('#likes-count');
    // const likeButton = document.querySelectorAll('#like-button');
    locationPath = window.location.pathname.split("/");
    photoId=parseInt(locationPath[2])
    
    fetch(`/like/${photoId}`, { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        likeCount.innerHTML = data["likes"];
        
        if (data["liked"] === "True") {
          likeButton.className = "fa-solid fa-heart";
        } else {
          likeButton.className = "fa-regular fa-heart";
        }
      })
  }
 if (likeButton) {
     likeButton.addEventListener('click',like);
 }


const deletePhotoBtn = document.querySelector('#delete-photo')

function deletePhoto() {
    locationPath = window.location.pathname.split("/");
    photoId=parseInt(locationPath[2])

    fetch(`/delete_photo/${photoId}`, { method: "POST" })
      .then((response) => response.text())
      .then((data) => {
        window.location.href = "http://localhost:5000";
})
}

if (deletePhotoBtn) {
    deletePhotoBtn.addEventListener('click',deletePhoto);
} 

const deleteCommentBtns = document.querySelectorAll("[id^='delete-comment']")
for (const deleteCommentBtn of deleteCommentBtns){
    
    deleteCommentBtn.addEventListener('click', deleteComment)

}


function deleteComment(evt) {
    getCommentId = evt.target.id.split("-");
    commentId=getCommentId[2];

    fetch(`/delete_comment/${commentId}`, { method: "POST" })
      .then((response) => response.text())
      .then((data) => {
        window.location.reload() ;
})
}

// fetch data from server to check if user is already following this user
// if following, display the unfollow button. 
// if not following display the follow button. 

function followUser (evt) {
  const followBtnsStatuses = document.querySelectorAll(".followBtnStatus")
  getFollowingUser = evt.target.id.split("-");
  FollowingUserId = getFollowingUser[2];
  
  fetch(`/follow/${FollowingUserId}`, { method: "POST" })
  .then((response) => response.json())
  .then((data) => {
       
        if (data["followed"] === true) {
          for (const followBtnStatus of followBtnsStatuses)

          followBtnStatus.className = "fa-solid fa-user-minus"          
        } 
        else 
        {
          for (const followBtnStatus of followBtnsStatuses)
          followBtnStatus.className = "fa-solid fa-user-plus";
          
        }
        
      })

}
const followBtns = document.querySelectorAll("[id^='follow-btn']")

for (const followBtn of followBtns){
    
  followBtn.addEventListener('click', followUser)

}

// direct user to location page
const addLocationBtn = document.querySelector('#add-location')
const locationBtns = document.querySelector('#location-btn')

function toLocationPage(evt) {
  const getPhotoId = locationPath = window.location.pathname.split("/")
  const photoId = getPhotoId[2]
  console.log(window.location.pathname)
  window.location.href = "http://localhost:5000/to_location/"+photoId
}
if (addLocationBtn){
    addLocationBtn.addEventListener('click', toLocationPage)
}
if (locationBtns){
   locationBtns.addEventListener('click',locationPage)
   
}

// autocomplete feature

const autocompleteInput = document.querySelector('#autocomplete')

let autocomplete;

function initAutocomplete(){
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'),
    {
      fields:['name', 'place_id','geometry','formatted_address']
    }
    
    );
    autocomplete.addListener('place_changed', onPlaceChanged); 

  }
  

  if (autocompleteInput){
    autocompleteInput.addEventListener('input', initAutocomplete)

  }
  
// Get place information e.g. placeId lat,lng formatted address. 

function onPlaceChanged(evt){
   let place = autocomplete.getPlace();
   let name = place.name
   let lat = place.geometry.location.lat();
   let lng = place.geometry.location.lng();
   let placeId = place.place_id;
   let getPhotoId = window.location.pathname.split('/');
   let photoId = getPhotoId[2]


   console.log(place)
   console.log(place.geometry.location.lat())
   let geolocation = place.formatted_address
       document.getElementById('output').innerHTML = geolocation;
        document.getElementById('lat').value = lat; 
        document.getElementById('lng').value = lng;
        document.getElementById('place-id').value= placeId;
        document.getElementById('photo-id').value=photoId
        document.getElementById('name').value=name
}

function locationPage() {
  const getPhotoId = locationPath = window.location.pathname.split("/")
  const photoId = getPhotoId[2]
  fetch(`/location/${photoId}`, { method: "POST" })
  .then((response) => response.json())
  .then((data) => {
    console.log(data.name)
    let lat = data.lat
    window.location.href = "http://localhost:5000/location/"+photoId 
    
    })
}
    
function initMap()  {
  const getPhotoId = locationPath = window.location.pathname.split("/")
  const photoId = getPhotoId[2]
    fetch(`/location/${photoId}`, { method: "POST" })
  .then((response) => response.json())
  .then((data) => {
    console.log(data)
    const photoImg = data.photo_img
    const locationCoords = { lat: data.lat, lng: data.lng };
    document.querySelector('#place-name').innerHTML = data.name;
    
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: locationCoords,
    });
    const contentString = `${data.name}  <div >
    <img id="infoWinImg"
      src="${photoImg}"
      alt="${data.name}"
    />
  </div>`
    
    

  const infowindow = new google.maps.InfoWindow({
    content: contentString 
  });
    
    const marker = new google.maps.Marker({
        position: locationCoords,
        map: map,
        title:data.name
    });
    
    marker.addListener("click", () => {
        infowindow.open({
          anchor: marker,
          map,
        });
})
})
}

function initAccountMap()  {
    const map = new google.maps.Map(document.getElementById("account-map"), {
        zoom: 2,
        center: {lat:39, lng:34},
    });
    const accountMapInfo = new google.maps.InfoWindow();

    const getUserId = locationPath = window.location.pathname.split("/")
    const userId = getUserId[2]
      fetch(`/account_map/${userId}`, { method: "POST" })
    .then((response) => response.json())
    .then((locations) => {
            for (const location of Object.values(locations)){
                const contentString = `${location.name}  <div >
                <img id="infoWinImg"
                src="${location.imgurl}"
                alt="${location.name}"
                />
                `;

                const accountMapMarker = new google.maps.Marker({
        position: {lat:location.lat, lng:location.lng},
        map: map,
        title:location.name
    });
        accountMapMarker.addListener('click', () => {
            accountMapInfo.close();
            accountMapInfo.setContent(contentString);
            accountMapInfo.open(map, accountMapMarker);
            
        });
    }})
}
            
            
 
    