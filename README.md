# Vital Signs

**This project is inspired by [Deniz's Vital Signs](https://www.denizcemonduygu.com/portfolio/vital-signs/), non-commercial use only**  
**本项目灵感来源于 [Deniz 的 Vital Signs](https://www.denizcemonduygu.com/portfolio/vital-signs/) ，且在设计方面几乎完全仿照原作者，故不用做也不得用作任何商业用途，仅供个人学习、练习使用**

***

## 说明 Introduction

原作者的说明：

> What you see is some of the daily data I’ve collected during the last 6 years of my life (2,132 days between 01/03/2014 and 01/01/2020) charted as basically as possible in order to allow global readings and comparisons. (A nice method is just to scroll up and down with the mouse cursor pointing to the time of interest.) I update it every January. I started to log some topics later on, and there is a period where I did not log mood for some technical reasons in mid-2015. I have a lot more data on medical issues, food, people, and daily activities, which I chose not to show here.
>
> How do I collect all this data? I don’t use motion/sleep/… trackers. I’m not comfortable with wearables and smartphones. All it takes is a few minutes of retrospective question answering on [Reporter](http://www.reporter-app.com/) (on my iPad) when I wake up and go to bed every day (+ [Last.fm](http://www.last.fm/) for songs). With this method, whereas a few scalar topics have well-defined scales in terms of numbers (sleep hours, medicine, socialization, songs listened), most of them (stress, work, physical activity, etc.) are logged with approximate values defined in my head such as “0: none, 1: very few, 2: normal, …”. I’m not interested in the absolute values of things; I want to see patterns of increase/decrease, and the correlations between topics.

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
  "filling": "柱状图填充色",
  "line": "折线图颜色",
  "text": "主文本颜色",
  "note": "辅助文本颜色",
  "grid": "网格颜色"
}
```

* `.\config\mapping_table.json`：将文本（multi-choice 选项）映射为数值的相关配置

```json
{
  "数据名": {
    "文本（选项文本）": 要映射的数值（推荐使用 1, 2, 3 ...）,
    ...
  },
  ...
}
```

* 



