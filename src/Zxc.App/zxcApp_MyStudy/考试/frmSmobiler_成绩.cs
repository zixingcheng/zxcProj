using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Smobiler.Core;
using Smobiler.Core.Controls;

namespace zxcApp.MyStudy
{
    partial class frmSmobiler_成绩 : Smobiler.Core.Controls.MobileForm
    {
        private int m_nNumRight = 0; int m_nNumWrong = 0; int m_nFraction = 0;

        public frmSmobiler_成绩(int nRight, int nWrong, int nFraction) : base()
        {
            m_nNumRight = nRight;
            m_nNumWrong = nWrong;
            m_nFraction = nFraction;

            //This call is required by the SmobilerForm.
            InitializeComponent();
        }
        private void frmSmobiler_成绩_Load(object sender, EventArgs e)
        {
            string strNumber = m_nFraction.ToString();
            this.lab_Static.Text = "总计：答错" + m_nNumWrong.ToString() + "题，答对" + m_nNumRight.ToString() + "题。";
            this.img_1.ResourceID = strNumber.Substring(0, 1) + ".png";
            this.lab_R2.Left = this.img_1.Left + this.img_1.Width;

            this.img_2.Visible = false;
            this.img_3.Visible = false;
            if (strNumber.Length > 1)
            {
                this.img_2.Visible = true;
                this.img_2.ResourceID = strNumber.Substring(1, 1) + ".png";
                this.lab_R2.Left = this.img_2.Left + this.img_2.Width;

                if (strNumber.Length > 2)
                {
                    this.img_3.Visible = true;
                    this.img_3.ResourceID = strNumber.Substring(2, 1) + ".png";
                    this.lab_R2.Left = this.img_3.Left + this.img_3.Width;
                }
            }
        }

        private void btn_控制_Press(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}