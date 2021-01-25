using System;
using System.Collections.Generic;
using System.Text;
using zxcCore.Image;

namespace zxcCore.Sudoku
{
	public class SudokuGrid
	{
		Sudoku _sudoku;
		ImageObj _img = new ImageObj(1754, 1240);       //595, 842；1240, 1754；2480, 3508
		string _colorLine = "black";
		int _x0, _y0, _h, _w, size = 122;

		public SudokuGrid(Sudoku sudoku)
		{
			_sudoku = sudoku;
			this.Init();
		}


		public bool Init()
		{
			this.InitGrid();
			return true;
		}
		public bool InitGrid(bool bHead = true)
		{
			_w = size * 9;
			_h = _w;
			_x0 = (_img.Image.Width - _w) / 2;
			_y0 = (_img.Image.Height - _h) / 2;
			float thickness = 1;

			//格网
			var color = ImageColor.Parse(_colorLine);
			for (int i = 0; i <= _sudoku._rows; i++)
			{
				thickness = i % 3 == 0 ? 2 : 0.6f;
				_img.Draw(_x0, _y0 + i * size, color, thickness, _w, 1);
			}
			for (int i = 0; i <= _sudoku._cols; i++)
			{
				thickness = i % 3 == 0 ? 2 : 0.6f;
				_img.Draw(_x0 + i * size, _y0, color, thickness, 1, _h);
			}

			//行列注解
			List<string> lstHead = new List<string>() { "A", "B", "C", "D", "E", "F", "G", "H", "I" };
			if (bHead)
			{
				for (int i = 0; i < _sudoku._rows; i++)
				{
					_img.DrawText(_x0 - size / 2, _y0 + i * size + size / 5 * 3, color, (i + 1).ToString(), null, 16);
					_img.DrawText(_x0 + size / 2 + _w, _y0 + i * size + size / 5 * 3, color, (i + 1).ToString(), null, 16);
					_img.DrawText(_x0 + i * size + size / 2, _y0 - size / 3, color, lstHead[i], null, 16);
					_img.DrawText(_x0 + i * size + size / 2, _y0 + size / 3 + _h + 6, color, lstHead[i], null, 16);
				}
			}
			return true;
		}
		public bool InitValue()
		{
			var color = ImageColor.Parse(_colorLine);
			for (int y = 0; y < _sudoku._rows; y++)
			{
				for (int x = 0; x < _sudoku._cols; x++)
				{
					if (_sudoku._values[y, x] == 0) continue;
					_img.DrawText(_x0 + x * size + size / 2 - 16, _y0 + y * size + size / 5 * 3 + 18, color, _sudoku._values[y, x].ToString(), null, 68);
				}
			}

			//标题
			_img.DrawText(_y0, _img.Image.Height - size / 5, color, string.Format("Lv {0}.     Spaces: {1}", _sudoku.Level.ToString(), _sudoku._spaces.ToString()), null, 18);
			return true;
		}

		public bool Save(string path)
		{
			return _img.Save(path);
		}

	}
}