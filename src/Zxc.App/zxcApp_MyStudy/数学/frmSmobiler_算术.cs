using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Smobiler.Core;
using Smobiler.Core.Controls;

namespace zxcApp.MyStudy
{
    partial class frmSmobiler_算术 : Smobiler.Core.Controls.MobileForm
    {
        private readonly Image[] imgs = new Image[20];               //图片数组 
        private readonly ImageButton[] imgRs = new ImageButton[4];   //图片数组 
        private SortedList<int, int[]> m_lstParms = new SortedList<int, int[]>();
        private SortedList<int, int[]> m_lstStatics = new SortedList<int, int[]>();
        private int[] m_Parms = { 0, 0, 0, 0 };                      //全局参数
        private int m_nTimer = 4; int m_nTimer2 = 0;
        private int m_nTimerCountdown = 30; int m_nTimerCountdown2 = 0;
        private int m_nNumber = 3; int m_nNumber2 = 0;
        private int m_nSteptimes = 1; int m_nSteptimes2 = 0;
        private int m_nIndex = 0;
        private readonly Random m_Random = new Random(unchecked((int)DateTime.Now.Ticks));
        private readonly string imgPath = AppDomain.CurrentDomain.BaseDirectory + "Resources\\User\\Math\\Number\\";

        public frmSmobiler_算术() : base()
        {
            //This call is required by the SmobilerForm.
            InitializeComponent();
        }
        private void FrmSmobiler_算术_Load(object sender, EventArgs e)
        {
            for (int i = 1; i < 21; i++)
            {
                Image img = new Image();
                img.Visible = false;
                img.Size = new System.Drawing.Size(80, 80);
                img.Name = "img_" + i.ToString();
                img.ResourcePath = "resNumber";
                img.ResourceMode = ResourceMode.File;
                img.ResourceID = "case.gif";
                imgs[i - 1] = img; this.Controls.Add(img);
            }
            imgRs[0] = this.imgR_0; imgRs[1] = this.imgR_1; imgRs[2] = this.imgR_2;
            this.Reset_题库(1, 9, 1, 9);
        }

        private void btn_控制_Press(object sender, EventArgs e)
        {
            this.timer1.Stop();
            if (this.btn_控制.Text == "开始")
            {
                MessageBox.Show("小朋友，开始考试啦!");
                m_lstStatics = new SortedList<int, int[]>();
                m_nNumber2 = 0; this.Next_题目();
            }
            else if (this.btn_控制.Text == "暂停")
            {
                this.btn_控制.Text = "继续";
                this.timer2.Stop();
            }
            else if (this.btn_控制.Text == "继续")
            {
                this.btn_控制.Text = "暂停";
                this.timer2.Start();
            }
            else if (this.btn_控制.Text.Substring(0, 2) == "下一")
            {
                this.Next_题目();
            }
        }
        private void imgR_Press(object sender, EventArgs e)
        {
            ImageButton imgR = (ImageButton)sender;
            if (imgR.Tag == null) { return; }

            int index = (int)imgR.Tag;
            if (m_Parms[3] == m_Parms[index])
            {
                //正确
                this.img_Result.ResourceID = imgR.ResourceID;
                this.img_Right.Location = imgR.Location;
                this.img_Right.Visible = true;
                this.Statics_题目(true);
                this.Play_Audio("right");
            }
            else
            {
                //错误
                if (this.img_Wrong.Visible == false)
                {
                    this.img_Wrong.Location = imgR.Location;
                    this.img_Wrong.Visible = true;
                }
                else
                {
                    this.img_Wrong2.Location = imgR.Location;
                    this.img_Wrong2.Visible = true;
                }
                this.Statics_题目(false);
                this.Play_Audio("wrong");
            }
        }
        private void imgBtn_Help_Press(object sender, EventArgs e)
        {
            int nY = 0;
            nY = this.Refesh_HelpInfo(this.panel1, m_Parms[1]);
            this.Refesh_HelpInfo(this.panel1, m_Parms[2], 200, 165, 10);
        }
        private void timer1_Tick(object sender, EventArgs e)
        {
            m_nTimer2 += 1;
            this.btn_控制.Text = "下一题（" + (m_nTimer - m_nTimer2).ToString() + "）秒";
            this.btn_控制.Enabled = true;
            if (m_nTimer2 >= m_nTimer)
            {
                m_nTimer2 = 0; timer1.Stop();      //关闭计时器
                this.Next_题目();
            }
        }
        private void timer2_Tick(object sender, EventArgs e)
        {
            m_nTimerCountdown2 += 1;
            this.lab_Countdown.Text = "剩余时间：" + (m_nTimerCountdown - m_nTimerCountdown2).ToString() + "秒！";
            if (m_nTimerCountdown2 >= m_nTimerCountdown)
            {
                m_nTimerCountdown2 = 0; this.timer2.Stop();     //关闭倒数
                this.Statics_题目(false);                       //标识为错误
                this.Next_题目();
            }
        }

        //下一题
        private void Next_题目(int nType = 1)
        {
            if (this.Check_答完()) return;  //题目答完

            this.img_遮挡.Visible = false;
            this.img_Right.Visible = false;
            this.img_Wrong.Visible = false;
            this.img_Wrong2.Visible = false;
            if (m_nSteptimes2 >= m_nSteptimes) this.btn_控制.Enabled = false; //暂停次数限制
            this.btn_控制.Text = "暂停";
            this.lab_Countdown.Text = "剩余时间：" + m_nTimerCountdown.ToString() + "秒！";
            m_nTimerCountdown2 = 0; this.timer2.Start();

            int[] pParams = m_lstParms[0];
            int index = m_Random.Next(0, m_lstParms.Count);
            bool bReset = true;
            while (bReset)
            {
                pParams = m_lstParms[index];

                //限定运算符号
                if (pParams[0] != nType)
                {
                    index = m_Random.Next(0, m_lstParms.Count);
                    continue;
                }
                bReset = false;
            }
            m_nIndex = index; m_Parms = pParams;
            m_lstStatics.Add(m_lstStatics.Count, new int[] { m_nIndex, 0, 0, 0 });
            this.Reset_题目(pParams);
        }
        private void Next_题目_延时()
        {
            if (this.Check_答完()) return;                        //题目答完

            this.btn_控制.Text = "下一题（" + m_nTimer.ToString() + "）秒";
            this.img_遮挡.Visible = true;
            this.lab_Countdown.Text = ""; this.timer2.Stop();     //关闭倒数
            m_nTimer2 = 0; this.timer1.Start();
        }
        //题目信息绘制
        private void Reset_题目(int[] pParams)
        {
            string strSymbol = "";
            switch (pParams[0])
            {
                case 1:
                    strSymbol = "+";
                    break;
                case 2:
                    strSymbol = "-";
                    break;
                case 3:
                    strSymbol = "*";
                    break;
                case 4:
                    strSymbol = "/";
                    break;
                default:
                    break;
            }

            this.img_1.ResourceID = pParams[1].ToString() + ".png";
            this.img_2.ResourceID = pParams[2].ToString() + ".png";
            this.img_3.ResourceID = "=.png";
            this.img_Symbol.ResourceID = strSymbol.ToString() + ".png";
            this.img_Result.ResourceID = "what.jpg";

            //备选结果
            for (int i = 4; i < 7; i++)
            {
                //imgRs[i - 4].ResourcePath = "resNumber";
                imgRs[i - 4].ResourceID = pParams[i].ToString() + ".png";
                imgRs[i - 4].Tag = i;
            }
        }
        //创建新题库(可设置范围)
        private void Reset_题库(int minValue = 1, int maxValue = 9, int minResult = 1, int maxResult = 9)
        {
            //循环所有值
            for (int i = minValue; i <= maxValue; i++)
            {
                for (int j = minValue; j <= maxValue; j++)
                {
                    for (int k = 1; k < 5; k++)
                    {
                        int[] pParams = this.Create_题目(i, j, k, minResult, maxResult);
                        if (pParams[3] == -999999)
                        {
                            continue;
                        }
                        m_lstParms.Add(m_lstParms.Count, pParams);
                    }
                }
            }
        }
        //创建单个题目参数信息
        private int[] Create_题目(int value1, int value2, int mType = 1, int minResult = 0, int maxResult = int.MaxValue)
        {
            int result = 0;
            switch (mType)
            {
                case 1:
                    result = value1 + value2;
                    break;
                case 2:
                    result = value1 - value2;
                    break;
                default:
                    break;
            }
            if (result > maxResult || result < minResult)
            {
                result = -999999;
            }

            int[] pParams = { mType, value1, value2, result, -1, -1, -1 };
            int index = m_Random.Next(4, 6);
            pParams[index] = result;

            if (result != -999999)
            {
                for (int i = 4; i < 7; i++)
                {
                    if (i == index) { continue; }

                    int valueW = m_Random.Next(minResult, maxResult);
                    for (int j = 4; j < 7; j++)
                    {
                        if (pParams[j] == valueW)
                        {
                            valueW = m_Random.Next(minResult, maxResult);
                            j = 3; continue;
                        }
                    }
                    pParams[i] = valueW;
                }
            }
            return pParams;
        }

        //统计
        private void Statics_题目(bool isTrue)
        {
            if (m_nNumber2 >= m_nNumber)    //题目答完
            {
                //统计答题信息
                int nCount_right = 0;
                m_nNumber = m_lstStatics.Count;
                for (int i = 0; i < m_nNumber; i++)
                {
                    int[] pParams = m_lstStatics[i];
                    if (pParams[1] == 1)
                        nCount_right += 1;
                }

                int nFraction = (int)(nCount_right * 1.0 / m_nNumber * 100);
                MessageBox.Show("小朋友，考试分数为" + nFraction.ToString() + "!");
            }
            else
            {
                //pParams：题目索引、对错、计算次数、错误次数
                int[] pParams = m_lstStatics[m_lstStatics.Count - 1];
                pParams[2] += 1;
                if (isTrue)
                {
                    pParams[1] = 1;
                    m_nNumber2 += 1;
                    this.Next_题目_延时();
                }
                else
                {
                    pParams[3] += 1;
                    if (pParams[3] >= 2)    //最多两次错误
                    {
                        m_nNumber2 += 1;
                        this.Next_题目_延时();
                    }
                }
            }
        }
        //检查是否答完
        private bool Check_答完()
        {
            if (m_nNumber2 >= m_nNumber)    //题目答完
            {
                this.timer2.Stop();         //关闭倒数
                this.lab_Countdown.Text = "";
                this.btn_控制.Text = "开始";
                this.Statics_题目(false);
                return true;
            }
            return false;
        }
        //播放声音
        private void Play_Audio(string tag)
        {
            try
            {
                this.Client.PlayAudio(tag + ".aac", "resNumber", ResourceMode.File);
            }
            catch (Exception ex)
            {
                this.Client.PlayAudio("2.aac", "resNumber", ResourceMode.File);
            }
        }

        //更新帮助图片内容
        private int Refesh_HelpInfo(Panel panel, int nNum, int pos_X = 6, int pos_Y = 165, int index = 0)
        {
            int nCols = 13;
            int nWidth = this.Width / (nCols + 1);
            int nBoder = 2;

            int nX = 0, nY = 0;
            panel.Controls.Clear();
            for (int i = 0; i < nNum; i++)
            {
                int nRow = i / 5;
                int nCol = i - nRow * 5;
                nX = pos_X + nBoder * (1 + nCol) + nWidth * nCol;
                nY = pos_Y + nRow * (nWidth + nBoder);

                imgs[i + index].Location = new System.Drawing.Point(nX, nY);
                imgs[i + index].Width = nWidth;
                imgs[i + index].Height = nWidth;
                imgs[i + index].Visible = true;
                panel.Controls.Add(imgs[i + index]);
            }
            return nY + nWidth;
        }

    }
}