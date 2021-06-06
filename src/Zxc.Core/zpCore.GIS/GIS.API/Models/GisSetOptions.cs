using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace zpCore.GIS.API.Models
{
    public class GisSetOptions
    {
        /// <summary>文件夹设置
        /// </summary>
        public class GisDataDirs
        {
            /// <summary>GIS数据的基路径
            /// </summary>
            public string BaseDir { get; set; }
            /// <summary>GIS数据的临时路径
            /// </summary>
            public string TempDir { get; set; }
            /// <summary>GIS数据的输出路径
            /// </summary>
            public string OutputDir { get; set; }
        }

    }
}
