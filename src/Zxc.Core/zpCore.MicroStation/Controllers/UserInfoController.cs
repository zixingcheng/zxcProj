using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Linq;
using zpCore.MicroStation.Common;
using zpCore.MicroStation.Models;

/// <summary>
/// 用户接口类
/// Add By StevenTam On Date：2020-11-04
/// </summary>
namespace zpCore.MicroStation.Controllers
{
    [Route("api/[controller]/[action]")]
    [ApiController]
    public class UserInfoController : ControllerBase
    {
        private db_MicroStationContext _context;
        public UserInfoController(db_MicroStationContext context)
        {
            _context = context;
        }

        /// <summary>
        /// User用户登录
        /// </summary>
        /// <param name="param">userName：用户名称/用户号码；userPwd：用户密码</param>
        /// <returns>返回是否登录成功以及用户信息</returns>
        [HttpPost]
        public ActionResult<string> UserLogin(dynamic param)
        {
            UserInfo user = new UserInfo();
            bool state = false;
            string msg = "";
            try
            {
                var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
                string userName = jsonParams.userName;
                string userPwd = jsonParams.userPwd;

                if (!string.IsNullOrEmpty(userName.Trim()) && !string.IsNullOrEmpty(userPwd.Trim()))
                {
                    userPwd = common.Md5Encrypt(userPwd.Trim());
                    user = (from a in _context.UserInfo
                                 where a.Isitavailable == 1 && a.UserPwd == userPwd.Trim() && (a.Username == userName.Trim() || a.Userphone == userName.Trim())
                                 select new UserInfo
                                 {
                                     UserInfoOid = a.UserInfoOid,
                                     Username = a.Username,
                                     Userphone = a.Userphone,
                                     Groupname = a.Groupname,
                                     Nodepath = a.Nodepath,
                                     Isitavailable = a.Isitavailable
                                 }).FirstOrDefault();
                              
                    if (user != null)
                    {
                        state = true;
                        msg = "用户登录成功！";
                    }
                    else 
                    {
                        msg = "用户登录失败，请检查登录信息！";
                    }
                }
            }
            catch (Exception)
            {
                msg = "系统服务出现异常，请联系管理员！";
            }
            return common.transResult((JToken)JsonConvert.DeserializeObject(JsonConvert.SerializeObject(user)), msg, state);
        }

        /// <summary>
        /// User用户修改密码
        /// </summary>
        /// <param name="param">userId：用户ID；userPwd：用户新密码</param>
        /// <returns>返回是否修改成功以及用户信息</returns>
        [HttpPost]
        public ActionResult<string> UpdateUserPwd(dynamic param)
        {
            UserInfo user = new UserInfo();
            bool state = false;
            string msg = "";
            try
            {
                var jsonParams = JsonConvert.DeserializeObject<dynamic>(param.ToString());
                string userId = jsonParams.userId;
                string userPwd = jsonParams.userPwd;

                if (!string.IsNullOrEmpty(userId.Trim()) && !string.IsNullOrEmpty(userPwd.Trim()))
                {
                    userPwd = common.Md5Encrypt(userPwd.Trim());
                    var query = _context.UserInfo.Where(p => p.UserInfoOid == userId && p.Isitavailable == 1).FirstOrDefault();
                    if (query != null)
                    {
                        query.UserPwd = userPwd.Trim();
                        _context.SaveChanges();

                        user.UserInfoOid = query.UserInfoOid;
                        user.Username = query.Username;
                        user.Userphone = query.Userphone;
                        user.Groupname = query.Groupname;
                        user.Nodepath = query.Nodepath;
                        user.Isitavailable = query.Isitavailable;

                        state = true;
                        msg = "修改密码成功！";
                    }
                    else 
                    {
                        msg = "修改密码失败！";
                    }
                }
            }
            catch (Exception)
            {
                msg = "系统服务出现异常，请联系管理员！";
            }
            return common.transResult(user, msg, state);
        }

    }
}