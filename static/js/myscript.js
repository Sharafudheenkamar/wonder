const input = document.getElementById('image-upload');

document.getElementById('image-upload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-pic').src = e.target.result;
            document.getElementById('save').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});
// Submit the form when the save button is clicked
document.getElementById('save').addEventListener('click', function() {
    document.getElementById('profile-form').submit();
});

//   add place modal
  var modal = document.getElementById("addPlaceModal");
    var btn = document.getElementById("addplace");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
        modal.style.display = "block";
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    
    // Handle modal display and close
window.onclick = function(event) {
    var addPlaceModal = document.getElementById("addPlaceModal");
    var changeUsernamePasswordModal = document.getElementById("changeUsernamePasswordModal");

    if (event.target == addPlaceModal) {
        addPlaceModal.style.display = "none";
    }
    if (event.target == changeUsernamePasswordModal) {
        changeUsernamePasswordModal.style.display = "none";
    }
}

// Handle modal open
document.getElementById("addplace").onclick = function() {
    document.getElementById("addPlaceModal").style.display = "block";
}

// Handle modal open
document.getElementById("editprofile").onclick = function() {
    document.getElementById("editProfileModal").style.display = "block";
}

document.getElementById("changeUsernamePassword").onclick = function() {
    document.getElementById("changeUsernamePasswordModal").style.display = "block";
}

var editProfileModal = document.getElementById("editProfileModal");
var closeModal = editProfileModal.getElementsByClassName("close")[0];
closeModal.onclick = function() {
    editProfileModal.style.display = "none";
}
var closepasswordModal = changeUsernamePasswordModal.getElementsByClassName("close")[0];
closepasswordModal.onclick = function() {
    changeUsernamePasswordModal.style.display = "none";
}
// Close modal when clicking outside the modal
window.onclick = function(event) {
    if (event.target == editProfileModal) {
        editProfileModal.style.display = "none";
    }
    if (event.target == changeUsernamePasswordModal) {
        changeUsernamePasswordModal.style.display = "none";
    }
    if (event.target == addPlaceModal) {
        addPlaceModal.style.display = "none";
    }
}
