
const webex = window.webex = Webex.init();

const token       = document.getElementById("token").innerHTML;
console.log(token);
const destination = document.getElementById('destino').innerHTML;
console.log(destination);

webex.once('ready', function() {
    webex.authorization.requestAccessTokenFromJwt({jwt: token})
      .then(() => {
                  
          webex.meetings.register()
          .catch((err) => {
            console.error(err);
            //alert(err);
            throw err;
          });

          function bindMeetingEvents(meeting) {
          meeting.on('error', (err) => {
           // console.error("XXXXXXX PUTO EL Q_Ue LO LEA ");
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


            try {
                  meeting.leave();
                } catch (error) {
                console.error(error);
                    // expected output: ReferenceError: nonExistentFunction is not defined
                    // Note - error messages will vary depending on browser
                }
        
          });

          console.log("llegamos al join meeting")
          return joinMeeting(meeting);

          }

          // Join the meeting and add media
          function joinMeeting(meeting) {
          return meeting.join().then(() => {
            const mediaSettings = {
              receiveVideo: true,
              receiveAudio: true,
              receiveShare: false,
              sendVideo: true,
              sendAudio: true,
              sendShare: false
            };

            // Get our local media stream and add it to the meeting
            return meeting.getMediaStreams(mediaSettings).then((mediaStreams) => {
              const [localStream, localShare] = mediaStreams;

              meeting.addMedia({
                localShare,
                localStream,
                mediaSettings
              });
            });
          });


          }

          document.getElementById('destination').addEventListener('submit', (event) => {


          
          // again, we don't want to reload when we try to join
          event.preventDefault();

          return webex.meetings.create(destination).then((meeting) => {
            // Call our helper function for binding events to meetings
            bindMeetingEvents(meeting);
            
            
          })
          .catch((error) => {
            // Report the error
            console.error(error);
           
          });
          });
      })
});
