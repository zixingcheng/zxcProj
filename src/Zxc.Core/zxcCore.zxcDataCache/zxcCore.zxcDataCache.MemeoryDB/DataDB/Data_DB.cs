using System;
using System.Collections.Generic;
using System.IO;
using zxcCore.Common;

namespace zxcCore.zxcDataCache.MemoryDB
{
    /// <summary>数据对象集类-数据库
    /// </summary>
    public class Data_DB
    {
        #region 属性及构造

        /// <summary>数据库路径
        /// </summary>
        public string DirBase { get; set; }
        /// <summary>数据库路径-系统表
        /// </summary>
        public string DirBase_Sys { get; set; }
        /// <summary>数据库路径-设置的根目录
        /// </summary>
        public string DirRoot { get; set; }

        protected internal bool _useCache_Realtime = true;
        /// <summary>是否使用实时缓存
        /// </summary>
        public bool UseCache_Realtime
        {
            get { return _useCache_Realtime; }
            set { _useCache_Realtime = value; }
        }

        protected internal Data_Permission _permissionDB = new Data_Permission();
        /// <summary>数据库权限
        /// </summary>
        public Data_Permission PermissionDB
        {
            get { return _permissionDB; }
            set { _permissionDB = value; }
        }

        /// <summary>库表-日志对象
        /// </summary>
        protected readonly DataTable_Log<DataModels_Log> _dtLog = null;

        /// <summary>配置文件信息
        /// </summary>
        protected internal ConfigurationHelper _configDataCache = new ConfigurationHelper("appsettings.json");
        public Data_DB(string dirBase, typePermission_DB permission = typePermission_DB.Normal, bool useCache = true, string dbName = "")
        {
            _useCache_Realtime = useCache;
            _permissionDB = new Data_Permission(permission);

            //初始根目录
            DirRoot = _configDataCache.config["DataCache.MemoryDB:Base_Dir"] + "";
            if (DirRoot == "")
                DirRoot = System.IO.Directory.GetCurrentDirectory();

            //默认路径数据库
            if (dirBase != "")
            {
                DirBase = dirBase;
                DirRoot = Directory.GetDirectoryRoot(DirBase);
                
            }
            else
            {
                if (dbName == "") return;
                DirBase = DirRoot + dbName;
            }

            //创建数据库
            if (DirBase != "")
            {
                this.OnDBModelCreating();

                //初始日志库表
                _dtLog = new DataTable_Log<DataModels_Log>(); this.InitDBModel(_dtLog);
            }
        }

        #endregion

        /// <summary>数据库模型创建
        /// </summary>
        protected virtual void OnDBModelCreating()
        {
            if (this.DirBase != "")
            {
                if (!System.IO.Directory.Exists(this.DirBase))
                    System.IO.Directory.CreateDirectory(this.DirBase);

                //创建日志库
                DirBase_Sys = this.DirBase + "/_DbSys";
                if (!System.IO.Directory.Exists(DirBase_Sys))
                    System.IO.Directory.CreateDirectory(DirBase_Sys);
            }
        }
        /// <summary>数据库模型创建库表
        /// </summary>
        protected virtual Data_Table<T> OnDBModelCreating<T>(Data_Table<T> objDataModel) where T : Data_Models, IData
        {
            string pathRevise = objDataModel._isSysTable ? "/_DbSys" : "";
            string path = this.DirBase + pathRevise + "/" + objDataModel._dtName + ".zxcdb";
            path = Path.GetFullPath(path);

            //反序列化
            Data_Table<T> Data_Table = new Data_Table<T>();
            string strJson = "";
            if (File.Exists(path))
            {
                strJson = File.ReadAllText(path);
                Data_Table = Newtonsoft.Json.JsonConvert.DeserializeObject<Data_Table<T>>(strJson);
            }

            //创建实时缓存文件夹
            if (_useCache_Realtime)
            {
                string dirDB = this.DirBase + pathRevise + "/_DbCache/" + objDataModel._dtName;
                if (!System.IO.Directory.Exists(dirDB))
                    System.IO.Directory.CreateDirectory(dirDB);
                Data_Table._dbPathCache = dirDB;
            }

            Data_Table._dbPath = path;
            Data_Table._dbContext = this;
            return Data_Table;
        }

        /// <summary>初始库表对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="objDataModel"></param>
        /// <returns></returns>
        protected virtual bool InitDBModel<T>(Data_Table<T> objDataModel) where T : Data_Models, IData
        {
            objDataModel.SetDB(this);

            Data_Table<T> dtTemp = this.OnDBModelCreating<T>(objDataModel);
            foreach (var item in dtTemp)
            {
                objDataModel.Add(item, false, true);
            }
            objDataModel._dbPath = dtTemp._dbPath;
            objDataModel._dbPathCache = dtTemp._dbPathCache;

            //同步缓存数据
            if (_useCache_Realtime)
            {
                string[] files = objDataModel.SyncChanges(true);
                objDataModel.SaveChanges(true);

                //清理缓存数据
                objDataModel.SyncChanges_Clean(files);
            }
            return true;
        }


        /// <summary>日志记录
        /// </summary>
        protected internal virtual void OnOperationLog(DataModels_Log objLog, string usrID = null)
        {
            if (objLog != null)
            {
                DataModels_Log pLog = new DataModels_Log()
                {
                    OpTime = DateTime.Now,
                    Operator = usrID,
                    OpType = objLog.OpType,
                    OpTable = objLog.OpTable,
                    OpInfo_Src = objLog.OpInfo_Src,
                    OpInfo_To = objLog.OpInfo_To,
                    OpInfo_Dif = objLog.OpInfo_Dif,
                    Remarks = objLog.Remarks
                };

                //写入库表
                this._dtLog.Add(pLog);
            }
        }


        /// <summary>权限检查
        /// </summary>
        /// <param name="permission">指定权限</param>
        protected virtual bool CheckPermission(typePermission_DB permission = typePermission_DB.Normal)
        {
            return PermissionDB.CheckPermission(permission);
        }

    }
}
