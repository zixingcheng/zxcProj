using System;
using System.Collections.Generic;
using System.Text;

namespace zxcCore.Sudoku
{
	public class Statics_buff
	{
		public int X { get; }
		public int Y { get; }
		public int Tag { get; protected set; }
		public int Nums { get; protected set; }
		public int Type { get; protected set; }
		public bool Lock { get; protected set; }
		int Nums_last = 0;

		public Statics_buff(int x, int y, int nums, int type)
		{
			X = x;
			Y = y;
			Nums = nums;
			Type = type;
			Tag = getTag(x, y, type);
		}

		public bool setNums(int delta)
		{
			if(Lock && delta < 0)
				this.setLock(false);

			Nums += delta;
			if (Nums <= 0)
				Nums = 0;
			if (Nums >= 9)
				this.setLock(true);
			return true;
		}
		public bool setLock(bool locked)
		{
			Lock = locked;
			if (locked)
			{
				Nums_last = Nums;
				Nums = -1;
				//Console.WriteLine(string.Format("   {0},{1}  --上锁： {2} ", X, Y, Nums));
			}
			else
			{
				Nums = Nums_last;
			}
			return locked;
		}


		public static int getTag(int row, int col, int type)
		{
			return type == 2 ? row * 3 + col + type * 10 : row + col + type * 10;
		}
	}
}