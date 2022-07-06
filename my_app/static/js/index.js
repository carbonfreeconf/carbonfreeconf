//import { ZoomMtg } from '@zoomus/websdk';
//ZoomMtg.setZoomJSLib('https://dmogdx0jrul3u.cloudfront.net/1.8.1/lib', '/av');
ZoomMtg.setZoomJSLib('https://source.zoom.us/1.8.3/lib', '/av');
ZoomMtg.preLoadWasm();
ZoomMtg.prepareJssdk();

// make an http request to your server to get the signature
const meetConfig = {
        apiKey: 'dlDAD3ZyRUiT8zM3uxPU3g',
        meetingNumber: 95429066648,
        leaveUrl: 'https://www.carbonfreeconf.com/',
        userName: 'Quentin Kral',
        userEmail: 'admin@carbonfreeconf.com',
        passWord: '45DhmN', // if required
        role: 0, // 1 for host; 0 for attendee
        };

function getSignature(meetConfig){
	fetch('signaturezoom', {
			method: 'POST',
			body: JSON.stringify({ meetingData: meetConfig })
		})
		.then(result => result.text())
		.then(response => {
			ZoomMtg.init({
				leaveUrl: meetConfig.leaveUrl,
				isSupportAV: true,
				success: function() {
				    console.log('sig'+response)
					ZoomMtg.join({
						signature: response,
						apiKey: meetConfig.apiKey,
						meetingNumber: meetConfig.meetingNumber,
						userName: meetConfig.userName,
						// password optional; set by Host
						passWord: meetConfig.passWord,
						error(res) {
							console.log(res)
						}
					})
				}
			})
	})
}

getSignature(meetConfig);
