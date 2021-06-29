namespace zxcCore.zxcData.Cache.MemoryDB
{
    /// <summary>数据库权限类型
    /// </summary>
    public enum typePermission_DB
    {
        ReadOnly = -1,
        Normal = 0,
        Writable = 1,
        Deleteable = 2,
        Modifiable = 3
    }

    /// <summary>数据权限对象
    /// </summary>
    public class Data_Permission
    {
        #region 属性及构造

        /// <summary>数据库权限类型
        /// </summary>
        public typePermission_DB Permission { get; set; }

        public Data_Permission(typePermission_DB permission = typePermission_DB.Normal)
        {
            Permission = permission;
        }

        #endregion

        /// <summary>权限检查
        /// </summary>
        /// <param name="permission">指定权限</param>
        public virtual bool CheckPermission(typePermission_DB permission = typePermission_DB.Normal)
        {
            bool isAvailable = false;

            switch (Permission)
            {
                case typePermission_DB.Normal:
                    isAvailable = true;
                    break;
                case typePermission_DB.ReadOnly:
                case typePermission_DB.Writable:
                case typePermission_DB.Modifiable:
                    if (permission == Permission)
                        isAvailable = true;
                    break;
                default:
                    break;
            }

            return isAvailable;
        }

        public virtual dynamic ToJson()
        {
            return null;
        }
        public virtual bool FromJson(dynamic jsonData)
        {
            return false;
        }

    }
}
