using System;
using System.Collections.Generic;
using System.Text;
using zpCore.GIS.Trans.Algorithm;
using zpCore.GIS.Trans;
using System.IO;

namespace zpCore.GIS
{
    public class Division
    {
        #region 属性及构造

        protected internal string _Name = "中国";
        public string Name
        {
            set { _Name = value; }
            get { return _Name; }
        }
        protected internal int _Level = 0;
        public int Level
        {
            set { _Level = value; }
            get { return _Level; }
        }

        protected internal Division _Parent = null;
        public Division Parent
        {
            set { _Parent = value; }
            get { return _Parent; }
        }
        protected internal List<Division> _Childs = null;
        public List<Division> Childs
        {
            set { _Childs = value; }
            get { return _Childs; }
        }


        public Division(string name, int level)
        {
            this.Init(name, level);
        }
        public Division(string name)
        {
            this.InitDivisions(name, 0);
        }
        ~Division()
        {
        }

        #endregion

        /// <summary>初始
        /// </summary>
        /// <param name="name"></param>
        /// <param name="level"></param>
        /// <returns></returns>
        public bool Init(string name, int level)
        {
            _Name = name;
            _Level = level;
            return true;
        }
        public bool InitDivisions(string name, int levelBase = 0)
        {
            string[] strNames = name.Split(".");
            if (strNames.Length < 1) return false;

            _Name = strNames[0];
            _Level = levelBase;
            Division parentDivision = this;
            for (int i = 1; i < strNames.Length; i++)
            {
                Division pDivision = new Division(strNames[i], levelBase + i);
                parentDivision.Childs = new List<Division>() { pDivision };
                parentDivision = pDivision;
            }
            return true;
        }

        public new string ToString()
        {
            string strName = "";
            Division pParent = _Parent;
            while (pParent != null)
            {
                strName = pParent.Name + "." + strName;
                pParent = pParent._Parent;
            }

            List<Division> pChilds = _Childs;
            while (pChilds != null)
            {
                Division pChild = pChilds[0];
                strName += "." + pChild.Name;
                pChilds = pChild._Childs;
            }
            strName = strName.Replace("..", ".");
            if (strName.Substring(0, 1) == ".")
                strName = strName.Substring(1);
            return strName;
        }

    }
}
