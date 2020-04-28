# 说明

	文件名为库名，二级节点为表名，以表结构进行字段设置与调整；
	
	索引类型： unique
	

## zxcUserInfo-*r

表说明：	用户信息表。	
	1). 个人信息，*ID、姓名、性别、会员级别、车辆信息（车型、颜色、时间，支持多辆？）、*电话、*微信ID、*微信名、*共享电桩编号、*更新时间、是否有效；
表结构如下：

	| 字段名 | 字段类型 | 字段长度 | 是否可空 | 是否索引 | 默认值 | 索引类型 |
	| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
	| id | int | 11 | False | True | - | - |
	| 用户ID | char | 12 | False | True | - | unique |
	| 用户名 | char | 12 | False | True | - | unique |
	| 用户昵称 | char | 12 | False | True | - | - |
	| 图像ID | char | 12 | False | True | - | - |
	| 姓名 | char | 12 | True | True | - | - |
	| 性别 | char | 1 | True | False | - | - |
	| 电话 | char | 11 | False | True | - | unique |
	| 省份 | char | 10 | False | True | - | - |
	| 城市 | char | 10 | False | True | - | - |
	| 微信ID | char | 16 | True | True | - | - |
	| 微信名 | char | 16 | True | False | - | - |
	| 电桩数 | int | 8 | True | False | - | - |
	| 车辆数 | int | 8 | True | False | - | - |
	| 备注 | char | 30 | True | False | - | - |
	

## zxcAccountInfo-*r

表说明：	账户信息。
	2). 账户信息，*ID、*充电桩编号、*服务状态、*余额、*利是余额、充值次数、充值总额、消费次数、消费总额、返利次数、返利总额、*更新时间、*备注；
表结构如下：

	| 字段名 | 字段类型 | 字段长度 | 是否可空 | 是否索引 | 默认值 | 索引类型 |
	| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
	| id | int | 11 | False | True | - | - |
	| 用户名 | char | 12 | False | True | - | unique |
	| 服务状态 | bool| 0 | False | False | - | - |
	| 余额 | DECIMAL(6,2) | 0 | False | False | - | - |
	| 利是余额 | DECIMAL(4,2) | 0 | False | False | - | - |
	| 充值次数 | int | 8 | False | False | - | - |
	| 充值总额 | DECIMAL(6,2) | 0 | False | False | - | - |
	| 消费次数 | int | 8 | False | False | - | - |
	| 消费总额 | DECIMAL(6,2) | 0 | False | False | - | - |
	| 返利次数 | int | 8 | False | False | - | - |
	| 返利总额 | DECIMAL(4,2) | 0 | False | False | - | - |
	| 备注 | char | 30 | True | False | - | - |
	
	
## zxcChargingInfo-*r

表说明：	电桩信息表。
	5). 电桩信息，*电桩编号、*桩主ID、*位置、*经纬度、
			*是否分时计价(实价计算，返利)、*基础电价(分时：电价)、服务费(桩主自定义+分润)、基础服务费(分润)、*收费配置(总费用对应电表配置)、
			*电桩功率、*电桩电压、*电装电流、*是否共享、*共享时段(.5小时间隔)、*更新时间、*更新次数；
表结构如下：

	| 字段名 | 字段类型 | 字段长度 | 是否可空 | 是否索引 | 默认值 | 索引类型 |
	| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
	| id | int | 11 | False | True | - | - |
	| 桩主ID | char | 12 | False | True | - | - |
	| 电桩编号 | char | 12 | False | True | - | unique |
	| 电桩功率 | DECIMAL(3,1) | 0 | False | False | - | - |
	| 电桩电压 | int | 8 | False | False | - | - | 
	| 电桩电流 | DECIMAL(3,1) | 0 | False | False | - | - | 
	| 位置 | char | 30 | False | False | - | - |
	| 经度 | char | 12 | False | False | - | - |
	| 纬度 | char | 12 | False | False | - | - |
	| 是否共享 | bool | 0 | False | False | - | - | 
	| 分时计价 | bool | 0 | False | False | - | - |
	| 基础电价 | DECIMAL(3,2) | 0 | False | False | - | - |
	| 服务费 | DECIMAL(3,2) | 0 | False | False | - | - |
	| 基础服务费 | DECIMAL(3,2) | 0 | False | False | - | - |
	| 收费配置 | char | 12 | False | False | - | - |
	| 共享时段 | char | 100 | False | False | - | - |
	| 更新次数 | int | 8 | False | False | - | - |






	
	