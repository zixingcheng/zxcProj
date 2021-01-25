
import os
import numpy as np
from netCDF4 import Dataset

import myIO_xlsx, myData_Trans
 

#https://www.cnblogs.com/android-16/p/11131901.html

dst = Dataset(r'D:\myDocuments\Documents3\气象数据\20200730.E41.arm_meas.nc', mode='r', format='NETCDF4')

for attr in dst.ncattrs():
    print('s%：s%' % (attr, dst.getncattr(attr)))


for var in dst.variables:
    print(var, end=':\n')
    for attr in dst[var].ncattrs():
        print('s%：s%' % (attr, dst[var].getncattr(attr)))
        

dims = ['time', 'depth', 'lat', 'lon']
for dim in dims:
    print('s%：s%' % (dim, dst.dimensions[dim].size))
    pass


var_dep = dst['depth']
for i in range(dst.dimensions['depth'].size):
    print(var_dep[i], end='\t')
    pass
print()


df = pd.DateFrame(arr, cloumns = cloumn)
csv_file = path.replace(".nc", ".csv")
df.to_csv(csv_file, sep=',')
pass