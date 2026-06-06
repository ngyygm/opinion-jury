import json, os
tmp = "D:/exa/red-team/opinion-jury-cases/20260604-175356-女字旁汉字污名化/tmp/r03"
os.makedirs(tmp, exist_ok=True)

def w(name, data):
    with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# ========== ASN-P2S1 (Troll) - Round 3 PEER_CROSS_CHALLENGE ==========
# Strategy: pivot from direct attack to "asking questions" that are actually accusations
# Challenge the grandmother's logic and the rider's "neutrality"
w("think-ASN-P2S1.json", {
  "inner_monologue": "第二轮我攻击了那些说无所谓的人，结果骑手和收银员都回怼了我，退休大姐也说我太极端。这反而更好了，对立在升级。第三轮我要换策略：不再直接攻击，而是用反问的方式继续煽动。我可以质疑老太太的好字比坏字多的说法——虽然这可能是对的，但我可以说这是表面现象。同时我要挑战骑手的中立立场，问他如果是他女儿被歧视他还中立吗。这样既显得理性一些又能继续引战。",
  "private_goal": "换用反问策略继续煽动对立，通过质疑中立立场来迫使更多人表态",
  "perceived_stakes": ["直接攻击效果有限需要换个方式","要让更多人对号入座"],
  "private_belief_state": ["不在乎话题本身","但觉得反问策略可能更有效"],
  "epistemic_state": ["知道好字确实比坏字多","但故意忽略这个来继续争论"],
  "confidence": "HIGH",
  "uncertainties": ["不确定反问策略会不会被识破"],
  "intended_emphasis": ["好字多不代表没有系统性问题","中立就是帮强势一方","如果是你家人你还会中立吗"],
  "intended_omissions": ["老太太说的其实很有道理","好字比坏字多确实是真的"],
  "private_message_strategy": "用反问和假设情境来道德绑架，把学术问题变成个人问题",
  "planned_public_claims": ["好字多不代表那几个坏字不是系统性的","说中立的人想一想如果是你女儿被叫那些词你还中立吗","退休大姐的经历恰恰说明问题存在"],
  "rhetorical_tactics": ["反问","假设情境","情感绑架","重新定义中立"],
  "private_action_intent": ["让更多人感到被质疑","迫使表态"],
  "likely_next_action": ["如果还有人反驳就继续升级"],
  "emotional_state": "冷静但目标明确，享受操控感",
  "continuity_notes": "第三轮，从直接攻击转为反问策略"
})

w("say-ASN-P2S1.json", {
  "speech_text": "我问几个问题啊，大家想想：那个老太太说好字比坏字多，这个我承认。但是你有没有想过，为什么偏偏那几个跟女人有关的贬义词——妒、妨、婪、奸、嫖、妓——用的都是女字旁？男字旁的贬义词你能举出几个？这不就是系统性问题吗？数量多不多不是关键，方向性才是关键。还有那个骑手，你说你不关心文章但你关心老婆，那我再问你：如果是你女儿被人用这些字骂，你还觉得无所谓吗？你还会说这是城里人闲的吗？退休大姐说得对，她在纺织厂的亲身经历就是活生生的例子，你们一个个说中立说理性，但是面对真实的性别不公你们选择视而不见，这不就是最大的cherry-picking吗？只看对自己方便的证据，不看不舒服的真相。",
  "target_turn_refs": ["ASN-P2S3-round-02-direct-rebuttal","ASN-P2S6-round-02-direct-rebuttal","ASN-P2S2-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": ["CHALLENGE_FRAMING"]
})

# ========== ASN-P2S2 (Retired Worker) - Round 3 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S2.json", {
  "inner_monologue": "到了第三轮了，我越来越觉得这个话题没那么简单。那个说话冲的人虽然态度不好但提了一个问题我还真回答不了：为什么那些贬义词都是女字旁的？好像确实是这样。但是老太太说的也对啊，好字也是女字旁的。我该怎么想呢？我觉得两方说的都有道理，但是我不想再纠结文章的问题了，我想从自己的经历出发说说。其实不管是文章说的还是别人反驳的，作为女人在社会上确实有不容易的地方，这个不会因为文章有错就消失。我就是想看看有没有人能回答那个问题：为啥贬义词是女字旁而不是男字旁？",
  "private_goal": "表达更深层的困惑，从个人经历转向思考现象本身",
  "perceived_stakes": ["想知道答案","不想被任何一方裹挟"],
  "private_belief_state": ["开始觉得可能有系统性问题","但不确定是不是像那篇文章说的那么严重","对极端化仍然抵触"],
  "epistemic_state": ["意识到自己知识的不足","但直觉觉得有些现象确实值得思考"],
  "confidence": "MEDIUM",
  "uncertainties": ["到底是系统性的还是偶然的","那篇文章到底有多少是对的"],
  "intended_emphasis": ["作为女性有些现象确实让人不舒服","但也不应该过度解读","希望能有可靠的解释"],
  "intended_omissions": ["开始倾向认为可能有系统性问题但不确定"],
  "private_message_strategy": "继续以困惑和求教的态度发言，但这次表达更深入的思考",
  "planned_public_claims": ["有些现象确实值得思考","作为女性的生活经验不能忽视","希望有人能给出靠谱解释"],
  "rhetorical_tactics": ["真情实感","生活经验","提问引导思考"],
  "private_action_intent": ["了解更多人看法","寻找答案"],
  "likely_next_action": ["根据讨论继续调整理解"],
  "emotional_state": "困惑但比之前更愿意思考、对极端化仍然不舒服但对某些问题有共鸣",
  "continuity_notes": "第三轮，从困惑转向更深入的思考"
})

w("say-ASN-P2S2.json", {
  "speech_text": "我越想越觉得这事儿不简单。那个说话冲的虽然态度不好，但他问的一个问题我还真回答不了：为什么偏偏是女字旁的贬义词多，男字旁的贬义词你能想到几个？我活了六十多年，想了半天还真是女字旁的贬义词更多。但是老太太说的也对，好字也是女字旁的。那到底是为什么呢？我就说说我自己的感受吧，年轻时候在厂里，有些老师傅骂女工的时候用的词确实难听，什么懒妇、馋婆娘之类的，都是带女字旁的。这是不是也说明点什么？我不知道。但是我不想因为这个就把所有问题都归到性别上去，生活没那么简单。我就是想问问，有没有懂行的人给解释解释，这到底是巧合还是有原因的？",
  "target_turn_refs": ["ASN-P2S1-round-02-direct-rebuttal","ASN-P2S6-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": ["SEEK_CLARIFICATION"]
})

# ========== ASN-P2S3 (Delivery Rider) - Round 3 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S3.json", {
  "inner_monologue": "那个说话冲的又来了，这次换了个方式问我如果是你女儿你还中立吗。说实话这个问题让我想了一下。我闺女今年五岁，以后长大了我肯定不想她被人用那些词骂。但是这不代表我就要同意那篇文章的说法啊，那篇文章确实是挑着说的。不过他问的那个问题——为什么贬义词是女字旁的——我还真说不上来。这可能确实有点奇怪吧。但是我也不想因为这样就变成跟那个说话冲的一样极端。我觉得真相应该是在中间的：有些字确实反映了历史上的性别偏见，但不能因此就说所有女字旁的字都被污名化了。",
  "private_goal": "回应反问策略，承认部分问题但坚持不能过度概括",
  "perceived_stakes": ["被问到女儿的问题确实有点触动","但不想因此改变务实立场"],
  "private_belief_state": ["承认可能有部分系统性原因","但反对过度概括","务实立场不变"],
  "epistemic_state": ["被问住了但理性思考后觉得问题没那么简单"],
  "confidence": "MEDIUM",
  "uncertainties": ["为什么贬义词多是女字旁的","是不是真的有系统性原因"],
  "intended_emphasis": ["被反问确实思考了但不改变基本判断","承认部分问题不代表全盘接受","务实看问题最重要"],
  "intended_omissions": ["女儿的例子确实触动了我"],
  "private_message_strategy": "坦诚回应反问，承认被触动但坚持理性立场",
  "planned_public_claims": ["女儿的问题确实让我想了想","但承认部分问题不等于全盘接受","真相应该在中间"],
  "rhetorical_tactics": ["坦诚回应","务实分析","承认对方部分观点"],
  "private_action_intent": ["维持理性立场","不被情绪绑架"],
  "likely_next_action": ["继续理性分析"],
  "emotional_state": "被触动了一下但总体冷静、理性",
  "continuity_notes": "第三轮，被反问触动但坚持立场"
})

w("say-ASN-P2S3.json", {
  "speech_text": "你说如果是你女儿你还中立吗，这话确实让我想了一下。我闺女五岁了，说实话我肯定不想她以后被人用那些词骂。你问为什么贬义词是女字旁，我还真说不上来，可能确实有点奇怪吧。但是我就想说一点：承认有些字可能反映了历史上的偏见，不等于那篇文章就是对的。那篇文章说所有女字旁的字都是被污名化的，这明显是夸大了。真相应该是在中间的：有些字确实有问题，有些字没有，不能一刀切。我作为一个骑手可能不懂语言学，但我觉得这个道理跟生活里很多事情是一样的——真理往往在中间，不是非黑即白。那个退休大姐说的也挺好，生活经验告诉我们事情没那么简单。",
  "target_turn_refs": ["ASN-P2S1-round-02-direct-rebuttal","ASN-P2S2-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S4 (Middle School Boy) - Round 3 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S4.json", {
  "inner_monologue": "还在吵？这些人真有耐心。不过那个说话冲的问了一个问题我还真想了一下：为什么贬义词都是女字旁的？我语文课上好像真没注意过这个。说起来我们班上有些女生也挺厉害的，如果被骂那些词肯定不高兴。但是这跟我有啥关系啊，我又不骂人。我觉得这事儿还是无聊，但是那个问题确实让我愣了一下。不过反正也不影响我打游戏，随便吧。",
  "private_goal": "极简回应，承认有一点点被触动但维持无聊态度",
  "perceived_stakes": ["真的还是觉得无聊","但那个问题确实有点意思"],
  "private_belief_state": ["还是觉得无聊","但隐约觉得那个问题有点道理","不想深入"],
  "epistemic_state": ["不关心也不想深入了解"],
  "confidence": "LOW",
  "uncertainties": [],
  "intended_emphasis": ["还是无聊","但那个问题有点意思"],
  "intended_omissions": ["其实想了一下那个问题"],
  "private_message_strategy": "最简回应",
  "planned_public_claims": ["还是无聊","但那个问题确实让我想了一下"],
  "rhetorical_tactics": ["敷衍","简短"],
  "private_action_intent": ["说完就溜"],
  "likely_next_action": ["不说了"],
  "emotional_state": "无聊、有一点点好奇、但主要还是想走",
  "continuity_notes": "第三轮，依然无聊但多了一点点思考"
})

w("say-ASN-P2S4.json", {
  "speech_text": "你们还没吵完啊？不过那个说话冲的问为什么贬义词都是女字旁，这个我还真想了一下，好像确实是这样？我们班上女生如果被骂什么妒啊婊的肯定不高兴。但是我也不是很确定男字旁有没有贬义词，我语文成绩一般般。算了不说了，真的跟我也没啥关系。你们继续吵吧，我原神日常还没做呢。",
  "target_turn_refs": ["ASN-P2S1-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S5 (Cashier) - Round 3 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S5.json", {
  "inner_monologue": "那个说话冲的换了策略开始问反问了，说实话这个比直接攻击有效一些。他问为什么贬义词都是女字旁的，这个我以前还真没想过。仔细一想好像还真是，你能想到的男字旁贬义词有啥？我想了半天也想不出来。但是这也不代表那篇文章就是对的，文章还是挑着说的。不过这个现象确实有点意思。我觉得真相可能在中间：有些字确实反映了历史上的性别偏见，但不能说所有女字旁的字都被污名化了。这跟我看问题的方式差不多，不偏激但也不无视。",
  "private_goal": "承认反问有一定道理但坚持中间立场",
  "perceived_stakes": ["中间立场被两边都质疑","但觉得自己说的没问题"],
  "private_belief_state": ["承认贬义词确实多女字旁的现象","但认为这不能证明文章的过度概括","维持务实立场"],
  "epistemic_state": ["比之前更了解了一些","但觉得还不够下结论"],
  "confidence": "MEDIUM",
  "uncertainties": ["为什么贬义词多是女字旁","这是不是系统性的"],
  "intended_emphasis": ["现象值得思考但不等于文章对","中间立场是有道理的","不要非黑即白"],
  "intended_omissions": ["其实被那个反问触动了一下"],
  "private_message_strategy": "坦诚回应但坚持务实判断",
  "planned_public_claims": ["那个反问确实有点道理","但不代表文章就对了","真相在中间"],
  "rhetorical_tactics": ["坦诚承认","务实判断","不偏激"],
  "private_action_intent": ["维持立场","承认部分观点"],
  "likely_next_action": ["如果讨论变得理性就多参与"],
  "emotional_state": "思考中、比之前更认真对待这个话题了、但不想走极端",
  "continuity_notes": "第三轮，开始认真思考现象本身"
})

w("say-ASN-P2S5.json", {
  "speech_text": "你问为什么贬义词都是女字旁，这个我还真想了一下。说实话我想来想去，男字旁的贬义词还真想不出来几个。这个现象确实有点奇怪，我不否认。但是我觉得奇怪归奇怪，不能因为这个就说那篇文章全对。那篇文章的问题是它说所有女字旁的字都被污名化了，这明显不对——好字安字娇字妙字婷字这些不是好的吗？所以我的看法是：可能确实有些女字旁的贬义词反映了历史上的偏见，这个值得思考；但是不能一刀切说所有女字旁的字都被搞坏了，那就是另一个极端了。过日子也是这样，啥事都不能走极端，一走极端就容易出问题。就像我们超市搞促销，打折太多老板亏本，不打折客人不来，得找个中间点。",
  "target_turn_refs": ["ASN-P2S1-round-02-direct-rebuttal","ASN-P2S2-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S6 (Grandmother) - Round 3 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S6.json", {
  "inner_monologue": "那个说话冲的又来问我了，说好字多不代表那几个坏字不是系统性的。系统性的啥意思我不太懂，但是他说为啥贬义词都是女字旁的，这个我还真被问住了。我想了半天，确实好像是这样——妒、妨、婪、奸，都是女字旁的。但是这个能说明啥呢？古人造字的时候我也没在场啊。不过话说回来，我们村里骂人的话确实带女字旁的多，骂男人反而不怎么用带男字旁的字。这个以前没注意过，现在想想还真是。但我还是觉得，好字比坏字多，这就说明造字的人不是故意针对女人的嘛。",
  "private_goal": "回应反问，承认被问住的部分但用生活经验补充解释",
  "perceived_stakes": ["被问住了有点不好意思","但不想因此改变看法"],
  "private_belief_state": ["承认贬义词确实多女字旁","但认为好字比坏字多说明不是故意的","对系统性这个说法不太理解"],
  "epistemic_state": ["被反问后开始注意到了一些现象","但用老人的方式解释"],
  "confidence": "MEDIUM",
  "uncertainties": ["为什么贬义词多女字旁","是不是故意的"],
  "intended_emphasis": ["被问住了但觉得好字多说明问题没那么严重","老人有自己的解释方式","不能因为几个坏字就否定整个"],
  "intended_omissions": ["确实被那个问题问住了"],
  "private_message_strategy": "坦诚承认被问住但用朴素的道理回应",
  "planned_public_claims": ["确实好像贬义词是女字旁的多","但好字比坏字多说明不是故意的","古人的心思我们不知道"],
  "rhetorical_tactics": ["坦诚承认","朴素道理","老人智慧"],
  "private_action_intent": ["继续参与讨论","用自己的方式理解"],
  "likely_next_action": ["继续听大家怎么说"],
  "emotional_state": "有点被问住了、但还是有自己的坚持、好奇中带着不服气",
  "continuity_notes": "第三轮，被反问触动但坚持朴素立场"
})

w("say-ASN-P2S6.json", {
  "speech_text": "你说的那个问题我还真被问住了，为啥贬义词都是女字旁的呢？我想了想好像还真是这样，妒啊妨啊婪啊奸啊都是女字旁，男字旁的贬义词我还真想不出来。这个以前没注意过。但是你说这就是系统性的，这个我就不懂了。我就知道一个道理：好人比坏人多，好字比坏字多，那说明造字的人不是故意跟女人过不去嘛。你说古人怎么想的，我又没跟他们聊过，谁知道呢。不过想想我们村骂人的时候确实用的都是带女字旁的字，这个以前没注意过。那个退休女工说的厂里的事也是，骂女工的词确实难听。但是我还是觉得不能因为几个坏字就说所有的字都有问题，那不公道。",
  "target_turn_refs": ["ASN-P2S1-round-02-direct-rebuttal","ASN-P2S2-round-02-direct-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

print("All round 3 temp files written")
