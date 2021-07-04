using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Reflection;
using zxcCore.Common;

namespace zxcCore.zxcData.Cache.MemoryDB
{
    /// <summary>数据对象集类-表
    /// </summary>
    public class Data_Table<T> : List<T> where T : Data_Models, IData
    {
        #region 属性及构造

        /// <summary>数据库对象
        /// </summary>
        protected internal Data_DB _dbContext { get; set; }
        /// <summary>数据库表名
        /// </summary>
        protected internal string _dtName { get; set; }
        /// <summary>数据库表数据路径
        /// </summary>
        protected internal string _dbPath { get; set; }
        /// <summary>数据库表数据缓存路径
        /// </summary>
        protected internal string _dbPathCache { get; set; }
        /// <summary>当前累积数据修改量
        /// </summary>
        protected internal long _nChanges { get; set; }
        /// <summary>数据库表权限
        /// </summary>
        protected internal Data_Permission _permissionDB = null;
        /// <summary>对象属性集
        /// </summary>
        protected internal PropertyInfo[] _propertyInfos = null;

        /// <summary>标识是否不允许删除操作
        /// </summary>
        protected internal bool _isNoDel { get; set; }
        /// <summary>标识是否不记录日志
        /// </summary>
        protected internal bool _isNoLog { get; set; }
        /// <summary>标识是否系统库表
        /// </summary>
        protected internal bool _isSysTable { get; set; }

        public Data_Table()
        {
            _permissionDB = new Data_Permission();
            _dtName = this.GetType().Name;
        }
        public Data_Table(string dtName)
        {
            _permissionDB = new Data_Permission();
            _dtName = dtName == null ? this.GetType().Name : dtName;
        }
        public Data_Table(typePermission_DB permission)
        {
            _permissionDB = new Data_Permission(permission);
            _dtName = this.GetType().Name;
        }
        /// <summary>注入数据库对象
        /// </summary>
        /// <param name="dbContext"></param>
        public void SetDB(Data_DB dbContext)
        {
            _dbContext = dbContext;
            _permissionDB = dbContext.PermissionDB;
        }

        //public InitData()
        //{
        //    //反序列化
        //    this = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<TestObj>>(strJson);
        //}

        #endregion


        /// <summary>权限检查
        /// </summary>
        /// <param name="permission">指定权限</param>
        protected virtual bool CheckPermission(typePermission_DB permission = typePermission_DB.Normal)
        {
            return this._permissionDB.CheckPermission(permission);
        }


        /// <summary>是否临时表
        /// </summary>
        /// <returns></returns>
        protected virtual bool IsTempTable()
        {
            return !(_dbContext != null && _dbPathCache != null);
        }
        /// <summary>对象是否存在
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public virtual bool IsExist(T item)
        {
            return this.Contains(item) || this.IsSame(item);
        }
        /// <summary>对象是否相同-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public virtual bool IsSame(T item)
        {
            return this.Query_Sames(item).Count() > 0;
        }
        /// <summary>查询相同对象-重写
        /// </summary>
        /// <param name="item"></param>
        /// <returns></returns>
        public virtual List<T> Query_Sames(T item)
        {
            return new List<T>();
        }


        /// <summary>添加对象-剔除存在
        /// </summary>
        /// <param name="item"></param>
        /// <param name="isUnique">唯一性检查</param>
        public virtual bool Add(T item, bool isUnique = true, bool bUpdata = false, bool bMultiple = false, bool bCacheData = true)
        {
            if (item == null) return false;
            if (!this.CheckPermission(typePermission_DB.Writable))
                throw (new Exception("没有写入权限"));

            if (isUnique)
                if (this.IsExist(item) && !bUpdata)
                    return false;
            bool _isUnique = bUpdata ? isUnique : !isUnique;
            if (this.IsTempTable())
                _isUnique = isUnique;

            if (isUnique == false) _isUnique = false;
            bool bResult = this.SetValue(item, typePermission_DB.Writable, _isUnique);

            if (!bMultiple)
                if (bCacheData && !this.IsTempTable())
                    bResult = bResult && this.SaveChanges_ToCache(item);
            return bResult;
        }
        /// <summary>添加对象集-剔除存在
        /// </summary>
        /// <param name="collection"></param>
        /// <param name="isUnique">唯一性检查</param>
        public virtual bool AddRange(IEnumerable<T> collection, bool isUnique = true, bool bUpdata = false, bool bCacheData = true)
        {
            if (collection == null || collection.Count() == 0) return false;
            if (!this.CheckPermission(typePermission_DB.Writable))
                throw (new Exception("没有写入权限"));

            bool bResult = true;
            foreach (var item in collection)
            {
                bResult = bResult && this.Add(item, isUnique, bUpdata, true, false);
            }
            if (bCacheData && !this.IsTempTable())
                bResult = bResult && this.SaveChanges_ToCache(collection);
            return bResult;
        }

        /// <summary>删除对象集
        /// </summary>
        /// <param name="collection"></param>
        public virtual bool DeleteRange(IEnumerable<T> collection)
        {
            if (collection == null || collection.Count() == 0) return false;
            if (_isNoDel) return false;
            if (!this.CheckPermission(typePermission_DB.Deleteable))
                throw (new Exception("没有删除权限"));

            //循环所有数据进行同步
            int nSum = 0;
            bool bResult = true;
            foreach (var item in collection)
            {
                if (!item.IsDel)
                {
                    item.IsDel = true;
                    bResult = bResult && this.SetValue(item, typePermission_DB.Deleteable, true);
                    nSum++;
                }
            }
            if (nSum > 0)
                bResult = bResult && this.SaveChanges_ToCache(collection);
            return bResult;
        }
        /// <summary>更新对象集
        /// </summary>
        /// <param name="collection"></param>
        public virtual bool UpdateRange(IEnumerable<T> collection, bool bCacheData = true)
        {
            if (collection == null || collection.Count() == 0) return false;
            if (!this.CheckPermission(typePermission_DB.Modifiable))
                throw (new Exception("没有写入权限"));

            bool bResult = true;
            foreach (var item in collection)
            {
                bResult = bResult && this.SetValue(item, typePermission_DB.Modifiable, true);
            }
            if (bCacheData && !this.IsTempTable())
                bResult = bResult && this.SaveChanges_ToCache(collection);
            return bResult;
        }

        /// <summary>设置对象
        /// </summary>
        /// <param name="item"></param>
        /// <param name="isUnique">唯一性检查</param>
        protected internal virtual bool SetValue(T item, typePermission_DB permission, bool isUnique = true, bool isSyncData = false)
        {
            if (isUnique)
            {
                if (this.IsExist(item))
                {
                    //uid查找
                    List<T> lstTemp = this.FindAll(e => e.UID == item.UID && e.IsDel == false);
                    if (lstTemp.Count > 1)
                        throw (new Exception("UID重复：" + item.UID));

                    //same查找
                    if (lstTemp.Count < 1)
                    {
                        lstTemp = this.Query_Sames(item);
                    }
                    if (lstTemp.Count > 1)
                        throw (new Exception("数据重复：" + item.ToJson()));

                    //更新数据
                    if (lstTemp.Count == 1)
                    {
                        //查找序号
                        int ind = this.FindIndex(e => e.UID == lstTemp[0].UID);
                        if (!isSyncData)
                            this.RefreshLog(item, this[ind], permission);    //更新操作信息
                        this[ind] = item;
                        return true;
                    }
                }
            }
            if (!isSyncData)
                this.RefreshLog(item, null, permission);    //更新操作信息
            base.Add(item);
            return true;
        }
        /// <summary>更新操作信息
        /// </summary>
        /// <param name="item"></param>
        /// <param name="itemBase">原始数据</param>
        /// <returns></returns>
        protected internal virtual bool RefreshLog(T item, T itemBase, typePermission_DB permission)
        {
            //更新日志信息
            //item.Operator = null;
            item.OpTime = DateTime.Now;
            _nChanges++;                    //标识修改数

            //记录日志
            if (this._isNoLog) return true;
            if (this.IsTempTable()) return true;

            //DataTable dtChange = this.ComparisonChange(item, itemBase);
            DataModels_Log pLog = new DataModels_Log()
            {
                OpTime = DateTime.Now,
                Operator = item.Operator,
                OpType = permission,
                OpTable = this._dtName,
                OpInfo_Src = itemBase == null ? null : itemBase.ToJson(),
                OpInfo_To = item.ToJson(),
                //OpInfo_Dif = Newtonsoft.Json.JsonConvert.SerializeObject(dtChange),
                Remarks = ""
            };

            //写入库表
            this._dbContext.OnOperationLog(pLog, item.Operator);
            return true;
        }
        /// <summary>开启日志记录功能
        /// </summary>
        /// <param name="bRecord"></param>
        /// <returns></returns>
        public virtual bool OpenLogRecord(bool bRecord = true)
        {
            _isNoLog = !bRecord;
            return true;
        }


        /// <summary>保存修改-缓存到数据文件
        /// </summary>
        /// <returns></returns>
        public virtual int SaveChanges(bool isForce = false)
        {
            //缓存时忽略全量保存
            if (!isForce)
            {
                if (_nChanges < 1) return 0;
                if (_dbContext._useCache_Realtime)
                    return 0;
            }

            int nSaved = 0;
            long nNums = _nChanges;
            string strJson = this.ToJson();

            if (this._dbContext != null)
            {
                //同步缓存数据
                string[] files = this.SyncChanges(isForce);

                if (zxcIOHelper.checkPath(_dbPath))
                    File.WriteAllText(_dbPath, strJson);

                //清理缓存数据
                this.SyncChanges_Clean(files);
            }
            _nChanges -= nNums;
            return nSaved;
        }
        /// <summary>保存修改-缓存到文件
        /// </summary>
        /// <returns></returns>
        public virtual bool SaveChanges_ToCache(T item)
        {
            //写入当前数据到文件
            string path = _dbPathCache + "/" + DateTime.Now.ToString("YYYYMMdd_HHmmss_ffff") + ".json";
            path = Path.GetFullPath(path);

            string strJson = Newtonsoft.Json.JsonConvert.SerializeObject(item);
            if (zxcIOHelper.checkPath(path))
                File.WriteAllText(path, "[\r\n" + strJson + "\r\n]");
            return true;
        }
        /// <summary>保存修改-缓存到文件
        /// </summary>
        /// <returns></returns>
        public virtual bool SaveChanges_ToCache(IEnumerable<T> collection)
        {
            //写入当前数据到文件
            string path = _dbPathCache + "/" + DateTime.Now.ToString("YYYYMMdd_HHmmss_ffff" + ".json");
            path = Path.GetFullPath(path);

            string strJson = Newtonsoft.Json.JsonConvert.SerializeObject(collection);
            if (zxcIOHelper.checkPath(path))
                File.WriteAllText(path, strJson);
            return true;
        }

        /// <summary>同步数据
        /// </summary>
        /// <param name="isForce">是否强制同步</param>
        /// <returns></returns>
        public virtual string[] SyncChanges(bool isForce = false, bool asynClean = true)
        {
            //读取所有缓存文件
            string[] files = Directory.GetFiles(_dbPathCache);
            List<T> lstTemp = new List<T>();
            foreach (var file in files)
            {
                //读取文件信息生成表对象
                Data_Table<T> Data_Table = new Data_Table<T>("");
                string strJson = File.ReadAllText(file);
                Data_Table = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<T>>(strJson);

                //记录缓存
                foreach (var rowItem in Data_Table)
                {
                    lstTemp.Add((T)rowItem.Clone());
                }
            }

            //同步成功，删除缓存文件
            if (this.SyncChanges(lstTemp))
            {
                if (asynClean) return files;
                this.SyncChanges_Clean(files);
            }
            return new string[] { };
        }
        /// <summary>同步数据
        /// </summary>
        /// <param name="collection">数据集</param>
        /// <returns></returns>
        public virtual bool SyncChanges(IEnumerable<T> collection)
        {
            //循环所有数据进行同步
            if (collection.Count() > 0)
            {
                collection = collection.OrderBy(p => p.OpTime).ToList();  //升序
                foreach (var item in collection)
                {
                    item.Init();        //主动调用初始操作，避免初始不完全    
                    this.SetValue(item, typePermission_DB.ReadOnly, true, true);
                }
            }
            return true;
        }
        /// <summary>同步数据缓存文件清理
        /// </summary>
        /// <param name="files">缓存文件集</param>
        /// <returns></returns>
        public virtual bool SyncChanges_Clean(string[] files)
        {
            //同步成功，删除缓存文件
            foreach (var item in files)
            {
                if (File.Exists(item))
                    File.Delete(item);
            }
            return true;
        }


        /// <summary>转为Json对象
        /// </summary>
        /// <returns></returns>
        public virtual dynamic ToJson()
        {
            return Newtonsoft.Json.JsonConvert.SerializeObject(this);
        }
        /// <summary>比对数据，返回变化表
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="item"></param>
        /// <param name="itemBase"></param>
        /// <returns></returns>
        private DataTable ComparisonChange(T item, T itemBase)
        {
            //提取数据对象属性集
            if (_propertyInfos == null)
                _propertyInfos = typeof(T).GetProperties();

            //初始别对结果表
            DataTable dt = new DataTable();
            foreach (PropertyInfo p in _propertyInfos)
            {
                //提取属性、检查是否为空
                Type columnType = p.PropertyType;
                if (p.PropertyType.IsGenericType && p.PropertyType.GetGenericTypeDefinition() == typeof(Nullable<>))
                {
                    //如果可以为null，则获取基础类型。例如，如果“Nullable<int>”，则只返回“int”
                    columnType = p.PropertyType.GetGenericArguments()[0];
                }

                //初始表类型
                dt.Columns.Add(new DataColumn(p.Name, columnType));
            }

            //循环对比
            object[] row = new object[_propertyInfos.Length];
            object[] rowBase = new object[_propertyInfos.Length];
            int i = 0;
            foreach (PropertyInfo p in _propertyInfos)
            {
                row[i] = p.GetValue(item, null);
                rowBase[i++] = itemBase == null ? null : p.GetValue(itemBase, null);
            }
            dt.Rows.Add(rowBase);
            dt.Rows.Add(row);
            return dt;
        }

    }
}
