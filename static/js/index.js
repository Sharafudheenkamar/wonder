$(document).ready(function () {
    //story slider
    $(".slider").owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        smartSpeed: 1000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 5
            }
        }
    });

    var owl = $(".slider");
    owl.owlCarousel();
    // Go to the next item
    $(".nxtBtn").click(function () {
        owl.trigger("next.owl.carousel");
    });





    $(".rooms").owlCarousel({
        loop: true,
        margin: 5,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        smartSpeed: 1000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 10
            }
        }
    });




    $(".people").owlCarousel({
        loop: true,
        margin: 5,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 3000,
        smartSpeed: 1000,
        autoplayHoverPause: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 3.5
            }
        }
    });


});

//function toggleMoreGroup() {
//    var moreGroups = document.getElementById("more-groups");
//    var seeMoreText = document.getElementById("see-more-text");
//
//    if (moreGroups.style.display === "none") {
//        moreGroups.style.display = "block";
//        seeMoreText.innerText = "See less";
//    } else {
//        moreGroups.style.display = "none";
//        seeMoreText.innerText = "groups";
//    }
//}
//function redirectToCreatePostPage() {
//    // Redirect to the create post page
//
//    window.location.href = "/client/loadaddpost"; // Replace "createpost.html" with your actual page URL
//}

function openImageDialog() {
    document.getElementById("file").click();
}

document.getElementById("file").addEventListener("change", function(event) {
    var file = event.target.files[0];
    var imageDiv = document.querySelector(".image-div");

    // Check if a file was selected
    if (file) {
        // Check if the selected file is an image
        if (file.type.startsWith("image/")) {
            var reader = new FileReader();
            reader.onload = function() {
                var img = document.createElement("img");
                img.src = reader.result;
                imageDiv.innerHTML = ""; // Clear previous content
                imageDiv.appendChild(img); // Append the new image
            };
            reader.readAsDataURL(file);
        } else {
            // Alert the user if the selected file is not an image
            alert("Please select an image file.");
        }
    }
});

function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
}
function displayComments(postId) {
    var commentDiv = document.getElementById('comment-div-' + postId);
    console.log(postId)
    if (commentDiv.style.display === 'none') {
        commentDiv.style.display = 'block';
    } else {
        commentDiv.style.display = 'none';
    }
}

