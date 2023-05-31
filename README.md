写分页按钮的Xpath真的是写够了！爬的网页越多，写分页按钮就越多，心好累！

从列表页上自动提取标题和链接的算法有了，从网页自动提取长文本的算法也有人研究，爬虫自动化只差自动翻页了！就不能让爬虫系统自动翻页么！



### 算法思路

![算法流程图](https://s2.loli.net/2023/05/31/DqYv27KUCIzSTxO.png)

列表页上的元素，只有两种可能：是下一页按钮，或者不是下一页按钮。

因此只需要设计合适的特征后交给分类器分类，再根据元素特征（id属性或者class属性）生成选择器就可以了！

项目里附带了数据集（来自真实的政务网站和新闻网站）、训练模型的代码和训练好的四个模型，如果对这部分不感兴趣，直接用handler就可以。

更详细的内容请看我的论文[《Intelligent Positioning Method of Paging Buttons Based on Machine Learning》](https://ieeexplore.ieee.org/abstract/document/10061879/)。

（论文里用的分类器是SVM，实话说效果并不好~~（评分函数设计成那个死德行）~~，在毕设论文里升级成了XGBoost，效果好很多，实用性大大提升了）

### 效果演示

单个元素分类

![image-20230531132909470](https://s2.loli.net/2023/05/31/C5EBNRzbFk4n97H.png)

![image-20230531132943032](https://s2.loli.net/2023/05/31/d9CK8uyfcVknv1X.png)



真实网页提取

![image-20230531133633809](https://s2.loli.net/2023/05/31/GmpfC6P1gFJyID7.png)