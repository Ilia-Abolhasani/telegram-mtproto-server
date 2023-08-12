const url = require('url');

function isValidMTProtoLink(link)
{
    const parsedUrl = url.parse(link, true);
    const requiredParams = [ 'server', 'port', 'secret' ];
    if (parsedUrl.protocol !== 'https:' ||
        parsedUrl.host !== 't.me' ||
        parsedUrl.pathname !== '/proxy')
        return false;

    if (Object.keys(parsedUrl.query).length !== requiredParams.length)
        return false;

    if (!parsedUrl.query.server ||
        !parsedUrl.query.port ||
        !parsedUrl.query.secret ||
        !/^\d+$/.test(parsedUrl.query.port))
        return false;

    return true;
}

module.exports = { isValidMTProtoLink };