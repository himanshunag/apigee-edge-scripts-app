const axios = require('axios');

const createReference = async (org, env, referenceName, referenceValue, apiKey) => {
    const url = `https://api.enterprise.apigee.com/v1/organizations/${org}/environments/${env}/references`;
    const data = {
        name: referenceName,
        value: referenceValue
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        console.log('Reference created successfully:', response.data);
    } catch (error) {
        console.error('Error creating reference:', error.response ? error.response.data : error.message);
        process.exit(1);
    }
};

// CLI entrypoint
if (require.main === module) {
    const [,, org, env, refName, refValue, token] = process.argv;
    if (!org || !env || !refName || !token) {
        console.error('Usage: node create_reference.js <org> <environment> <referenceName> <referenceValue> <accessToken>');
        process.exit(1);
    }
    createReference(org, env, refName, refValue || '', token);
}

module.exports = createReference;