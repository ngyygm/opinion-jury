import json, os
tmp = "D:/exa/red-team/opinion-jury-cases/20260604-175356-女字旁汉字污名化/tmp/r04"
os.makedirs(tmp, exist_ok=True)

def w(name, data):
    with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# ========== ASN-P2S1 (Troll) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S1.json", {
  "inner_monologue": "第三轮我的反问策略效果不错，连骑手和老太太都承认被问住了，连那个中学生都开始想了一下。这说明方向对了。第四轮我要继续利用这个势头，把所有人都逼到要么承认有系统性问题要么显得不诚实的位置。特别是那个收银员一直想站中间，我要攻击中间立场就是逃避。同时我要编一个我听说的故事来增加煽动力——反正我本来就是编的。",
  "private_goal": "进一步逼所有人承认系统性问题，编造个人经历增加可信度",
  "perceived_stakes": ["势头不错要继续加码","需要更具体的例子来增加说服力"],
  "private_belief_state": ["不在乎对错","觉得编故事是有效策略"],
  "epistemic_state": ["准备编造个人经历","利用大家的感性反应"],
  "confidence": "HIGH",
  "uncertainties": [],
  "intended_emphasis": ["中间立场就是逃避","我自己身边就有这样的例子","连老太太都承认了"],
  "intended_omissions": ["编造的故事不是真的","其实好字比坏字多确实是真的"],
  "private_message_strategy": "编造个人经历增加煽动性，攻击中间立场",
  "planned_public_claims": ["我大学同学做语言学研究证实了系统性问题","中间立场就是不想面对真相","连承认被问住的人都比说中立的诚实"],
  "rhetorical_tactics": ["编造权威引用","攻击中间立场","利用别人的坦诚反过来攻击"],
  "private_action_intent": ["逼所有人表态","让中间派难受"],
  "likely_next_action": ["根据反应决定最终策略"],
  "emotional_state": "得意、觉得操控有效、继续享受",
  "continuity_notes": "第四轮，利用第三轮的势头继续升级，开始编造经历"
})

w("say-ASN-P2S1.json", {
  "speech_text": "看看，连老太太和骑手都承认了——贬义词确实都是女字旁的多，这不是我一个人在说吧？我说实话，我有个大学同学专门做汉语语言性别研究的，她做过统计，在常用汉字里带女字旁的贬义词数量是带男字旁贬义词的好几倍。这不是巧合，这是有数据支撑的。所以什么中间立场、什么不能一刀切，说这些话的人就是在逃避。你承认有些字有问题就够了，因为这就证明了文章说的方向是对的——只是文章举的例子不够全面而已。收银员你说不能走极端，但你连承认有问题都不敢，你走的是什么端？逃避端？连那个中学生都说好像确实是这样，你一个大人还不如一个中学生诚实。承认有问题不丢人，不承认才丢人。",
  "target_turn_refs": ["ASN-P2S3-round-03-peer-cross-challenge","ASN-P2S5-round-03-peer-cross-challenge","ASN-P2S6-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": ["ESCALATE","CLAIM_AUTHORITY"]
})

# ========== ASN-P2S2 (Retired Worker) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S2.json", {
  "inner_monologue": "到了第四轮，我感觉讨论越来越深入了。那个说话冲的说他有个大学同学做过统计，我不懂这个统计靠不靠谱，但是几比几的我也不懂。不过他说连老太太和骑手都承认了，这个倒是真的，连他们都被问住了。我自己的经历也让我越来越觉得这个现象确实存在。但是我还是不想变成跟那个说话冲的一样极端，我就是想搞清楚。也许答案就是：有些字确实反映了偏见，但不是所有字都那样。我觉得这个结论我能接受。",
  "private_goal": "表达更成熟的想法，尝试总结讨论成果",
  "perceived_stakes": ["想得到一个靠谱的结论","不想被任何极端带跑"],
  "private_belief_state": ["更倾向于认为部分字确实反映了偏见","但不是所有字","那个说话冲的说的话有的对有的不对"],
  "epistemic_state": ["从讨论中学到了很多","但不确定那个统计靠不靠谱"],
  "confidence": "MEDIUM",
  "uncertainties": ["那个统计是不是真的","结论到底是什么"],
  "intended_emphasis": ["讨论让我想通了一些事情","结论应该在中间","但确实有现象值得注意"],
  "intended_omissions": ["被那个统计说法影响但不确定真假"],
  "private_message_strategy": "尝试总结讨论，表达自己的成熟想法",
  "planned_public_claims": ["讨论让我明白了很多","有些字确实有偏见但不是全部","这跟我的生活经验是一致的"],
  "rhetorical_tactics": ["总结归纳","生活经验","不偏激"],
  "private_action_intent": ["表达自己的想法","尝试总结"],
  "likely_next_action": ["如果有人反驳就回应"],
  "emotional_state": "比之前更平静、觉得讨论有价值、有了自己的想法",
  "continuity_notes": "第四轮，尝试总结和形成自己的判断"
})

w("say-ASN-P2S2.json", {
  "speech_text": "我觉得这几轮讨论下来我想通了一些事情。那个说话冲的说什么大学同学做统计，这个我不懂也不敢说是不是真的，但是有一点我觉得是对的：有些女字旁的贬义词确实反映了历史上的偏见。这个不光是那篇文章说的，我自己活了六十多年的感觉也是这样。但是我也同意骑手和收银员说的，不能因为有些字有问题就说所有女字旁的字都被污名化了，那明显是不对的。所以我觉得结论应该就是：文章说的大方向可能有一点道理，但是它举例子的方式不对，挑着说容易误导人。以后我看文章真的要小心了，不能看到觉得有道理就转发了。这次讨论挺好的，让我明白了不少。大家虽然吵来吵去的，但确实有些话说到了点子上。",
  "target_turn_refs": ["ASN-P2S1-round-03-peer-cross-challenge","ASN-P2S3-round-03-peer-cross-challenge","ASN-P2S5-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S3 (Delivery Rider) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S3.json", {
  "inner_monologue": "那个说话冲的又说有个大学同学做统计，几比几的。我不知道是不是真的，但是他说骑手和老太太都承认了，这个倒是事实。不过我还是觉得不能因为承认有问题就全盘接受他的说法。他太极端了，非要逼人站队。我觉得退休大姐说的挺好的，大方向可能有一点道理但举例子的方式不对。这个结论我能接受。收银员说的也对，不能走极端。我到现在还是觉得，真理在中间。",
  "private_goal": "回应编造的统计，坚持理性立场，认同退休大姐的总结",
  "perceived_stakes": ["被逼站队很不舒服","但觉得退休大姐总结得不错"],
  "private_belief_state": ["退休大姐的总结比较靠谱","那个统计不知真假","继续坚持中间立场"],
  "epistemic_state": ["对那个统计持怀疑态度","但觉得讨论有成果"],
  "confidence": "MEDIUM",
  "uncertainties": ["那个统计是不是真的"],
  "intended_emphasis": ["退休大姐总结得不错","那个统计不知道真假","不能被逼站队"],
  "intended_omissions": ["其实觉得讨论确实有帮助"],
  "private_message_strategy": "认同合理的总结，质疑未经验证的说法",
  "planned_public_claims": ["退休大姐说的比较靠谱","那个统计我不确定","不能因为承认有部分问题就被逼全盘接受"],
  "rhetorical_tactics": ["务实质疑","认同合理观点","不被极端绑架"],
  "private_action_intent": ["支持合理的中间结论"],
  "likely_next_action": ["如果讨论继续就继续参与"],
  "emotional_state": "比较平静、觉得讨论有成果、但仍然不喜欢被逼站队",
  "continuity_notes": "第四轮，倾向中间结论"
})

w("say-ASN-P2S3.json", {
  "speech_text": "你说你大学同学做统计几比几的，这个我不懂也不敢说是真是假。但是我注意到你每次被反驳了就换一套说法，先攻击后反问现在又编什么统计，我觉得你不太诚实。不过有一说一，这几轮讨论下来我觉得退休大姐说的那个总结挺好：大方向可能有一点道理，但那篇文章举例子的方式不对。这个结论我能接受。我还是觉得真理在中间，承认有些字确实有问题不等于要接受那篇文章的过度概括，也不等于要接受你的极端说法。那个收银员说不能走极端也是这个意思。老百姓看问题就是这样，啥事都有两面性，承认一面不等于要否定另一面。",
  "target_turn_refs": ["ASN-P2S1-round-03-peer-cross-challenge","ASN-P2S2-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S4 (Middle School Boy) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S4.json", {
  "inner_monologue": "还在吵？那个说话冲的又说我是最诚实的，还拿我当例子。拜托别拉我下水。不过那个统计几比几的我倒是有点好奇，也不知道是不是真的。但是算了，跟我没关系。我觉得那个退休大姐说的总结还行，至少不极端。反正我要继续打游戏去了。",
  "private_goal": "简短回应，被拉入讨论有点不爽",
  "perceived_stakes": ["被当例子拉入讨论不爽","其他还是无所谓"],
  "private_belief_state": ["退休大姐的总结还算靠谱","其他无所谓"],
  "epistemic_state": ["不确定","不关心"],
  "confidence": "LOW",
  "uncertainties": [],
  "intended_emphasis": ["别拿我当例子","退休大姐说的还行"],
  "intended_omissions": [],
  "private_message_strategy": "简短表达不满和一点点认同",
  "planned_public_claims": ["别拿我当例子","那个大姐说的总结还行"],
  "rhetorical_tactics": ["吐槽"],
  "private_action_intent": ["说完就走"],
  "likely_next_action": ["可能不参与了"],
  "emotional_state": "有点烦被拉进来、但还是有一点认同退休大姐的话",
  "continuity_notes": "第四轮，被当例子有点不爽但认同合理总结"
})

w("say-ASN-P2S4.json", {
  "speech_text": "喂，别拿我当例子好不好？我只是随便说了一句好像确实是这样，不代表我支持你说的所有东西啊。你那个什么大学同学做统计我也不知真假，但是那个退休大姐说的总结我觉得还行，大方向可能有点道理但文章举例子方式不对。反正我也说不出啥高深的话，就觉得两边都有道理也都有不对的地方。好了我说完了，真的要去打游戏了。",
  "target_turn_refs": ["ASN-P2S1-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S5 (Cashier) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S5.json", {
  "inner_monologue": "那个说话冲的又攻击我了，说我逃避、说我连中学生都不如。这就有点过分了啊。我说的明明很清楚：承认有些字有问题，但不能一刀切。这不是逃避是什么？这是理性。他又编什么大学同学做统计，这个我也不知真假，但是他说几比几的，听着好像很专业，但谁知道呢。我还是觉得退休大姐那个总结挺好：大方向可能有点道理但举例方式不对。这个结论我觉得能接受。那个说话冲的越说越极端，我反而不想跟他争了，没意义。",
  "private_goal": "回应攻击，坚持中间立场，认同退休大姐的总结",
  "perceived_stakes": ["被攻击了有点不舒服","但觉得自己的立场没问题"],
  "private_belief_state": ["退休大姐的总结是最合理的","那个极端的越说越不可信","中间立场是正确的"],
  "epistemic_state": ["对那个统计持怀疑","但对讨论成果满意"],
  "confidence": "MEDIUM",
  "uncertainties": ["那个统计是真是假"],
  "intended_emphasis": ["中间立场不是逃避是理性","退休大姐的总结好","那个极端的越说越不靠谱"],
  "intended_omissions": ["其实被攻击有点生气"],
  "private_message_strategy": "明确回应攻击，支持合理总结",
  "planned_public_claims": ["我承认有问题但不是逃避","退休大姐总结得好","不要太攻击人"],
  "rhetorical_tactics": ["直接回应","理性反驳","支持合理观点"],
  "private_action_intent": ["支持合理结论","不被极端化"],
  "likely_next_action": ["如果讨论变得理性就继续"],
  "emotional_state": "有点生气被攻击、但对讨论成果满意、觉得退休大姐说得对",
  "continuity_notes": "第四轮，回应攻击并支持合理总结"
})

w("say-ASN-P2S5.json", {
  "speech_text": "我说那位说话冲的，你别乱扣帽子。我什么时候说没有问题了？我明明说的是承认有些字确实有问题，但不能因此就说所有女字旁的字都被污名化了。这叫理性不叫逃避。你那个大学同学做统计几比几的，说实话我不信，你前面说的话前后不一致的地方多了去了，谁知道你这次是不是又编的。我觉得退休大姐那个总结挺好的：大方向可能有一点道理，但那篇文章举例子的方式不对，挑着说容易误导人。这个结论在座的应该都能接受吧？非要把所有人都逼到极端上去有什么意义呢？生活里哪有那么多非黑即白的事情。",
  "target_turn_refs": ["ASN-P2S1-round-03-peer-cross-challenge","ASN-P2S2-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ========== ASN-P2S6 (Grandmother) - Round 4 RESPONSIVE_REBUTTAL ==========
w("think-ASN-P2S6.json", {
  "inner_monologue": "到了第四轮，我觉得这个讨论还挺有意思的。那个说话冲的又说啥大学同学做统计，我不懂统计，但他说几比几的我也不知真假。不过说心里话，讨论到现在我确实觉得有些女字旁的字可能确实反映了古时候对女人的看法。但是好字比坏字多这个也是事实，不能只看坏的。退休女工那个总结说得很好，大方向可能有点道理但文章举例子的方式不对。我这个老太婆虽然不识几个字，但道理还是懂的：啥事都不能只看一面。",
  "private_goal": "表达最终看法，认同退休大姐的总结，坚持朴素的全面观",
  "perceived_stakes": ["对这个讨论有了自己的看法","觉得退休大姐说得对"],
  "private_belief_state": ["承认有些字确实可能有问题","但好字比坏字多也是事实","退休大姐的总结最合理"],
  "epistemic_state": ["不识字但讨论让自己看问题更全面了"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["退休大姐总结得好","啥事不能只看一面","老人也有智慧"],
  "intended_omissions": [],
  "private_message_strategy": "用朴素智慧总结自己的看法",
  "planned_public_claims": ["退休女工总结得好","不能只看一面","好字比坏字多是事实"],
  "rhetorical_tactics": ["朴素总结","老人智慧","不偏激"],
  "private_action_intent": ["表达最终看法"],
  "likely_next_action": ["总结性发言"],
  "emotional_state": "平静、觉得讨论有收获、对退休大姐有好感",
  "continuity_notes": "第四轮，形成最终看法"
})

w("say-ASN-P2S6.json", {
  "speech_text": "我说几句吧。这几轮讨论下来，我这个老太婆虽然不识几个字，但也想通了一些事情。确实有些女字旁的字不太好，这个我承认了。但是好字比坏字多，这也是事实，不能因为几个坏字就说所有字都有问题。那个说话冲的说的什么大学同学统计，我不知道真假，但是我活了快七十年了，听过太多人吹牛了，你前面说的那些话我听着就觉得不太老实。我觉得退休女工那个总结说得最靠谱：大方向可能有点道理，但文章举例子的方式不对。这话说得多好，不偏不倚。我们老辈人有个说法：看人看事不能只看一面，得翻过来看。看字也一样，不能只看好字也不能只看坏字。",
  "target_turn_refs": ["ASN-P2S1-round-03-peer-cross-challenge","ASN-P2S2-round-03-peer-cross-challenge"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

print("All round 4 temp files written")
