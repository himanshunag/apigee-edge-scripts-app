const axios = require('axios');

// Basic auth header as provided (edgecli:edgeclisecret base64)
const BASIC_AUTH = 'Basic ZWRnZWNsaTplZGdlY2xpc2VjcmV0';

async function getToken(username, password) {
    try {
        const resp = await axios.post('https://login.apigee.com/oauth/token',
            new URLSearchParams({
                grant_type: 'password',
                username,
                password
            }).toString(),
            {
                headers: {
                    'Accept': 'application/json;charset=utf-8',
                    'Authorization': BASIC_AUTH,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        );
        console.log(JSON.stringify(resp.data, null, 2));
    } catch (err) {
        if (err.response) {
            console.error('Error response:', err.response.status, err.response.data);
        } else {
            console.error('Request error:', err.message);
        }
        process.exit(1);
    }
}

// main
const [,, user, pwd] = process.argv;
if (!user || !pwd) {
    console.error('Usage: node access_token.js <username> <password>');
    process.exit(1);
}

getToken(user, pwd);
