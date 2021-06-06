namespace zpCore.zpDataCache.Memory
{
    /// <summary>数据结构接口
    /// </summary>
    interface IData
    {
        /// <summary>对象转为字符串
        /// </summary>
        string ToString();
        /// <summary>字符串转对象
        /// </summary>
        void FromString();

        /// <summary>对象转为Json对象
        /// </summary>
        dynamic ToJson();
        /// <summary>Json对象转对象
        /// </summary>
        /// <param name="jsonData"></param>
        /// <returns></returns>
        bool FromJson(dynamic jsonData);
    }

    /// <summary>数据结构接口-泛型
    /// </summary>
    interface IData<T> : IData
    {
        /// 数据值
        /// </summary>
        T Value { get; set; }
    }
}
