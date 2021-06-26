using System;
using System.Collections.Generic;

namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据因子对象集
    /// </summary>
    public interface IData_Factors : IData_Factor
    {
        /// <summary>因子集
        /// </summary>
        Dictionary<string, IData_Factor> Factors { get; set; }

        ///// <summary>数据设置管理对象-注入
        ///// </summary>
        //IDataSets_Manage_Iot DataSets { get; }


        //索引因子对象
        bool IndexData_Factor(IData_Factor infoFactor);
        //提取因子对象
        IData_Factor GetData_Factor(string strTag);
    }
}
