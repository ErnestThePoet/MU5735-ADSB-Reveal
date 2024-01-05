# MU5735 ADS-B Reveal
## 说明
[事故近两年后，深度分析MU5735航班的ADS-B数据](https://zhuanlan.zhihu.com/p/675731808)文章数据资料仓库
## 文件清单
- `Flightradar24 Granular Data.csv` Flightradar24 Granular Data
- `Variflight Data.xlsx` 飞常准业内版ADS-B数据
- `Merged Data.xlsx` 融合版ADS-B数据
- `Charts.xlsx` 包含各种图表的表格文件
- `MU5735.kml` MU5735 ADS-B数据的Google Earth KML，基于[cathaypacific8747/mu5735](https://github.com/cathaypacific8747/mu5735)中的代码导出，具体包含：
  - `FR24 Red` FR24 Granular Data飞行轨迹，红色
  - `FR24 Red(No ALT)` FR24 Granular Data飞行轨迹，红色，无高度
  - `Merged` 融合版ADS-B数据飞行轨迹
  - `Merged(No ALT)` 融合版ADS-B数据飞行轨迹，无高度
  - `Critical Points` 飞行关键节点
  - `Time Points(No ALT)` 起飞、巡航阶段飞行轨迹部分时间点，无高度
  - `Time Points(ALT)` 坠落阶段部分时间点和高度，带高度
  - `G Points` 坠落阶段部分时间点和垂直过载，带高度
- `NavData-AIRAC2311-N17E73-N55E145.kml` Navigraph AIRAC Cycle 2311导航数据的Google Earth KML，仅包含N17E73-N55E145以内的部分，使用本人[PMDGNav2Kml](https://github.com/ErnestThePoet/PMDGNav2Kml)脚本从PMDG格式导航数据中导出
- `crc_collision.py` 文章中寻找`DF=5`的Mode S报文CRC冲突的脚本代码