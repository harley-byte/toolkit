# toolkit
一些小工具

### gis里是一个坐标转换工具
- 支持百度转高德，高德转百度，wgs84 分别转百度，高德，以及坐标实际距离计算。 bd<=>wgs84,gcj02<=>wgs84, bd<=>gcj02。
- text里是有关文本操作
  - textSimilarity.py 包含了几种判断文本相似性的算法，如最小编辑距离，编辑距离-莱文斯坦距离，Jaccard相似性系数，以及利用结巴分词求相似。如利用局部哈希算法判断相似性
- util 
  - snowFlake.go instgram id生成策略go语言实现，俗称雪花算法。支持分布式下的唯一id生成。
