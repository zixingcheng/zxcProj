using Newtonsoft.Json.Linq;
using System.ComponentModel.DataAnnotations;
using System.Drawing;
using zpCore.Image;

namespace zpCore.GIS.Renderer
{
    public enum emRenderType
    {
        [Display(Name = "无渲染")]
        /// <summary>无渲染
        /// </summary>
        None = -1,
        [Display(Name = "简单渲染")]
        /// <summary>单值渲染
        /// </summary>
        Simple = 0,
        [Display(Name = "单值")]
        /// <summary>单值渲染
        /// </summary>
        Unique = 1,
        [Display(Name = "已分类")]
        /// <summary>已分类
        /// </summary>
        Classify = 2,
        [Display(Name = "拉伸")]
        /// <summary>拉伸
        /// </summary>
        Stretch = 2,
    }

    public interface IRenderer
    {
        /// <summary>渲染类型
        /// </summary>
        emRenderType RenderType { get; }
        /// <summary>是否为栅格渲染
        /// </summary>
        bool IsRaster { get; }
        /// <summary>分段标题集
        /// </summary>
        string[] Titles { get; }
        /// <summary>分段标题别名集
        /// </summary>
        string[] TitlesAlias { get; }
        /// <summary>颜色集
        /// </summary>
        string[] Colors { get; }
        /// <summary>断点集合
        /// </summary>
        double[] Breaks { get; }
        /// <summary>值集合
        /// </summary>
        dynamic[] Values { get; }

        /// <summary>渲染图
        /// </summary>
        ImageObj Image { get; }

        //初始参数信息
        public bool InitParams(string strParams, bool useTestParam = false);
        public bool InitParams(JObject parmObj);

        public bool Render(ImageObj img = null);
        /// <summary>渲染绘制
        /// </summary>
        /// <param name="img"></param>
        /// <returns></returns>
        public bool Render_Draw(ImageObj img = null);

        ImageColor GetColor(double value);
        /// <summary>提取渲染结果json信息
        /// </summary>
        /// <returns></returns>
        public dynamic ToRendererStr(bool toStr = true);

        public bool Output(string path, string name = "");
    }
}