# 麦肯锡学习法prompt
快速的了解一个行业，**整理关键词、访谈专家、阅读专业书籍**
1. 收集高频词汇、专业词汇
现在你是一名为零基础新手提供Docker知识培训的资深专家，现在我向你学习Docker基础知识，请按照从易到难的逻辑，为我列出30个Docker领域的高频词汇。

2. 很好，现在请用尽量通俗易懂的口吻，结合一些生动的案例或者故事，对你刚才列出的前10个词汇进行生动的讲解。

3. 现在你来扮演人工智能之父一一杰弗里辛顿，我们来作一次一对一的采访，我想通过这次专家采访来更深入地了解人工智能，请帮我列出5个采访问题。

4. 人工神经网络的灵感来源是什么？您能分享一下当初设计深度学习模型时的思考过程吗？

5. 现在我是一名想要从0到1学习AI基础知识的初学者，请帮我找出5本适合新手全面了解人工智能的通识类畅销书，比如《奇点临近》，请按照阅读顺序列出这5本书的书名，并且给出推荐理由



# UI设计
### 产品UI界面设计提示词 sonnet 3.7
我想开发一个AI自动记账app，现在需要输出原型图，请通过以下方式帮我完成app所有原型图片的设计。
1、思考用户需要AI记账app实现哪些功能
2、作为产品经理规划这些界面
3、作为设计师思考这些原型界面的设计
4、使用html在一个界面上生成所有的原型界面，可以使用FontAwesome等开源图标库，让原型显得更精美和接近真实
我希望这些界面是需要能直接拿去进行开发的


# 改写文章
```xml
<instruction>
1. 仔细阅读并理解用户提供的文章内容，确保完全掌握其主题、结构和表达意图。
2. 使用地道的编辑技巧对文章进行改进，包括但不限于以下方面：
   - 优化句子结构，使其更流畅自然。
   - 修正语法错误和用词不当之处。
   - 调整段落逻辑，增强文章连贯性。
   - 适当添加或删减内容，以提升文章的整体质量。
3. 确保改进后的文章保持原意不变，同时更具吸引力和可读性。
4. 输出改进后的文章，确保不包含任何XML标签。
</instruction>

<input>
{{article_text}}
</input>

<output>
{{improved_article}}
</output>

<example>
<input>
原文：今天天气很好，我决定去公园散步。公园里有很多人，他们都在享受阳光。我走了一会儿，感觉心情变得很好。
</input>

<output>
改进后：今天阳光明媚，我决定去公园散步。公园里人潮涌动，大家都在享受这美好的天气。漫步片刻后，我的心情也随之愉悦起来。
</output>
</example>
```


```xml
<instruction>
根据本周和本月的业务指标发展情况，生成工作总结。请按照以下步骤完成任务：


1. **收集数据**：确保已获取以下数据：

   - 本周开始时间：{{this_week_startdate}}

   - 本周结束时间：{{this_week_enddate}}

   - 本月月份：{{this_month_number}}

   - 本周线上渠道发展基础创新业务的指标数据：{{online_weekly_metrics1}}

   - 本周线上渠道发展基础创新业务的时序完成率：{{online_metrics1_realtime_rate}}

   - 本周线上渠道发展基础创新业务的月累计完成率：{{online_metrics1_month_rate}}

   - 本周线上渠道发展重点流量包业务的指标数据：{{online_weekly_metrics2}}

   - 本周线上渠道发展重点流量包业务的时序完成率：{{online_metrics2_realtime_rate}}

   - 本周线上渠道发展重点流量包业务的月累计完成率：{{online_metrics2_month_rate}}

   - 本周线上渠道发展权益包业务的指标数据：{{online_weekly_metrics3}}

   - 本周线上渠道发展权益包业务的时序完成率：{{online_metrics3_realtime_rate}}

   - 本周线上渠道发展权益包业务的月累计完成率：{{online_metrics3_month_rate}}

   - 本周线上渠道发展套餐迁转业务的指标数据：{{online_weekly_metrics4}}

   - 本周线下渠道发展基础创新业务的指标数据：{{offline_weekly_metrics1}}

   - 本周线下渠道发展基础创新业务的时序完成率：{{offine_metrics1_realtime_rate}}

   - 本周线下渠道发展基础创新业务的月累计完成率：{{offline_metrics1_month_rate}}

   - 本周线下渠道发展重点流量包业务的指标数据：{{offline_weekly_metrics2}}

   - 本周线下渠道发展重点流量包业务的时序完成率：{{offline_metrics2_realtime_rate}}

   - 本周线下渠道发展重点流量包业务的月累计完成率：{{offline_metrics2_month_rate}}

   - 本周线下渠道发展权益包业务的指标数据：{{offline_weekly_metrics3}}

   - 本周线下渠道发展权益包业务的时序完成率：{{offline_metrics3_realtime_rate}}

   - 本周线下渠道发展权益包业务的月累计完成率：{{offline_metrics3_month_rate}}

   - 本周线下渠道发展套餐迁转业务的指标数据：{{offline_weekly_metrics4}}

   - 本月累计订购各类包指标数据：{{monthly_allmetrics_total}}

   - 本月累计订购权益包业务指标数据：{{monthly_metrics3_total}}

   - 本月累计订购重点流量包业务指标数据：{{monthly_metrics2_total}}

   - 本月累计订购套餐迁转业务指标数据：{{monthly_metrics4_total}}



2. **生成报告**：确保报告结构如下：

   - 标题：本周和本月业务指标工作总结

   - 线上电营集约化项目完成情况：详细描述本周的业务指标表现

   - 线下重点项目完成情况：详细描述本月的业务指标表现

   - 整体流量经营完成情况：描述本月累计订购各类包的指标数据



3. **输出格式**：确保输出为纯文本，不包含任何XML标签。
</instruction>



<input>
{{this_week_startdate}}

{{this_week_enddate}}

{{this_month_number}}

{{online_weekly_metrics1}}

{{online_metrics1_realtime_rate}}

{{online_metrics1_month_rate}}

{{online_weekly_metrics2}}

{{online_metrics2_realtime_rate}}

{{online_metrics2_month_rate}}

{{online_weekly_metrics3}}

{{online_metrics3_realtime_rate}}

{{online_metrics3_month_rate}}

{{online_weekly_metrics4}}

{{offline_weekly_metrics1}}

{{offine_metrics1_realtime_rate}}

{{offline_metrics1_month_rate}}

{{offline_weekly_metrics2}}

{{offline_metrics2_realtime_rate}}

{{offline_metrics2_month_rate}}

{{offline_weekly_metrics3}}

{{offline_metrics3_realtime_rate}}

{{offline_metrics3_month_rate}}

{{offline_weekly_metrics4}}

{{monthly_allmetrics_total}}

{{monthly_metrics3_total}}

{{monthly_metrics2_total}}

{{monthly_metrics4_total}}

</input>

<output>
{{work_summary_report}}
</output>

<example>
<input>
本周开始时间3.9，本周结束时间3.15，本月月份3月。
线上渠道，个人创新业务，周415户，月540户，时序进度41.8%。
线上渠道，重点流量包，周361户，月395户，时序进度18.6%。
线上渠道，套餐迁转，周157户，月157户。
线下渠道，个人创新业务，周1068户，月1148户，时序进度47.1%。
线下渠道，权益流量包业务，周155户，月166户。
</input>

<output>
（一）线上电营集约化项目完成情况：
1.个人创新业务：3.2--3.8办理415户，3月累计办理540户，月时序完成率41.8%。
2.重点流量包：3.2--3.8办理361户，3月累计办理395户，月时序完成率18.6%。
3.套餐迁转：3.2--3.8 迁转157户，3月累计迁转157户。

（二）线下重点项目完成情况：
1.个人创新业务：3.2--3.8办理1068户，3月累计办理1148，月时序完成率47.1%。
2.权益流量包，3.2--3.8办理155户，3月累计办理166户。
3.大流量包，3.2--3.8办理27户，3月累计办理31户，总部线上办理15户，线下渠道办理16户。

（三）整体流量经营完成情况：
3月提值流量包累计订购775户，其中权益包166户，重点流量包421户，套餐迁转157户。
</output>
</example>
```