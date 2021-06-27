using System;
using System.IO;

namespace zxcCore.Common
{
    public static class zxcIOHelper
    {

        /// <summary>检查文件路径(修正文件夹目录)
        /// </summary>
        /// <param name="path"文件路径></param>
        /// <param name="autoCreate">自动创建文件夹</param>
        /// <returns></returns>
        public static bool checkPath(string path, bool autoCreate = true)
        {
            string strDir = Path.GetDirectoryName(path);
            if (!Directory.Exists(strDir))
            {
                //创建文件夹
                string strDir_Parent = Path.GetDirectoryName(strDir);
                if (!Directory.Exists(strDir_Parent))
                    return checkPath(strDir);
                else
                    if (autoCreate)
                    Directory.CreateDirectory(strDir);
                else
                    return false;
            }
            return true;
        }

    }
}
