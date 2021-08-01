using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using zxcCore.Extensions;

namespace zxcCore.Sudoku
{
    public class Sudoku
    {
        #region 属性及构造

        protected internal string _CheckCode = "";
        public string CheckCode
        {
            get { return _CheckCode; }
        }
        protected internal int _Level = 0;
        public int Level
        {
            get { return _Level; }
        }


        protected internal int _spaces = 0;         //留白数量
        protected internal int _rowsCell = 3;       //9宫格行数
        protected internal int _colsCell = 3;       //9宫格列数
        protected internal int _rows = 9;           //总行数
        protected internal int _cols = 9;           //总列数
        protected internal int[,] _values = null;   //全部行列值
        protected internal List<int> _valuesSpare = null;           //9宫格备用值
        protected internal Dictionary<int, Statics_buff> _statics = null;
        protected internal bool _debug = true;
        protected internal int _numBacks = 0;
        protected internal SudokuGrid _sudokuGrid = null;

        public Sudoku(int level)
        {
            //_debug = false;
            _Level = level;
            _valuesSpare = new List<int>() { 1, 2, 3, 4, 5, 6, 7, 8, 9 };
        }
        ~Sudoku()
        {
        }

        #endregion

        #region 测试

        //打印
        public bool Test()
        {
            Init(20, false);
            _values[0, 0] = 8;
            _values[1, 2] = 3;
            _values[1, 3] = 6;
            _values[2, 1] = 7;
            _values[2, 4] = 9;
            _values[2, 6] = 2;
            _values[3, 1] = 5;
            _values[3, 5] = 7;
            _values[4, 4] = 4;
            _values[4, 5] = 5;
            _values[4, 6] = 7;
            _values[5, 3] = 1;
            _values[5, 7] = 3;
            _values[6, 2] = 1;
            _values[6, 7] = 6;
            _values[6, 8] = 8;
            _values[7, 2] = 8;
            _values[7, 3] = 5;
            _values[7, 7] = 1;
            _values[8, 1] = 9;
            _values[8, 6] = 4;

            Console.WriteLine("Test Solve");
            this.Print();
            Console.WriteLine("");

            _debug = true;
            if (this.Solve())
            {
                Console.WriteLine("Test Solved");
            }
            return true;
        }

        #endregion

        //初始
        public bool Init()
        {
            return Init(this._Level);
        }
        //初始
        public bool Init(int level, bool autoData = true)
        {
            _Level = level;
            _Level = _Level > 20 ? 20 : _Level;
            _values = new int[9, 9];
            _sudokuGrid = null;
            if (autoData == false) return true;

            //求解
            this.InitValue();       //初始随机种子
            if (this.Solve())
            {
                Console.WriteLine(string.Format("MD5Hash: {0}", this.checkMD5Hash()));

                //按级别初始
                bool bResult = this.InitValue_Space(_Level);
                this.Print();
                //if (this.Solve())
                //{
                //    Console.WriteLine(string.Format("MD5Hash: {0}", this.checkMD5Hash()));
                //}
                return bResult;
            }
            return true;
        }
        //创建初始区域中心宫
        protected bool InitValue()
        {
            //初始 中心宫
            InitValue_Cell(1, 1);

            //初始行
            for (int j = 0; j < _cols; j++)
            {
                _values[3, j] = this.InitValue_Grid(3, j, _values[3, j]);
                //_values[5, j] = this.InitValue_Grid(5, j, _values[5, j]);
            }

            //初始列
            for (int i = 0; i < _rows; i++)
            {
                _values[i, 3] = this.InitValue_Grid(i, 3, _values[i, 3]);
                //_values[i, 5] = this.InitValue_Grid(i, 5, _values[i, 5]);
            }
            return true;
        }
        //创建初始宫
        protected int InitValue_Cell(int rowCell, int colCell)
        {
            //计算9宫格的数据区间
            int rowMin = rowCell * _rowsCell;
            int rowMax = rowMin + _rowsCell;
            int colMin = colCell * _colsCell;
            int colMax = colMin + _colsCell;

            for (int i = rowMin; i < rowMax; i++)
            {
                for (int j = colMin; j < colMax; j++)
                    _values[i, j] = this.InitValue_Grid(i, j, _values[i, j]);
            }
            return rowCell * colCell;
        }
        //创建随机数(剔除重复)
        protected int InitValue_Grid(int row, int col, int defalut)
        {
            //剔除重复
            List<int> values = getValues(row, col);
            List<int> valuesSpare = zxcCloneDeep.Clone_List<int>(_valuesSpare);
            for (int i = 0; i < values.Count; i++)
            {
                int valueInd = valuesSpare.FindIndex(s => s == values[i]);
                if (valueInd >= 0)
                {
                    valuesSpare.RemoveAt(valueInd);
                }
            }

            int ind = new Random().Next(valuesSpare.Count);
            return valuesSpare.Count == 0 ? defalut : valuesSpare[ind];
        }
        //创建随机空白处
        protected bool InitValue_Space_Random(int level)
        {
            List<int> lstGrid = new List<int>();
            _spaces = 6 + level * 3;

            int ind, x, y, nSpace = _spaces;
            for (int i = 0; i < _rows; i++)
            {
                for (int j = 0; j < _cols; j++)
                    lstGrid.Add(i * _rows + j);
            }

            while (nSpace > 0)
            {
                ind = new Random().Next(lstGrid.Count);
                x = (int)Math.Floor(1.0 * ind / _rows);
                y = ind - x * _rows;
                _values[x, y] = 0;
                nSpace--;
            }
            return true;
        }
        //创建随机空白处-9宫随机-均匀
        protected bool InitValue_Space(int level)
        {
            _spaces = 6 + level * 3;

            int nSpace = _spaces, nCells = 6;
            while (nSpace > 0)
            {
                this.InitValue_Space_Cells(nCells);
                nSpace -= nCells;
                nCells++;
                if (nCells > _rows) nCells = _rows;
                if (nCells > nSpace) nCells = nSpace;
            }
            return true;
        }
        //创建随机空白处-9宫随机
        protected bool InitValue_Space_Cells(int cells)
        {
            List<int> lstCell = zxcCloneDeep.Clone_List<int>(_valuesSpare);
            int ind, nCells = cells;
            while (nCells > 0)
            {
                ind = new Random().Next(lstCell.Count);
                this.InitValue_Space_Cell(lstCell[ind] - 1);
                lstCell.RemoveAt(ind);
                nCells--;
            }
            return true;
        }
        //创建随机空白处-宫
        protected bool InitValue_Space_Cell(int indCell)
        {
            int x = (int)Math.Floor(1.0 * indCell / _rowsCell);
            int y = indCell - x * _rowsCell;

            List<int> lstGrid = new List<int>();
            for (int i = x * _rowsCell; i < x * _rowsCell + _rowsCell; i++)
            {
                for (int j = y * _colsCell; j < y * _colsCell + _colsCell; j++)
                    if (_values[i, j] != 0)
                        lstGrid.Add(i * _rows + j);
            }

            int ind = new Random().Next(lstGrid.Count);
            x = (int)Math.Floor(1.0 * lstGrid[ind] / _rows);
            y = lstGrid[ind] - x * _rows;
            _values[x, y] = 0;
            return true;
        }


        //求解
        protected bool Solve()
        {
            try
            {
                DateTime dtStart = DateTime.Now;
                _numBacks = 0;

                //统计获取第一个种子
                this.Statics();
                (int x, int y) = getSolve_Next();

                //返回计算结果
                bool bResult = Solve(x, y);
                if (bResult)
                    this.Print();
                DateTime dtEnd = DateTime.Now;
                Console.WriteLine(string.Format("**求解完成**，耗时 {0} s，回退 {1} 步。", (dtEnd - dtStart).TotalMilliseconds / 1000, _numBacks));
                return bResult;
            }
            catch (Exception)
            {
                throw;
            }
        }
        //求解-递归
        protected bool Solve(int row, int col)
        {
            try
            {
                //提取备用值,循环判断
                if (_debug)
                    Console.WriteLine(string.Format("{0},{1}  --求解：", row, col));
                List<int> valuesSpare = Solve_Values(row, col);
                if (valuesSpare.Count == 0)
                    return false;

                //循环求解
                for (int i = 0; i < valuesSpare.Count; i++)
                {
                    _values[row, col] = valuesSpare[i];
                    this.Statics(row, col, 1);
                    if (_debug)
                        Console.WriteLine(string.Format("   {0},{1}  --求解值：{2} ", row, col, _values[row, col]));

                    //下一个种子
                    (int x, int y) = getSolve_Next();
                    if (x == -1 && y == -1) return true;
                    if (x > -1 && y > -1)
                    {
                        //递归求解
                        if (this.Solve(x, y))
                            return true;
                    }

                    //恢复-重新统计
                    if (_debug)
                        Console.WriteLine(string.Format("   {0},{1}  --无解： {2} ", x, y, _values[x, y]));
                    _values[row, col] = 0;
                    this.Statics();

                    //this.Statics(row, col, -1);
                    if (_debug)
                        Console.WriteLine(string.Format("   {0},{1}  --已回退：{2}, 已重新统计", row, col, _values[row, col], _values[row, col]));
                }
                return false;

            }
            catch (Exception)
            {

                throw;
            }
        }
        //计算该位置的备用
        protected List<int> Solve_Values(int row, int col)
        {
            //剔除重复
            List<int> values = getValues(row, col);
            List<int> valuesSpare = zxcCloneDeep.Clone_List<int>(_valuesSpare);
            for (int i = 0; i < values.Count; i++)
            {
                int valueInd = valuesSpare.FindIndex(s => s == values[i]);
                if (valueInd >= 0)
                {
                    valuesSpare.RemoveAt(valueInd);
                }
            }
            return valuesSpare;
        }
        //统计获取第一个种子
        protected (int, int) getSolve_Next()
        {
            _statics = _statics.OrderByDescending(p => p.Value.Nums).ToDictionary(p => p.Key, o => o.Value);
            Statics_buff pStatics_buff = _statics.Values.First();

            if (pStatics_buff.Type == 0)
            {
                for (int j = 0; j < this._cols; j++)
                {
                    int value = _values[pStatics_buff.X, j];
                    if (!checkValue(value))
                        return (pStatics_buff.X, j);
                }
            }
            else if (pStatics_buff.Type == 1)
            {
                for (int i = 0; i < this._rows; i++)
                {
                    int value = _values[i, pStatics_buff.Y];
                    if (!checkValue(value))
                        return (i, pStatics_buff.Y);
                }
            }
            else if (pStatics_buff.Type == 2)
            {
                //计算9宫格的数据区间
                int rowMin = pStatics_buff.X * _rowsCell;
                int rowMax = rowMin + _rowsCell;
                int colMin = pStatics_buff.Y * _colsCell;
                int colMax = colMin + _colsCell;

                for (int i = rowMin; i < rowMax; i++)
                {
                    for (int j = colMin; j < colMax; j++)
                    {
                        int value = _values[i, j];
                        if (!checkValue(value))
                            return (i, j);
                    }
                }
            }
            return (-1, -1);
        }


        //统计各格子可用数据数
        protected bool Statics()
        {
            //统计行、列、宫有效信息
            _statics = new Dictionary<int, Statics_buff>();
            for (int i = 0; i < this._rows; i++)
                Statics_Cell_Buffer(i, 0, 0);

            for (int j = 0; j < this._cols; j++)
                Statics_Cell_Buffer(0, j, 1);

            for (int i = 0; i < _rowsCell; i++)
            {
                for (int j = 0; j < _colsCell; j++)
                    Statics_Cell_Buffer(i, j, 2);
            }
            _numBacks++;
            Console.WriteLine(string.Format("**求解数**，回退 {0} 步。", _numBacks));
            return true;
        }
        //修正统计各格子可用数据数
        protected bool Statics(int row, int col, int delta = 1)
        {
            //行、列、宫
            _statics[Statics_buff.getTag(row, 0, 0)].setNums(delta);
            _statics[Statics_buff.getTag(0, col, 1)].setNums(delta);

            int rowCell = getCellInd_Row(row);
            int colCell = getCellInd_Col(col);
            _statics[Statics_buff.getTag(rowCell, colCell, 2)].setNums(delta);
            return true;
        }
        //统计行、列、宫有效数
        protected int Statics_Cell(int row, int col, int type)
        {
            Dictionary<int, int> values = new Dictionary<int, int>();
            if (type == 0)
                getValues_Row(row, values);
            else if (type == 1)
                getValues_Col(col, values);
            else if (type == 2)
                getValues_Cell(row * _rowsCell, col * _colsCell, values);
            return values.Count;
        }
        // //统计行、列、宫有效数信息
        protected void Statics_Cell_Buffer(int row, int col, int type)
        {
            int nNums = this.Statics_Cell(row, col, type);
            Statics_buff pStatics = new Statics_buff(row, col, nNums, type);

            if (nNums == 9)
                pStatics.setLock(true);
            _statics[pStatics.Tag] = pStatics;
        }


        //打印
        protected bool Print()
        {

            for (int i = 0; i < this._rows; i++)
            {
                Console.WriteLine();
                for (int j = 0; j < this._cols; j++)
                {
                    Console.Write(string.Format("{0},", _values[i, j]));
                }
            }
            Console.WriteLine();
            return true;
        }
        //转换未图片
        public bool SaveImage(string path, string name = "")
        {
            _sudokuGrid = new SudokuGrid(this);
            return _sudokuGrid.InitValue() && _sudokuGrid.Save(path, name);
        }

        #region 属性及构造

        /// <summary>提取行、列、9宫格内所有有效值集
        /// </summary>
        /// <param name="row"></param>
        /// <param name="col"></param>
        /// <returns></returns>
        protected List<int> getValues(int row, int col)
        {
            Dictionary<int, int> values = new Dictionary<int, int>();
            getValues_Row(row, values);
            getValues_Col(col, values);
            getValues_Cell(row, col, values);
            return values.Keys.ToList();
        }
        /// <summary>提取行有效值
        /// </summary>
        /// <param name="row"></param>
        /// <param name="values">有效值集</param>
        /// <returns></returns>
        protected bool getValues_Row(int row, Dictionary<int, int> values)
        {
            for (int j = 0; j < this._cols; j++)
            {
                int value = _values[row, j];
                if (checkValue(value))
                    values[value] = 1;
            }
            return true;
        }
        /// <summary>提取列有效值
        /// </summary>
        /// <param name="col"></param>
        /// <param name="values">有效值集</param>
        /// <returns></returns>
        protected bool getValues_Col(int col, Dictionary<int, int> values)
        {
            for (int i = 0; i < this._rows; i++)
            {
                int value = _values[i, col];
                if (checkValue(value))
                    values[value] = 1;
            }
            return true;
        }
        /// <summary>提取所在9宫格有效值
        /// </summary>
        /// <param name="row"></param>
        /// <param name="col"></param>
        /// <param name="values">有效值集</param>
        /// <returns></returns>
        protected bool getValues_Cell(int row, int col, Dictionary<int, int> values)
        {
            //提取9宫格行列号
            int rowCell = getCellInd_Row(row);
            int colCell = getCellInd_Col(col);

            //计算9宫格的数据区间
            int rowMin = rowCell * _rowsCell;
            int rowMax = rowMin + _rowsCell;
            int colMin = colCell * _colsCell;
            int colMax = colMin + _colsCell;

            for (int i = rowMin; i < rowMax; i++)
            {
                for (int j = colMin; j < colMax; j++)
                {
                    int value = _values[i, j];
                    if (checkValue(value))
                        values[value] = 1;
                }
            }
            return true;
        }


        /// <summary>提取宫格行号
        /// </summary>
        /// <param name="row"></param>
        /// <returns></returns>
        protected int getCellInd_Row(int row)
        {
            return (int)Math.Floor(1.0 * row / _rowsCell);
        }
        /// <summary>提取宫格列号
        /// </summary>
        /// <param name="row"></param>
        /// <returns></returns>
        protected int getCellInd_Col(int col)
        {
            return (int)Math.Floor(1.0 * col / _colsCell);
        }

        /// <summary>校正值是否有效
        /// </summary>
        /// <param name="value"></param>
        /// <returns></returns>
        protected bool checkValue(int value)
        {
            if (value <= 0)
                return false;
            return true;
        }
        //数据排列MD5 校检码
        protected string checkMD5Hash()
        {
            string strTemp = "";
            for (int i = 0; i < _rows; i++)
            {
                for (int j = 0; j < _cols; j++)
                    strTemp += _values[i, j].ToString();
            }

            var md5 = new MD5CryptoServiceProvider();
            var bytes = System.Text.Encoding.Default.GetBytes(strTemp);
            var sb = new StringBuilder();
            for (int i = 0; i < bytes.Length; i++)
            {
                sb.Append(bytes[i].ToString("x2"));
            }
            return sb.ToString();
        }

        #endregion

    }
}
