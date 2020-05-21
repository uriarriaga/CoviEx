const webex = window.webex = Webex.init();
const token = document.getElementById("token").innerHTML;
console.log(token);
const destination = document.getElementById('destino').innerHTML;
console.log(destination);
webex.once('ready', function () {
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

            return joinMeeting(meeting);
        }


        // Join the meeting and add media
        function joinMeeting(meeting) {
            // Get constraints
            const constraints = {
                audio: true,
                video: true
            };

            return meeting.join().then(() => {
                return meeting.getSupportedDevices({
                    sendAudio: constraints.audio,
                    sendVideo: constraints.video
                })
                    .then(({ sendAudio, sendVideo }) => {
                        const mediaSettings = {
                            receiveVideo: false, //true
                            receiveAudio: true,
                            receiveShare: false,
                            sendShare: false,
                            sendVideo: false, //true
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

        document.getElementById('toogle-audio').addEventListener('click', () => {
            if (activeMeeting) {
                var video = document.getElementById('toogle-audio').value;
                if (video == "on") {
                    activeMeeting.muteAudio().then(() => {
                        console.log("Mute");
                        document.getElementById('toogle-audio').value = "off";
     

                        $("#mute").removeAttr("src").attr("src", "static/mute.png");
                    });
                } else {
                    activeMeeting.unmuteAudio().then(() => {
                        console.log("unMute");
                        document.getElementById('toogle-audio').value = "on";
                        $("#mute").removeAttr("src").attr("src", "static/mic.png");
             
                    });
                }
            }
        });

        document.getElementById('toogle-video').addEventListener('click', () => {
            if (activeMeeting) {
                var video = document.getElementById('toogle-video').value;
                if (video == "on") {
                    activeMeeting.muteVideo().then(() => {
                        console.log("Mute");
                        document.getElementById('toogle-video').value = "off";
                        document.getElementById('remote-view-video').style.visibility = 'hidden';
                        document.getElementById('self-view').style.visibility = 'hidden';
                        document.getElementById('self-view').style.height = '0px';
                        document.getElementById('remote-view-video').style.height = '0px';
                        document.getElementById('audioOnly').style.visibility = 'visible';
                        document.getElementById('audioOnly').style.height = '100px';
                        $("#videox").removeAttr("src").attr("src", "static/video-off.png");
                    });
                } else {
                    activeMeeting.unmuteVideo().then(() => {
                        console.log("unMute");
                        document.getElementById('toogle-video').value = "on";
                        document.getElementById('remote-view-video').style.visibility = 'visible';
                        document.getElementById('self-view').style.visibility = 'visible';
                        document.getElementById('self-view').style.height = "100px";
                        document.getElementById('remote-view-video').style.height = null;
                        document.getElementById('audioOnly').style.visibility = 'hidden';
                        document.getElementById('audioOnly').style.height = '0px';
                        $("#videox").removeAttr("src").attr("src", "static/video-on.png");
                    });
                }
            }
        });


        document.getElementById('destination').addEventListener('submit', (event) => {

            // again, we don't want to reload when we try to join
            event.preventDefault();

            return webex.meetings.create(destination).then((meeting) => {
                // Call our helper function for binding events to meetings
                activeMeeting = meeting;

                bindMeetingEvents(meeting);
            

            })
                .catch((error) => {
                    // Report the error
                    console.error(error);
                });
        });
    })
});
window.addEventListener('beforeunload', () => {
activeMeeting.leave()
});