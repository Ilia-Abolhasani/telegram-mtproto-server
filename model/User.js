const Base = require("./Base");

module.exports = (sequelize, DataTypes) =>
{
    return Base(sequelize, DataTypes, "user", {
        id: { type: DataTypes.INTEGER, allowNull: false, primaryKey: true, autoIncrement: true },
        // name: { type: DataTypes.STRING, allowNull: false },        
        // approved: { type: DataTypes.BOOLEAN, defaultValue: false, allowNull: false },        
        // strike: { type: DataTypes.INTEGER, allowNull: false, defaultValue: 0 },                
    });
};