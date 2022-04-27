/*********************************
 getUserMedia returns a Promise
 resolve - returns a MediaStream Object
 reject returns one of the following errors
 AbortError - generic unknown cause
 NotAllowedError (SecurityError) - user rejected permissions
 NotFoundError - missing media track
 NotReadableError - user permissions given but hardware/OS error
 OverconstrainedError - constraint video settings preventing
 TypeError - audio: false, video: false
 post_data - post data to flask api
 *********************************/
let post_address = "/receive";
let delay = 2000;
let save_file_format = `${new Date().toString()}.wav`;
let constraintObj = {audio: true};


if (navigator.mediaDevices === undefined) {
  navigator.mediaDevices = {};
  navigator.mediaDevices.getUserMedia = function (constraintObj) {
    let getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    if (!getUserMedia) {
      return Promise.reject(new Error("getUserMedia is not implemented in this browser"));
    }
    return new Promise(function (resolve, reject) {
      getUserMedia.call(navigator, constraintObj, resolve, reject);
    });
  };
} else {
  navigator.mediaDevices
    .enumerateDevices()
    .then((devices) => {
      devices.forEach((device) => {
        console.log(device.kind.toUpperCase(), device.label);
      })
    })
    .catch((err) => {
      console.log(err.name, err.message);
    });
}

navigator.mediaDevices
  .getUserMedia(constraintObj)
  .then(function (mediaStreamObj) {
    let start = document.getElementById('recordStart');
    let mediaRecorder = new MediaRecorder(mediaStreamObj);
    let chunks = [];

    start.addEventListener("click", () => {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      setTimeout(() => {
        mediaRecorder.stop();
        console.log(mediaRecorder.state);
      }, delay)
    })
    mediaRecorder.ondataavailable = function (ev) {
      chunks.push(ev.data);
    }
    mediaRecorder.onstop = () => {
      let blob = new Blob(chunks, {'type': 'audio/wav;'});
      post_data(blob)
      chunks = [];
    }
  })
  .catch(function (err) {
    console.log(err.name, err.message);
  });

function post_data(blob) {
  const fd = new FormData();
  const xhr = new XMLHttpRequest();

  xhr.open("POST", post_address, false);
  fd.append("file", blob, save_file_format);
  xhr.send(fd);
  console.log(xhr.responseText);
}
