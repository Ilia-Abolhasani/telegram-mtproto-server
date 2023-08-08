const Sequelize = require('sequelize');
const { Op } = require('sequelize');
const { throwError } = require("./util/error_operation");

module.exports = class Context
{
    constructor()
    {
        this.database = require('./config/database');
    }

    //#region Basic Functions
    static initWhere(column, value)
    {
        if (value)
        {
            let toks = value.split(' ');
            if (toks.length > 0)
            {
                let conditions = [];
                for (let i = 0; i < toks.length; i++)
                {
                    let obj = {};
                    obj[ column ] = { [ Sequelize.Op.like ]: '%' + toks[ i ] + '%' };
                    conditions.push(obj);
                }
                return conditions;
            }
        }
        return [];
    }

    init()
    {
        // General Tables
        const User = require("./model/User");
        const user = User(this.database, Sequelize.DataTypes);

        // set foreignKeys
        // check.belongsTo(group, {
        //     foreignKey: { name: "group_id", allowNull: false },
        // });        
        // review.hasMany(review_check);                                        

        this.database.sync({ force: false });
    }

    addFunction(model)
    {
        model.getColumns = (secure) =>
        {
            return this.getColumns(model, secure);
        };
        model.secure = (obj) =>
        {
            let Cs = this.getColumns(model, true);
            for (let i = 0; i < Cs.length; i++)
            {
                const element = Cs[ i ];
                delete obj.dataValues[ element ];
            }
            return obj;
        };
        return model;
    }

    getColumns(model, secure)
    {
        let ans = [];
        for (const [ key, value ] of Object.entries(model.fieldRawAttributesMap))
        {
            if (secure === true)
            {
                if (value.secure)
                    ans.push(key);
            }
            else if (secure === false)
            {
                if (!value.secure)
                    ans.push(key);
            }
            else
                ans.push(key);
        }
        return ans;
    }

    async startTrx(handler)
    {
        let transaction = await this.database.transaction();
        try
        {
            let result = await handler(transaction);
            await transaction.commit();
            return result;
        }
        catch (error)
        {
            await transaction.rollback();
            throw error;
        }
    }

    async startOrResumeTrx(handler, trx)
    {
        if (trx)
            return await handler(trx);
        else
            return this.startTrx(handler);
    }

    async getModel(model, options, noErrorOnEmpty, trx)
    {
        if (!options)
            options = {};
        options.transaction = trx;
        let value = await this.database.models[ model ].findOne(options);
        if (!noErrorOnEmpty)
            if (!value)
                throwError(404, "Could not found " + model);
        return value;
    }

    async deleteModel(model, options, trx)
    {
        let value = await this.getModel(model, options, false, trx);
        return await value.destroy();
    }
    //#endregion

    //#region UserSession
    async getUser(id, trx)
    {
        return await this.getModel("user", { where: { id } }, false, trx);
    }
    //#endregion
};