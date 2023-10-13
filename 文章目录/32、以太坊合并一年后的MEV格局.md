<!--StartFragment-->

以太坊合并的一整年以来，MEV-Boost的市占率稳居90%，这就是估值达10亿美金的Flashbots，如今的MEV复杂度极高，仅涉及非用户角色就有 Searcher，Builder，Relayer，Validator，Proposer 他们共同在这12秒的出块时间里多方势力错综交错互相博弈，只为谋求各自的最大收益。

本文试图对比MEV前后的利润率变化，梳理合并后MEV生命周期，并分享前沿问题的个人观点

笔者在之前的研究《[UniswapX协议解读](https://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484203\&idx=1\&sn=e728ad75369b5596217f628bb078ce84\&scene=21#wechat_redirect)》中，总结UniswapX的运作流程利润来源，便想完整刻画出MEV的具体收益率，毕竟这就是他所对抗并分红给用户的来源（本质上损失交易的实时性但换更好的兑换价格）。

所以近期笔者详细分析几种MEV类型和对比多个数据利润数据来源，来计算以太坊合并前后的MEV利润情况，完整推理过程见研报：[《以太坊合并一周年后 MEV 格局》](https://research.web3caff.com/zh/archives/11824?ref=shisi)，取部分数据结论如下：



## 1、**合并后MEV利润大幅下跌**

* 合并前一年，从MEV-Explore 算出平均利润为22MU/M（21年9月开始22年9月合并前结束，数值合并有Arbitrage和liquidation模式）
* 合并后一年，从Eigenphi算出平均利润为8.3MU/M（22年12月开始到23年9月底结束，数值合并了Arbitrage和Sandwich模式）

最终收益的变化结论是：

在上述数据的统计，剔除不应该归属于MEV的黑客事件后，整体收益率对比下降显著达62%。

注意由于MEV-Explore的统计其实是不涵盖三明治攻击的数据，又包含了liquidation的收益，所以如果只看纯Arbitrage对比可能下跌会更多。

补充说明：由于不同平台统计方法有差异（且均不含Cex的套利以及模式混杂），因此只能做宏观验证非绝对精确，另外有研报同样采用不同数据源对比了合并前后的收益，见附录link

是合并致使的链上MEV收益暴跌吗？这点需要从合并前后MEV流程出发




## **2、传统MEV模式**

其实MEV 一词很容易产生误导，因为大家会认为是矿工在提取这一价值。事实上，目前以太坊上的 MEV 主要是由 DeFi 交易者通过多种结构性套利交易策略捕获的，而矿工只是间接地从这些交易者的交易费用中获利。

这篇经典MEV入门文章[《Escaping the Dark Forest》 ](https://www.paradigm.xyz/2020/08/ethereum-is-a-dark-forest)，核心理念是链上存在很聪明的黑客不断挖掘合约的漏洞，但是当他们发现了漏洞又将陷入另一个矛盾，如何获取利润并且不被别人抢跑。

毕竟他的交易签名发送会进入以太坊内存池，公开传播，再借由矿工排序出块，这个过程可能只有3s或是几分钟，然而就这短短的几秒时间，签名的交易内容可以被无数的猎人盯上，重新模拟推演。

如果黑客是愚蠢的，直接执行获取利润的方式，就会被猎人高价抢跑。

如果黑客是聪明的，则可能会类似这篇文章的作者一样，采用合约套合约（即内部交易）的方式来隐藏自己最终能牟利的交易逻辑，可惜结局就不像那篇[《Escaping the Dark Forest》
  ](https://samczsun.com/escaping-the-dark-forest/),最终获得了成功，而是依旧被抢跑了。

这也意味着猎人们不仅分析链上交易父交易，也分析了每一笔子交易，进行模拟获利推演。甚至进一步检测了网关合约的部署逻辑并且同样复现了，而这竟然是在几秒内自动完成的。

### 所谓黑暗森林其实不只如此

笔者在之前测试BSC节点的时候，发现大量的游离节点他们只愿意接受P2P的链接，但是不主动传递TxPool的数据出来，并且从节点暴露的IP来看，甚至可以认为他们包围了BSC的主要核心出块节点。

动机上，这些占据了P2P的链接但是不给数据，只为在白名单内的节点互通，这样就可以变现用资源规模来提升MEV的利润率，因为BSC是标准3s一个区块，普通玩家看到的交易信息越晚，就也就越晚推演出合适MEV方案，并且当普通玩家发生MEV交易需要打包时，由于BSC是超级节点的模式，所以从延迟上会低于本身地理位置就包围了BSC的头部MEV玩家。

除了超级节点的包围，交易所的服务器也同样会被包围，毕竟CeFi和DeFi利差更大，乃至于交易所本身就是最大的套利机器人。十分类似早期web2抢票抢购的场景，黑灰产业会提前埋伏在服务器附近，并通过Dos攻击遏制普通用户的正常活动。

总之，虽然传统交易也有很多黑暗森林的隐形竞争，但相对是一个清晰的获利模式，这点在以太坊合并后，复杂的系统架构很快打破了传统MEV模式，并且头部效应越发显著。


## 3、**合并后的MEV模式**

以太坊合并是指其共识机制从POW转为POS的升级，最终的合并方案取舍的依据是最轻量级的复用了合并前以太坊的基础设施，而单独剥离了出块决策的共识模块。

对于 POS 每个块12 秒一次，而不是之前的波动值。区块挖矿奖励减少约 90% 从 2 ETH降至0.22 ETH。

这对MEV非常重要，有以下两点：

1、以太坊出块间隔变得稳定了。不再是之前3-30S相对离散随机的一个情况，这对MEV而言是优缺各半，虽然Searcher不用着急看到稍微有利润的交易，就直接发送出去，而是可以不断积蓄一个更好的交易总序列，在出块前交托给验证者，但也加剧了Searcher之间的竞争。

2、矿工激励降低，促使验证者更乐意接受MEV的交易拍卖，在短短的2-3月让MEV达到90%的市占率。



**3.1、**合并后交易的生命周期****

合并后，总计会涉及到Searcher、Builder、Relay、proposer、Validator这些角色，其中后两者属于POS中系统角色，而前三者属于MEV-boost，实现分离出块职责和出块排序。

* Searcher：搜索者，他们是各种内存池寻找有利可图的交易，通过编排交易序列组成局部序列Bundle交付给Builder。
* Builder：构建者，收集各式各样的Searcher发送的Bundle交易序列包，选择更有收益的交易序列，可以是多个捆绑包进行组合，也可能是自己重新构建。
* Relay：中继器，是中立设施，负责验证交易序列本身的有效性和重新计算收益，给出若干的区块序列包，最后让验证者选择打包。
* proposer和Validator：是合并后以太坊的Miner，会选取Relay给的最大利润交易序列组合完成出块工作，既可以获得共识奖励（区块奖励），也可以获得执行奖励（MEV+Tips）


![Untitled.png](https://img.learnblockchain.cn/attachments/2023/10/G1ZkD97f65295444dbe32.png)


综合这些角色，如今每个区块生命周期是：

1. 构建者通过从用户、搜索者或其他（私人或公共）订单流接收交易创建一个区块

2. 构建者将该区块提交给中继（即存在多个构建者）

3. 中继会验证块的有效性并计算它应该向出块者支付的金额

4. 中继向当前 slot 的出块者发送交易序列包和收益价格（亦是拍卖出价）

5. 出块者评估他们收到的所有出价，选择选择对自己最高收益的序列包

6. 出块者将此已签名标题发送回中继（即完成了本轮拍卖）

7. 发布区块后奖励通过区块内的交易和区块奖励分配给构建者和提议者。



## 4、**总结**

 **1） 合并对MEV的生态影响是什么？**

本文从合并前后的利润数据对比，到合并前后的交易上链出块MEV挖掘流程出发进行梳理，可以说MEV-Boost 的兴起，从根本上重塑了交易生命周期的模式，拆分出更精细的环节让各种参与者产生博弈，搜索者做不好最新策略的研究就会毫无收益，做得好就可以逐步扩大利润成为构建者。

抛开链上交易量的萎缩，Searchers和Builders之间处于高度内部竞争的情况，因为在系统结构上他们互相能替代，但最终都会以订单流为王，Searchers会希望逐步扩大自己的利润率，就需要他的私有订单量够大（最终构建的区块利润够高），也就逐渐成为Builder的角色。

比如在Curve因为编译器漏洞致使重入保护失效的攻击事件中，甚至出现单笔交易的手续费达到**570 ETH**，这是以太坊历史上第二高手续费的MEV 交易，竞争态势可见一斑。

虽然MEV并不是以太坊合并本身要解决的问题，但系统的博弈对抗的提升结合多少环境因素，最终让目前MEV的总利润率降低，这里，并不代表MEV的涉及金额降低了，而是利润率降低意味着[更多收益流向了验证者们](https://writings.flashbots.net/open-sourcing-the-flashbots-builder)，对用户而言倒是好事，利润低会降低一些链上交易攻击的动机。

**2）还有哪些最前沿围绕MEV进行中的探索点？**


* 从隐私交易出发：有阈值加密 Threshold Encryption和延迟加密 Delayed Encryption以及SGX 加密，基本都是从加密交易信息，对解密条件进行要求，或是时间锁或是多签或是可信硬件的模式
* 从公平交易出发：有公平排序 FSS和订单流拍卖的MEV Auction 以及MEV-Share，Mev-Blocker等，差别在于从完全无利润到分享利润到权衡利润，即由用户来决定用怎样的成本来获取交易的相对公平性。
* 协议级完善PBS，目前PBS实际上是以太坊基金会提案，但实现借助MEV-boost达成了分离，未来对于这样核心机制会转为以太坊本身的协议机制。

**3）面对OFAC的审查以太坊有抵抗力吗？**

随着加密货币行业的成熟，监管是不可避免的，所有在美国注册成立的实体及其运营以太坊 POS 验证器的机构都应符合 OFAC 要求，但是区块链的系统机制注定了他不会只在美国存在，只要有其他符合当地政策的中继就可以确保在某个契机可以上链传播。

即使超过90%的Validator都通过MEV来审查中继路由的交易，那些抗审查的交易仍然能够在一个小时内上链，所以只要不是100%就等于0%

 **4）缺乏激励的中继器具有可持续性吗？**

这目前看是个隐形问题，没有利润还要维持复杂的中继服务，最终会导致强中心化的转变，近期Blocknative也停止MEV-boost中继服务，以太坊未来超90%区块结算将掌握在4家公司手中。可以说现在的MEV-Boost中继是100%的风险却是0%的回报，由于中继有会汇聚各个Builder上报的txs，作为数据的聚集地，或许会通过MEV-share和MEV Auction等逐步完善的系统获得收益，比如直接接收用户的隐私交易请求。曾经地图软件APP也是困于此类服务，作为公关物品不可能以会员的模式收费，但在接入曝光排序广告，接入多元打车服务的试点模式下也依旧活的很好，总之，有流量有用户有公平，就不会毫无收益。

 **5）ERC4337捆绑交易在MEV下会如何影响？**

目前已经有超过 68.7 万个 AA（账户抽象）钱包，超过 200 万次用户操作（UserOps），整体趋势相对于过往缓慢的CA钱包增长量而言，算爆发性增长了。ERC-4337有复杂的运作机制，，尤其是交易签名的传播并不共用以太坊本身的内存池，虽然初期会加大MEV的难度，但长期看不可阻挡。

可拓展阅读之前研报：[《账户抽象方案 ERC-4337 最新过审方案研究报告》](https://research.web3caff.com/zh/archives/6900?ref=shisi)

 **6）面对MEV的威胁DeFi可以追赶CeFi吗？**

虽然目前很多方案都是从体验上让DeFi更顺滑，比如借助元交易或者跨链Swap或者ERC-4337来降低用户必须有手续费才能执行交易的限制，或者通过合约钱包多元自定义的功能来提升账号安全性（分层、分级、社交回复），在笔者看来，无论怎样追赶CeFi总有特有的无可比拟的优势，从速度到体验，但DeFi也有独特优势同样也是CeFi无可比拟的，各有各自的受众群体，也就各有发展周期。

**7）Layer-2 中的 MEV现状如何？**

在Optimism 存在着一个独有的叫做序列器（Sequencer）的模块，用来生成保证交易执行和排序的已签名收据。序列器将由一组检验者进行检查有罚没权限吗，并且使用 MEVA（MEV Auction）方案，通过拍卖过程选取唯一的序列器。

在Arbitrum在序列器结构上，Arbitrum 使用 Chainlink 开发的 FSS（Fair Sequencing Services）方案决定顺序。

以上方式都在一定幅度上借助L2的特殊性消除了来自于矿工的 MEV，但不与以太坊主网互通的侧链则依旧存在MEV的机会，比如BSC，BASE等

最后，本文系1/3节选，还有涉及数据以及结论推理可见完整研报：[《以太坊合并一周年后 MEV 格局万字研报：面向高复杂博弈对抗之下，受益者链条正如何呈现？》](https://research.web3caff.com/zh/archives/11824?ref=shisi)



> *附录*
> 
> *https\://github.com/flashbots/mev-research/blob/main/resources.md*
> 
> *https\://web3caff.com/zh/archives/60550*
> 
> *https\://web3caff.com/zh/archives/61086*
> 
> *https\://collective.flashbots.net/t/merge-anniversary-a-year-in-review/2400*
> 
> *https\://docs.google.com/spreadsheets/d/1POtuj3DtF3A-uwm4MtKvwNYtnl_PW6DPUYj6x7yJUIs/edit#gid=1299175463*
> 
> *https\://hackmd.io/@flashbots/mev-in-eth2*
> 
> *https\://frontier.tech/the-orderflow-auction-design-space*
> 
> *https\://web3caff.com/zh/archives/54535*




###

### **【十四君-原创回顾】**

* [从UniSwapX和AA出发冷静看待意图为中心的落地挑战](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484213\&idx=1\&sn=2d4810c3a53adc39adfe502984c6d1a5\&chksm=e83aa4efdf4d2df976204f4457fbc7677cd31524c2e8668f48abb9eab024f77fba88ff6c38ff\&scene=21#wechat_redirect)\


* [UniswapX研报(上)：总结V1-3发展链路，解读下一代 DEX的原理创新与挑战](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484203\&idx=1\&sn=e728ad75369b5596217f628bb078ce84\&chksm=e83aa4f1df4d2de792c693397012f222f60de23a473b9377c33a2edff4ed547ad0544b59c0c7\&scene=21#wechat_redirect)\


* [NFT即钱包的ERC-6551 真有那么神奇吗？](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484191\&idx=1\&sn=57da23bd8ef33337cf3c0d6038cce826\&chksm=e83aa4c5df4d2dd3be0427a9cd7e7e8ea64ab16df4a9be43444ddbff97cadd6f01a868ca3d3b\&scene=21#wechat_redirect)

* [深入EVM-合约分类这件小事背后的风险](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484184\&idx=1\&sn=d35568df26fcc0846171556094b60ea9\&chksm=e83aa4c2df4d2dd438e3d9d336e5964380a8ba05a64de9acd92895c2a5d4ae71bc182643928b\&scene=21#wechat_redirect)

* [用一个小时讲清楚账号抽象这件事](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484171\&idx=1\&sn=3b5635fa84742e21cd6ca47e60ec1d6b\&chksm=e83aa4d1df4d2dc73a690e49477f27726f81335995b7bb9343d412211223b278ce2f67466276\&scene=21#wechat_redirect)

* [解读比特币Oridinals协议与BRC20标准 原理创新与局限](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484156\&idx=1\&sn=cefc374edbe3478817fe2e864ed85649\&chksm=e83aa526df4d2c30addb352b2fd9cf1af4c24a6a1e25c04bf0c8790702a664ab1c0370bf0037\&scene=21#wechat_redirect)

* [跨链赛道研报：LayerZero全链互操作协议凭什么估值30亿美金(上）](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484151\&idx=1\&sn=345fb4a3ae6efbe52606fe2af4b85a3e\&chksm=e83aa52ddf4d2c3bd84d1ddfefdfc3a1a06a8274dbd28f43cea205202364acd2a15e63231edc\&scene=21#wechat_redirect)




可后台留言作者，探讨web3行业问题

点赞关注，十四用技术视角带给你价值

周更博主，推荐加星标减少漏过最新原创观点！

<!--EndFragment-->
