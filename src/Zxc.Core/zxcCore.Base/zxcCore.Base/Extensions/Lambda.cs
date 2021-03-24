using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;

namespace zxcCore.Extensions
{
    public class Lambda
    {
        /// <summary>lambda操作（外部传入参数）
        /// </summary>
        /// <param name="source">源对象</param>
        /// <param name="predicate">lambda对象</param>
        /// <returns></returns>
        public static IEnumerable<T> LambdaDo<T>(IEnumerable<T> source, Func<IEnumerable<T>, IEnumerable<T>> predicate)
        {
            var objTemp = predicate(source);
            return objTemp;
        }

    }
}
