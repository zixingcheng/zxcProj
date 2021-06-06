using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace zpCore.GIS.API.Models
{
    public class FileSetOptions
    {
        /// <summary>
        /// 允许的文件类型
        /// </summary>
        public string FileTypes { get; set; }
        /// <summary>
        /// 最大文件大小
        /// </summary>
        public int FileMaxSize { get; set; }
        /// <summary>
        /// 文件的基路径
        /// </summary>
        public string FileBaseDir { get; set; }
        /// <summary>
        /// 文件的浏览地址
        /// </summary>
        public string FileUrl { get; set; }
    }
}
