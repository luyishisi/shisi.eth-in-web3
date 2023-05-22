<!--StartFragment-->

“The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.”

——比特币创世区块



最近BTC上手续费区块收入占比最高到74%，大约4.85 BTC手续费，而仅仅两个月前才2%左右，源于数个百倍币的诞生以及大众fomo的情绪，让BRC20的市场迎来爆发，5月7日 Bitcoin 网络上有超过 40 万笔交易待确认，虽然他和我们熟知的ERC20虽然都被称为代币标准，但是实现的机制原理差异巨大，本文将从技术视角尝试解读其实现以及价值。



* ***

## **1、Ordinals协议的核心思想**
### **1.1、概述**

每一枚比特币都是由一亿个「聪（Satoshis）」构成 (1 btc = 10^8 sat)，这些sat每一个都有唯一标识且无法分割。

1、根据比特币里面sat的「序数（ordinal）」，

2、赋予每一个聪特定的含义「Inscriptions（铭刻）」

这就是Ordinals协议。


![Untitled.png](https://img.learnblockchain.cn/attachments/2023/05/89gWJQSK646b1bf3c25c4.png)


## **2、**聪是如何编号的？****

他借由比特币独特的出块流程和UTXO模型，从而让每一个「**聪（sat）**」具有独特的编号。

比特币是在「**挖矿**」中产生的，挖矿过程是矿工通过解决复杂的数学问题（POW）获得出块权，来验证新交易并添加到区块链中，比特币网络每10分钟左右会生成一个新的区块，每个区块包含一组新的交易和之前区块的哈希值，其中矿工的收益又被称为**Coinbase区块**

在以太坊中采用“账户余额模型”，即每个地址有单独的存储结构和空间余额（balance）便是其中的一个字段。

这种模型的优点是：

* 简单，非常容易理解和编码实现。
* 高效，每笔交易只需要验证发送账户是否有足够的余额来支付交易；

缺点：会出现双重支出攻击。

可拓展阅读：[【前沿解读】斯坦福研究员论文-以太坊可逆交易标准ERC20/721R的机制、创新与局限](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247483981\&idx=1\&sn=376c2d0b9b28aff74af74926bf4891de\&chksm=e83aa597df4d2c818850eb3b6f47a7d02bc54a8342d8ba05852dec07e5ce96c5fe7ad97993e4\&scene=21#wechat_redirect)\



![Untitled (1).png](https://img.learnblockchain.cn/attachments/2023/05/3PJbFZDa646b1c0726abe.png)

但是比特币网络不同，他账户的余额并不是由一个数字表明，而是由当前区块链网络中所有跟当前账户有关的UTXO（未花费的交易输出）组成。




### **2.1、比特币的 UTXO 模型**

UTXO（Unspent Transaction Output）是一种账本模型，在比特币系统中，每一笔交易都会产生一些输出，比如转账交易的输出就是接收方的比特币地址和转账金额。这些输出被存储在 UTXO 集合中，用于记录未花费的交易输出。

每一笔交易都由若干个输入（Input） 和若干个 输出（Output） 构成。每一笔交易都要花费一笔输入，产生一笔输出，而其所产生的输出，就是“未花费过的交易输出”；一个Input指向的是前面区块的某个Output，只有Coinbase交易没有输入，只有凭空输出。

UTXO 模型的优点是更加安全和隐私保护，因为它没有中心化的账户记录和传统账户模型可能泄露的账户余额信息。

UTXO 模型的缺点是增加了交易的验证成本和存储成本。每次交易时都需要验证交易的支付和接收是否合法，同时也需要存储大量的 UTXO 信息。

所以任何交易，**总是可以由Input溯源到Coinbase交易 继而追溯每一个聪被挖矿挖出时的序号。**

![Untitled (2).png](https://img.learnblockchain.cn/attachments/2023/05/LYbnNX7c646b1c13ee643.png)

所以我们说自己有多少比特币（bitcoin）实际上是指的我们拥有所有权的那些UTXO中所指明的比特币（bitcoin）的数量，因此如果我们想要统计一个地址的BTC数量:

1. 从创始块开始扫描；
2. 遇到某笔交易的某个output是指定的地址，余额增加；
3. 遇到某笔交易的某个input是指定的地址，余额减少；



### **2.2、sat和UTXO的关系**

注意是每一个sat不是UTXO! 由于UTXO是不可再分的最小交易单元，因此sat只能存在于UTXO中，且UTXO包含了一定范围的sats，且只能在花费某一UTXO后产生新的输出中对sats编号进行拆分

比如我在创世块或者CoinBase区块获得了50个BTC的奖励，对应的Input和Output则是


```
### inputs //为空
### outputs ：addr_a:[0 -> 4,999,999,999] sats

```

如果我进行一笔20BTC的转账给B地址，则UTXO集中会呈现，这里的input是上一笔的output

```
### inputs"
addrA: [0 -> 4,999,999,999] sats
### outputs# 30 btc to addrA, index=0
addrA: [0 -> 2,999,999,999] sats
# 20 btc to addrB, index=1
addrB: [3,000,000,000 -> 4,999,999,999] sats
```

这里的sats消耗顺序，是基于FIFO"先进先出"（First-In-First-Out ）原则，在交易费用相同的情况下，较早的UTXO将比较晚的UTXO更优先被用于交易。

这些就是Ordinal NFT的核心技术支撑，非常的简洁但是却能衍生出很多好玩的东西! 这个Ordinal Number甚至可以用来表示域名等。



### **2.3、Ordinal number的表示方法**

Ordinal Number则有很多种表示方式，比如度数表示法(Degree Notation)

```
A°B′C″D‴
│ │ │ ╰─ Index of sat in the block(每10分钟一个块)
│ │ ╰─── Index of block in difficulty adjustment period(每2016个块调整一次，~2周)
│ ╰───── Index of block in halving epoch(每210,000个块减半，~4年一次)
╰─────── Cycle, numbered starting from 0(减半和难度调整时间重合，~24年一次)
```

这种表示法有趣的地方在于，它根据比特币自身的周期性特征，人为地为sat创造了一种稀缺性：

* common: 所有不是区块mint出的第一个sat的sats
* uncommon: 该sat是某区块挖出的第一个sat(D==0)
* rare: 难度调整时挖出的第一个sat(C==0&\&D==0)
* epic: 减半时挖出的第一个sat(B==0&\&D==0)
* legendary: 发生Cycle轮换时挖出的第一个sat(B==C==D==0)
* mythic: 创世区块挖出的第一个sat(A==B==C==D==0)

比如：https\://ordinals.com/sat/1°0′0″0‴ ，所以目前产生Fomo追逐的核心点并非是mint的内容中包含什么东西，而是对应的Ordinal Number这样的序号值。

如果说序号是结合了比特币原生的诸多技术特性产生的，那么铭刻（Inscriptions）则是注入sat具体内容的方法，所以问题便来到，有了唯一标识的sat如何定义其绑定的任意内容呢？



## **3、如何Inscriptions（铭刻）任意内容**

在讨论铭刻之前，咱们先了解下比特币扩容的两次重大升级：SegWit 和Taproot


### **3.1、SegWit（隔离见证）**

他是比特币的一个重大升级于2017年8月激活，主要目的是优化比特币的交易处理能力、降低交易费用，并在更安全的条件下实现比特币的扩容。SegWit 是一个软分叉（Soft Fork）升级，涵盖多个 BIP（141、142、143、144 和 145），所谓软分叉也就是可以兼容老版本的比特币客户端，没有破坏比特币网络的兼容性。

它的**核心改变是把交易中的签名（Witness Data）从交易数据中分离出来**，使交易数据更小，从而减少交易费用，并提高比特币网络的容量。

SegWit 的实现方式是将所有的交易数据分为两部分，一部分是交易的基本信息（Transaction Data），另一部分是交易的签名信息（Witness Data），并把签名信息保存在一个新的数据结构中，是被称为“隔离见证（witness）”的新区块中，并与原始交易分开传输。

这样，比特币交易的交易数据大小提高了上限，同时降低了签名数据的交易费用。在SegWit升级之前，比特币的容量上限是1MB，而SegWit之后，比特币交易的容量上限达到了4MB。

所以Oridnals Inscription的**本质就是把铭刻数据藏在见证数据中。**


### **3.2、Taproot升级**

与SegWit升级类似，Taproot升级同样是一种软分叉升级，是 Bitcoin Core 贡献者 Gregory Maxwell 在 2018 年提出的比特币升级提案，它并不会改变比特币协议本身，而是对现有的比特币交易机制进行改进。

该升级主要包含 3 个技术概念 —— P2SH、MAST 和 Schnorr 。其结果是让复杂的交易如多签名交易、时间锁交易看起来如同普通的比特币交易，增强了比特币的隐私性，目的是推动了比特币实现智能合约部署、拓展用例等各种场景升级。

在 SegWit 升级中，比特币协议增加了一个新的版本号，用于表示新的交易格式。在 Taproot 升级中，比特币协议最重要的更改是将脚本验证程序从 ScriptVerify flag 更新为 ScriptVerifyv2 flag，以支持 `Tapscript`。

一个`Tapscript`的上链需要分为两个步骤：commit和reveal。而Inscription（铭刻）的内容则包含在reveal交易的第一个输入中，从而铭刻在此交易的第一个输出的第一个sat上。比如


```
OP_FALSE
OP_IF
    OP_PUSH "ord" 
    OP_1 
    OP_PUSH "text/plain;charset=utf-8" 
    OP_0 
    OP_PUSH "Hello, world!"
OP_ENDIF
```

这里有多个操作指令，但是开头必然是`OP_``FALSE`此指令被推入执行栈后脚本就会停止运行，但仍然被存在了链上。

所以Ordinal Inscription的本质是：在比特币网络上**借助一个永远不会被执行的脚本tapscript，搭建了一个简易的记账层** ，进行资产和数据的统计和记录

由于只有记账，这就意味着不会有类似智能合约的脚本执行以及验证的过程，**必然高度依赖链下的中心化管理和上报结果。**



## **4、什么是BRC20？**

BRC-20的名字乍一看很像以太坊的ERC20，但其实两者技术差别非常大，ERC-20代币的持有状态保存于链上 ，能在链上得到网络共识。而BRC20则是借助Ordinals协议铭刻的\*\*JSON格式铭文，\*\*该规范只是定义了brc-20代币的部署、铸造和转账行为， 且BRC-20代币的持有状态由链下服务维护 。

部署的json是什么样的？


```
{  
"p": "brc-20",//Protocol: 帮助线下的记账系统识别和处理brc-20事件  
"op": "deploy",//op 操作: 事件类型 (Deploy, Mint, Transfer)  
"tick": "ordi", //Ticker: brc-20代币的标识符，长度为4个字母（可以是emoji） 
"max": "21000000",//Max supply: brc-20代币的最大供应量  
"lim": "1000"//Mint limit: 每次brc-20代币铸造量的限制}
```



对应的op还有Mint和Transfer，两个格式几乎一致，当然如果熟悉以太坊上交易的话，会觉得奇怪，这里的转账接收方to怎么表示呢？

这是因为转账交易生效时，就是该铭文内容对应的sat被交易的时候，所以铭文对应的sat被谁接收，谁就是transfer的对象 ，因此 brc-20的转账必须伴随比特币所有权的转移 （不是只是作为手续费被消耗）。

中心化机构则依据链上登记的各个op来推导出用户当前应该有的余额。

如unisat.io这样客户端软件（索引器），根据`mint`、`transfer` 事件进行统计获得。如：UTXO中包含 `mint` 铭文，就为第一个所有者添加，`transfer `则在发起者的地址上扣除余额，接收者地址加上余额。

拓展阅读：[【源码解读】你买的NFT到底是什么？](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247483815\&idx=1\&sn=5f91df631b450944739419be185e597c\&chksm=e83aa67ddf4d2f6bf24b9f6139bd685db9b5f3ff5a131f84c179a5166ad42337f0b2aabe0bf0\&scene=21#wechat_redirect)

在这个过程中，铭文是 ‘附加’ 交易（聪）上的，**比特币的矿工并不会处理这些铭文**，从链上来看跟其它聪依然是没有分别的，他们都是当做普通的聪来转移的。




## **5、如何评价Ordinals与BRC20**

BRC-20 及 Ordinals NFT， 给比特币带来了很多争论，基本分成两种阵营：

支持方认为，只要你支付手续费，**你就有全权以任意的方式使用区块空间，不论交易是什么内容**，他们 认为BRC-20 与 NFT 给比特币带来了新的文化与叙事，有利于提高比特币的实际应用价值。

反对方认为，这些BRC-20与NFT毫无价值是垃圾交易，过多的垃圾交易会抢占交易带宽，导致交易入块时间变长以及手续费变高。

笔者看来，通过上文的技术实现路线可以显然感受到，虽然新生事物在价格上爆火，但是其技术缺陷也十分显著

**1、过于中心化**

Ordinals协议，必须基于比特币网络之外的线下服务进行状态维护。如果底层的状态服务不可用或者有缺陷，可能导致资产损失，**因为比特币网络没办法阻止失效铭文上链**，中心化平台要裁定谁的铭文有效，在该平台上就是有效的。

**2、缺乏可信验证机制**

不是采用智能合约公开透明的代码规则，所以该协议无法满足共识、防止双花等资金安全的需求。

可拓展阅读：[解读最新Final的ERC-6147：极简的半强制性NFT产权分离标准](http://mp.weixin.qq.com/s?\__biz=MzIyMTQ5MTg5Mw==\&mid=2247484127\&idx=1\&sn=4b930ce55709c5c18f9b308e5115f6e0\&chksm=e83aa505df4d2c13a450bd34728e2ed24ed17946e9fca4cddc74e3b3193a829ed2a4d6572a8d\&scene=21#wechat_redirect)

**3、比特币网络性能局限**

目前比特币出块间隔长达十分钟，交易确认的速度过慢，也会导致交易体验不佳。而且比特币的交易成本太高，并且，一笔成功的上链铭文交易要扣掉三方抽成，平台网络数据延迟，以及各种卡顿带来的预估差错成本，所以矿工费拉满至少要 2-3 倍才行

**4、缺乏基础设施**

比如作为token最核心的交易和定价服务，现在是主要依靠交易平台的订单系统保障，完全中心化的结果缺乏权威的交易方法和定价方法。比如其交易场景若没有中心化平台裁定极易被双花作恶。铭文先到先得的 fomo 机制和矿工按矿工费优先打包的机制存在的逻辑悖论，这就决定了 mint 并不一定是公平的

**5、缺乏安全性**

BRC20 容易让用户产生错觉，使其认为 BRC20 是利用了比特币的安全性进行创造的代币，会和比特币一样的安全以及稳定，但其实它与 BTC 并不一样，BTC 的安全是建立在加密以及共识算法所支撑之上，已经相对稳定运行了相当长的时间，经受住了时间的考验，而 BRC20 是利用 Ordinals 协议与 BTC 进行绑定，Ordinals 协议目前运行时间短，还在发展初始阶段，其中可能会存在一些安全隐患还未被发现。

慢雾也发出BRC 20 存在的安全风险的提醒：

近期 BRC-20 比较火，我们注意到 BRC-20 从 Mint 代币到交易，可能存在安全风险：Mint 代币上，相关的 BRC20 代币铸造平台安全性存疑，防御措施较为薄弱，容易被恶意攻击篡改代码，从而导致用户 Mint 时资产被盗。在交易方法上，有两种方式：一是私下找第三方担保交易，很容易遇到骗子、假币等；二是去专门的交易平台挂单交易，这些交易平台的安全性无法得到保证。

笔者虽然并不看好眼前的Ordinals，毕竟他对区块空间的应用还是太单调只是把图片、NFT 放进去并没有产生更多价值。但是作为一个有趣的尝试，如此破圈的创新也能重新引发大家的思考：

如何利用比特币可编程性？毕竟如今的公链中不会有比比特币更强的共识与安全性了。

都是存储空间的利用，其实Ordinals协议在 OP-Ruturn 输出的金融交易，这在本质上和全节点存储的其他东西没有什么不同，但是是否比特币只能为高净值交易服务？是否可自由的将区块空间去存储和执行一些低成本的数据？

这也让我想起曾经Vitalik 为代表提出的：“当你合理地使用技术并且支付了相应的花费，那你的行为就是有合法性的”


> *附录*
> 
> *https\://docs.ordinals.com/introduction.html*
> 
> *https\://github.com/casey/ord/blob/master/bip.mediawiki#specification*
> 
> *https\://docs.lightning.engineering/the-lightning-network/taproot-assets/taproot-assets-protocol*
> 
> *https\://learnblockchain.cn/article/3050*
> 
> *https\://www\.wu-talk.com/index.php?m=content\&c=index\&a=show\&catid=6\&id=13659*
> 
> *https\://learnblockchain.cn/article/5376*

<!--EndFragment-->
