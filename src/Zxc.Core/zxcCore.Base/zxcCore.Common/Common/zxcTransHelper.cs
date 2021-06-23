using System;

namespace zxcCore.Common
{
    public static class zxcTransHelper
    {
        /// <summary>转换为Double
        /// </summary>
        /// <param name="data"></param>
        /// <param name="decimals">精度</param>
        /// <returns></returns>
        public static double ToDouble(dynamic data, int decimals = 6)
        {
            if (data == null) return 0;
            double dValue = Convert.ToDouble(data);
            return Math.Round(dValue, decimals);
        }

    }
}
