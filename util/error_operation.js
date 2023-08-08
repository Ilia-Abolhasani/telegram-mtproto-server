function throwError(code, message)
{
    let error = new Error(message);
    error.code = code;
    throw error;
};
module.exports = {
    throwError,
};