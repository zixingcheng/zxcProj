using System;

namespace zxcCore.Sudoku.App
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            Sudoku pSudoku = new Sudoku(2);
            try
            {
                pSudoku.Init();
                pSudoku.SaveImage(@"C:\Users\16475\Desktop\myTest");

                pSudoku.Test();
            }
            catch (Exception ex)
            {

                throw;
            }

            try
            {
                int nLv = 4;
                int nNums = 10;
                string dir = @"C:\Users\16475\Desktop\myTest\Lv" + nLv.ToString();
                if (System.IO.Directory.Exists(dir) == false)
                    System.IO.Directory.CreateDirectory(dir);
                for (int i = 0; i < nNums; i++)
                {
                    Sudoku pSudoku2 = new Sudoku(nLv);
                    pSudoku2.Init();
                    pSudoku2.SaveImage(dir, string.Format("{0}_{1}_{2}.png", DateTime.Now.Ticks, nLv, i));
                }
            }
            catch (Exception)
            {

                throw;
            }
            return;
        }
    }
}
