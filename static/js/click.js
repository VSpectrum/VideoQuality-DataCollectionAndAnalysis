var userrateArr = [];
var ratedateArr = [];
var keepgoing = true;

$(document).keyup(function(event){
    if(event.which == 66) $("#BadAud").click();
    if(event.which == 78) $("#BadVid").click();
    if(event.which == 77) $("#BadA_V").click();
});

$("#BadA_V").click(function(){
    var currentdatetime = new Date();
    userrateArr.push("A");
    ratedateArr.push(currentdatetime);

    userrateArr.push("V");
    ratedateArr.push(currentdatetime);
});

$("#BadAud").click(function(){
    var currentdatetime = new Date();
    userrateArr.push("A");
    ratedateArr.push(currentdatetime);
});

$("#BadVid").click(function(){
    var currentdatetime = new Date();
    userrateArr.push("V");
    ratedateArr.push(currentdatetime);
});




myVid = document.getElementById("myVid");
var video = $("#myVid"), //jquery-wrapped video element
    mousedown = false;

video.on('play', function () {
    var currentdatetime = new Date();

    userrateArr.push("ST");
    ratedateArr.push(currentdatetime); //start

    window.setTimeout(wrapup, 30000);
}); 

function wrapup(){
    keepgoing = false;
    myVid.pause();
    document.getElementById("SubmBtn").disabled = false;
    document.getElementById("BadAud").disabled = true;
    document.getElementById("BadVid").disabled = true;
    document.getElementById("BadA_V").disabled = true;
}


video.on('pause', function () {
    if(keepgoing) myVid.play();
});


$('#SubmBtn').click(function(){
    for (var i = 0; i < userrateArr.length; i++) {
        console.log(userrateArr[i]);
    }

    var id = '';
    for(id = ''; id.length < 32;) id += Math.random().toString(36).substr(2, 1);

    $.ajax({
        type: "POST",
        url: 'recvData',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            ratings: JSON.stringify(userrateArr),
            daterate: JSON.stringify(ratedateArr),
            userid: id,
            usergender: $('input[name="gender"]:checked').val(),
            userage: $('#age').val(),
        },
        success: function(data) {
            alert("Successfully completed");

            document.getElementById("SubmBtn").disabled = true;
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error Occurred");

            document.getElementById("SubmBtn").disabled = true;
        }
    });
});



$( document ).ready(function() {
    var r = new XMLHttpRequest();
    r.onload = function() {
        myVid.src = URL.createObjectURL(r.response);
        //ready
        $("#cover").fadeOut(100); //after done.
    };
    if (myVid.canPlayType('video/mp4;codecs="avc1.42E01E, mp4a.40.2"')) {
        r.open("GET", "{% static 'vid/calib_vid.mp4' %}");
    }
    else {
        //error
    }
    r.responseType = "blob";
    r.send();

    $("#cover").fadeIn(100);
    alert("Loading Calibration Video (3MB)");
});