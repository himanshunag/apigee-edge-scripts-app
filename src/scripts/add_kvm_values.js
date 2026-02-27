const axios = require('axios');

const addKvmValues = async (org, kvmName, environment, entries, apiKey) => {
    try {
        const url = `https://api.enterprise.apigee.com/v1/organizations/${org}/environments/${environment}/keyvaluemaps/${kvmName}/entries`;

        // Normalize incoming entries: accept JSON objects or key=value strings
        const normalized = entries.map(v => {
            if (typeof v === 'string') {
                const trimmed = v.trim();
                if (trimmed.startsWith('{')) {
                    try {
                        return JSON.parse(trimmed);
                    } catch (e) {
                        // fall through
                    }
                }
                // support key=value format
                if (trimmed.includes('=')) {
                    const [name, ...rest] = trimmed.split('=');
                    return { name: name.trim(), value: rest.join('=').trim() };
                }
            }
            return v;
        });

        // use same structure as createKVM: entry array
        const payload = { entry: normalized };
        console.log('POST', url);
        console.log('Request payload:', JSON.stringify(payload, null, 2));
        console.log('Request headers:', JSON.stringify({ Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' }));

        const response = await axios.post(url, payload, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
        console.log('Values added successfully:', response.data);
    } catch (error) {
        console.error('Error adding values to KVM:', error.response ? error.response.data : error.message);
        process.exit(1);
    }
};

// CLI entrypoint
if (require.main === module) {
    // Expect: node add_kvm_values.js <org> <kvmName> <environment> <accessToken> <entriesJson | entry1 entry2 ...>
    const [, , org, kvmName, env, token, ...rest] = process.argv;
    if (!org || !kvmName || !env || !token) {
        console.error('Usage: node add_kvm_values.js <org> <kvmName> <environment> <accessToken> <entriesJson | entry1 entry2 ...>');
        process.exit(1);
    }

    let entries = [];
    if (rest.length === 1) {
        // single argument - maybe a JSON array string
        let first = rest[0];
        // strip outer quotes if present (handles some CLI quoting scenarios)
        if ((first.startsWith('"') && first.endsWith('"')) || (first.startsWith("'") && first.endsWith("'"))) {
            first = first.slice(1, -1);
        }
        if (first.trim().startsWith('[')) {
            try {
                entries = JSON.parse(first);
            } catch (e) {
                console.error('Failed to parse JSON entries array:', e.message);
                process.exit(1);
            }
        } else {
            // single non-JSON arg - treat as single entry
            entries = [first];
        }
    } else if (rest.length > 1) {
        // multiple args - treat as individual entry strings
        entries = rest;
    }

    addKvmValues(org, kvmName, env, entries, token);
}

module.exports = addKvmValues;