
var webex = Webex.init();

const token = document.getElementById("token").innerHTML;
console.log(token);
const destination = document.getElementById('destino').innerHTML;
console.log(destination);

webex.once(`ready`, function () {
    webex.authorization.requestAccessTokenFromJwt({ jwt: token })
        .then(() => {

            webex.meetings.register()
                .catch((err) => {
                    console.error(err);
                    alert(err);
                    throw err;
                });

            function bindMeetingEvents(meeting) {
                meeting.on('error', (err) => {
                    console.error(err);
                });

                // Handle media streams changes to ready state
                meeting.on('media:ready', (media) => {
                    if (!media) {
                        return;
                    }
                    if (media.type === 'local') {
                        document.getElementById('self-view').srcObject = media.stream;
                    }
                    if (media.type === 'remoteVideo') {
                        document.getElementById('remote-view-video').srcObject = media.stream;
                    }
                    if (media.type === 'remoteAudio') {
                        document.getElementById('remote-view-audio').srcObject = media.stream;
                    }
                });

                // Handle media streams stopping
                meeting.on('media:stopped', (media) => {
                    // Remove media streams
                    if (media.type === 'local') {
                        document.getElementById('self-view').srcObject = null;
                    }
                    if (media.type === 'remoteVideo') {
                        document.getElementById('remote-view-video').srcObject = null;

                    }
                    if (media.type === 'remoteAudio') {
                        document.getElementById('remote-view-audio').srcObject = null;
                    }
                });

                // Of course, we'd also like to be able to leave the meeting:
                document.getElementById('hangup').addEventListener('click', () => {
                    meeting.leave();
                });
            }


            // Join the meeting and add media
            function joinMeeting(meeting) {
                // Get constraints
                const constraints = {
                    audio: document.getElementById('constraints-audio').checked,
                    video: document.getElementById('constraints-video').checked
                };

                return meeting.join().then(() => {
                    return meeting.getSupportedDevices({
                        sendAudio: constraints.audio,
                        sendVideo: constraints.video
                    })
                        .then(({ sendAudio, sendVideo }) => {
                            const mediaSettings = {
                                receiveVideo: constraints.video,
                                receiveAudio: constraints.audio,
                                receiveShare: false,
                                sendShare: false,
                                sendVideo: true,
                                sendAudio: true
                            };

                            // Get our local media stream and add it to the meeting
                            return meeting.getMediaStreams(mediaSettings).then((mediaStreams) => {
                                const [localStream, localShare] = mediaStreams;

                                meeting.addMedia({
                                    localShare,
                                    localStream,
                                    mediaSettings
                                });

                            })

                        })
                });
            }
            
            document.getElementById('start-sending-audio').addEventListener('click', () => {
                if (activeMeeting) {
                  activeMeeting.unmuteAudio().then(() => {
                    document.getElementById('microphone-state').innerHTML = 'on';
                  });
                }
              });
        
              document.getElementById('stop-sending-audio').addEventListener('click', () => {
                if (activeMeeting) {
                  activeMeeting.muteAudio().then(() => {
                    document.getElementById('microphone-state').innerHTML = 'off';
                  });
                }
              });
        
              document.getElementById('start-sending-video').addEventListener('click', () => {
                if (activeMeeting) {
                  activeMeeting.unmuteVideo().then(() => {
                    document.getElementById('camera-state').innerHTML = 'on';
                  });
                }
              });
        
              document.getElementById('stop-sending-video').addEventListener('click', () => {
                if (activeMeeting) {
                  activeMeeting.muteVideo().then(() => {
                    document.getElementById('camera-state').innerHTML = 'off';
                  });
                }
              });


            document.getElementById('destination').addEventListener('submit', (event) => {

                // again, we don't want to reload when we try to join
                event.preventDefault();

                return webex.meetings.create(destination).then((meeting) => {
                    // Call our helper function for binding events to meetings
                    bindMeetingEvents(meeting);

                    return joinMeeting(meeting);
                })
                    .catch((error) => {
                        // Report the error
                        console.error(error);
                    });
            });
        })
});


window.addEventListener('load', () => {
    // Get elements from the DOM
    const audio = document.getElementById('constraints-audio');
    const video = document.getElementById('constraints-video');

    // Get access to hardware source of media data
    // For more info about enumerateDevices: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/enumerateDevices
    if (navigator && navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        navigator.mediaDevices.enumerateDevices()
            .then((devices) => {
                // Check if navigator has audio
                const hasAudio = devices.filter(
                    (device) => device.kind === 'audioinput'
                ).length > 0;

                // Check/uncheck and disable checkbox (if necessary) based on the results from the API
                audio.checked = hasAudio;
                audio.disabled = !hasAudio;

                // Check if navigator has video
                const hasVideo = devices.filter(
                    (device) => device.kind === 'videoinput'
                ).length > 0;

                // Check/uncheck and disable checkbox (if necessary) based on the results from the API
                video.checked = hasVideo;
                video.disabled = !hasVideo;
            })
            .catch((error) => {
                // Report the error
                console.error(error);
            });
    }
    else {
        // If there is no media data, automatically uncheck and disable checkboxes
        // for audio and video
        audio.checked = false;
        audio.disabled = true;

        video.checked = false;
        video.disabled = true;
    }
});





window.addEventListener('beforeunload', () => {
    activeMeeting.leave()

});