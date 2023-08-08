const fs = require('fs');
const path = require('path');

module.exports = async function (file_path)
{
	file_path = `../${file_path}`;
	const filePath = path.join(__dirname, file_path);

	return await fs.readFileSync(filePath, 'utf8');
}