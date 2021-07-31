//===============================================================================
// Copyright @ 2021 Guangzhou Yijian Life Technology Co.,Ltd. All rights reserved.
// Copyright @ 2021 广州易简生活科技有限公司.  版权所有.
//===============================================================================
// 文件名称： 
// 功能描述：Word_Manager --汉字管理类
// 创建标识：zxc   2021-07-24
// 修改标识： 
// 修改描述：
//===============================================================================
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using zxcCore.Common;
using zxcCore.Extensions;
using zxcCore.zxcData.Cache.MemoryDB;
using zxcCore.zxcStudy.Record;

namespace zxcCore.zxcStudy.Word
{
    /// <summary>汉字管理类
    /// </summary>
    public class Word_Manager : Data_DB
    {
        public static readonly Word_Manager _Manager = new Word_Manager("");

        #region 属性及构造

        /// <summary>库表--汉字表
        /// </summary>
        public DataWord<Word> _zxcWords { get; set; }
        /// <summary>库表--拼音表
        /// </summary>
        public DataWord_Pingyin<Word_Pingyin> _zxcPinyins { get; set; }

        /// <summary>库表--汉字记录表
        /// </summary>
        public DataWord_Records<Word_Record> _zxcWordRecords { get; set; }


        protected internal string _dirWordBase = "";
        protected internal Word_Manager(string dirBase) : base(dirBase, typePermission_DB.Normal, true, "/Datas/DB_Word")
        {
            _dirWordBase = zxcConfigHelper.ConfigurationHelper.config["ZxcStudy:Word:Word_Datas"] + "/";
            if (_dirWordBase == "/")
            {
                _dirWordBase = Path.GetDirectoryName(this.DirBase) + "/Word_Datas/";
            }
            zxcIOHelper.checkPath(_dirWordBase + "Fonts/");
            zxcIOHelper.checkPath(_dirWordBase + "Sounds/");
            zxcIOHelper.checkPath(_dirWordBase + "Strokes/");
            zxcIOHelper.checkPath(_dirWordBase + "WordInfos/");
            this.InitWord_system();
        }

        #endregion


        protected override void OnDBModelCreating()
        {
            base.OnDBModelCreating();

            //初始zxc用户信息
            _zxcWords = new DataWord<Word>(); this.InitDBModel(_zxcWords);
            _zxcPinyins = new DataWord_Pingyin<Word_Pingyin>(); this.InitDBModel(_zxcPinyins);
            _zxcWordRecords = new DataWord_Records<Word_Record>(); this.InitDBModel(_zxcWordRecords);
        }
        /// <summary>初始系统用户
        /// </summary>
        protected void InitWord_system()
        {
            //初始字体库
            string filePath = _dirWordBase + "Word.csv";
            string[] lineSets = File.ReadAllLines(filePath);
            for (int i = 1; i < lineSets.Length; i++)
            {
                string[] strTemps = lineSets[i].Split(",");
                if (string.IsNullOrEmpty(strTemps[0] + strTemps[1]))
                    continue;

                Word pWord = this.GetWord(strTemps[1], false);
                if (pWord == null)
                {
                    pWord = new Word()
                    {
                        WordInd = Convert.ToInt32(strTemps[0]),
                        WordStr = strTemps[1],
                        WordType = strTemps[2]
                    };
                    this._zxcWords.Add(pWord, true, true);
                }
                else
                {
                    pWord.WordInd = Convert.ToInt32(strTemps[0]);
                    pWord.WordStr = strTemps[1];
                    pWord.WordType = strTemps[2];

                    //学习日志记录更新
                    List<Word_Record> lstWordRecord = this._zxcWordRecords.Where(e => e.WordStr == pWord.WordStr && e.IsDel == false).ToList();
                    foreach (var item in lstWordRecord)
                    {
                        item.WordStr = pWord.WordStr;
                        item.WordInd = pWord.WordInd;
                        item.WordType = pWord.WordType;
                    }
                }
            }
            this._zxcWords.SaveChanges(true);
        }

        //初始汉字拼音信息 
        protected internal bool InitWord_Pinyin(string strPinyin, string urlVedio)
        {
            Word_Pingyin pPingyin = new Word_Pingyin();
            pPingyin.Init_ByUrl(strPinyin, urlVedio, _dirWordBase + "Sounds/");
            return this._zxcPinyins.Add(pPingyin, true, true);
        }
        //初始汉字字体信息 
        protected internal bool InitWord(string strWord)
        {
            Word pWord = this.GetWord(strWord);
            if (pWord != null) return false;

            pWord = new Word();
            return this._zxcWords.Add(pWord, true, true);
        }
        //初始汉字学习信息 
        public bool InitWord_Record(string usrTag, Word pWord, typeWordRecord typeWordRecord, string recordInfo)
        {
            if (pWord == null) return false;
            if (this._zxcWordRecords.Find(e => e.WordStr == pWord.WordStr && e.RecordType == typeWordRecord && e.UserTag == usrTag && e.IsDel == false) != null)
                return false;

            Word_Record pWord_Record = new Word_Record()
            {
                UserTag = usrTag,
                WordStr = pWord.WordStr,
                WordInd = pWord.WordInd,
                WordType = pWord.WordType,
                RecordType = typeWordRecord,
                RecordInfo = recordInfo
            };
            return this._zxcWordRecords.Add(pWord_Record, true, true);
        }


        /// <summary>提取用户汉字
        /// </summary>
        /// <param name="usrTag"></param>
        /// <returns></returns>
        public Word GetWord_ByUser(string usrTag)
        {
            if (string.IsNullOrEmpty(usrTag)) return null;
            List<Word_Record> pRecords = this._zxcWordRecords.Where(e => e.UserTag == usrTag && e.RecordType == typeWordRecord.字形 && e.IsDel == false).ToList();

            //计算当前下一个汉字序号
            int nInd = 1;
            if (pRecords.Count > 0)
            {
                //int minInd = pRecords.Min(e => e.WordInd);
                int maxInd = pRecords.Max(e => e.WordInd);
                if (maxInd == pRecords.Count)
                    nInd = pRecords.Count + 1;
                else
                {
                    for (int i = 1; i <= maxInd; i++)
                    {
                        if (pRecords.Find(e => e.WordInd == i) != null)
                        {
                            nInd = i; break;
                        }
                    }
                }
            }
            Word pWord = this._zxcWords.Where(e => e.WordInd == nInd && e.IsDel == false).FirstOrDefault();
            if (pWord == null) return null;
            return this.GetWord(pWord.WordStr);
        }
        /// <summary>提取指定汉字对象
        /// </summary>
        /// <param name="strWord"></param>
        /// <returns></returns>
        public Word GetWord(string strWord, bool autoInit = true)
        {
            if (string.IsNullOrEmpty(strWord)) return null;
            Word pWord = this._zxcWords.Where(e => e.WordStr == strWord && e.IsDel == false).FirstOrDefault();

            if (pWord != null && pWord.VerTag != Word_Initial._APIs._verWord && autoInit)
            {
                if (Word_Initial._APIs.Init_WordInfo(pWord))
                    this._zxcWords.Add(pWord, true, true);
            }
            return pWord;
        }
        /// <summary>提取指定拼音对象
        /// </summary>
        /// <param name="strWord"></param>
        /// <returns></returns>
        public Word_Pingyin GetWord_Pinyin(string strPinyin)
        {
            if (string.IsNullOrEmpty(strPinyin)) return null;
            return this._zxcPinyins.Where(e => e.Pinyin == strPinyin && e.IsDel == false).FirstOrDefault();
        }

    }
}
