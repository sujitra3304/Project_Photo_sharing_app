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

const locationBtns = document.querySelector('#location-btn')

function toLocationPage(evt) {
  const getPhotoId = locationPath = window.location.pathname.split("/")
  const photoId = getPhotoId[2]
  console.log(window.location.pathname)
  window.location.href = "http://localhost:5000/location/"+photoId
}
if (locationBtns){
   locationBtns.addEventListener('click',toLocationPage)
   
}

// autocomplete feature

const autocompleteInput = document.querySelector('#autocomplete')

let autocomplete;

function initAutocomplete(){
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('autocomplete'),
    {
      fields:['place_id','geometry','formatted_address']
    }
    
    );
    autocomplete.addListener('place_changed', onPlaceChanged); 

  }
  


  autocompleteInput.addEventListener('input', initAutocomplete)

// Get place information e.g. placeId lat,lng formatted address. 

function onPlaceChanged(evt){
   let place = autocomplete.getPlace();
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

  //  if (!place.geometry){
  //   document.getElementById('autocomplete').placeholder = 'Enter Location';
  //  }
  //  else {
  //   document.getElementById('output').innerHTML = place.formatted_address;
  //  }
}

function initMap() {
  const getPhotoId = locationPath = window.location.pathname.split("/")
  const photoId = getPhotoId[2]
  fetch(`/follow/${FollowingUserId}`, { method: "POST" })
  .then((response) => response.json())
  .then((data) => {
    console.log (data)
  
  
  
  
  })

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}


