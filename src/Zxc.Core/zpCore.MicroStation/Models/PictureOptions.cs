using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace zpCore.MicroStation.Models
{
    public class PictureOptions
    {
        /// <summary>
        /// 允许的文件类型
        /// </summary>
        public string FileTypes { get; set; }
        /// <summary>
        /// 最大文件大小
        /// </summary>
        public int MaxSize { get; set; }
        /// <summary>
        /// 图片的基地址
        /// </summary>
        public string ImageBaseUrl { get; set; }
        /// <summary>
        /// 图片的浏览地址
        /// </summary>
        public string ImageUrl { get; set; }
    }
}
