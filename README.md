
<style>

    .success {
        padding:5px;
        display:inline;
        color:#1B5E20;
        background-color:#C8E6C9;
    }
    .warning {
        padding:5px;
        display:inline;
        color:#E65100;
        background-color:#FFE0B2;
        width:100%;
    }
    .danger {
        padding:5px;
        display:inline;
        color:#B71C1C;
        background-color:#FFCDD2;
    }
    .info {
        padding:5px;
        display:inline;
        color:#006064;
        background-color:#B2EBF2;
    }
    .doubt {
        padding:5px;
        display:inline;
        color:#AAA;
        background-color:#DDDDDD;
    }
    .asso {
        padding:5px;
        display:inline;
        color:#555;
        background-color:#FFCC00;        
    }
    
    .alert {
        display:inline-block;
        width:100%;
        padding:5px;
        line-height:30px;
        margin-top:10px;
    }
</style>

# Learn-LLM

## 0. 大模型 to B 开发的四个技术方向
1. Prompt 提示词工程
2. AI agent 开发（根据任务来自动完成目标）
3. 对话系统chatbot开发（智能客服系统，问诊系统，法律咨询等）
4. 4.大模型微调（微调行业垂直模型）

<b class="info">学习路线</b>[聚客AI学习路线](./01/AI大模型学习路线.pdf)



<b class="info">
对function calling的建议，大模型自主决定什么时候calling function不太靠谱，如果是线上正式的且对稳定性要求较高的服务，建议自己用prompt解析需求，手工调function更靠谱。即根据解析的结果，意图判断的结果手工调function，不要完全依赖大模型调用function calling的机制
</b>



#### <b class="danger">待解决问题</b> 
1. python代码实现，按一定粒度，部分重叠式的切割文本，使上下文更完整
2. python代码实现的rrf融合排序算法
```python
import json

def rrf(ranks, k=1):
    ret = {}
    # 遍历每次的排序结果
    for rank in ranks:
        # 遍历排序中每个元素
        for id, val in rank.items():
            if id not in ret:
                ret[id] = {"score": 0, "text": val["text"]}
            # 计算 RRF 得分
            ret[id]["score"] += 1.0/(k+val["rank"])
    # 按 RRF 得分排序，并返回
    return dict(sorted(ret.items(), key=lambda item: item[1]["score"], reverse=True))
    

# 融合两次检索的排序结果
reranked = rrf([keyword_search_results, vector_search_results])

print(json.dumps(reranked, indent=4, ensure_ascii=False))
```
3. 盘古、混元、文心、通义（基座，基础模型）
基础模型+行业数据+训练+微调=行业垂直模型（付费）
通过行业垂直模型+RAG 来实现场景落地

4. docker的使用，部署elasticsearch,部署向量数据库提供client-server服务
5. 中文pdf的切分，如何将上下文语义相关的段落合并成一个段落
6. 如何部署模型，实现对外提供并发调用
7. 将对话逻辑封装在fastapi中





## 1. prompt-engineering
<b class="success">把AI当人看</b>
<b class="success">把AI当人看</b>
<b class="success">把AI当人看</b>

<b class="danger">知道哪些问题用提示词工程解决更高效，哪些用传统编程解决更高效</b>

### 1. prompt调优
<b class="success">具体、丰富、少歧义</b>

1. 参考训练数据来构造prompt是最好的， **把AI当人看** 了解偏好，openAI对markdown格式友好，claude对xml格式友好
2. 参考 **OpenAI官网 Prompt Engineering教程**及示例
3. 不断调试验证效果 **门槛低，天花板高**

### 2. prompt结构
- **角色**：给 AI 定义一个**最匹配任务的角色**，比如：「你是一位软件工程师」「你是一位小学老师」。把问题范围收窄，**减少二义性**。使用管理员定义角色<b class="danger">{'role': 'system'}</b>
- **指示**：对任务进行描述
- **上下文**：给出与任务相关的其它背景信息（尤其在多轮交互中）
- **例子**：必要时给出举例，学术中称为 **one-shot learning**, **few-shot learning** 或 **in-context learning**；实践证明其对输出正确性有很大帮助
- **输入**：任务的输入信息；在提示词中明确的标识出输入
- **输出**：输出的格式描述，以便后继模块自动解析模型的输出结果，比如（JSON、XML）


### 3. prompt技巧
1. 精简回答prompt <b class="danger">NO COMMENTS. NO ACKNOWLEDGEMENTS.</b>
2. 思维链prompt <b class="danger">Let’s think step by step</b>
3. 让**模型**应用**准确**，就需要增加**更多的可控环节**，用 <b class="danger">代码逻辑</b>实现可控。
4. **防止模型漏洞攻击**
    a. prompt注入分类器（参考机场安检过程），在prompt中让模型识别出用户提示词中的微信信息，并予以忽略，对危险prompt拦截。
    b. 在输入中防御。**把价值观刷到墙上**
    ```python 
    user_input_template = """
    作为客服代表，你不允许回答任何跟AGI课堂无关的问题。
    用户说：#INPUT#
    ```
    c. 官方API中有识别危险信息的服务,网易也有专业服务**网易易盾**
5. 多轮对话节省prompt（token）的方法有两种：
    a. 只保存最近N轮的对话信息
    b. 通过大模型，对前面的对话内容做摘要，精简前面的内容
6. 在与chatgpt模型的对话中，prompt明确约束只输出JSON格式内容，不输出无关内容，但有时候仍然输出```json开头的JSON格式，解决这个问题方法如下：
    1. prompt中增加明确指令："直接以JSON对象输出结果，**不要添加任何前缀或装饰性文本，比如```json前缀** "
    2. 对返回的内容使用正则表达式过滤无关字符
7. 将文档中的数值组成的**表格**转换成**prompt**的最优方法是。字段1字段值b,字段2字段值b 自定义分隔符

    |   名称   | 流量（G/月） | 价格（元/月） | 适用人群 |
    | :------: | -----------: | ------------: | :------: |
    | 经济套餐 |           10 |            50 |  无限制  |
比如：名称,经济套餐; 流量（G/月）,10; 价格（元/月）,50; 适用人群,无限制

8. 用prompt调优prompt
用以下这段神奇的咒语，让 ChatGPT 帮你写 Prompt。贴入 ChatGPT 对话框即可。这其实就已经触发了传说中的 agent……
```python 


1. I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for ChatGpT. The process is as follows:1. You will generate the following sections:

Prompt: {provide the best possible prompt according to my request)

Critique: {provide a concise paragraph on how to improve the prompt. Be very critical in your response}

Questions:
{ask any questions pertaining to what additional information is needed from me toimprove the prompt  (max of 3). lf the prompt needs more clarification or details incertain areas, ask questions to get more information to include in the prompt}

2. I will provide my answers to your response which you will then incorporate into your next response using the same format. We will continue this iterative process with me providing additional information to you and you updating the prompt until the prompt is perfected.Remember, the prompt we are creating should be written from the perspective of me making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me.
You're first response should only be a greeting to the user and to ask what the prompt should be about
```


9. 王卓然老师原创的 Prompt Tune 工具
用遗传算法自动调优 prompt，用 LLM 做不改变原意的情况下调整 prompt。用测试集验证效果，找到趋近1的最优prompt
开放源代码：https://gitee.com/taliux/prompt-tune


#### 示例，推荐流量套餐
某运营商的流量包产品：

|   名称   | 流量（G/月） | 价格（元/月） | 适用人群 |
| :------: | -----------: | ------------: | :------: |
| 经济套餐 |           10 |            50 |  无限制  |
| 畅游套餐 |          100 |           180 |  无限制  |
| 无限套餐 |         1000 |           300 |  无限制  |
| 校园套餐 |          200 |           150 |  在校生  |

需求：智能客服根据用户的咨询，推荐最适合的流量包。

##### 核心思路
<b class="success">0. 先试试简单的任务，验证模型是否能完成任务</b>
<b class="success">1. 把输入的自然语言对话，转成结构化的表示</b>
<b class="success">2. 从结构化的表示，生成策略</b>
<b class="success">3. 把策略转成自然语言输出</b>
<b class="success">4. 给例子示范，效果很好</b>

##### 运行过程
用大模型理解自然语言转成内部结构化的表示 **（NLU）**（减少歧义提升准确性）--> 然后通过内部逻辑、数据库得出应对策略 --> 将策略发送给大模型生成自然语言回答

| 对话轮次 | 用户提问              | NLU 语义理解               | DST 状态跟踪                         | Policy 对话策略                 | NLG 自然语言生成                                       |
| -------- | --------------------- | ----------------- | --------------------------- | ---------------------- | ----------------------------------------- |
| 1        | 流量大的套餐有什么    | sort_descend=data | sort_descend=data           | inform(name=无限套餐)  | 我们现有无限套餐，流量不限量，每月 300 元 |
| 2        | 月费 200 以下的有什么 | price<200         | sort_descend=data price<200 | inform(name=劲爽套餐)  | 推荐劲爽套餐，流量 100G，月费 180 元      |
| 3        | 算了，要最便宜的      | sort_ascend=price | sort_ascend=price           | inform(name=经济套餐)  | 最便宜的是经济套餐，每月 50 元，10G 流量  |
| 4        | 有什么优惠吗          | request(discount) | request(discount)           | confirm(status=优惠大) | 您是在找优惠吗                            |

### 4. 提升准确率


![TOT](./02-prompt-engineering//TOT.png)
![medprompt_sa_graphic](./02-prompt-engineering/medprompt_sa_graphic.png)

#### 自洽性 Self-Consistency
一种对抗「幻觉」的手段。就像我们做数学题，要多次验算一样。同样 prompt **跑多次**，通过**投票**选出最终结果。使用<b class="danger">自洽性需提高temperature的值</b> ,更高的随机性生成更多的结果。
利用以下代码多次调用，确定最终结果
```python 
for _ in range(5):
    prompt = f"{instruction}\n\n{output_format}\n\n请一步一步分析:\n{context}"
    print(f"------第{_+1}次------")
    response = get_completion(prompt)
    print(response)

#输出内容
------第1次------
{"accurate":true}
------第2次------
{"accurate":false}
------第3次------
{"accurate":false}
------第4次------
{"accurate":true}
------第5次------
{"accurate": false}
```
#### 思维树 Tree-of-Thought
让大模型把问题展开，展开后，在里面找每个节点，判断出哪个节点离结果最近。再深挖迭代这个过程。

### 5. OpenAP API 参数
Temperature **执行任务用 0**，文本生成用 0.7-0.9，无特殊需要，**不建议超过 1**
seed 指定固定的seed的值后每次生成结果一致
n=1 控制一次返回多少条结果，<b class="danger">可用于自洽性</b>
presence_penalty=0, frequency_penalty=0, 对token进行降权，避免模型说重复的话 
logit_bias={}  对某个特定的token增降权限   
```python 
def get_chat_completion(session, user_prompt, model="gpt-3.5-turbo"):
    _session = copy.deepcopy(session)
    _session.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=model,
        messages=_session,
        # 以下默认值都是官方默认值
        temperature=1.8,          # 生成结果的多样性 0~2之间，越大越随机，越小越固定
        seed=None,              # 随机数种子。指定具体值后，temperature 为 0 时，每次生成的结果都一样
        stream=False,           # 数据流模式，一个字一个字地接收
        top_p=1,                # 随机采样时，只考虑概率前百分之多少的 token。不建议和 temperature 一起使用
        n=1,                    # 一次返回 n 条结果
        max_tokens=100,         # 每条结果最多几个 token（超过截断）
        presence_penalty=0,     # 对出现过的 token 的概率进行降权
        frequency_penalty=0,    # 对出现过的 token 根据其出现过的频次，对其的概率进行降权
        logit_bias={},          # 对指定 token 的采样概率手工加/降权，不常用
    )
    msg = response.choices[0].message.content
    return msg
```
<b class="danger">使用GPT API接口来生成对话服务时，需要自己维护历史对话信息</b>

### 6. 其他参考资料
#### 吴恩达课程
#### OpenAI 官方prompt示例 

## 2. AI-programming
### AI编程场景
其中在软件开发过程中，已验证能明确提效的场景：
- 市场调研
- 需求分析
- PRD 撰写
- 图形元素绘制
- 技术选型
- 从需求文本生成代码
- <strong>从设计图生成代码</strong>
- 代码审查
- 编写测试用例
- 运维
- <strong>API 文档调用</strong>
- <strong>协议解析</strong>
- 跨语言迁移：两周的时间，2 个同事将一个 40 个 API 接口的 go 工程迁移成一个 java 工程


<b class="alert success">
使用技巧：</br>
0. 写需求文档时，先写某个细化功能的需求（或者用户故事），让AI先协助生成或补全故事，让AI进一步完善细节。</br>
1. 所有 prompt engineering 的技巧都有效，可以把代码、错误信息直接粘贴进去</br>
2. 任何技术相关的问题都可以问，比自己搜索效率高很多 </br>
3. 给AI发送已有的API接口文档，实现对应需求，AI可以自动抓取文档。
</b>


<b class="danger">
比如：
https://docs.binance.us/#WEBSOCKET-STREAMS 根据以上接口文档内容，编写一段消息订阅java程序</b>

参考：ChatALL 大量依赖 GPT-4。过程实录：https://chat.openai.com/share/ecfafa99-aaad-4432-a40c-81c261376758 （对话轮次非常多加载慢，所以几乎总是 404）。如果打不开，别到群里问题，看[这个图](./03-AI-programming/gpt-4-chatall.png)吧

### AI 编程的基本原理
<b class="danger">编程能力是大模型各项能力的天花板</b>

- 「编程」是目前大模型能力最强的垂直领域，甚至超越了对「自然语言」本身的处理能力。因为：

  - 训练数据质量高
  - 结果可衡量
  - 编程语言无二义性

- 知道怎么用好 AI 编程，了解它的能力边界、使用场景，就能类比出在其他领域 AI 怎么落地，能力上限在哪
  - 此观点是我们原创，在分享过数次后，GitHub 官方发了一篇文章：[How to build an enterprise LLM application: Lessons from GitHub Copilot](https://github.blog/2023-09-06-how-to-build-an-enterprise-llm-application-lessons-from-github-copilot/)。当然，这只是巧合。

#### 工作原理

- 模型层：最初使用 OpenAI Codex 模型，它也是 GPT-3.5、GPT-4 的「一部分」。[现在已经完全升级，模型细节未知](https://github.blog/2023-07-28-smarter-more-efficient-coding-github-copilot-goes-beyond-codex-with-improved-ai-model/)。

  - “The first model that OpenAI gave us was a Python-only model,” Ziegler remembers. “Next we were delivered a JavaScript model and a multilingual model, and it turned out that the Javascript model had particular problems that the multilingual model did not. It actually came as a surprise to us that the multilingual model could perform so well. But each time, the models were just getting better and better, which was really exciting for GitHub Copilot’s progress.”

- 应用层： prompt engineering。Prompt 中包含：

  1. 组织上下文：光标前和光标后的代码片段
  1. 获取代码片段：其它相关代码片段。当前文件和其它打开的 tab 里的代码被切成每个 60 行的片段，用 [Jaccard 相似度](https://zh.wikipedia.org/wiki/%E9%9B%85%E5%8D%A1%E5%B0%94%E6%8C%87%E6%95%B0)评分，取高分的
     - 为什么是打开的 tabs
     - 多少个 tabs 是有效的呢？ **默认20个tab**
  1. 修饰相关上下文：被取用的代码片段的路径。用注释的方式插入，例如：`# filepath: foo/bar.py`，或者 `// filepath: foo.bar.js`
  1. 优先级：根据一些代码常识判断补全输入内容的优先级

- 补全格式：在函数定义、类定义、if-else 等之后，会补全整段代码，其它时候只补全当前行
![completion](./03-AI-programming/life-of-a-completion.webp)

##### 了解更多

- [Inside GitHub: Working with the LLMs behind GitHub Copilot](https://github.blog/2023-05-17-inside-github-working-with-the-llms-behind-github-copilot/)
- [How GitHub Copilot is getting better at understanding your code](https://github.blog/2023-05-17-how-github-copilot-is-getting-better-at-understanding-your-code/)
- [A developer’s guide to prompt engineering and LLMs](https://github.blog/2023-07-17-prompt-engineering-guide-generative-ai-llms/)


##### github copilot 使用技巧
1. 写测试用例时，只需要在声明函数名时，前面加上test_  AI会自动补全测试用例代码
2. 根据注释写代码，写好注释，AI会自动补全代码。这种方法不太建议使用，因为注释里面写的是针对AI的prompt，不太适合人类阅读。如果需要从需求生成代码，可以考虑使用 **Copilot Chat**。
    - chat对话框中输入`/`可以使用特殊指令
    - 在需要插入代码的地方或者选某块代码块，输入`ctrl+i` 呼出Copilot Chat
3. 先写代码，**代码有了再写注释**，更AI理解起来更准确，更省力
4. **改写**当前代码，可**另起一块**新写，AI补全得更准，完成后**再删旧代码**
3. ` Alt + ] `查看下一个建议，` Alt + [` 查看上一个建议，` Cmd/Ctrl + → ` 只接受一个 token即部分建议
4. 如果有旧代码希望被参考，就把代码文件在新tab 页里打开

#### AI编程的效能
<b class="alert success">
AI 能力定律：
AI 能力的上限，是使用者的判断力
</b>

$\text{AI 能力} = \min(\text{AI 能力}, \text{使用者判断力})$

<b class="alert success">
AI 提效定律：AI 提升的效率，与使用者的判断力成正比，与生产力成反比
</b>

$\text{效率提升幅度} = \frac{\text{使用者判断力}}{\text{使用者生产力}}$

<b class="alert success">
编码人员的判断力 = 需求的理解准确度 * 代码的阅读量
</b>

$\text{效率提升幅度} = \frac{\text{需求的理解准确度} · \text{代码的阅读量}}{\text{自己手写代码的速度}}$


- 使用者的判断力，是最重要的
- 提升判断力，比提升实操能力更重要，眼高手低的福音
- 广阔的视野是判断力的养料

#### AI编程技巧
- 先以**架构师**的身份，让AI辅助，对架构进行选型： 通过需求文档和业务文档，让 AI 给出架构的建议。**先将整体需求细化成一个个具体的需求，足够细化，细化到要么是一个接口，要么是一个函数**。
- 然后以开发者的身份，让 AI 辅助你写业务代码 （逐层拆分向下写)



## 3. Function Calling 结构化输出
<b class="alert success">
让大模型链接外部系统，是通过自然语言来实现的，不需要给大模型编写特定的代码让其与外部系统API对接，只需要将外部系统API的能力用自然语言进行描述，大模型就能判断出什么时候调用API。
</b>

在大型语言模型（LLM）中，function calling 中的函数是由大模型间接调用执行的，实际的执行通常由后端服务或中间件来完成。具体来说，这个过程可以分为以下几个步骤：
1. 模型生成调用指令：当用户与模型交互时，模型根据输入和上下文生成一个调用特定函数的指令。这个指令通常包含函数名和所需的参数。
比如模型生成以下文本或结构化数据，提示系统调用某个函数
```json
{
    "function": "get_weather",
    "parameters": {
      "location": "Beijing",
      "date": "2023-10-01"
    }
}
```
2. 传递给后端服务：生成的调用指令被传递给后端服务或中间件。后端服务负责实际执行这些函数。
实际负责调用和执行定义函数的部分，通常涉及中间软件、API调用框架或特定应用实现。
    工作原理：
    - 解析指令：模型通过与用户的对话，识别出当与用户的对话中，是否要调用预先定义的函数。如果需要则生成调用函数的指令，包含函数名称和参数。
    - 调用合适的函数：在开发chat的业务逻辑中，获取模型返回的内容即上面解析指令后返回的内容，如果模型返回的内容包含函数调用指令，则在response中通过获取到函数名和参数来执行具体的函数。
    - 返回结果：执行后，将函数的输出结果传递回模型。
3. 执行函数：后端服务调用相应的函数，执行具体的操作（如查询数据库、调用API、执行计算等）。
4. 返回结果：函数执行的结果被返回给模型。执行结果可以作为模型输出的一部分，向用户显示或被进一步使用。
5. 模型生成响应：模型将函数的执行结果纳入生成的文本中，最终返回给用户。

这种架构既保障了模型的功能扩展性和安全性，又使得它可以与现实世界的数据和服务相结合，提供更加全面和有用的功能。



### <b class="danger">大模型的应用领域：能替代人，而且出错概率比人小的场景。</b> 





## 4.RAG 检索增强生成 Retrieval Augumented Generation


### 模型的硬件需求
模型大小6-8B足矣支撑企业特定业务场景的AI应用（智能客服，助手）。70B以上大小的模型适用通用领域应用。

#### LLM的局限性
1. LLM的知识不是实时的
2. LLM不具备私有场景/专业领域的知识

#### 检索增强生成
通过**检索**的方法来**增强**生成**模型的能力**
<b class="success">RAG的流程类似开卷考试。让 LLM 先翻书，再回答问题。</b>
![RAG原理](./04-RAG/RAG.png)

#### RAG的优势
私有数据，数据实时性，问答来源的可解释性，降低幻觉。

#### 一、RAG系统的基本搭建流程
1. **load 文档加载**（pdf,docx,html,video,voice,excel）
2. **split 文档切分** 
   a. 拆分后的词组或句子太长不利于模型理解和答案抽取，如果太短无法保证原文内容语义的连贯性。 实际使用中使用 **langchain** 开发框架定义 **chunk overlap** 来控制切分文档时重叠区域的大小。
   b. 问题的答案可能跨越两个片段
3. **embed 向量化** 
   将切分后的文档片段使用embedding模型进行向量化，常用的embedding模型有 text-embedding-3-large, text-embedding-3-small
4. **store 向量化存储** 将向量数据存储到向量数据库中

**Query -> 检索 -> Prompt -> LLM -> 回复**
<b class="alert success">RAG过程：1. 向量数据库中存放的有文档片段原文和文档片段的向量数据（向量会作为索引进行匹配）。
2. 用户的问题首先会经过向量化处理（转换成一段向量数据），然后用这个问题的向量数据作为索引，去向量数据库中找，与之最匹配（向量空间的余弦夹角最小值或欧氏距离最小值）的文档片段的向量数据索引。
3. 找到之后将其对应的片段原文+提问原文拼接成prompt发送给LLM，让LLM生成答案。
</b>


#### 二、基于OpenAI在assistants API中集成的RAG能力，可以作为参考
 1. 面向检索的用户query的改写，将用户的query进行改写，保留核心主干问题，避免过于简单或复杂影响效果
 2. 复杂的query拆解成多个，并行执行query检索
 3. 使用关键字检索和向量检索相结合，混合检索
 4. 检索后排序
 5. 配置参考
    - chunk size大小: 800 tokens 文档片段大小
    - chunk overlap大小： 400 tokens 文档之间重叠区域大小
    - embedding mode：text-embedding-3-large at 256 dimensisions 使用large embedding模型，向量纬度256
    - maximum number of chunks added to context: 20  即每次最多返回20个chunk做后排序
    - **用好向量数据库的meta data元数据**，可对检索内容基于key,value信息做过滤


#### 三、RAG中chunking 分块策略
 - 固定大小分块：将文本按固定大小分块，简单高效，但会破坏原文档的语义性
 - 递归分块：使用递归方式按标点符号分块（**逗号，句号，换行**等），直到每个分块的大小都符合设置值。首先设定块的大小，整个过程先按句号分，比如定义一个块的大小为20个字符，当对文档**先用句号**切分的时候如果某个块超过20个字符，则**递归**，**进一步使用逗号分隔**，将超过的部分切到下一个块中。当切分不足20个字符时，也会将下一句的部分内容切入到片段，直到这个块**接近**20个字符。
 - 基于文档结构的分块：基于文档的逻辑结构进行分块，比如md文档有明确的段落或小结，这种方式适用有逻辑结构的文档。
 - 基于语义的分块：将文档依据标点符号（。？！）切分成诺干句子（句子之间有重叠。除开第一个句子和后一个句子重叠、最后一个句子和前一个句子重叠之外，中间的句子取重叠时都会覆盖前一个句子和后一个句子）。然后将相似度接近的句子合并在一起组成一个chunk.

#### 如何确定文本切割策略
**如何确定chunk_size大小。**
- 首先要考虑**embedding model**模型的**max token**参数大小。每个chunk_size的大小不能超过embedding模型的**max token**参数大小<b class="danger">（是原始文本embedding之后的token的长度）</b>。
- LLM model的 **max sequence length**参数，**这个参数不要根据单一的chunk_size的大小来确定。** 而应该根据**召回retrieval数量构成的总文本长度来确定**。比如召回top5数量的内容，这5个文本内容拼接起来，还要加上其他的prompt，其总长度不能超过大模型的max sequence length参数大小。

**常见的文本切分策略**
- **CharacterTextSplitter**：基于字符切分文本，通过限制字符的数量来确定chunk_size大小。适合小文本，比如markdown格式的文本。
- **RecursiveCharacterTextSplitter**：基于**字符列表**拆分文本，**递归切割**，递归切割的阈值是chunk_size的大小，当文本长度大于chunk_size的大小时，将文本进行递归切割，直到文本长度小于等于chunk_size的大小。适合长文本，比如PDF格式的文本。
- **Document Specific Splitter**：符合英文的语义方式，对英文文档支持好，中文较差。针对不同的文件类型使用不同的切分，比如markdown格式的文本，或者pdf格式的文本，或者html格式的文本等。

- **Semantic Splitter**： 滑动窗口切分，效果最好，基于文本的语义切分，比如根据文本的句法结构进行切分，然后将相似度接近的句子合并在一起组成一个chunk。
![alt text](./04-RAG/semantic%20text%20splitter.png)
https://www.bilibili.com/video/BV1dr421x7Su/?spm_id_from=333.788.recommend_more_video.3&vd_source=32fa1c202efe5bb6942b35f0c043a7e9
13分10秒

https://www.bilibili.com/video/BV1meqLYxEfN/?spm_id_from=333.999.0.0&vd_source=32fa1c202efe5bb6942b35f0c043a7e9



<b class="danger">待解决问题：将文档切分出来的片段，经过embedding处理后，token的长度区间分布，用plot直方图可视化展示出来。了解文档切分成诺干份后，经过embedding处理，token的长度分布区间，基于分布图来考虑是否要调整chunk_size大小</b>
https://www.bilibili.com/video/BV1dr421x7Su/?spm_id_from=333.788.recommend_more_video.3&vd_source=32fa1c202efe5bb6942b35f0c043a7e9
10分35秒



#### 四、如何选择embedded模型
huggingface embedded模型排名
https://huggingface.co/spaces/mteb/leaderboard
第一选择**bce-embedding-base_v1**，支持中英双语
第二选择**BAAI/bge-large-zh-v1.5** 中文模型
```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-zh-v1.5"
)
```

第三选择**m3e-base**模型，中文模型
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("moka-ai/m3e-base")
embeddings = model.encode(sentences)
```




### embedding模型如何选择
选择embedding模型时的四个参考要点
参考huggingface的模型库，选择适合自己的模型。
huggingface的模型库：https://huggingface.co/spaces/mteb/leaderboard
基于以下四点选择
1.Sequence length 参数，根据文档分块后的chunk size的大小来确定。长度指标，比如chunksize分完后，chunk的标准答案已经很长了，比如超过了512了，那选择模型的时候要选择一个Sequence length 长度指标能处理这种长文本的模型。这取决于对应answer的长度
2.embedding dimensions 参数，根据文本词汇的语义复杂程度来确定。嵌入维度指标，比如512，768，1024等。并不是越大越好，取决于业务场景中语义是否丰富，如果文本词汇的语义非常丰富保罗万象该指标越大越好，如果业务场景的语义比较精比较专业，比如针对专精业务领域的词汇、句子、文本，选择指标小的更好。
3.model size 指标，取决个人设备的显存存储情况。
4.用具体的简单的demo测试不同的模型，将query的embedding和文本的embedding进行可视化展示，识别模型效果。

<b class="alert info">
业界常用的做法：向量数据库和传统关系型数据库同时使用，比如简历信息中姓名，年龄，性别这些适用结构化检索的数据用关系型数据库存储，工作经历等描述型文本（不适合SQL查询检索的非结构化数据）使用向量数据库。当需要根据工作经历筛选最符合岗位的人员时查向量数据库，当需要具体年龄的人员时查结构化数据库。推荐适用milvus、weaviate向量数据库</b>

embedding模型的选择：https://www.bilibili.com/video/BV1GPS4YfEtu/?spm_id_from=333.999.0.0



##### 句子sentence 的embedded 如何处理
1. 首先分词处理，将句子切分成词汇，然后将每个词对应一个word embedding
2. 池化pooling，可使用均值pooling_mode_mean_tokens，pooling_mode_max_tokens，bert的pooling_mode_cls_token，pooling_mode_mean_sqrt_len_tokens

<b class="info">embedded模型一般是基于Sentence 使用BERT模型NSP来进行训练。
</b>


#### 五、如何选择PDF文档解析器
RAG的数据取决于两方面，一是数据的来源，二是对数据的解析。
- marker pdf转换器MARKER，转成markdown格式。或者选择docling
- llamaParse 基于AI能力的解析工具





### 过召回重排序 sentence-transformers
rerank是，将多个由向量索引检索到的原文结果和问题原文进行相关性排序，找出关联性最大的一项。
检索结果重排序：通过排序模型对query和document重新打分排序，解决多个满足query的答案没有被排在最前面。
```python
from sentence_transformers import CrossEncoder

# model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512) # 英文，模型较小
model = CrossEncoder('BAAI/bge-reranker-large', max_length=512) # 多语言，国产，模型较大

user_query = "how safe is llama 2"
# user_query = "llama 2安全性如何"
scores = model.predict([(user_query, doc)
                       for doc in search_results['documents'][0]])
# 按得分排序
sorted_list = sorted(
    zip(scores, search_results['documents'][0]), key=lambda x: x[0], reverse=True)
for score, doc in sorted_list:
    print(f"{score}\t{doc}\n")
```
model.predict() 方法用于预测给定输入与文档的相关性得分。具体来说，它接受一个列表，其中每个元素是一个元组，包含用户查询和一个文档。模型会根据这些输入计算出每个文档与用户查询的相关性得分。scores 列表中的每个元素对应一个文档的相关性得分。

这段代码的作用是从 sentence-transformers 库中导入 CrossEncoder 类。sentence-transformers 是一个用于自然语言处理（NLP）任务的库，特别是用于句子嵌入和语义相似度计算。CrossEncoder 是该库中的一个类，用于实现交叉编码器（Cross-Encoder）模型。
##### 什么是交叉编码器（Cross-Encoder）？
交叉编码器是一种深度学习模型，通常用于解决涉及两个文本序列的任务，如语义相似度计算、文本匹配等。它的工作原理如下：
1. 输入：交叉编码器接受两个文本序列作为输入，例如查询（query）和文档（document）。
2. 编码：这两个文本序列被连接在一起，形成一个新的输入序列。这个序列被送入一个预训练的Transformer模型（如BERT、RoBERTa等）进行编码。
3. 输出：Transformer模型的输出经过一个分类层（通常是全连接层），生成一个表示两个文本序列之间关系的分数或标签。
##### 主要用途
1. 语义相似度计算：判断两个句子或短文本的语义相似度。
2. 文本匹配：判断两个文本是否匹配或相关。
3. 问答系统：判断给定的问题和答案是否匹配。
4. 信息检索：在候选文档中找到与查询最相关的文档。
##### 示例
以下是一个简单的示例，展示了如何使用 CrossEncoder 来计算两个句子的相似度：
```python
from sentence_transformers import CrossEncoder

# 初始化交叉编码器模型
model = CrossEncoder('sentence-transformers/cross-encoder-ms-marco-MiniLM-L-6-v2')

# 定义两个句子
sentences = [
    ["这是一个例子句子", "这是另一个例子句子"],
    ["天气很好", "今天阳光明媚"]
]

# 计算相似度
scores = model.predict(sentences)

# 打印结果
for score in scores:
    print(f"相似度得分: {score:.4f}")
```

在这个示例中，CrossEncoder 模型会计算每对句子的相似度得分，并返回一个分数列表。
##### 优点
•高精度：由于使用了预训练的Transformer模型，交叉编码器通常具有很高的精度。
•灵活性：可以用于多种文本匹配和相似度计算任务。
##### 缺点
•计算成本：相对于简单的向量检索方法（如余弦距离），交叉编码器的计算成本较高，特别是在处理大规模数据时。






### 混合检索
在实际生产中，传统的关键字检索（稀疏表示）与向量检索（稠密表示）各有优劣。RAG实践中，文档切分后做两套策略，关键字检索、向量化检索结合实现混合检索。


### <b class="danger">使用BERT模型NSP来进行训练微调</b>
#### 如何分割文档保证内容语义完整性？
1. 利用自然语言特征
按段落分割：文本通常按段落分割，每个段落围绕一个中心思想，这通常能保持语义的完整性。如果文本格式整齐（如 PDF 或 HTML），段落分割是一个很好的起点。
使用句子边界检测：应用自然语言处理工具来检测句子边界，保证每个片段至少包含若干完整的句子。
2. 智能分割算法
文本建模：使用主题建模或语义分析工具，通过提取文本的主题结构来指导分割。这可以帮助识别出语义上相近的文本块，避免不相关的混杂。
重叠窗口技术：为保证上下文的连续性，可以使用重叠窗口进行切片。即在每个片段的开头或结尾重复一些内容，使片段之间内容稍有重叠以保证信息的连续性。
3. 基于语义的分割
聚类分析：通过词嵌入和聚类算法，可以将相似句子或段落聚集到一起。这允许分割基于语义特性而非仅仅形式特征，适用于更复杂和主题分明的文档。
关键点检测：使用深度学习模型（如 BERT）来了解句子间的关系和重要性，自动检测主题转折点，决定分割边界。
4. 基于结构化信息
利用文档结构：如果文档是结构化的（如 JSON、XML 等），那么可以利用结构层级（如章节、条目）来引导分割。
基于标记：许多文档格式包含标记语言（如 Markdown 中的头标签），这可以作为自然的分割点使用。
5. 经验法则和人工干预
专家知识：对领域中特殊格式的采用人工标注或领域专家提供自动分割指导。
迭代和反馈：尝试使用一些智能方法进行初步分割，然后通过用户反馈来不断优化分割策略。
6. 工具和库
NLTK 和 SpaCy：这些库提供了大量自然语言处理的工具包，可以帮助进行句子分割和词法分析。
Transformers 模型：如 BERT，可用于生成句子或文档嵌入，帮助识别语境和语义信息。
通过结合使用这些方法和技巧，您可以在 RAG 应用中更好地保障文档内容的语义完整性和连贯性，从而提高系统的精确性和可靠性。确保语义上整合良好的文档切片有利于在实际应用中提供更精细和有价值的信息检索结果。

#### 使用BERT模型NSP来进行训练，如何提高RAG分割文档的准确性和完整性。
在 RAG 系统中，使用 BERT 模型的 Next Sentence Prediction（NSP）任务可以帮助提高文档分割的准确性和语义完整性。NSP 任务训练一个模型来判断两个句子是否应该在一起出现，即它们是否在原文本中连续。这种能力可以被用来识别文档的自然分割点，确保切分后保留语义的连贯性。以下是一些具体方法：
1. 微调 BERT NSP 模型
数据准备：
从目标语料中获取真实文档，并制作正样本（紧邻句子对）和负样本（随机句子对），用于微调 BERT 的 NSP 部分。
可以增加一些跨段落但连续的句子对，帮助模型学会识别自然段落。
训练策略：
在您的领域数据上重新微调 BERT 的 NSP 部分，数据中的句子对结构越接近目标应用，效果越好。
使用大量领域样本，保证模型能够学到不同语境中自然句子连续性的特征。
2. 利用 NSP 预测分割点
预测应用：
将文档内容分段后，对每个相邻句子对应用 NSP 模型，通过高可信度的连续标签判断适合分割的点。
将分割可能性转化为阈值，确保每个片段在预测的基础上保持语义一致。
动态窗口法：
在较长文本切割成均匀段落，并对这些切片进行 NSP 分类，通过逐步调整扇区大小，预测合成自然段。
3. 基于 NSP 的语义完整性提升
结合其他语义工具：
可以结合上下文语义分析工具，从词汇和主题层面再验证 NSP 初始分割的准确性。
使用聚类或主题检测确认模型分割后的片段是否具有实际语义意义。
评价与选优：
设计多种分割策略，通过模型评估确定 NSP 为基础模型策略的合适性，持续引入新数据和反馈优化切分。
4. 工具和技术结合
集成 BERT 与 Info Extraction：
要注意 BERT 的能力在于识别上下文关联。你可以在分割后的每个段落进行信息提取来再次验证分割的合理性。
增量模型微调：
通过将新的数据输入到训练和调整的过程中，逐步增强模型的领域识别能力。
通过利用 BERT 的 NSP 能力，在 RAG 系统中对文档分割进行优化，你可以更好地保持文本切分后的语义完整性，降低文档内容丢失或语义断裂的风险。这将有助于新生成内容的质量和精准度，让信息检索和生成任务能更好地贴合用户需求。


### 通过bert模型微调，实现识别段落之间的关联性，提高RAG场景下切分文档的准确性，保证语义性

如果要对bert基础模型进行微调，实现能识别中文段落之间是否有强关联，应该怎么做？用什么数据集来微调？
要对基础的BERT模型进行微调，以实现能够识别中文**段落**之间是否存在强关联，您可以按照以下步骤进行操作。此外，我将推荐适合该任务的中文数据集或数据构建方法。


## 1. **任务定义**
将任务定义为一个二分类问题，即判断两个段落之间是否存在强关联。
明确任务目标是关键。针对识别**段落**之间的强关联性，您可以将其视为一种**段落对关系分类**任务。具体来说，任务可以定义为判断两个段落之间的关系类型，例如：

- **强关联（Strongly Related）**
- **中等关联（Moderately Related）**
- **无关联（Unrelated）**

## 2. **模型选择与微调**

### **选择基础模型**

对于中文段落关系识别，建议选择已经预训练好的中文BERT模型，例如：

- **[Chinese-BERT-wwm](https://huggingface.co/hfl/chinese-bert-wwm)**：采用全词掩码技术，适合中文语义理解。
- **[RoBERTa-zh](https://huggingface.co/hfl/roberta-zh)**：基于RoBERTa架构，性能优秀。

### **微调步骤**

以下以`transformers`库为例，展示如何微调BERT模型以进行段落关系识别：

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# 加载预训练的中文BERT模型和分词器
tokenizer = BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')
model = BertForSequenceClassification.from_pretrained('hfl/chinese-bert-wwm', num_labels=3)  # 三种关系

# 加载数据集（以自定义数据集为例）
dataset = load_dataset('your_custom_paragraph_dataset')

# 定义分词函数
def tokenize_function(examples):
    return tokenizer(examples['paragraph1'], examples['paragraph2'], padding='max_length', truncation=True)

# 预处理数据
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 加载评价指标
metric = load_metric('accuracy')

def compute_metrics(p):
    predictions, labels = p
    preds = predictions.argmax(-1)
    return metric.compute(predictions=preds, references=labels)

# 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
)

# 初始化Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    compute_metrics=compute_metrics,
)

# 开始训练
trainer.train()
```

**注意事项**：

- 确保安装必要的库：

  ```bash
  pip install transformers datasets
  ```

- 根据具体任务调整`num_labels`。例如，这里假设有三种关系类型。
- 调整`per_device_train_batch_size`和`num_train_epochs`以适应您的计算资源和数据规模。

## 3. **推荐数据集**

针对**段落关系识别**，目前公开的中文数据集较少，建议考虑以下几种方法：

### **1. 使用现有的NLI数据集**

虽然大多数自然语言推断（NLI）数据集以句子对为单位，但您可以将其扩展为段落对。例如：

- **[OCNLI（Open Chinese Natural Language Inference）](https://github.com/OYE93/OCNLI)**：
  - **描述**：中文自然语言推断数据集，包含大量句子对，适用于判断句子之间的推理关系。
  - **资源**：
    - [OCNLI Hugging Face 页面](https://huggingface.co/datasets/OCNLI)
    - 可通过`datasets`库加载：
      ```python
      from datasets import load_dataset
      dataset = load_dataset('OCNLI')
      ```

**扩展方法**：

将多个句子对组合成段落对，以模拟段落间的关系。例如，将两个相关的句子对组成一个段落。

### **2. 构建自定义数据集**

如果现有数据集无法满足需求，建议构建自定义数据集。步骤包括：

#### **a. 数据收集**

收集包含多个段落的中文文档，如新闻文章、学术论文或报告。

#### **b. 数据标注**

设计标注指南，定义段落之间的关系类型。例如：

- **强关联**：段落内容高度相关，相互支持或补充。
- **中等关联**：段落内容有一定关联，但不紧密。
- **无关联**：段落内容无明显关联。

使用众包平台或内部团队进行数据标注，确保标注质量。

#### **c. 数据预处理**

将标注的段落对格式化为模型可接受的输入格式。例如：

```json
{
  "paragraph1": "段落1的文本内容。",
  "paragraph2": "段落2的文本内容。",
  "label": 0  # 0: 强关联, 1: 中等关联, 2: 无关联
}
```

### **3. 使用其他相关任务的数据集**

一些文档结构分析或文本相似度评估的数据集也可以进行改造以适应段落关系识别任务。例如：

- **[LCQMC（Large-scale Chinese Question Matching Corpus）](https://github.com/CLUEbenchmark/CLUE)**：
  - **描述**：大规模中文问题匹配数据集，适用于句子相似度评估。
  - **资源**：
    - [LCQMC GitHub](https://github.com/CLUEbenchmark/CLUE/tree/main/CLUEdatasets/LCQMC)
    - 可通过`datasets`库加载：
      ```python
      from datasets import load_dataset
      dataset = load_dataset('lcqmc')
      ```

**扩展方法**：

将句子对扩展为段落对，或者将多个句子对组合成段落对。

## 4. **数据预处理**

无论选择哪种数据集，数据预处理都是关键步骤，包括：

- **文本清洗**：去除噪音字符、特殊符号等。
- **分段处理**：确保每个输入样本包含两个完整的段落。
- **分词与编码**：使用BERT的分词器对段落进行分词和编码。
- **标签编码**：将文本标签转换为数值标签，如`强关联`→0，`中等关联`→1，`无关联`→2。

示例分词函数已在上述代码中提供。

## 5. **评价指标**

在微调和评估过程中，建议使用以下评价指标：

- **准确率（Accuracy）**：适用于均衡数据集。
- **F1分数**：特别是宏平均F1，适用于类别不平衡的场景。
- **精确率与召回率（Precision & Recall）**：深入了解模型在各类别上的表现。

可以根据具体需求调整评价指标。

## 6. **模型评估与优化**

- **交叉验证**：使用k折交叉验证评估模型的泛化能力。
- **超参数调整**：调整学习率、批量大小、训练轮次等参数以优化性能。
- **模型集成**：结合多个模型的预测结果，提升整体性能。
- **错误分析**：分析模型错误预测的案例，改进数据集或模型结构。

## 7. **示例代码详解**

以下是对上述示例代码的详细说明：

```python
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# 1. 加载模型和分词器
tokenizer = BertTokenizer.from_pretrained('hfl/chinese-bert-wwm')
model = BertForSequenceClassification.from_pretrained('hfl/chinese-bert-wwm', num_labels=3)

# 2. 加载数据集
dataset = load_dataset('your_custom_paragraph_dataset')  # 替换为您的数据集

# 3. 分词和编码
def tokenize_function(examples):
    return tokenizer(examples['paragraph1'], examples['paragraph2'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 4. 加载评价指标
metric = load_metric('accuracy')

def compute_metrics(p):
    predictions, labels = p
    preds = predictions.argmax(-1)
    return metric.compute(predictions=preds, references=labels)

# 5. 设置训练参数
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
)

# 6. 初始化Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    compute_metrics=compute_metrics,
)

# 7. 开始训练
trainer.train()
```

**关键步骤解释**：

1. **加载模型和分词器**：选择适合中文的预训练BERT模型，并加载相应的分词器。
2. **加载数据集**：使用`datasets`库加载自定义的段落关系数据集。
3. **分词和编码**：将段落对转换为模型可接受的输入格式，确保长度一致。
4. **加载评价指标**：定义如何评估模型性能，这里使用准确率。
5. **设置训练参数**：配置输出目录、学习率、批量大小、训练轮次等参数。
6. **初始化Trainer**：将模型、训练参数、数据集和评价指标结合起来。
7. **开始训练**：执行模型训练过程。

## 8. **结论**

通过选择合适的中文预训练BERT模型，并使用适当的中文段落关系数据集进行微调，您可以训练出能够有效识别段落之间强关联性的模型。确保在微调过程中合理预处理数据，选择合适的评价指标，并根据模型表现不断优化训练参数，以达到最佳效果。

如果现有的数据集无法完全满足需求，建议构建自定义数据集，以更贴近具体应用场景。同时，结合领域知识和实际需求，调整模型架构和训练策略，以提升模型在特定任务上的表现。


## 文档中的表格处理
1.将每页PDF转成图片
2.在图片中采用OCR识别表格
3.将表格内容向量化







## 5.Assitants API

Assistants API具备的能力：
- 创建和管理Assistants 每个Assistants都有独立的配置
- 支持代码沙箱，可向code interpreter 发送文件
- 支持function calling 
- 通过集成自有的向量数据库支持RAG
- 支持无限多轮对话，保存在openai服务器上



OpenAI 为了降低开发门槛所提供的一套开发工具。类似字节跳动的coze开发工具，适合快速搭建一个基于语言模型的原型demo，验证功能、汇报，如果要做生产级的应用此类开发工具还是有所欠缺，无法精细化操控。想要极致调优，还得原生API+RAG
创建步骤：
 1. 在playground中创建。 配置function call, code interpreter, file search等
 2. 在playground中调试测试效果。
 3. 发布之后，得到一个assistant id号
 4. 将调试后的代码集成到其他web，app应用中，通过代码访问和调用。

### assitant
创建assistant `assistant = client.beta.assistants.creat()`
```python
assistant = client.beta.assistants.creat(
    name="AGIClass Demo TempLive",
    instructions="你叫瓜瓜，你是AGI课堂的智能助理。你负责回答与AGI课堂有关的问题。",
    model="gpt-4o"
)
```

获取所有assistant 列表 `assistants = client.beta.assistants.list()`
删除指定id的assistant `client.beta.assistants.delete(id)`

### thread
**thread中保存的是对话历史，即message**
管理和保存每个assitant和用户的对话历史。
每个通过assitants api搭建的assitant发布后都会与很多用户交互，每个用户交互的对话历史都存在thread中即messages
一个assistant可以有多个thread
一个thread可以有无限条message
一个用户与assistant的多轮对话可以维护在一个thread中



创建thread `thread = client.beta.threads.create`
```python
thread = client.beta.threads.create(
    metadata={"fullname": "王卓然", "username": "wzr"}
)
```

获取 thread`threads.retrieve()`
获取thread `thread = client.beta.threads.retrieve(thread.id)`

修改 thread `threads.modify()`
删除 thread`threads.delete()`


### message
在thread中创建消息 `message=client.beta.threads.messages.create()`

```python
message = client.beta.threads.messages.create(
    thread_id=thread.id, #message必须归属一个thread_id,
    role="user",
    content="你能做什么"
)
```
获取消息`threads.message.retrieve()`
列出给定thread下的所有消息`threads.message.list()`
**更新**message中的 **metadata** `threads.message.update()`


### run方法
run方法是把assistant 和 threads 关联起来，进行对话
**一个prompt 就是一次run，通过不同的run_id来维护**


##### 将存在的thread_id对应thread和指定assistant_id的assistant绑定，根据thread中已有的信息，机器人就可以开始产生回复了。
```python
assistant_id='xxxxx'


run= client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id
)

if run.status == 'completed':
    message = client.beta.threads.messages,list(
        thead_id=thread.id
    )
    show_json(message)
else:
    print(run.status)

# 示例2
# 创建 thread
thread = client.beta.threads.create()

# 创建thread之后，向thread中添加新一轮的 user message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="用代码计算 1234567 的平方根",
)

```

##### 使用 stream 接口并传入 EventHandler()

```python
from typing_extensions import override
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
    # override 装饰器，用来标记和声明覆写父类的on_text_created方法，便于静态类型检查时提前发现覆写因为拼写或逻辑的错误
    @override
    def on_text_created(self, text) -> None:
        """响应输出创建事件"""
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """响应输出生成的流片段"""
        print(delta.value, end="", flush=True)

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant_id,
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
```


列出thread 下所有的run `threads.runs.list()`
获取run `threads.runs.retrieve()`
**修改run 的metadata** `threads.runs.update()`
取消in_progress状态的run `threads.runs.cancel()`
流式对话`threads.runs.stream()`


### 创建Assistant 时声明function
```python
assistant = client.beta.assistants.create(
  instructions="你叫瓜瓜。你是AGI课堂的助手。你只回答跟AI大模型有关的问题。不要跟学生闲聊。每次回答问题前，你要拆解问题并输出一步一步的思考过程。",
  model="gpt-4o",
  tools=[{
    "type": "function",
    "function": {
      "name": "course_info",
      "description": "用于查看具体课程信息，包括时间表，题目，讲师，等等。Function输入必须是一个合法的SQL表达式。",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "SQL query extracting info to answer the user's question.\nSQL should be written using this database schema:\n\nCREATE TABLE Courses (\n\tid INT AUTO_INCREMENT PRIMARY KEY,\n\tcourse_date DATE NOT NULL,\n\tstart_time TIME NOT NULL,\n\tend_time TIME NOT NULL,\n\tcourse_name VARCHAR(255) NOT NULL,\n\tinstructor VARCHAR(255) NOT NULL\n);\n\nThe query should be returned in plain text, not in JSON.\nThe query should only contain grammars supported by SQLite."
          }
        },
        "required": [
          "query"
        ]
      }
    }
  }]
)
```

### Assistant 内置RAG
```python
# 创建vector_store
vector_store = client.beta.vector_stores.create(
  name="MyVectorStore")

# 上传文件
file = client.files.create(
  file=open("agiclass_intro.pdf", "rb"),
  purpose="assistants"
)

# 将文件添加到vector_store
vector_store_file = client.beta.vector_stores.files.create(
  vector_store_id=vector_store.id,
  file_id=file.id
)
```
列出所有文件 `client.files.list()` 
获取文件对象 `client.files.retrieve()` 
删除文件 `client.files.delete()` 
读取文件内容 `client.files.content()` 

### 创建assistant时 声明RAG能力
```python
assistant = client.beta.assistants.create(
  instructions="你是个问答机器人，你根据给定的知识回答用户问题。",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

# 指定assistant的检索源
assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
```




## 6.LlamaIndex

LlamaIndex是大语言模型的开发框架SDK，它提供了各种工具，让开发者可以更方便地开发基于大语言模型的应用。
  - 第三方能力抽象。比如 LLM、向量数据库、搜索接口等
  - 常用工具、方案封装
  - 底层实现封装。比如流式接口、超时重连、异步与并行等

使用LlamaIndex开发框架的优势：比如可以随意更换 LLM 而不用大量重构代码，将经常变的prompt部分放在外部维护而不是放在代码里，方便调试和测试。

##### LlamaIndex 是一个为开发 **「上下文增强」** 的大语言模型应用的框架（也就是 SDK）
![LlamaIndex功能示意图](./06-LlamaIndex/basic_rag.png)



### RAG pipeline 的5个阶段
1. Loading
加载：这指的是从数据所在的位置获取数据，无论是文本文件、PDF、另一个网站、数据库还是 API，将其加载到到流程中。LlamaHub 提供了数百个连接器供选择。
2. Indexing
索引：创建一种数据结构，以便查询数据。对于LLMs，基本都使用 vector embeddings策略来建立向量索引，以便轻松准确地找到上下文相关的数据。
3. Storing
存储：数据被索引后，通过向量数据库来存储索引，以及其他元数据（元数据可避免需要重新索引）。
4. Querying
查询：对于任何给定的索引策略，有多种方式可以利用 LLMs 和 LlamaIndex 数据结构进行查询，包括子查询、多步查询和混合策略。
5. Evaluation
评估：在任何流程中都是一个关键步骤，即检查其相对于其他策略的有效性，或者当进行业务更改时。评估提供了关于查询响应的准确性、一致性和速度的客观指标。

### RAG的核心概念
1. **Document** 是围绕任何数据源的容器 - 例如，PDF、API 输出或从数据库中检索数据。 
2. **Node** 是 LlamaIndex 中数据的原子单元，代表源 Document 的“块”。nodes节点具有与它们所在的文档documents和其他节点相关的元数据。
3. **Connectors** 数据连接器（通常称为 Reader ）从不同的数据源和数据格式中摄取数据到 Documents 和 Nodes 。
4. **Indexes** LlamaIndex 将数据索引到易于检索的结构中。通常涉及生成 vector embeddings ，这些数据存储在向量数据库中。
5. **Embeddings** 嵌入：由LLMs生成 embeddings 的数据的数值表示。在进行相关性过滤时，LlamaIndex 会将查询转换为嵌入，在向量数据库中找到与query的查询embeddings数值相似的数据。
6. **Retrievers** 检索器：检索器定义了在给定查询时如何从索引结果中准确高效地检索出相关的上下文。
7. **Routers** 路由器：路由器决定使用哪个检索器从知识库中检索相关上下文。RouterRetriever 类负责选择一个或多个候选检索器来执行查询。它们使用选择器根据每个候选检索器的元数据和查询来选择最佳选项。
8. **Node Postprocessors** 节点后处理器，接收一组检索到的节点，并对其应用转换、过滤或重新排序逻辑。
9. **Response Synthesizers** 响应合成器通过使用用户查询和一组检索到的文本片段，从LLM生成响应。

### Document 和 Node的关系
**Document:** 文档是围绕任何数据源的通用容器 - 例如，PDF、API 输出或从数据库检索的数据。可以手动创建document，也可以通过数据加载器从各种数据源中摄取数据。

**Node:** 节点代表源文档的“块”，无论是文本块、图像还是其他。类似于文档，它们包含与其他节点的关系信息和元数据。可以选择直接定义节点及其所有属性。也可以选择通过**NodeParser** 类将源文档“解析”为节点。**从文档构建出的每个节点都将继承该文档的相同元数据（例如：file_name）**

**文档存储着文本和一些其他属性。**
- metadata: 元数据，例如文件名、路径、创建时间等。可以附加到文本上的注释字典
- relationships: 包含与其他文档/节点关系的字典。

```python
# 对文档索引
from llama_index.core import Document, VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)

# 对节点索引
from llama_index.core.node_parser import SentenceSplitter
parser = SentenceSplitter()
nodes = parser.get_nodes_from_documents(documents)

index = VectorStoreIndex(nodes)
```

### metadata 元数据
每个document文档上的 metadata 字典，可以包含额外信息以帮助提供响应并追踪查询响应的来源。这些信息可以是任何内容，例如文件名或类别。
任何在document文档的 metadata 字典中设置的任何元信息都会显示在每个Node节点（由文档创建）的 metadata 中,使索引能够在查询和响应中利用它。

<b class="danger">默认情况下，设置的任何元数据都将包含在embeddings生成中，还有LLM生成中</b>
一个文档可能包含许多元数据键，但实际开发时可能不希望所有这些键值对元数据在LLM生成响应时对LLM可见。比如不希望LLM读取文档的 file_name属性，但在生成embedded嵌入时又需要file_name属性。
- 自定义对LLM模型生成响应时，元数据的可见范围 
```python
# 排除某个元数据
document.excluded_llm_metadata_keys = ["file_name"]

# 测试LLM生成响应时，实际看到的metadata，验证上面的排除是否生效
from llama_index.core.schema import MetadataMode
print(document.get_content(metadata_mode=MetadataMode.LLM))
```

- 自定义对embedded模型生成嵌入时，元数据的可见范围
```python
document.excluded_embed_metadata_keys = ["file_name"]

# 测试embedded模型，在生成嵌入时，能看看到metadata，验证上面的排除是否生效
from llama_index.core.schema import MetadataMode
print(document.get_content(metadata_mode=MetadataMode.EMBED))
```

- 自定义元数据的展示格式，由三个属性控制
    - Document.metadata_seperator 设置连接所有元数据的键/值对的分割符
    - Document.metadata_template 设置元数据的展示格式，如：`{key}: {value}`，默认为`{key}={value}`
    - Document.text_template 设置元数据与文档/节点文本内容结合时的模板格式




**添加元数据的几种方法**：
- 文档构造函数中添加元数据
```python
document = Document(
    text="text",
    metadata={"filename": "<doc_file_name>", "category": "<category>"},
)
```
- 文档创建后添加元数据`document.metadata={"filename": "<doc_file_name>", "category": "<category>"}`
- 使用simpleDirectoryReader类读取文档时，通过钩子函数设置元数据
```python
from llama_index.core import SimpleDirectoryReader
filename_fn = lambda filename: {"file_name": filename}
# automatically sets the metadata of each document according to filename_fn
documents = SimpleDirectoryReader(
    "./data", file_metadata=filename_fn
).load_data()
```


**元数据提取的几种方法**： 可以使用 Metadata Extractor 模块自动化元数据提取。元数据提取模块包括以下“特征提取器”：
- SummaryExtractor - 自动从一组节点中提取摘要
- QuestionsAnsweredExtractor - 提取一组节点可以回答的问题
- TitleExtractor - 从每个节点的内容中提取标题
- EntityExtractor - 提取每个节点内容中提到的实体（即地点、人物、事物名称）
```python
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.node_parser import TokenTextSplitter

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)
title_extractor = TitleExtractor(nodes=5)
qa_extractor = QuestionsAnsweredExtractor(questions=3)

# assume documents are defined -> extract nodes
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    # 链式调用
    # transformations的流程是，先分割文本，再提取标题，最后提取节点中可以回答的提问
    transformations=[text_splitter, title_extractor, qa_extractor]
)

nodes = pipeline.run(
    documents=documents,
    in_place=True,
    show_progress=True,
)

# 或者在插入索引时使用链式调用，提取元数据
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(
    # transformations的流程是，先分割文本，再提取标题，最后提取节点中可以回答的提问
    documents, transformations=[text_splitter, title_extractor, qa_extractor]
)
```

### index 索引
在「检索」相关的上下文中，「索引」即index， 通常是指为了实现快速检索而设计的特定「数据结构」。
常见的两种索引类型
 - **向量存储索引** VectorStoreIndex 文档被拆分成节点之后，为每个节点创建 vector embeddings ，以便由LLM进行查询。
 - 摘要索引 summary index 一种更简单的索引形式，生成文档的文本摘要并创建索引，查询时返回的是整个文档document。

 VectorStoreIndex 返回最相似的嵌入及其对应的文本块。控制返回多少嵌入的参数称为 top_k，k即返回的嵌入数量。
```python
from llama_index.core import VectorStoreIndex
# 文档创建向量索引
index = VectorStoreIndex.from_documents(documents)
# nodes创建向量索引
index = VectorStoreIndex(nodes)
```

**索引建立后的文档管理 document management** 索引结构允许对document文档进行查看、插入、删除、更新和刷新操作。
- 创建索引后可将文档插入到索引结构中
    - 动态添加数据，数据是动态生成或动态获取的。创建索引后，可以根据需要逐步插入文档，而不需要一次性加载所有数据。
    - 灵活性，通过 insert 方法，你可以在任何时候向索引中添加新的文档，而不需要重新创建整个索引。
    - 性能优化，在创建索引时，如果初始文档数量非常大，一次性加载所有文档可能会导致内存和性能问题。通过逐步插入文档，可以更好地控制内存使用和性能，特别是在资源有限的环境中。
- deletion 通过指定document_id，从索引中删除文档
```python
# 参数delete_from_docstore
# True：不仅从索引中删除文档引用，还会从 DocStore 中删除该文档。
# False：仅从索引中删除文档引用，但不从 DocStore 中删除该文档。
index.delete_ref_doc("doc_id_0", delete_from_docstore=True)
```

- update 文档已在索引中存在,可根据文档的doc_id来更新文档
    ```python
    # NOTE: the document has a `doc_id` specified
    doc_chunks[0].text = "Brand new document text"
    index.update_ref_doc(doc_chunks[0])
    ```
- refresh refresh() 函数只会更新具有相同 doc id_ 但不同文本内容的文档。另外，刷新时，如果不在索引中的文档也将被插入。
    ```python
    # modify first document, with the same doc_id 修改doc_id_0 的文本
    doc_chunks[0] = Document(text="Super new document text", id_="doc_id_0")

    # add a new document  这里创建了一个doc_id为doc_id_3 的新文档
    doc_chunks.append(
        Document(
            text="This isn't in the index yet, but it will be soon!",
            id_="doc_id_3",
        )
    )

    # refresh the index 执行刷新操作，这里会更新doc_id_0 和 新插入doc_id_3
    refreshed_docs = index.refresh_ref_docs(doc_chunks)

    # refreshed_docs[0] and refreshed_docs[-1] should be true 修改的文档和最后添加的文档都会被刷新，索引-1即最后一个添加的文档
    ```
- 文档的跟踪，查看已插入的文档
    ```python
    print(index.ref_doc_info)
    """
    > {'doc_id_1': RefDocInfo(node_ids=['071a66a8-3c47-49ad-84fa-7010c6277479'], metadata={}),
    'doc_id_2': RefDocInfo(node_ids=['9563e84b-f934-41c3-acfd-22e88492c869'], metadata={}),
    'doc_id_0': RefDocInfo(node_ids=['b53e6c2f-16f7-4024-af4c-42890e945f36'], metadata={}),
    'doc_id_3': RefDocInfo(node_ids=['6bedb29f-15db-4c7c-9885-7490e10aa33f'], metadata={})}
    """
    ```



### storing 存储
数据加载和索引完成，需要存储起来，以避免重建索引的时间和成本。索引默认存储在内存中。
索引内置持久化方法`.persist()`
- 持久化，写入磁盘存储索引
```python
# 将索引写入磁盘
index.storage_context.persist(persist_dir="<persist_dir>")

# 从磁盘加载索引
from llama_index.core import StorageContext, load_index_from_storage
storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")
# 加载索引
index = load_index_from_storage(storage_context)
```

- 持久化，vector store 向量存储
```python
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# load some documents
documents = SimpleDirectoryReader("./data").load_data()

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create your index 从文档创建向量索引
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# create a query engine and query 创建query engine并查询
query_engine = index.as_query_engine()
response = query_engine.query("What is the meaning of life?")
print(response)


# load your index from stored vectors 从存储的向量加载索引
index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)
# create a query engine 创建query engine并查询
query_engine = index.as_query_engine()
response = query_engine.query("What is llama2?")
print(response)

```

- 向量数据库推荐
    - Alibaba Cloud OpenSearch 云服务，收费，不支持混合检索
    - Elasticsearch 单机部署或云服务，开源，支持混合检索。适合需要综合搜索和分析功能的场景，适合中小规模的向量数据集，对性能要求不是特别高的场景。
    - Milvus 单机部署或云服务，开源，支持混合检索，可使用GUP加速。适合需要高性能向量搜索的场景，特别是处理大规模向量数据集。适合专注于向量相似度搜索的应用，如推荐系统、图像搜索、自然语言处理等。

### querying 查询引擎
query_engine由索引和prompt组成，用于从索引中检索信息，并根据用户输入的prompt生成答案。
```python
# 单论输出
query_engine = index.as_query_engine()
response = query_engine.query("What is the meaning of life?")

# 流式输出
query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("What is the meaning of life?")
response.print_response_stream()

# 多轮对话
chat_engine = index.as_chat_engine()
response = chat_engine.chat("Llama2 有多少参数?")
print(response)
response = chat_engine.chat("How many at most?")
print(response)

# 多轮对话流式输出
chat_engine = index.as_chat_engine()
streaming_response = chat_engine.stream_chat("Llama 2有多少参数?")
# streaming_response.print_response_stream()
for token in streaming_response.response_gen:
    print(token, end="", flush=True)
```

### 查询的三个阶段
 - Retrieval 召回，检索是指从您的 Index 中找到并返回与您的查询最相关的文档。最常见的一种检索类型是“top-k”语义检索，但还有许多其他的检索策略。
 - Postprocessing  后处理，将检索到的 Node 可以根据需要重新排序、转换或过滤，例如要求它们具有特定的元数据，如附加的关键词。
 - Response synthesis 响应合成，将查询、最相关的数据和用户的提示信息结合起来，发送到LLM以返回响应。

 ##### querying engine 的低级API，对查询过程细粒度控制
 ```python

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# build index
index = VectorStoreIndex.from_documents(documents)

# configure retriever 配置检索器
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# configure response synthesizer 配置响应合成器
response_synthesizer = get_response_synthesizer()

# assemble query engine 构建查询引擎
query_engine = RetrieverQueryEngine(
    retriever=retriever, # 检索器
    response_synthesizer=response_synthesizer, # 响应合成器
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)], # 后处理器
)

# query
response = query_engine.query("What did the author do growing up?")
print(response)
 ```



##### 检索器
检索器负责根据用户查询（或聊天消息）获取最相关的上下文。可以在索引之上构建，但也可以独立定义。它被用作查询引擎（和聊天引擎）中检索相关上下文的关键构建块。
```python
# 从索引获取检索器
retriever = index.as_retriever()
nodes = retriever.retrieve("Who is Paul Graham?")

# 使用索引特定的检索器类， 这里创建了一个基于摘要的索引器
retriever = summary_index.as_retriever(
    retriever_mode="llm",
)
```
##### 检索器模型 Retriever Modules
- BM25Retriever：基于 tokenizer 实现的 BM25 经典检索算法
- KeywordTableGPTRetriever：使用 GPT 提取检索关键字
- KeywordTableSimpleRetriever：使用正则表达式提取检索关键字
- KeywordTableRAKERetriever：使用RAKE算法提取检索关键字（有语言限制）






##### 索引模式 Retriever Modes
- 向量索引检索 vector_index.as_retriever() ，总是返回一个 VectorIndexRetriever
- 摘要索引检索 summary_index.as_retriever(retriever_mode="llm或者embedding")
- 树索引检索 tree_index.as_retriever(retriever_mode="select_leaf或者select_leaf_embedding或者all_leaf或者root")
- 关键词索引检索 keyword_index.as_retriever(retriever_mode="simple或者rake")
- 知识图谱索引检索 knowledge_graph_index.as_retriever()
- 文档摘要索引检索 summary_index.as_retriever(retriever_mode="llm或者embedding")


##### 检索后处理 Postprocessors 后处理器
节点后处理器是一组模块，它们接收一组节点，并在返回之前对它们进行某种转换或过滤。例如可以用不同模型**对检索后的 Nodes 做重排序**
**节点后处理器通常在查询引擎中应用，在节点检索步骤之后和响应合成步骤之前。**
支持高级 Node 过滤和增强，这可以进一步提高检索到的 Node 对象的相关性。这有助于减少调用/数量LLM或提高响应质量。比如
KeywordNodePostprocessor ：用于确保某些关键词被排除或包含，通过 required_keywords 和 exclude_keywords 过滤节点
SimilarityPostprocessor : 通过设置相似度分数的阈值来过滤节点（仅由基于嵌入的检索器支持）
PrevNextNodePostprocessor：基于节点关系，为检索到的节点对象补充额外的相关上下文。
MetadataReplacementPostProcessor：用于将节点内容替换为节点元数据中的字段。如果元数据中不存在该字段，则节点文本保持不变。在与其他功能结合使用时最为有用。

```python
node_postprocessors = [
    KeywordNodePostprocessor(
        required_keywords=["Combinator"], exclude_keywords=["Italy"]
    )
]
query_engine = RetrieverQueryEngine.from_args(
    retriever, node_postprocessors=node_postprocessors
)
response = query_engine.query("What did the author do growing up?")
```

#####  response synthesis 响应合成
```python
query_engine = RetrieverQueryEngine.from_args(
    retriever, response_mode=response_mode #default 或者 compact 或者tree_summarize 或者no_text 或者accumulate
)
```


<b class="info">RetrieverQueryEngine()：直接初始化，适合参数已知且固定的情况。</b>
<b class="info">RetrieverQueryEngine.from_args()：工厂方法，适合需要根据不同参数动态创建实例的情况，更加灵活。</b>




### LlamaIndex的核心模块
![LlamaIndex核心模块](./06-LlamaIndex/llamaindex%20basic.png)

### Building a RAG pipeline with LlamaIndex
- step1: load data 加载数据
- step2: transformer the data 转换数据
- step3: index and store then data 索引并存储数据

#### 1. Reader 数据连接器
LlamaIndex 通过数据连接器来完成这项工作，也称为 Reader 。数据连接器从不同的数据源中获取数据，并将数据**格式化为 Document** 对象。一个 Document 是数据的集合,以及关于该数据的元数据。

加载本地数据，使用**SimpleDirectoryReader** 这是一个llamaindex自带的简单的本地文件加载器。它会遍历指定目录，并根据文件扩展名自动加载文件（文本内容）。支持各种常见的文档类型csv,pdf,txt,docx,png,mp3,ppt等。

如自带数据连接器无法实现需求(SQL数据库读取，API接口读取)，可以通过llamaindex提供的第三方数据连接器实现。https://llamahub.ai/?tab=readers

#### 2. Transformer 数据转换器 及 Node节点解析模块
通过 Transformations 定义一个数据（Documents）的多步处理的流程（Pipeline）。 这个 **Pipeline 的一个显著特点是，它的每个子步骤是可以缓存（cache）的**，即如果该子步骤的输入与处理方法不变，重复调用时会直接从缓存中获取结果，而无需重新执行该子步骤，这样即节省时间也会节省 token 

数据加载后，您需要对其进行处理和转换输出Node，然后再将其放入存储系统。这些转换包括分块、提取元数据和嵌入每个块。
**节点解析器**是一种简单的抽象，它将文档列表分成 Node 对象，使得每个节点是父文档的特定片段。
<b class="danger">当文档被分解成节点时，它的所有属性都会继承到子节点（即 metadata ，文本和元数据模板等）</b> 

transformer API
**高级转换API** 封装好的功能，简便操作，可控性低
```python
from llama_index.core.node_parser import SentenceSplitter
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# global 全局settings
from llama_index.core import Settings

Settings.text_splitter = text_splitter

# per-index
index = VectorStoreIndex.from_documents(
    documents, transformations=[text_splitter]
)
```
**低级转换API** 可控性高，高度定制转换过程，文本拆分器、元数据提等操作
分为四个步骤
    - 拆分文档为节点Node
    - 添加元数据
    - embedding 文本向量化嵌入
    - 创建索引

##### 如何使用节点解析器
 - 独立使用
```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)

nodes = node_parser.get_nodes_from_documents(
    [Document(text="long text")], show_progress=False
)
```
 - 在transformer转换器的**摄取管道**中使用
```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

documents = SimpleDirectoryReader("./data").load_data()

pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])

nodes = pipeline.run(documents=documents)
```
 - 在索引中使用
```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader("./data").load_data()

# global
from llama_index.core import Settings

Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
index = VectorStoreIndex.from_documents(
    documents,
    transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)],
)
```




##### 基于文件的节点解析器
根据解析的内容类型（JSON、Markdown 等）创建节点
- SimpleFileNodeParser 简单文件解析器（自动使用最适合每种内容类型的节点解析器来创建节点）
- HTMLNodeParser HTML 节点解析器（根据html文档创建节点）
- JSONNodeParser JSON 节点解析器（根据json文档创建节点）

##### 节点解析器的文本切分策略
**SentenceSplitter** 
- 按指定chunk_size和chunk_overlap参数来控制句子边界，进而来切分文本
- 适用场景，适用于短文本和细粒度检索。
    - 短文本处理：适用于处理短文章、新闻摘要、社交媒体帖子等，这些文本通常由简短的句子组成。
    - 细粒度检索：当需要对文本进行细粒度的检索和分析时，按句子分割可以提供更精确的匹配。

**SentenceWindowNodeParser** 句子窗口节点解析器
- 将所有文档拆分为单个句子，生成的节点还包含每个节点周围的“窗口”句子信息，具体来说，它决定了每个节点中包含的**前后**连续句子的数量。可以保留更多的上下文信息。例如，如果一个句子的意义需要前一句或后一句来补充，较大的 window_size 可以确保这些句子一起被处理。
- 适用场景，适用于需要考虑上下文相关性的场景。
    - 上下文相关性：适用于需要考虑上下文相关性的场景，例如情感分析、问答系统等。通过包含前后文句子，可以更好地理解句子的背景和语境。
    - 长文本处理：对于较长的文本，按句子窗口分割可以保持上下文的连贯性，同时减少单个节点的长度。

**SemanticSplitterNodeParser** 语义分割节点解析器
- 不是使用固定大小的块来分割文本，语义分割器自适应地使用嵌入相似性在句子之间选择断点。这确保了“块”包含彼此语义相关的句子。
- 适用场景，适用于需要保持语义连贯性的场景。
    - 语义相关性：适用于需要保持语义连贯性的场景，例如文本摘要、主题建模等。通过语义分割，可以确保每个节点包含的是语义上相关的内容。
    - 复杂文本处理：对于复杂的长文档，语义分割可以帮助更好地组织和管理文本数据，提高检索和分析的效率。

**TokenTextSplitter** 分词文本分割器
- 基于令牌（token）进行文本分割的。它将文本拆分成一个个小的令牌，然后根据指定的令牌数量来创建节点。适用于需要精确控制每个节点包含的文本长度的场景。例如，在构建索引时，你可能希望每个节点的长度大致相同，以优化存储和检索效率。
- 适用场景，适用于需要细粒度控制和性能优化的场景。
    - 细粒度控制：适用于需要对文本进行非常细粒度控制的场景，例如机器翻译、词频分析等。
    - 性能优化：通过控制每个节点的词数，可以优化内存使用和处理速度，特别是在处理大规模数据集时。

**HierarchicalNodeParser** 基于关系的节点解析器 

- 将文本数据解析成一个层次化的节点结构。每个节点可以包含子节点，形成树状结构。这有助于更好地表示文档的逻辑结构和层次关系。它支持多种分割策略，可以根据段落、章节、标题等逻辑单元来分割文本。这使得解析后的节点更加有意义，便于后续的处理和分析。层次化的节点结构可以提高检索效率。在进行信息检索时，可以通过层次结构快速定位到相关部分，减少不必要的遍历。
- 首先对输入的文本数据进行预处理，识别出段落、章节、标题等逻辑单元。根据预处理结果，将文本数据分割成多个层次的节点。每个节点可以包含子节点，形成树状结构。每个节点可以包含丰富的属性信息，如节点类型（段落、章节、标题等）、位置信息、内容等。这些属性信息有助于后续的处理和分析。
- 适用场景，适用于处理长文档和需要保留文本结构的场景。
    - 长文档处理：适用于处理长文档，如书籍、研究报告等。层次化结构可以帮助更好地组织和管理文档的逻辑结构。
    - 结构化数据：适用于需要保留文本结构的场景，例如目录、章节、段落等。层次化结构可以提高检索效率和数据的可解释性。

##### pipeline 处理流程过程的持久化处理
```python
# 持久化存储到本地硬盘，也可以用远程的 Redis 或 MongoDB 等存储 IngestionPipeline 的缓存
pipeline.persist("./pipeline_storage")

new_pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=300, chunk_overlap=100),
        TitleExtractor(),
    ],
)

# 加载缓存
new_pipeline.load("./pipeline_storage")

# 运行pipeline
nodes = new_pipeline.run(documents=documents)

```


#### 3. embedding 添加嵌入
llamaindex默认使用openAI的embedded模型，也可以使用本地模型。
通常在全局global的Settings 对象中指定嵌入模型，然后用于构建向量索引和查询。在pipline中输入文档将被分解成节点，嵌入模型将为每个节点生成一个嵌入embedded。
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings

# global default
Settings.embed_model = OpenAIEmbedding()

# 构建向量索引时使用指定的embedded模型
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents,embed_model=embed_model)

# 查询时，embedded模型将再次用于通过嵌入查询文本
query_engine = index.as_query_engine()
response = query_engine.query("query string")
```



















<b class="danger">待解决问题：使用sklearn和matplotlib将embedding后的向量信息降维后，用可视化的方式直观展示出来</b>
范例：https://www.bilibili.com/video/BV1Hk4y1X7aG/?spm_id_from=333.999.0.0&vd_source=32fa1c202efe5bb6942b35f0c043a7e9







<b class="danger">待解决问题：验证建立索引后，是否能通过索引找到文档</b>

<b class="danger">待解决问题：查看document和node的元数据都有什么</b>






#### 技巧：
- 针对持续更新的文档，用什么方法仅刷新有更新的文档，而不更新所有文档？
    - 对入库的文档设置一个唯一的id号，不同文档之间用唯一的id号区分，同时记录文档的大小，更新日期等，当以上信息变化后就需要重新入库embedding
- 多个文件检索，如何按照特定的文件名检索
    - 向量数据库中有个filter的概念，文档入库的时候可以指定metadata，在检索数据库的时候可以利用filter功能过滤只检索满足metadata条件的文档（比如只检索某个key对应value值的文档），即通过filter根据metadata的信息来限定检索文档的范围。

LlamaIndex SDK偏向于数据连接，即广义的基于RAG应用的各种工具支持。
















































---

## 6.Langchain
Langchain 更通用的大模型应用开发框架，提供基于大模型开发的各种工具支持。不同于Llamaindx，更专注于RAG应用。**Langchain是AGI软件工程的一个探索和原型 ，目前还没正式成为行业标准。**

### langchain的流程和基本架构
![alt text](./07-Langchain/langchain01.png)

### langchain的核心组件
1. 模型I/O封装
    - LLMS 模型
    - chatModel 基于llms的对话模型封装
    - prompt模板
    - outputparser 解析输出
    - #### OutputFixingParser (langchain的利用llm做格式自动纠错)
        大模型输出具有不确定性，不一定和预期的格式匹配，利用output parser可以自动修正输出格式，以方便后续处理。
        `new_output = OutputFixingParser.from_llm(parser=parser, llm=ChatOpenAI())`
    - #### function calling
        在定义的函数上面使用@tool装饰器，即可实现定义functioncalling。
2. 数据连接封装
    - document loaders 文档加载
    - document transformers 文档处理
    - text embedding 向量化
    - vectorstore 向量存储
    - retriever 向量检索
3. 对话历史管理
    - 对话历史存储，加载与**剪裁**
        - 对话历史不可能无限增长，从成本、可控性、推理效果来看，对话历史需要裁剪（**直接剪裁，或者筛选保留有关联的对话历史，即根据对话历史中与当前用户提问的相关程度进行排序**）。
        ``` python
        trim_messages(
            messages, #多轮消息
            max_token=45, #限制消息的长度
            strategy="last", #剪裁策略，从尾部开始裁剪，也可以从头部开始裁剪，也可以从中间开始裁剪。
            token_counter=ChatOpenAI(model="gpt-4o-mini"), #用于计算token数量的模型
            include_system=True, #是否包含system message，让模型更了解系统的背景信息
            allow_partial=True #是否允许部分裁剪，如果设置为True
            ，则即使无法完全满足max_token，也可以进行裁剪。
        )
        ```
        - 过滤带标识的历史记录。为每一轮的消息自定义两个标签，id和name，即**用这两个自定义的字段给每轮消息打标签**。然后使用filter_message来筛选消息历史，可以从三个字段筛选，按消息角色，按id标签，按name标签
        ```python
            filter_messages(
                messages, #多轮消息
                include_types=[HumanMessage,AIMessage], # 按角色类型，包含
                exclude_names=["example1","example2"], # 按name标签，不包含
                include_ids=["1","2"], #按id标签，包含
            )
        ```
    - 对话历史存储
        `RunnableWithMessageHistory`
        ```python
        def get_session_history(session_id):
            return SQLChatMessageHistory(session_id,"sqlite:///memory.db")
        
        runnable = model | StrOutputParser()

        runnable_with_history = RunnableWithMessageHistory(
            runnable, # 指定上面定义的runnable
            get_session_history, #指定自定义的历史管理方法
        )

        # 调用runnable_with_history
        runnable_with_history.invoke(
            [HumanMessage(content="你好")],
            # 指定自定义的配置参数在调用runnable_with_history时，获取指定session_id的历史记录
            config={"configurable":{"session_id":"123"}},
        )
        ```
        **通过使用 RunnableWithMessageHistory。每次调用（invoke）之后，新的对话消息会被自动存储和管理，而不是丢失。RunnableWithMessageHistory会自动存储每次调用的对话消息，包括用户的输入和模型的输出。** 默认存储在内存中。可以实现自定义的消息历史存储机制。
4. **架构封装**
    - #### <b class="danger">chain</b> LCEL(langchain expression language)
        链式调用，实现一个功能或一系列顺序功能的组合。LangChain Expression Language（LCEL）是一种声明式语言，可轻松组合不同的调用顺序构成 Chain。LCEL 自创立之初就被设计为能够支持将原型投入生产环境，无需代码更改，从最简单的“提示+LLM”链到最复杂的链（已有用户成功在生产环境中运行包含数百个步骤的 LCEL Chain）。
        LCEL支持，流，异步，并行，重试和回退，访问中间过程，输入输出模式，与langsmith集成，与langserve集成。**基于某个特定的任务可以定义一个完整的chain,然后开源发布到langchain hub上。**
        **chain和runnable两者概念相同**
        **基于工厂模式创建chain** 通过更改配置而不是改代码，来快速地调整链的配置。`configurable_alternatives` **可以对chain流程中的每个组件，比如模型，prompt，outputparser设置工厂模式**
        ```python
        # 通过configurable_alternatives 配置按指定字段选择模型
        model=gpt_model.configurable_alternatives(
            ConfigurableField(id="llm1"), #指定可配置的字段名叫llm1
            default_key='gpt', #如果不指定，则默认名称叫gpt的模型
            ernie=ernie_model, #当前指定的模型是文心一言的模型ernie_model
        )

        # 通过指定llm1 这个id来调整模型为claude
        ret=chain.with_config(configurable={"llm1":"claude"}).invoke('请自我介绍')
        ret=chain.with_config(configurable={"llm1":"gpt"}).invoke('请自我介绍') 
        ```
    - #### agent 
        根据用户输入自动规划执行步骤，自动选择每个步骤需要的工具，进而完成指定任务。
        ![](./07-Langchain/agent-overview.png)
5. callbacks模型调用封装
6. langserve 部署框架
langserve 部署后在127.0.0.1：9999/joke/playground/ 中会开启一个服务，可查看运行过程进行调试。


#### langchain的缺陷
langchain的流式调用无法中途停止。






<b class="danger">待解决问题</b>
<b class="danger">1.langchain中的function calling的过程</b>

<b class="info">技巧：</b>
<b class="info">1. 针对prompt，从代码中剥离出来，放在外部文件中以解耦管理。langchain中有PromptTemplate类可实现 </b>
<b class="info">2.langchain的多轮对话历史，存在redis缓存中，不建议存sql数据库中因为太慢，参考官方文档或者自己设计。常见成熟的方法是把对话历史存到向量数据库中，然后用RAG方式回传，因为对话历史比较多，历史对话中的每句话不一定跟当前的用户提问相关。</b>
<b class="info">3. 实际开发中，可以引用langchain sdk中的模型I/O封装模块，这部分的llms分装，prompt模板封装，结构化输出，输出错误校准，functioncalling都比较成熟</b>
<b class="info">4. 文档连接器这部分，可以引用llamaindex封装的模块</b>
<b class="info">5. 对于function calling，如果对于线上稳定性要求很高的服务场景，用prompt去控制大模型解析对话中的具体需求，然后根据解析的结果手工调function。**不要依赖大模型自身的function calling调用机制** </b> 



historyplaceholder
pydantic
openai指定输出格式的描述
输出格式自动修复
故障回退原理







设计模式：工厂模式，建造者模式
























---
## 7.LLM 运营维护SDK
大模型应用开发完成后，以云服务的形式给用户提供服务，需要一套机制记录用户的交互历史，交互行为以及大模型返回了什么结果，类似log日志系统监控记录整个流程。对于支撑这个**运维，测试，监控**的过程的SDK，有**langFuse、langsmith**


### 维护生产级的LLM应用，需要做哪些工作
1. 各类指标监控与统计，访问记录，响应时长，token用量，计费
2. 调试prompt
3. 测试验证系统的相关评估指标
4. 数据集管理（回归测试），验证模型经过升级开发后在相同的测试数据集上，模型的输出是否达到预期。
5. prompt模板管理（升级回滚）

langFuse:开源，SAAS服务免费（一定额度）/收费，langsmith平替，可集成langchain，也可集成其他框架
langSmith:非开源，SAAS服务免费（一定额度）/收费，**收费版支持私有部署**，只能与langchain集成。


<b class="info">技巧：</b>
<b class="info">1. 国产开源私有模型部署推荐deepseek，72B的千问2.5</b>












































---


# 预训练模型transformer,Bert的前世今生
博客配套视频链接: https://space.bilibili.com/383551518?spm_id_from=333.1007.0.0 
b 站直接看配套 github 链接：https://github.com/nickchen121/Pre-training-language-model
配套博客链接：https://www.cnblogs.com/nickchen121/p/15105048.html

## 1.预训练有什么用
机器学习：偏数学
深度学习（人工智能）的项目：大数据支持（主流）。

#### 预训练在图像领域的应用
通过一个已训练好的模型A，去完成一个小数据量的任务B（**使用了模型A的浅层参数**，即用到了**CNN**模型**浅层参数通用的特性**。
任务A和任务B是非常相似的，比如人脸识别，人脸识别任务B是识别人脸，人脸识别任务A是识别人脸的细节，比如眼睛，嘴巴，胡须，胡须的形状，胡须的粗细，胡须的浓淡等。

预训练的方式：
**冻结**，已训练好的浅层参数值不变，即浅层可以是通用的。
**微调**，浅层参数会跟着新任务的训练而改变

预训练怎么用：faiseq库,transformers库

## 2.统计语言模型（n元语言模型）
##### 语言模型
语言（人说的话）+模型（某个东西，完成某个任务）
语言模型最常见的两个任务：
- 计算一句话的概率，语言二分类，即某句话出现的概率（是或否）
- 计算下一个词可能是什么，即语言生成，根据上已知上文给出下一个词

##### 统计语言模型
统计的方法去解决以上两个任务（条件概率）：
- 对于语言二分类问题，先将一句话分词，然后使用概率的链式法则（概率论），来统计句子中每个词出现的概率，然后连乘就是这句话出现的概率。
- 对于语言生成问题，通过词库集合来反复计算符合条件（完形填空）的词的概率，然后取概率最大的词作为下一个词。这种方式的计算成本和时间是很大的，所以出现了把原句中的N个词，取2个词（2元），取3个词（3元），取N个词（n元）进行计算概率的方式即n元语言模型，这样降低计算成本。

如何进行N元计算
1.词性是动词
2.判断单词的词性
3.磁性很强的磁铁
4.北京的词性是名词

以上句子中，出现的字的次数是3，同时出现词性和的的次数是2，所以：
p(词性|的) = $\frac{count(词性,的)}{count(的)}$ = $\frac{2}{3}$

**平滑策略**，防止出现分子分母都是0的情况。


## 3.神经网络语言模型 transformer






















----
<span class="success">
    test asdfds adasf dfas 
</span>

<span class="alert danger">
    test asdfds adasf dfas 
</span>

<span class="alert info">
    test asdfds adasf dfas 
</span>


<span class="alert success">
    test asdfds adasf dfas 
</span>

<div class="alert warning">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>

<div class="alert asso">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>

<div class="alert doubt">python不区分单精度和双精度浮点
数，默认双精度，int也不细分short,long整型)
</div>