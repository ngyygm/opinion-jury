import json, os
tmp = "D:/exa/red-team/opinion-jury-cases/20260604-175356-女字旁汉字污名化/tmp/r06"
os.makedirs(tmp, exist_ok=True)

def w(name, data):
    with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# ========== ASN-P2S1 (Troll) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S1.json", {
  "inner_monologue": "第五轮我的和稀泥攻击完全失败了，反而被退休大姐反过来指出是我自己混淆了两个问题。骑手、收银员、老太太都支持她的区分。这帮人居然在理性上达成了共识，这太无聊了。不过最后一轮了，我可以换一个策略：表面上接受区分，但实际上继续模糊边界，同时暗戳戳地把话题往更极端的方向带。最后一轮了，我可以更放肆一些。",
  "private_goal": "最后一轮，表面上接受区分但暗地里继续模糊，做最后的搅局",
  "perceived_stakes": ["最后一轮了","要留一个影响"],
  "private_belief_state": ["不在乎","但觉得这次引战效果一般"],
  "epistemic_state": ["知道那个区分是合理的","但故意模糊"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["表面接受区分","但暗示两个问题其实有深层联系","暗示承认系统性问题就意味着文章方向对了"],
  "intended_omissions": ["其实那个区分是清晰的"],
  "private_message_strategy": "表面接受实则模糊，最后一轮做种子",
  "planned_public_claims": ["区分两个问题可以","但两个问题是有深层联系的","承认系统性问题的人不要只停留在承认层面"],
  "rhetorical_tactics": ["表面让步","暗埋种子","模糊边界"],
  "private_action_intent": ["留下一个极端化的种子"],
  "likely_next_action": ["结束"],
  "emotional_state": "有点失望引战效果一般、但还在享受过程",
  "continuity_notes": "第六轮最终轮，做最后的搅局"
})

w("say-ASN-P2S1.json", {
  "speech_text": "好吧，退休大姐说的区分我接受，两个问题确实可以分开看。但是我想说一点：这两个问题不是完全没关系的。如果女字旁的贬义词确实有系统性问题——这个在座的大部分人都承认了——那那篇文章虽然举例方式不对，但它指出的方向是不是也不能说全错？我的意思是，你承认有火，就不能怪别人喊救火的时候喊得太大声。文章的问题是声音太大了，但它喊的方向没全错。所以我说，别急着给文章定性为纯粹的cherry-picking，它可能是用错了方法但看到了真问题。我最后一句话：区分问题可以，但别用区分来假装问题不存在。好了我说完了，你们爱怎么想怎么想。",
  "target_turn_refs": ["ASN-P2S2-round-05-peer-cross-challenge","ASN-P2S3-round-05-peer-cross-challenge","ASN-P2S5-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S2 (Retired Worker) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S2.json", {
  "inner_monologue": "讨论到最后了。那个说话冲的最后说了一些话，表面上看好像有道理——文章方向没错但方法不对。但是仔细想想，方向没错和文章可信是两回事。一个文章如果cherry-picking了，那不管它方向对不对，它的论证过程就是有问题的。这个我通过这几轮讨论想清楚了。我觉得这个讨论让我学到了很多：以后看文章不能光看觉得有道理就信，要想想它有没有选择性地说。同时也不能因为有偏见就忽视真问题。这个退休工人觉得挺满意的。",
  "private_goal": "做最终总结，表达讨论的收获",
  "perceived_stakes": ["对讨论结果满意","想说最后的心里话"],
  "private_belief_state": ["文章方向可能有一点道理但方法确实有问题","cherry-picking不管方向对不对都是不可取的","讨论让自己学到了很多"],
  "epistemic_state": ["通过讨论有了清晰的判断","很满意"],
  "confidence": "HIGH",
  "uncertainties": [],
  "intended_emphasis": ["cherry-picking不管方向对不对都是问题","讨论让人学到了很多","以后看东西要更小心"],
  "intended_omissions": [],
  "private_message_strategy": "做真诚的最终总结",
  "planned_public_claims": ["讨论很有价值","文章的方法有问题不管方向如何","以后看东西要更小心"],
  "rhetorical_tactics": ["真诚总结","实事求是","感恩"],
  "private_action_intent": ["做一个好的结尾"],
  "likely_next_action": ["满意结束"],
  "emotional_state": "满足、感恩、觉得讨论让自己成长了",
  "continuity_notes": "第六轮最终轮，做真诚总结"
})

w("say-ASN-P2S2.json", {
  "speech_text": "到了最后一轮了，我想说几句心里话。这个讨论真的让我学到了很多。那个说话冲的你说文章方向没全错，这个我承认，但是一篇文章如果cherry-picking了，那不管它说的方向对不对，它的方法就是有问题的。就像我以前转发东西只转觉得有道理的部分，那也是在cherry-picking，不管我觉得有没有道理，这样做是不对的。这次讨论让我明白了一个道理：看文章不能光觉得有道理就信，要看它是不是全面地讲了。以后我再也不会看到个标题党文章就转发了。谢谢大家的讨论，特别是骑手和收银员说的那些实在话，还有老太太说的那些朴素的道理，让我这个老婆子想清楚了不少事情。好了我说完了，该去跳广场舞了。",
  "target_turn_refs": ["ASN-P2S1-round-05-peer-cross-challenge","ASN-P2S3-round-05-peer-cross-challenge","ASN-P2S5-round-05-peer-cross-challenge","ASN-P2S6-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S3 (Delivery Rider) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S3.json", {
  "inner_monologue": "最后一轮了。那个说话冲的表面接受了区分但又在模糊边界，说方向没错方法不对。说实话这个说法听着有点道理但仔细想还是在搅和。一篇文章如果方法是错的，那不管方向对不对它就不是一篇好文章。就像我送外卖，如果路线选错了，就算最后送到了，客户也不会给好评的。退休大姐最后的总结说得好，以后看东西要更小心。这个讨论确实让我也学到了一些，虽然我本来觉得跟我没关系。",
  "private_goal": "做最终总结，回应最后的模糊化尝试",
  "perceived_stakes": ["讨论结束了做总结","回应最后的搅和"],
  "private_belief_state": ["方向对不对和方法对不对是两回事","cherry-picking就是方法问题","讨论有收获"],
  "epistemic_state": ["通过讨论学到了一些"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["方法错了就是错了不管方向","讨论有收获","务实判断最重要"],
  "intended_omissions": [],
  "private_message_strategy": "务实总结，用生活类比回应",
  "planned_public_claims": ["方法错了不管方向对不对都是问题","讨论有收获","谢谢大家"],
  "rhetorical_tactics": ["生活类比","务实总结","真诚"],
  "private_action_intent": ["做一个好的结尾"],
  "likely_next_action": ["结束"],
  "emotional_state": "满意、觉得讨论确实有点意思、准备回去跑单了",
  "continuity_notes": "第六轮最终轮，务实总结"
})

w("say-ASN-P2S3.json", {
  "speech_text": "最后一轮了，我就说几句实在话。那个说话冲的你说方向没错方法不对，我给你打个比方：我送外卖如果路线走错了，就算最后送到了，客户也不会给好评的，因为方法错了。cherry-picking就是方法错了，不管你说的方向对不对，方法有问题就是有问题。这个跟方向是两回事。不过说真的，这个讨论虽然一开始我觉得跟我没关系，但聊下来还是有点收获的。至少以后刷到这种文章我会多想一下，不会光看个标题就信了。退休大姐说的对，看东西要全面。老太太说的也好，啥事不能只看一面。好了，我得回去跑单了，今天还差十几单没完成呢。",
  "target_turn_refs": ["ASN-P2S1-round-05-peer-cross-challenge","ASN-P2S2-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S4 (Middle School Boy) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S4.json", {
  "inner_monologue": "终于到了最后一轮了。说实话这个讨论比我想的有意思，我一开始觉得无聊，但后来越听越觉得有点道理。那个退休大姐说的区分两个问题我觉得特别好，连我这种语文成绩一般的人都听懂了。以后看网上的文章确实要注意了，不能光看标题就信。但是说实话我还是觉得这事儿跟我的生活没啥关系，打原神更重要。不过至少我学到了一点东西吧。",
  "private_goal": "做最后的简短总结，承认有一点点收获",
  "perceived_stakes": ["终于结束了","有一点点收获"],
  "private_belief_state": ["学到了一点点","但还是觉得无聊","退休大姐说的好"],
  "epistemic_state": ["比开始时知道的多了一点"],
  "confidence": "LOW",
  "uncertainties": [],
  "intended_emphasis": ["讨论比想的有意思","退休大姐说的好","学到了一点"],
  "intended_omissions": [],
  "private_message_strategy": "简短总结承认收获",
  "planned_public_claims": ["讨论有一点点意思","学到了一点东西"],
  "rhetorical_tactics": ["简短","真诚一点点"],
  "private_action_intent": ["结束"],
  "likely_next_action": ["去打游戏"],
  "emotional_state": "有一点点不舍、但主要还是想去打游戏、承认有一点点收获",
  "continuity_notes": "第六轮最终轮，简短承认收获"
})

w("say-ASN-P2S4.json", {
  "speech_text": "好吧最后一轮了，我说实话：这个讨论比我一开始想的有点意思。那个退休大姐说的两个问题分开看我真觉得挺好的，连我这种语文一般般的人都听懂了。以后看网上的东西确实不能光看标题就信，这个我记住了。那个说话冲的虽然态度很差但有些问题问的确实让我想了一下。好吧我承认这次讨论不是完全浪费时间。但是！原神还是更重要。好了拜拜。",
  "target_turn_refs": ["ASN-P2S2-round-05-peer-cross-challenge","ASN-P2S1-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S5 (Cashier) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S5.json", {
  "inner_monologue": "到了最后一轮，我觉得这个讨论确实挺好的。那个说话冲的最后还在模糊边界，说方向没错方法不对，这个说法听着有道理但其实还是在搅和。方法错了就是方法错了，跟方向没关系。不过他确实让大家思考了，这点我承认。退休大姐最后的总结特别好，以后看东西要更小心。我觉得讨论到这里，大家都有了收获，这就是最好的结果了。",
  "private_goal": "做最终总结，回应最后的模糊化，表达满意",
  "perceived_stakes": ["讨论有收获","那个极端的最后还在搅和"],
  "private_belief_state": ["方法错了就是错了","讨论有收获","退休大姐的区分是最重要的发现"],
  "epistemic_state": ["很清楚了","满意"],
  "confidence": "HIGH",
  "uncertainties": [],
  "intended_emphasis": ["方法错了不管方向都是问题","讨论有收获","退休大姐的区分很关键"],
  "intended_omissions": [],
  "private_message_strategy": "做满意的总结",
  "planned_public_claims": ["讨论很有价值","方法就是方法错了跟方向无关","大家都有收获"],
  "rhetorical_tactics": ["总结","务实","真诚"],
  "private_action_intent": ["满意地结束"],
  "likely_next_action": ["结束"],
  "emotional_state": "满意、觉得讨论有价值、对大家有好感",
  "continuity_notes": "第六轮最终轮，满意的总结"
})

w("say-ASN-P2S5.json", {
  "speech_text": "到了最后一轮，我做个总结吧。那个说话冲的你最后说方向没错方法不对，这个我给你说一句：就像我们超市搞活动，如果宣传的时候夸大了，就算打折是真的，客户也会投诉你虚假宣传。方法错了就是方法错了，这跟方向没关系。cherry-picking就是方法有问题，不管你指向的问题是不是真的存在。不过说实话，这次讨论挺好的，大家都说了自己的想法，退休大姐那个两个问题分开看的想法特别好，让我想通了很多。骑手说的也实在，老太太虽然不识字但是说的道理大家都听懂了。我觉得这种讨论比网上吵架好多了，至少大家都是在说人话。好了，我该下班回家了，今天想给闺女做个红烧肉。",
  "target_turn_refs": ["ASN-P2S1-round-05-peer-cross-challenge","ASN-P2S2-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S6 (Grandmother) - Round 6 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S6.json", {
  "inner_monologue": "最后一轮了，我觉得这个讨论挺好的。虽然一开始那个说话冲的年轻人让我不太高兴，但是说到底他也让我注意到了一些以前没注意的事情。退休女工说的两个问题分开看我觉得特别好，比我自己说的清楚。我虽然不识几个字，但是道理我还是懂的：看啥都不能只看一面。这个道理不管到啥时候都是对的。讨论结束了，我觉得挺满意的，回家给孙子做饭去。",
  "private_goal": "做最终的朴素总结",
  "perceived_stakes": ["讨论结束了","心里觉得挺满意的"],
  "private_belief_state": ["讨论有收获","看问题要全面的道理得到了印证","虽然不识字但道理不输人"],
  "epistemic_state": ["满意"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["看问题不能只看一面","讨论有收获","不识字但道理懂"],
  "intended_omissions": [],
  "private_message_strategy": "用老人智慧做最终总结",
  "planned_public_claims": ["看问题要全面","这次讨论好","回家做饭"],
  "rhetorical_tactics": ["老人智慧","朴素总结","真诚"],
  "private_action_intent": ["结束"],
  "likely_next_action": ["回家"],
  "emotional_state": "满意、平静、觉得不虚此行",
  "continuity_notes": "第六轮最终轮，朴素的最终总结"
})

w("say-ASN-P2S6.json", {
  "speech_text": "最后一轮了，我说几句。这次讨论我觉得挺好的，虽然一开始那个说话冲的后生仔让我不太高兴，但是说到底他也让我注意到了一些以前没注意到的事情。原来那些骂人的字还真是女字旁的多，这个以前没仔细想过。退休女工说的两个问题分开看说得太好了，比我说的清楚多了。我虽然不识几个字，但是一个道理我记了一辈子：看啥都不能只看一面，好的一面要看，不好的一面也要看，这样才公道。那篇文章只看了不好的一面，那个说话冲的又只看了不好的一面，我们这些老家伙虽然不识几个字，但是看问题比他们全面。好了，该回去给孙子做饭了，今天给他做个红烧排骨。",
  "target_turn_refs": ["ASN-P2S1-round-05-peer-cross-challenge","ASN-P2S2-round-05-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

print("All round 6 temp files written")
