const axios = require('axios');

async function createKeystore(org, keystoreName, environment, apiKey) {
    const url = `https://api.enterprise.apigee.com/v1/organizations/${org}/environments/${environment}/keystores`;
    
    const data = {
        name: keystoreName,
        // Add any additional parameters required for keystore creation
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        console.log('Keystore created successfully:', response.data);
    } catch (error) {
        console.error('Error creating keystore:', error.response ? error.response.data : error.message);
        process.exit(1);
    }
}

// CLI entrypoint when script is executed directly
if (require.main === module) {
    const [,, org, keystoreName, env, token] = process.argv;
    if (!org || !keystoreName || !env || !token) {
        console.error('Usage: node create_keystore.js <org> <keystoreName> <environment> <accessToken>');
        process.exit(1);
    }
    createKeystore(org, keystoreName, env, token);
}

module.exports = createKeystore;