using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Linq.Dynamic.Core;
using System.Security.Cryptography;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using zpCore.MicroStation.Models;

namespace zpCore.MicroStation.Common
{
    public class common
    {
        public static UserManger userManger = new UserManger();
        public static readonly int pageSize = 3;        //默认分页条数
        public static string coon = "";                 //
        public static string ftpDir = "";               //
        public static int rand = 0;                  

        /// <summary> 返回Json串(不带双引号)
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        public static ActionResult<string> transResult(dynamic objDatas, dynamic objMsg = null, bool objSuccess = true)
        {
            var data = new { code = 0, is_success = objSuccess, msg = objMsg, datas = objDatas };
            var result = JsonConvert.SerializeObject(new { data = data });
            return new ContentResult { Content = result, ContentType = "application/json" };
        }
        public static JObject transResult_page(int pageInd, int pageSize, int pageCount)
        {
            JObject objRes = new JObject();
            objRes["pageInfo "] = new JObject();
            objRes["pageInfo "]["pageInd"] = pageInd;
            objRes["pageInfo "]["pageSize"] = pageSize;
            objRes["pageInfo "]["pageCount"] = pageCount / pageSize + 1;
            return objRes;
        }

        public static DateTime checkTime(dynamic varTime)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null && varTime != "")
                dtTime = Convert.ToDateTime(varTime);
            return dtTime;
        }
        public static DateTime checkTimeH(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null && varTime != "")
                dtTime = Convert.ToDateTime(varTime);
            int offset = bzero ? -1 : 1;
            dtTime = dtTime.AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset).AddHours(0);
            return dtTime;
        }
        public static DateTime checkTimeD(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = DateTime.Now;
            if (varTime != null && varTime != "")
                dtTime = Convert.ToDateTime(varTime);
            int offset = bzero ? -1 : 1;
            dtTime = dtTime.AddHours(-dtTime.Hour).AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset);
            return dtTime;
        }

        public static List<int> checkCondition_ID(dynamic jsonParams, string fieldname, int ind, ref string sql)
        {
            string uSql = sql;

            // 筛选ID集
            if (jsonParams.condition != null)
            {
                var condition = jsonParams.condition;
                if ((bool)condition.city == false)
                {
                    JArray streets = (JArray)condition.streets;
                    JArray communitys = (JArray)condition.communitys;
                    JArray delopys = (JArray)condition.delopys;
                    List<int> delopyss = condition.delopyss.ToObject<List<int>>();    // 正确

                    if (delopyss.Count > 0)
                    {
                        if (uSql != "") uSql += " And ";
                        uSql += "@" + ind.ToString() + ".Contains(" + fieldname + ")";
                        sql = uSql;
                    }
                    return delopyss;
                }
            }
            return new List<int>();
        }
        public static UserPermission checkPermissions(string userName)
        {
            UserInfo User = userManger.GetUser(userName);
            UserPermission perm = new UserPermission(User.Permission);
            perm.User = User;
            return perm;
        }
        public static List<int> checkPermission_IDs(string userName, db_MicroStationContext context)
        {
            UserPermission permissions = common.checkPermissions(userName);
            List<int> delopyIds = new List<int>();
            if (permissions.HasPermission)
            {
                // 提取权限对应的设备ID号  
                if (permissions.DelopyIds.Count > 0)
                {
                    delopyIds = context.MicroStation.Where(x => permissions.DelopyIds.Contains(x.DeployId)).Select(x => x.DeployId).ToList();
                }
                else
                {
                    if (permissions.Communitys.Count > 0)
                    {
                        delopyIds = context.MicroStation.Where(x => permissions.Communitys.Contains(x.CommunityName)).Select(x => x.DeployId).ToList();
                    }
                    else
                    {
                        if (permissions.TownStreets.Count > 0)
                        {
                            delopyIds = context.MicroStation.Where(x => permissions.TownStreets.Contains(x.StreetName)).Select(x => x.DeployId).ToList();
                        }
                    }
                }
            }
            return delopyIds;
        }


        public static string createName(string baseDirect, string suffix)
        {
            rand += 1;
            int ind = rand;
            Console.WriteLine(ind.ToString());
            DateTime dtNow = DateTime.Now;
            string newName = $@"pic_{dtNow:yyyyMMdd}_{dtNow:HHmm}_{dtNow:ssffff}_" + ind.ToString();
            string path = $@"{baseDirect}/{newName}{suffix}";

            while (Directory.Exists(path))
            {
                dtNow.AddMilliseconds(1);
                newName = $@"pic_{dtNow:yyyyMMdd}_{dtNow:HHmm}_{dtNow:ssffff}";
                path = $@"{baseDirect}/{newName}{suffix}";
            }
            if (rand > 1000) rand = 0;
            return newName;
        }

        public static ActionResult<string> errResult(string errInfo)
        {
            return new ContentResult { Content = errInfo, ContentType = "application/json" };
        }

        public static UserInfo getUserInfo(string usrName)
        {
            //if (usrName == null) usrName = "";
            //if (usrName == "") usrName = "ADMIN";
            //if (userManger.UserInfos.ContainsKey(usrName))
            //    return userManger.UserInfos[usrName];
            return userManger.GetUser(usrName);
        }

        /// <summary>
        /// MD5 加密
        /// </summary>
        /// <param name="strSource">需要加密的字符串</param>
        /// <returns>MD5加密后的字符串</returns>
        public static string Md5Encrypt(string strSource)
        {
            //把字符串放到byte数组中  
            byte[] bytIn = System.Text.Encoding.UTF8.GetBytes(strSource);
            //建立加密对象的密钥和偏移量          
            byte[] iv = { 102, 16, 93, 156, 78, 4, 218, 32 };//定义偏移量  
            byte[] key = { 55, 103, 246, 79, 36, 99, 167, 3 };//定义密钥  
            //实例DES加密类  
            DESCryptoServiceProvider mobjCryptoService = new DESCryptoServiceProvider();
            mobjCryptoService.Key = iv;
            mobjCryptoService.IV = key;
            ICryptoTransform encrypto = mobjCryptoService.CreateEncryptor();
            //实例MemoryStream流加密密文件  
            System.IO.MemoryStream ms = new System.IO.MemoryStream();
            CryptoStream cs = new CryptoStream(ms, encrypto, CryptoStreamMode.Write);
            cs.Write(bytIn, 0, bytIn.Length);
            cs.FlushFinalBlock();

            string strOut = System.Convert.ToBase64String(ms.ToArray());
            return strOut;
        }

        public dynamic transParam(dynamic param, List<string> lstNames)
        {
            var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
            JObject objParm = new JObject();
            foreach (var item in lstNames)
            {
                objParm[item] = jsonParams[item];
            }
            return objParm;
        }
    }
}
