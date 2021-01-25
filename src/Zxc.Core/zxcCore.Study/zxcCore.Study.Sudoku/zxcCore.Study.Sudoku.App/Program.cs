using System;

namespace zxcCore.Sudoku.App
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            Sudoku pSudoku = new Sudoku(2);

            pSudoku.Init();
            pSudoku.SaveImage(@"C:\Users\16475\Desktop\myTest");

            pSudoku.Test();

        }
    }
}
