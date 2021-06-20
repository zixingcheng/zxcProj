//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：zxcEnum --枚举扩展类
// 创建标识：zxc   2021-06-20
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Reflection;

namespace zxcCore.Extensions
{
    /// <summary>枚举扩展类(提取枚举特性)
    /// </summary>
    public static class EnumExtensione
    {
        /// <summary>获取属性信息
        /// </summary>
        /// <param name="emValue"></param>
        /// <returns></returns>
        public static T GetAttr<T>(Enum emValue) where T : Attribute
        {
            Type tp = emValue.GetType();
            MemberInfo[] mi = tp.GetMember(emValue.ToString());
            if (mi != null && mi.Length > 0)
            {
                T attr = Attribute.GetCustomAttribute(mi[0], typeof(T)) as T;
                return attr;
            }
            return default(T);
        }

        /// <summary>获取枚举的自定义名称
        /// </summary>
        /// <param name="emValue"></param>
        /// <returns></returns>
        public static string Get_AttrName(this Enum emValue)
        {
            EnumAttr pEnumAttr = GetAttr<EnumAttr>(emValue);
            return pEnumAttr == null ? null : pEnumAttr.AttrName;
        }

        /// <summary>获取枚举的自定义值
        /// </summary>
        /// <param name="emValue"></param>
        /// <returns></returns>
        public static object Get_AttrValue(this Enum emValue)
        {
            EnumAttr pEnumAttr = GetAttr<EnumAttr>(emValue);
            return pEnumAttr == null ? null : pEnumAttr.AttrValue;
        }

        /// <summary>获取枚举的自定义区域
        /// </summary>
        /// <param name="emValue"></param>
        /// <returns></returns>
        public static object Get_Area(this Enum emValue)
        {
            EnumArea pEnumAttr = GetAttr<EnumArea>(emValue);
            return pEnumAttr == null ? null : pEnumAttr.Area;
        }

        /// <summary>获取枚举的备注信息
        /// </summary>
        /// <param name="emValue"></param>
        /// <returns></returns>
        public static object Get_Remark(this Enum emValue)
        {
            EnumRemark pEnumAttr = GetAttr<EnumRemark>(emValue);
            return pEnumAttr == null ? null : pEnumAttr.Remark;
        }

        public static string Get_Description(this Enum emValue)
        {
            DescriptionAttribute pEnumAttr = GetAttr<DescriptionAttribute>(emValue);
            return pEnumAttr == null ? null : pEnumAttr.Description;
        }

    }

    /// <summary>Enum特性（属性、名称）
    /// </summary>
    [AttributeUsage(AttributeTargets.Field)]
    public class EnumAttr : Attribute
    {
        public string AttrName { get; set; }
        public object AttrValue { get; set; }
        public EnumAttr(string attrName, object attrValue)
        {
            this.AttrName = attrName;
            this.AttrValue = attrValue;
        }

    }

    /// <summary>Enum特性（备注）
    /// </summary>
    [AttributeUsage(AttributeTargets.Field)]
    public class EnumRemark : Attribute
    {
        public object Remark { get; set; }
        public EnumRemark(object remark)
        {
            this.Remark = remark;
        }

    }

    /// <summary>Enum特性（地区）
    /// </summary>
    [AttributeUsage(AttributeTargets.Field)]
    public class EnumArea : Attribute
    {
        public object Area { get; set; }
        public EnumArea(object Area)
        {
            this.Area = Area;
        }

    }

}
