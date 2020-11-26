# Vital Signs

**This project is inspired by [Deniz's Vital Signs](https://www.denizcemonduygu.com/portfolio/vital-signs/), non-commercial use only**  
**本项目灵感来源于 [Deniz 的 Vital Signs](https://www.denizcemonduygu.com/portfolio/vital-signs/) ，且在设计方面几乎完全仿照原作者，故不用做也不得用作任何商业用途，仅供个人学习、练习使用**

***

## 说明 Introduction

原作者的说明：

> What you see is some of the daily data I’ve collected during the last 6 years of my life (2,132 days between 01/03/2014 and 01/01/2020) charted as basically as possible in order to allow global readings and comparisons. (A nice method is just to scroll up and down with the mouse cursor pointing to the time of interest.) I update it every January. I started to log some topics later on, and there is a period where I did not log mood for some technical reasons in mid-2015. I have a lot more data on medical issues, food, people, and daily activities, which I chose not to show here.
>
> How do I collect all this data? I don’t use motion/sleep/… trackers. I’m not comfortable with wearables and smartphones. All it takes is a few minutes of retrospective question answering on [Reporter](http://www.reporter-app.com/) (on my iPad) when I wake up and go to bed every day (+ [Last.fm](http://www.last.fm/) for songs). With this method, whereas a few scalar topics have well-defined scales in terms of numbers (sleep hours, medicine, socialization, songs listened), most of them (stress, work, physical activity, etc.) are logged with approximate values defined in my head such as “0: none, 1: very few, 2: normal, …”. I’m not interested in the absolute values of things; I want to see patterns of increase/decrease, and the correlations between topics.

同原作者一样，我选择使用 [Reporter App](http://www.reporter-app.com/) 记录每天的数据，包括早上醒来记录睡眠质量（记录创建时间即为起床时间）、每天晚上睡前记录当天的相关数据（记录创建时间即为入睡时间）

本项目旨在实现制图的步骤

## 第三方库 Requirements

* `numpy >= 1.19.1`
* `pandas >= 1.0.5`
* `plotly >= 4.12.0`

## 用法 Usage

### 数据来源

源数据均由 [Reporter App](http://reporter-app.com/) 采集，导出为`reporter-export.csv`并保存在`.\data`目录下

### 配置文件

所有相关的配置均保存在`.\config`目录下，以下为各文件的说明：

* `.\config\colors.json`：色彩配置

```json
{
  "background": "背景色",
  "filling": "整型柱状图填充色",
  "filling_2": "布尔型柱状图填充色",
  "line": "折线图填充色",
  "title": "标题颜色",
  "grid": "月份分割线颜色",
  "grid2": "水平网格颜色",
  "zero": "零线颜色"
}
```

* `.\config\types.json`：对每一项记录采取的操作，应当是`Reporter App`里的问题标题

```json
{
  "Discard": [
    "舍弃记录（如自带的位置信息等）"
  ],
  "Number": [
	"记录转化为整型"
  ],
  "Bool": [
    "记录转化为布尔型"
  ]
}
```

* `.\config\mapping_table.json`：将文本（`Reporter App`中的答案选项）映射为数值，这些问题（数据名）应当同时出现在`.\config\types.json`的`Number`列表中

```json
{
  "数据名": {
    "文本（选项文本）": "要映射的数值（推荐使用 1, 2, 3 ...）"
  }
}
```


* `.\config\tokens.json`：提取`Reporter App`中的答案选项，这些问题（数据名）**不**应当出现在`.\config\types.json`中，答案会分别转成布尔型的记录（在画图中，每个答案的地位与`.\config\types.json`中`Bool`列表内的数据地位相同）

```json
{
  "数据名": ["答案选项"]
}
```


* `.\config\sleep.json`：睡眠时间的范围，以及睡眠时长的映射值

```json
{
  "wake_up": ["最早起床时间的分钟数，整型", "最晚起床时间的分钟数，整型"],
  "sleep": ["最早睡觉时间的分钟数，整型", "最晚睡觉时间的分钟数，整型"],
  "hours": ["睡眠时长可取值，浮点型"]
}
```

示例如下，表示最早 $4$ 点起床，最晚 $11$ 点起床；最早 $19$ 点入睡，最晚 $3$ 点入睡：

```json
{
  "wake_up": [240, 660],
  "sleep": [1140, 180],
  "hours": [3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11]
}
```

* `.\config\subplots`：要绘制的子图及其类型、高度

```json
{
  "数据名": ["绘图类型", "子图高度，用像素表示，整型"]
}
```

程序会依次绘制（从上到下）在该配置文件中的数据

`绘图类型`可选项：`bar|bool|sactter|line|space`（`space`表示空行）

### 运行方法

在配置好配置文件与数据源后，直接运行`main.py`

## 样例 Example

![](https://github.com/RenZihou/Vital_Signs/blob/master/example/example.png)
