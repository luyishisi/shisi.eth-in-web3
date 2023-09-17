<!--StartFragment-->

最近，在 Web3 知名风投 Paradigm 的《Intent-Based Architectures and Their Risks》文章中， “以意图为中心的（Intent-centric）的协议及基础设施” 位居十个加密领域的首位趋势，结合在巴黎ETHCC大会上Bob the Solver项目和Anomo、DappOs 数年的沉淀与探索。引发了行业对于 Intent-centric 架构以及该赛道的重点关注，其核心目标立足于大幅提升用户体验，完全隐去繁杂的交易细节，所以被视为促成 Web3 普及的新引擎。

笔者亦这次Token2049的黑客松比赛中，与AstroX钱包技术团队(ToB端服务侧重高ROI增长的产品），一起实现了基于intent理念的DeFi赛道第二名项目：Ethtent。本文将从自身实现Solver的历程以及两大落地中的应用ERC4337和UniSwapX出发聊聊 Intent-centric 。

探究"intent"是什么？可以如此美好吗？有怎样的应用？落地的挑战是什么？

### 1、回顾Intent-centric 是什么？

正如账号抽象的概念甚至远于以太坊本身的开发，其实最早具体的 “意图”的理念可追溯至 18 年 DEX Wyvern Protocol 在介绍其设计理念中。其理念的核心点在于，与传统交易的侧重点不同，对普通用户而言，一直追求的其实是结果的一致性和准确性，并不是执行过程的严丝合缝。

假定一个场景，我要完成某Token的swap。

* 在传统交易：得先进行3笔交易，转入eth作为gas，给与approve授权交易，再提交swap交易
* 在意图交易：只需用户签名，我愿意用X个Token尽量快且多的换到YToken，可以给1%的手续费

我们可以将以“意图”为中心的协议理解为是一组经过签名的合约，允许用户将交易的过程外包给第三方，而不会放弃对交易的完全控制。

**用户只需明确想要干什么的意图，一个签名就能完成所有操作。**

即交易 = 你具体要如何做；意图 = 你制定你想要什么，但不必关心如何实现它。




类比于传统互联网的发展历程，本身也是有同样的经历，从服务商有什么卖什么转换到用户需要什么来撮合什么，再到智能化的服务平台，回顾20多年互联网兴衰演变其核心的脉络是

1. 早期的垂直服务（各类门户入口，用户自己来查号码找工人买服务）

2. 中期的服务聚合平台（58同城等，通过聚合流量撮合服务商与用户需求）

3. 后期的智能化平台（结合算法匹配推荐，提升意图准度，如滴滴跨城顺风车，定制化服务）

   


可以说 Intent-centric 的确实理念很美好，且web2的发展历程也验证了这是扩大用户量的关键路径，那么真的可以如此美好吗？让我们先从市场应用情况出发。

## 2、Intent-centric 的典型应用

尽管以意图为中心的概念刚刚被提出，但涉及的项目数量已不再少数，或者说很多落地中的项目本身的立意也是以用户意图为中心。在Bastian Wetzel 的这篇文章中\<Intent-Based Architectures and Projects Experimenting with Them> ，亦归类了各种主流项目。

下图中可以看出，很多协议其实并非属于通用意图解决方案，而是特定意图解决方案，比如uniswap、Seaport，这点对比web2做得好垂类解决方案也是意图为中心的必经发展之路。

而ERC-4337则是协助意图的一个基础设施，由于bundler的存在降低了对用户原有gas的必要性。

![Untitled.png](https://img.learnblockchain.cn/attachments/2023/09/u3f2Bwo26506ec61a734e.png)
 但是我们的核心目标也还是探究这些项目的商业模式，是否足够支撑起intent的落地。笔者看来目前跑在落地最前沿的即是UniswapX围绕交易的意图实现，以及ERC4337将会作为意图的必要基础设施。

### 2.1 从UniSwapX的经济设计看intent-centric

笔者在UniSwapX官宣后即作为Filler和参与作为报价员参与RFQ系统，之所以说他是最前沿可落地的Intent之一，关键在于他是最成熟的最直接解决了意图的对手方经济激励问题的系统。

#### 2.1.1、为什么要有UniSwapX ？

总结uniswapV1-3的发展，可以说在过往Amm协议都面临了用户成本、成交价格、交易链路、路由服务、LP 激励等等具体的问题。如今 Swap 的市场情况可以说 MEV 完全包围了链上的内存池，每一笔大规模的 Swap 都几乎面临着被夹。用户总是以最差的价格成交，其中的利润被MEV分走。

而UniswapX 的推出便是通过彻底改变了 AMM 成交机制的方法来从另一种维度尝试降维打击解决上述问题。

拓展阅读 ：[UniswapX研报(上)：总结V1-3发展链路，解读下一代 DEX的原理创新与挑战](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484203\&idx=1\&sn=e728ad75369b5596217f628bb078ce84\&chksm=e83aa4f1df4d2de792c693397012f222f60de23a473b9377c33a2edff4ed547ad0544b59c0c7\&scene=21#wechat_redirect)

#### 2.1.2、UniSwapX是什么？

从定义来说：UniswapX 是一种新的无需许可、开源 (GPL)、基于拍卖的路由协议，用于跨 AMM 和其他流动性来源进行交易。

其实对于 Web3 的交易市场运作模型，大体上是三类，除了AMM模式外还有

* 链上撮合链上成交的订单簿模式。拓展阅读：《[【合约解读】CryptoPunk 世界上最早的去中心化 NFT 交易市场](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247483924\&idx=1\&sn=30a642fa1acec069e31b40937e2d7de4\&chksm=e83aa5cedf4d2cd861d3cf09c555720d7e6b89febb909ee88853d88f86ca913d3a1d701c1c00\&scene=21#wechat_redirect)》
* 链下撮合链上成交的订单簿模式。拓展阅读：《[X2Y2 NFT Market 系统运转架构](https://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247483957\&idx=1\&sn=ab8e4bfe0068fc19dccbb8b00d358541\&scene=21#wechat_redirect)》

UniswapX 便是从 改变了UniswapV1-3的 AMM 模式 转变为了链下撮合链上成交的订单簿模式。

### **2.1.3、UniSwapX 如何运作？**

从**用户端视角看，假如场景是**用户希望以 1900 左右的价格（允许 2% 的滑点）进行 ETH<=> 和 USDT 的交易，只需要：

1. 选择订单，价格衰退曲线限制订单时限（如 1 天内从 1950U 兑换 1ETH ，最低为 1850U ）
2. 签名订单，并发布到订单簿的服务集群中。
3. 等待交易，需由 Filler 发现并完成成交

对于用户而言，要做的仅此而已。

从**Fillers 端视角看，他是**主动完成用户交易订单的人。是有着充裕资金，熟练信息跨链服务，并且构建有全链全 DexPool 状态监控的 服务商，他要

1. 扫描链上各协议的 Pool，构建实时订单计算所需的基础数据
2. 扫描 Mempool，预估后续的价格变化趋势
3. 扫描 RFQ Fillers 专用网络，通过提供报价获取到优先成交权。
4. 扫描 Fillers 公开网络的订单信息，分析最优成交链路
5. 满足营收条件，则参与竞价（这里的每一分钟都需要争取，荷拍的模式下越晚上链则结束价格越低）
6. 分析其他 Fillers 的竞价底线，寻找在下一次有收益的订单中优先他们竞价（哪怕因此我的单笔收益会减少但会获得更多单量）

那为什么他有这样成交的动机呢？这就回到了uniswapX的经济模型上。

#### 2.1.4、如何评价UniswapX的意图设计

解决意图本身的发布意愿是关键的落地问题。

曾经 DEX 面对 CEX 的很多局限性，比如交易成本，MEV，滑点磨损，无常损失等等，未来都将通过更专业的 Filler 群体来与 MEV 群体进行对抗，在技术竞争中逐步啃下一块肉，并最后回归到用户手里，形成发展的正循环（更多用户使用 UniswapX，更多的 Filler 有手续费分红）。

并且，链上交易拆单路由的复杂性也将分散到后端系统中，用户只需要作为甲方提出订单，而不需要去思考这样麻烦路由的问题。

所以这是一个良性的经济循环，双方都有收益，经济模型是良性就总会落地到实处。


![Untitled (1).png](https://img.learnblockchain.cn/attachments/2023/09/WZPJLlq56506e933e20ad.png)

 拓展阅读：https\://research.web3caff.com/zh/archives/10004?ref=shisi

### **2.2 从ERC4337看intent-centric**

在上文的应用图中，最下方即是围绕账号抽象AA的板块，对于uniswapX这样的系统而言，由于交易本身是Fillers提交，所以对于用户而言，本身就是可以完成无需gas的跨链交易。

但是要在整个交易周期里，用户还是需要先提交一笔`approve`交易去许可uniswapX的链上合约可以代扣用户金额，如果真想纯意图的交易模式（完全无需用户发起交易），就还是需要ERC4337作为账号主体以及paymaster的整合设计。

关于ERC4337是什么、实现原理、发展历程等，十四君在过往有过直播和总结，拓展阅读：[用一个小时讲清楚账号抽象这件事](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484171\&idx=1\&sn=3b5635fa84742e21cd6ca47e60ec1d6b\&chksm=e83aa4d1df4d2dc73a690e49477f27726f81335995b7bb9343d412211223b278ce2f67466276\&scene=21#wechat_redirect) 

简单来说，ERC4337是套基础设施

* 链上通过`entryPoint`合约来验证用户的签名以鉴权，最终驱动用户的CA账号作为身份主体
* 链下通过用户签署`UserOperation`作为指令，传递在`Bundlers`网络，由`Bundler`批量打包上链执行。

这套机制的优化核心是可通过CA的高度定制能力提升局部功能，比如社交恢复钱包、或者项目方帮用户垫付 Gas 费、支持USDT等作为Gas支付方式等功能

但是今儿我们则是从商业模式角度，来分析4337对intent的价值。

回溯到我们看UniswapX 之所以认为他的商业模式好，是因为Token成交的双方（用户与fillder）都会因此收益，只有mev是损失的一方。但回过头来看，通过手续费确保成交对手方的利润和意愿，其实只是商业模式的一种，而未来大部分的 “意图” 应用走的模式会是直接 To B 做收入或者主产品 To C 拿书续费，但主产品的服务不只有满足 “意图” 的服务。

就像是作为支付系统，微信支付或者支付宝等，不会在C2C的流水中收费，但是一般会在商家支付提走资金时候收取0.6%的手续费（亦需要给给底层交易系统付费）。

在过去十年的移动互联大战中，基本也都是做高用户量为目标，收益的闭环可以放在用户基数之后。

所以未来会有更多的Dapp出现，且为了用户能够体验和使用其Dapp，会乐于为用户提供免Gas的服务器，就类似Lens 社交协议，在polygon上会为了培养用户的使用和内容生态，先行为用户每周数十万刀的垫付手续费，而这，在曾经打车大战每天消耗上千万的补贴成本对比之下，还只是毛毛雨而已。

那么最符合标准，最通用的代付机制，最值得信任的平台信用体系，就必然会是在ERC4337上的`paymaster`系统（源于元交易但超于元交易）。

他是一种特殊的智能合约账户，可以为其他人支付 Gas 费。付款主合同需要对每笔交易进行某种验证逻辑，并在交易进行时进行检查。`Paymaster`合约可以在“`v``alidatePaymasterUserOp`”方法中检查是否有足够的已批准的ERC-20余额，然后在“`postOp`”调用中使用“transferFrom”提取它。（具体执行逻辑解读可参考上文拓展阅读里的b站直播录屏）

总之，这是一套比起元交易更为通用的免Gas方案，即不存在非标的混乱，也没有向前兼容性问题（元交易需要合约的改动支持）

## 3、Intent落地的挑战有什么？

综上所述，意图确实很美好，意图也必然是持续发展和优化的方向，抛开商业模式的挑战之外，还有那些技术细节是其落地的核心难题呢？

### 3.1、与AI结合的矛盾点

虽然不少intent的分析观点会认为AI提供的交易意图解析能力是体验的优化点，但笔者曾经从事过安全策略行业，期间一大感悟就是，可解释性和可还原性是AI在策略场景应用的最重要环节，例如封号，如果无法提供准确的策略命中原因，则一旦用户发起投诉就很难自圆其说。同样的，对于任何金融系统而言，追求稳定一致性是第一要务，任何机构都无法保证 AI 在掌握资产权限后不会作恶。

所以AI在长时间内都只能作为意图解析的辅助性工具，并且链上数据解析需要对区块链运作原理层面的深刻理解，否则极易出现误报。

可拓展阅读：[深入EVM-合约分类这件小事背后的风险](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484184\&idx=1\&sn=d35568df26fcc0846171556094b60ea9\&chksm=e83aa4c2df4d2dd438e3d9d336e5964380a8ba05a64de9acd92895c2a5d4ae71bc182643928b\&scene=21#wechat_redirect)

### 3.2、intentPool 的抗Dos风险与Solver匹配问题

对于IntentPool类似于ERC4337的内存池，也将会是一大卡点。首先intentPool无法复用目前以太坊客户端（Geth，Eirgon）等的MemPool内存池机制，必须单独自建出intentPool。

即使有ERC4337的BundlerPool作为参考，但MemPool设计都有各自优缺

* 去中心化的内存池模式：存在传播机理问题，因为对于许多应用程序来说，执行意图是一项有利可图的活动。因此，操作意图池的节点有动力不传播，以减少执行意图时的竞争。
* 中心化的内存池模式：解决了传播机制问题，但无法避免中心化审计和干预问题。

总之，**设计一种既兼容激励又不集中的意图发现和匹配机制并非易事。**

### 3.3、意图隐私性风险

签名具有不可撤销特性，即使在签名内容里加上过期时间，也存在此过期时间之前无法低成本取消签名的问题（凡是取消都必须发交易上链）。

所以目前也涌现出一些试图解决意愿的标准性、隐私性的通用意图方案如Anomo。

隐私性的保护很难通过EVM系统得到实现，所以目前更前沿还有围绕新型隐私保护意图语言的开发在开发，比如juvix，用于创建注重隐私的去中心化应用程序。它可以编译为 WASM，或者通过VampIR编译为电路，以便在Anoma或以太坊上使用Taiga进行私有执行。

## 4、总结

其实看到Intent的概念火热起来，还是很值得高兴的，终于web3开始不在那么闭目自嗨，开始为真正用户普及的卡点尝试破局之道了，只有围绕用户最实际的需求出发，而不是陶醉于高大上的叙事嗨点，放下身段贴心服务，才能赢得广度用户的逐步青睐。

未来的Intent的模式上要么是类似UniswapX从手续费上创造营收补贴对手方的意愿，要么从整体系统用户分级的角度，少量付费高客单价用户和大量不付费但是重要生态构成的用户。

所以，意图这件事，本身就是在优化产品本身的体验，而不是为了意图而意图。

并且，DeFi 也将是Intent绽放的第一舞台，已经有 20 余个 DeFi 协议与 DappOS 合作，其次是 Brink Trade 开发出了意图引擎（Intent Engine），可以将 Bridge、Swap 和 Transfer 等操作都可以通过一次签署包含在一个意图内。此外，CowSwap、1inch、Uniswap、LlamaSwap 等老牌协议也在不断扩充自己的功能以满足用户的更多意图。

在本次Token2049的黑客松比赛里，笔者参与的亦是从DeFi赛道，解决了一个跨链Swap+策略辅助定投场景的Intent solver（Ethtent系统运作如下图）。

![Untitled (2).png](https://img.learnblockchain.cn/attachments/2023/09/bdlu8p2z6506e8b766158.png)

也不禁感慨，其实在现有EVM的基础设施上，实现固定需求的垂类的意图并不难，真正困难的是在未来能出现intent solver 的market或者称之为协作标准的协作框架，如何让不同的solver进一步组合、复用实现通用标准化的意图解决方案，还能调配经济模式解决双方意愿。

标准化这件事，往往需要自上而下的标准定义，目前看DappOs和Anomo都走在这条路的前沿上，值得期待。

> *附录*
> 
> *《Intent-Centric 赛道万字研报“以意图为中心” 架构能否成为 Web3 大规模采用新引擎？ 》*
> 
> *https\://research.web3caff.com/zh/archives/11091#comment-1393?ref=shisi*
> 
> *https\://github.com/neeboo/ethtent*
> 
> *https\://www\.paradigm.xyz/2023/06/intents#the-middlemen--their-mempools*
> 
> *https\://www\.xiaoyuzhoufm.com/episode/64eca0013fa4090b747de18f*
> 
> *https\://bwetzel.medium.com/intent-based-architectures-and-projects-experimenting-with-them-c3ee63ae24c*

###

### **【十四君-原创回顾】**

* [UniswapX研报(上)：总结V1-3发展链路，解读下一代 DEX的原理创新与挑战](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484203\&idx=1\&sn=e728ad75369b5596217f628bb078ce84\&chksm=e83aa4f1df4d2de792c693397012f222f60de23a473b9377c33a2edff4ed547ad0544b59c0c7\&scene=21#wechat_redirect)\


* [NFT即钱包的ERC-6551 真有那么神奇吗？](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484191\&idx=1\&sn=57da23bd8ef33337cf3c0d6038cce826\&chksm=e83aa4c5df4d2dd3be0427a9cd7e7e8ea64ab16df4a9be43444ddbff97cadd6f01a868ca3d3b\&scene=21#wechat_redirect)

* [深入EVM-合约分类这件小事背后的风险](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484184\&idx=1\&sn=d35568df26fcc0846171556094b60ea9\&chksm=e83aa4c2df4d2dd438e3d9d336e5964380a8ba05a64de9acd92895c2a5d4ae71bc182643928b\&scene=21#wechat_redirect)

* [用一个小时讲清楚账号抽象这件事](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484171\&idx=1\&sn=3b5635fa84742e21cd6ca47e60ec1d6b\&chksm=e83aa4d1df4d2dc73a690e49477f27726f81335995b7bb9343d412211223b278ce2f67466276\&scene=21#wechat_redirect)

* [解读比特币Oridinals协议与BRC20标准 原理创新与局限](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484156\&idx=1\&sn=cefc374edbe3478817fe2e864ed85649\&chksm=e83aa526df4d2c30addb352b2fd9cf1af4c24a6a1e25c04bf0c8790702a664ab1c0370bf0037\&scene=21#wechat_redirect)

* [跨链赛道研报：LayerZero全链互操作协议凭什么估值30亿美金(上）](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484151\&idx=1\&sn=345fb4a3ae6efbe52606fe2af4b85a3e\&chksm=e83aa52ddf4d2c3bd84d1ddfefdfc3a1a06a8274dbd28f43cea205202364acd2a15e63231edc\&scene=21#wechat_redirect)




可后台留言作者，探讨web3行业问题

点赞关注，十四用技术视角带给你价值

周更博主，推荐加星标减少漏过最新原创观点！


![Untitled (3).png](https://img.learnblockchain.cn/attachments/2023/09/Jh7L2goO6506e897a7fba.png)



<!--EndFragment-->
