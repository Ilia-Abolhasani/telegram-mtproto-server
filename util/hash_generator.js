const crypto = require('crypto');

function getRandom()
{
    const hash = crypto.randomBytes(64).toString('hex');
    return hash;
}

module.exports = { getRandom };