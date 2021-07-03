using System;
using zxcCore.Enums;

namespace zxcCore.Common
{
    public static class zxcTimeHelper
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
        public static DateTime checkTimeS(dynamic varTime, bool bzero = true)
        {
            DateTime dtTime = checkTime(varTime);

            int offset = bzero ? 0 : -1;
            dtTime = dtTime.AddMilliseconds(-dtTime.Millisecond + offset);
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


        /// <summary>按时间频率修正时间
        /// </summary>
        /// <param name="dtBase"></param>
        /// <param name="timeFrequency"></param>
        /// <returns></returns>
        public static DateTime CheckTime(DateTime dtBase, typeTimeFrequency timeFrequency)
        {
            DateTime dtTime = dtBase;
            switch (timeFrequency)
            {
                case typeTimeFrequency.day:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, 0, 0, 0);
                    break;
                case typeTimeFrequency.m1:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, dtBase.Minute, 0);
                    break;
                case typeTimeFrequency.m5:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, (int)Math.Floor(dtBase.Minute / 5.0) * 5, 0);
                    break;
                case typeTimeFrequency.m10:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, (int)Math.Floor(dtBase.Minute / 10.0) * 10, 0);
                    break;
                case typeTimeFrequency.m15:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, (int)Math.Floor(dtBase.Minute / 15.0) * 15, 0);
                    break;
                case typeTimeFrequency.m30:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, (int)Math.Floor(dtBase.Minute / 30.0) * 30, 0);
                    break;
                case typeTimeFrequency.m60:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, 0, 0);
                    break;
                case typeTimeFrequency.m120:
                    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, 0, 0);
                    break;
                //case typeTimeFrequency.Week:
                //    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, 0, 0, 0);
                //    break;
                //case typeTimeFrequency.Second_30:
                //    dtTime = new DateTime(dtBase.Year, dtBase.Month, dtBase.Day, dtBase.Hour, dtBase.Minute, (int)Math.Floor(dtBase.Second / 30.0) * 30);
                //    break;
                default:
                    break;
            }
            return dtTime;
        }
    }
}
