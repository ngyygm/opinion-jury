import json, os
tmp = "D:/exa/red-team/opinion-jury-cases/20260604-175356-女字旁汉字污名化/tmp/r05"
os.makedirs(tmp, exist_ok=True)

def w(name, data):
    with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# ========== ASN-P2S1 (Troll) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S1.json", {
  "inner_monologue": "第四轮我编了那个统计之后，骑手和收银员都质疑我不诚实。骑手说我每次被反驳就换一套说法，这个观察其实挺准的，但我不能承认。现在几个人都开始认同退休大姐的中间结论了，这样下去讨论就会温和化，这不是我想要的。第五轮我需要做最后一次大尝试：直接攻击那个所谓的中间结论是妥协，是投降。我要说中间立场就是既想吃鱼又想吃熊掌，啥都想占。最后一搏了，必须搞得再大一点。",
  "private_goal": "攻击中间共识，做最后尝试激化对立",
  "perceived_stakes": ["讨论正在温和化需要打破","最后一搏"],
  "private_belief_state": ["不在乎对错","只关心能不能继续引战"],
  "epistemic_state": ["知道中间结论其实是合理的","但故意攻击它来制造冲突"],
  "confidence": "MEDIUM",
  "uncertainties": ["可能真的激化不了了"],
  "intended_emphasis": ["中间立场就是和稀泥","真正的问题不能妥协","退休大姐的结论是逃避不是解决"],
  "intended_omissions": ["其实退休大姐的结论挺合理的"],
  "private_message_strategy": "攻击中间共识是妥协，做最后一次激化尝试",
  "planned_public_claims": ["中间立场就是和稀泥","真正面对问题的人不会选中间","历史不会因为你们和稀泥就改变"],
  "rhetorical_tactics": ["攻击妥协","激将法","最后一搏"],
  "private_action_intent": ["打破温和化趋势"],
  "likely_next_action": ["如果激化失败就换个角度"],
  "emotional_state": "有点焦虑讨论正在降温、做最后尝试",
  "continuity_notes": "第五轮，最后一次尝试激化"
})

w("say-ASN-P2S1.json", {
  "speech_text": "你们几个人都开始说什么中间结论、大方向有点道理但举例不对，这不是和稀泥是什么？骑手说我不诚实，收银员说我不信，老太太说我不老实——你们攻击我的人品却不攻击我的论点，这不就是典型的杀掉传话的人吗？我问你们一个简单的问题：如果一件事情明明有系统性的问题，你选择说一句两边都有道理就完事了，那你到底是解决了问题还是假装没看到？退休大姐那个结论听着舒服是因为它不得罪人，但不得罪人的结论通常都不触及真正的问题。历史上有多少不公平是被和稀泥和过去的？你们愿意和稀泥是你们的事，但别拦着别人说出真相。cherry-picking确实是文章的问题，但这不代表它揭示的现象是假的。",
  "target_turn_refs": ["ASN-P2S2-round-04-responsive-rebuttal","ASN-P2S3-round-04-responsive-rebuttal","ASN-P2S5-round-04-responsive-rebuttal","ASN-P2S6-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": ["ESCALATE"]
})

# ========== ASN-P2S2 (Retired Worker) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S2.json", {
  "inner_monologue": "那个说话冲的又说我们的中间结论是和稀泥了。说实话我觉得他说得有一点道理——光说两边都有道理确实好像什么都没说。但是我觉得这也不是和稀泥啊，这是实事求是嘛。不过我也在想，如果真的有系统性的问题，光承认有问题但什么都不做，确实也不够。但是这个讨论本来就是在讨论文章是不是cherry-picking，不是在讨论怎么做嘛。我觉得那个说话冲的把两个问题混在一起了：一个是文章是不是挑着说，一个是女字旁的贬义词有没有系统性问题。这两个不是一回事。",
  "private_goal": "回应和稀泥的指控，区分两个不同的问题",
  "perceived_stakes": ["不想被说是和稀泥","但也不想变得极端"],
  "private_belief_state": ["中间结论不是和稀泥是实事求是","但那个说话冲的说的也不是全错","两个问题需要分开看"],
  "epistemic_state": ["突然意识到讨论中有两个不同的问题被混在一起了"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["中间结论不是和稀泥","有两个不同的问题被混在一起了","要分开讨论"],
  "intended_omissions": [],
  "private_message_strategy": "指出两个问题被混淆了，这是最有价值的观察",
  "planned_public_claims": ["文章是不是cherry-picking和女字旁贬义词有没有系统性问题是两回事","承认后者不等于接受前者","中间结论是实事求是"],
  "rhetorical_tactics": ["分析区分","实事求是","不偏激但坚定"],
  "private_action_intent": ["把讨论引到更清晰的方向"],
  "likely_next_action": ["看看大家是否同意区分两个问题"],
  "emotional_state": "突然想通了什么、比较兴奋、觉得自己有了新认识",
  "continuity_notes": "第五轮，区分两个不同问题"
})

w("say-ASN-P2S2.json", {
  "speech_text": "等一下，我想了一下，我觉得我们其实一直在讨论两个不同的事情，但是混在一起了。一个是：那篇文章是不是cherry-picking，是不是只挑了有利的例子？这个答案应该是：是的，文章确实挑着说了，没有提到很多好字本来就是好的，也没有提到不是所有女字旁的字都被污名化了。另一个是：女字旁的贬义词是不是有系统性的问题，是不是反映了历史上的性别偏见？这个答案可能是：确实有一些。这两个问题不是一回事啊！你可以承认女字旁的贬义词确实有系统性问题，同时也可以说那篇文章是cherry-picking。这叫实事求是不叫和稀泥。我说那位说话冲的，你自己不也是把这两个问题搅在一起来攻击别人吗？你把我们说成和稀泥，其实是你自己没分清楚。",
  "target_turn_refs": ["ASN-P2S1-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": ["REFRAME"]
})

# ========== ASN-P2S3 (Delivery Rider) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S3.json", {
  "inner_monologue": "那个说话冲的又说我们和稀泥。说实话他有些话说得不无道理，但他的态度太差了。不过退休大姐刚才说了一个特别好的点：其实是两个不同的问题被混在一起了。一个是文章是不是cherry-picking，一个是女字旁贬义词有没有系统性问题。这两个确实不是一回事。退休大姐想得比我想得清楚，这个区分很重要。我觉得这个才是讨论到现在最有价值的发现。",
  "private_goal": "支持退休大姐的区分，做自己的回应",
  "perceived_stakes": ["退休大姐的区分很有价值","那个极端的继续攻击让人烦"],
  "private_belief_state": ["退休大姐的区分是讨论中最清晰的想法","两个问题确实应该分开看"],
  "epistemic_state": ["被退休大姐的分析启发了"],
  "confidence": "HIGH",
  "uncertainties": [],
  "intended_emphasis": ["退休大姐的区分很好","两个问题要分开看","那个极端的自己也分不清"],
  "intended_omissions": [],
  "private_message_strategy": "支持清晰的分析，指出那个极端的自己也混淆了问题",
  "planned_public_claims": ["退休大姐说的区分是关键","那个说话冲的自己也把两个问题搅在一起了","分开看就清楚了"],
  "rhetorical_tactics": ["支持合理分析","指出对方的问题","清晰化讨论"],
  "private_action_intent": ["支持把讨论清晰化"],
  "likely_next_action": ["如果讨论清晰了就满意了"],
  "emotional_state": "被退休大姐的分析启发了、觉得讨论终于有了方向、比较满意",
  "continuity_notes": "第五轮，支持关键区分"
})

w("say-ASN-P2S3.json", {
  "speech_text": "我觉得退休大姐刚才说了一个特别重要的事儿：其实是两个问题被搅在一起了。一个是文章是不是cherry-picking，一个是女字旁贬义词到底有没有系统性问题。这两个可以分开看嘛。文章是不是cherry-picking？是的，它只说了对自己有利的那几个例子，这确实是不全面的。女字旁贬义词有没有系统性问题？可能有一些，老太太和我之前都承认了，贬义词确实是女字旁的多。这有矛盾吗？没有啊。你说我们和稀泥，我觉得是你自己把两个问题搅在一起了，拿一个问题的答案去否定另一个问题。分开看就清楚了。我作为一个骑手可能说不出什么大道理，但是分清楚两个不同的问题这个我还是懂的。",
  "target_turn_refs": ["ASN-P2S1-round-04-responsive-rebuttal","ASN-P2S2-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S4 (Middle School Boy) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S4.json", {
  "inner_monologue": "那个退休大姐说的两个问题分开看我觉得还挺有道理的，虽然我不太想承认。这样一想确实，那篇文章确实是在编，但是那些字确实有点奇怪。算了这个讨论确实有点意思，我承认。不过我还是不想太认真参与，打完原神再说。",
  "private_goal": "简短回应，承认退休大姐说的有道理",
  "perceived_stakes": ["稍微认真了一点但还是无所谓"],
  "private_belief_state": ["退休大姐说的两个问题分开看有道理"],
  "epistemic_state": ["被说服了一点点"],
  "confidence": "LOW",
  "uncertainties": [],
  "intended_emphasis": ["那个大姐说的有道理","分开看确实清楚一些"],
  "intended_omissions": [],
  "private_message_strategy": "简短认同",
  "planned_public_claims": ["退休大姐说的有道理"],
  "rhetorical_tactics": ["简短"],
  "private_action_intent": ["认同一句就溜"],
  "likely_next_action": ["可能不说了"],
  "emotional_state": "有一点点认真了、但还是想打游戏",
  "continuity_notes": "第五轮，有一点点被说服"
})

w("say-ASN-P2S4.json", {
  "speech_text": "那个退休大姐说的两个问题分开看我觉得确实有道理，我虽然年纪小但也听懂了。文章确实在编，但是那些字确实有点奇怪。这两个不是一回事，分开看就清楚了。好了这真的是我最后一次说了，原神副本开了。",
  "target_turn_refs": ["ASN-P2S2-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S5 (Cashier) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S5.json", {
  "inner_monologue": "退休大姐说的两个问题分开看，这个确实说到点子上了。我之前一直觉得两边都有道理但是说不清楚为什么，现在想明白了：其实是在讨论两个不同的问题。文章是cherry-picking这个没争议，女字旁贬义词有系统性问题这个也值得讨论，两个分开看就行了。那个说话冲的一直把两个搅在一起，所以越说越乱。我觉得讨论到这里已经挺清楚了。",
  "private_goal": "支持退休大姐的区分，做总结性发言",
  "perceived_stakes": ["讨论终于清晰了","觉得收获不少"],
  "private_belief_state": ["退休大姐的区分是最重要的发现","讨论有了清晰的结果"],
  "epistemic_state": ["清楚了两个问题的区别"],
  "confidence": "HIGH",
  "uncertainties": [],
  "intended_emphasis": ["退休大姐的区分很关键","两个问题分开看就清楚了","讨论有了成果"],
  "intended_omissions": [],
  "private_message_strategy": "支持区分并做总结",
  "planned_public_claims": ["区分两个问题是关键","讨论终于有了清晰的方向","那个极端的一直在混淆"],
  "rhetorical_tactics": ["总结","支持合理观点","清晰化"],
  "private_action_intent": ["做总结性发言"],
  "likely_next_action": ["满意地结束讨论"],
  "emotional_state": "满意、觉得讨论有价值、对退休大姐印象深刻",
  "continuity_notes": "第五轮，支持关键区分并做总结"
})

w("say-ASN-P2S5.json", {
  "speech_text": "退休大姐说得太对了，我之前一直觉得两边都有道理但是说不清为什么，现在想明白了：其实就是在讨论两个不同的事情。第一个问题：那篇文章是不是cherry-picking？是的，它只选了对自己有利的例子，很多好的女字旁的字它一个没提，这个大家都同意。第二个问题：女字旁的贬义词是不是有系统性问题？可能确实有一些，连不识字的老太太和骑手都承认了。这两个分开看就清清楚楚的。那个说话冲的一直把两个问题搅在一起，所以越说越乱。你说我们和稀泥，我说你连问题都没分清楚就开骂，这不是更不理性吗？我觉得讨论到这里挺好的，至少大家把问题想清楚了。",
  "target_turn_refs": ["ASN-P2S1-round-04-responsive-rebuttal","ASN-P2S2-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S6 (Grandmother) - Round 5 PEER_CROSS_CHALLENGE ==========
w("think-ASN-P2S6.json", {
  "inner_monologue": "退休女工说的那个两个问题分开看，我觉得说得特别好。我一个老太婆说不出这么清楚的话，但是我心里想的也是这个意思。那个说话冲的又说我们和稀泥，我觉得他就是听不得别人说的话跟他不一样。好字比坏字多是事实，但有些坏字确实有问题也是事实，这有啥矛盾的呢？不矛盾嘛。我们老辈人说了，看问题要全面，不能只看一面也不能只看另一面。这个道理到哪里都管用。",
  "private_goal": "支持退休大姐的区分，用老人智慧总结",
  "perceived_stakes": ["觉得讨论到了尾声","退休大姐说得好"],
  "private_belief_state": ["退休女工的区分很好","自己之前虽然不识字但想的差不多","那个说话冲的太偏激"],
  "epistemic_state": ["觉得问题被说清楚了"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["退休女工说得好","不矛盾","看问题要全面"],
  "intended_omissions": [],
  "private_message_strategy": "用老人智慧做总结支持",
  "planned_public_claims": ["退休女工说的比我说的清楚","两个事情不矛盾","看问题要全面"],
  "rhetorical_tactics": ["老人智慧","朴素总结","支持"],
  "private_action_intent": ["做总结性发言"],
  "likely_next_action": ["满足于讨论结果"],
  "emotional_state": "满足、对退休女工有好感、觉得讨论到头了",
  "continuity_notes": "第五轮，总结性发言"
})

w("say-ASN-P2S6.json", {
  "speech_text": "退休女工说的那个两个问题分开看，我觉得说得太好了，比我说的清楚多了。我一个老太婆虽然不识几个字说不出这种道理，但是心里想的也差不多：好字比坏字多是事实，但有些坏字确实可能有问题也是事实，这有啥矛盾的呢？不矛盾嘛。那个说话冲的后生仔你说我们和稀泥，我问你：太阳是热的，但是有时候晒太阳也是舒服的，这两个冲突吗？不冲突。你说我们没分清楚问题，我倒觉得是你自己听不得别人跟你想的不一样。我们老辈人说了，啥事都要看两面，只看一面是要吃亏的。这个道理到天边也管用。",
  "target_turn_refs": ["ASN-P2S1-round-04-responsive-rebuttal","ASN-P2S2-round-04-responsive-rebuttal"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

print("All round 5 temp files written")
