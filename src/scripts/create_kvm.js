const axios = require('axios');

const createKVM = async (org, kvmName, environment, description, encrypted, entries, apiKey) => {
    // use enterprise management API host
    const url = `https://api.enterprise.apigee.com/v1/organizations/${org}/environments/${environment}/keyvaluemaps`;
    
    // Normalize entries: accept JSON array or parse if string
    let entryArray = [];
    if (typeof entries === 'string') {
        const trimmed = entries.trim();
        if (trimmed.startsWith('[')) {
            try {
                entryArray = JSON.parse(trimmed);
            } catch (e) {
                console.error('Failed to parse entries JSON:', e.message);
                process.exit(1);
            }
        }
    } else if (Array.isArray(entries)) {
        entryArray = entries;
    }

    const data = {
        name: kvmName,
        description: description,
        encrypted: (typeof encrypted === 'string' ? encrypted.toLowerCase() === 'true' : encrypted === true)
    }
    if (entryArray.length > 0) {
        data.entry = entryArray;
    }
    

    try {
        const payload = data;
        console.log('POST', url);
        console.log('Request payload:', JSON.stringify(payload, null, 2));
        
        const response = await axios.post(url, payload, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        console.log('KVM created successfully:', response.data);
    } catch (error) {
        console.error('Error creating KVM:', error.response ? error.response.data : error.message);
        process.exit(1);
    }
};

// CLI entrypoint
if (require.main === module) {
    const [,, org, kvmName, env, description, encrypted, entriesJson, token] = process.argv;
    if (!org || !kvmName || !env || !token) {
        console.error('Usage: node create_kvm.js <org> <kvmName> <environment> <description?> <encrypted?> <entriesJson?> <accessToken>');
        process.exit(1);
    }
    createKVM(org, kvmName, env, description || '', encrypted || false, entriesJson || '[]', token);
}

module.exports = createKVM;