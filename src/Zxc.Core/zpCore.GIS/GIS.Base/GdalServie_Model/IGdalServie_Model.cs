namespace zpCore.GIS.Models.Service
{
    public enum emModeState
    {
        /// <summary>已初始，但无操作
        /// </summary>
        None = -1,
        /// <summary>参数准备完毕
        /// </summary>
        Preparing = 0,
        /// <summary>运行中
        /// </summary>
        Running = 1,
        /// <summary>运行中断
        /// </summary>
        Runbreak = 21,
        /// <summary>运行中止
        /// </summary>
        Runstop = 22,
        /// <summary>运行完毕
        /// </summary>
        Runout = 20,
        /// <summary>运行出错
        /// </summary>
        Runerror = 30,
    }

    public interface IGdalServie_Model
    {
        /// <summary>模型状态
        /// </summary>
        emModeState ModeState { get; }

        /// <summary> 初始参数
        /// </summary>
        /// <param name="strParams">参数</param>
        /// <param name="useTestParam">是否使用默认测试参数（未传入参数时）</param>
        /// <returns></returns>
        bool InitParams(string strParams, bool useTestParam = false);
        /// <summary>模型参数校检
        /// </summary>
        /// <returns></returns>
        bool CheckParams();

        /// <summary> 初始默认测试参数
        /// </summary>
        /// <returns></returns>
        string InitParam_Test(string tag = "");

        /// <summary> 初始模型结果返回结构
        /// </summary>
        /// <returns></returns>
        bool InitResult();

        /// <summary>初始模型错误信息
        /// </summary>
        /// <param name="strErr">错误信息</param>
        /// <param name="bRunend">是否停止</param>
        /// <returns></returns>
        bool InitError(string strErr, bool bRunend = false);

        /// <summary>运行模型
        /// </summary>
        /// <param name="strParams_run">运行参数</param>
        /// <returns></returns>
        bool RunModel(string strParams_run = "");
        /// <summary>模型结果渲染及输出
        /// </summary>
        /// <param name="strParams_renderer"></param>
        /// <returns></returns>
        bool Renderer(string strParams_renderer = "");

        /// <summary>提取模型运行状态
        /// </summary>
        /// <returns></returns>
        emModeState GetModelState();

        /// <summary>提取模型运行结果
        /// </summary> 
        /// <returns></returns>
        string GetResult(bool autoSave = true);
    }
}