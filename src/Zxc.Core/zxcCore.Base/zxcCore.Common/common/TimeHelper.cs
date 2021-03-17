using System;

namespace zxcCore.Common
{
    public static class TimeHelper
    {
        public static DateTime checkTime(dynamic varTime)
        {
            if (varTime != null && varTime.GetType().Name == "DateTime")
            {
                return varTime;
            }
            else
            {
                DateTime dtTime = DateTime.Now;
                if (varTime != null && varTime != "")
                    dtTime = Convert.ToDateTime(varTime);
                return dtTime;
            }
        }
        public static DateTime checkTimeM(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = checkTime(varTime);

            int offset = bzero ? 0 : -1;
            dtTime = dtTime.AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset);
            return dtTime;
        }
        public static DateTime checkTimeM5(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = checkTimeM(varTime, bzero);
            if (dtTime.Minute % 5 != 0)
            {
                int offset = bzero ? 0 : -1;
            }
            return dtTime;
        }

        public static DateTime checkTimeH(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = checkTime(varTime);

            int offset = bzero ? 0 : -1;
            dtTime = dtTime.AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + offset);
            return dtTime;
        }
        public static DateTime checkTimeD(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = checkTime(varTime);

            int offset = bzero ? 0 : -1;
            dtTime = dtTime.AddHours(-dtTime.Hour).AddMinutes(-dtTime.Minute).AddSeconds(-dtTime.Second).AddMilliseconds(-dtTime.Millisecond + 0);
            return dtTime;
        }

    }
}
