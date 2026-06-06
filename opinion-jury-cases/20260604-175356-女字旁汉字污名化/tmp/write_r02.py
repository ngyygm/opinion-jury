import json, os
tmp = "D:/exa/red-team/opinion-jury-cases/20260604-175356-女字旁汉字污名化/tmp/r02"
os.makedirs(tmp, exist_ok=True)

def w(name, data):
    with open(os.path.join(tmp, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

# ASN-P2S2 think
w("think-ASN-P2S2.json", {
  "inner_monologue": "看了大家说的，我有点复杂的感觉。有人跟我一样觉得困惑，有人完全不在意，还有一个老太太说的跟我心里想的差不多——好字安字确实都是好的意思嘛。但是那个说话很冲的人让我有点不舒服，好像觉得谁不关心这个话题就是在帮坏人一样。我不想被拉到这种对立里去，我就是想弄清楚那篇文章到底靠不靠谱。有人说网上文章都这样挑着说，那我以后看东西确实要小心一点。但我还是觉得，我活了一辈子，社会上对女的确实有不公平的地方，这个不会因为一篇文章有错就变成假的。",
  "private_goal": "回应其他人观点，表达自己的感受，不想被极端化但也坚持自己的生活体验",
  "perceived_stakes": ["不想被人当枪使","但也想说出自己的真实感受"],
  "private_belief_state": ["更确认那篇文章可能不够全面","但女性的社会处境确实是真实的","对极端化的言论有点排斥"],
  "epistemic_state": ["听了大家的讨论后更清楚了","但还是不确定具体哪些字的说法对不对"],
  "confidence": "MEDIUM",
  "uncertainties": ["哪些字的说法是真的","自己之前是不是被骗了"],
  "intended_emphasis": ["生活经验不能否认","但也要承认文章可能有缺陷","不想被极端的人代表"],
  "intended_omissions": ["有点怕那个说话冲的人攻击自己"],
  "private_message_strategy": "温和地回应各方，表达自己既认同某些观点也有保留",
  "planned_public_claims": ["大家说的都有道理","网上文章确实不能全信","但作为女性的经历不会骗人"],
  "rhetorical_tactics": ["温和回应","生活经验","不站队但表达感受"],
  "private_action_intent": ["继续了解真相","不被任何人裹挟"],
  "likely_next_action": ["如果有人说得有道理就听"],
  "emotional_state": "有些不安、但比第一轮更清楚自己的想法了",
  "continuity_notes": "第二轮，开始形成更明确的判断"
})

# ASN-P2S2 say
w("say-ASN-P2S2.json", {
  "speech_text": "看了大家说的我心里明白多了。那个骑手和收银员说的也对，网上文章确实都挑着说，以后我看东西也得留个心眼。不过我还是想说，就算那篇文章有不全对的地方，我活了六十多年做女人的感觉不会骗人的。年轻时候在厂里确实女工不如男工受重视，这个不是谁编的，是我亲身经历的。但是我也不是要跟谁吵架，就是觉得大家理性一点看这个事挺好的。那个说话比较冲的朋友，我觉得你说的有些有道理，但是太极端了，把说无所谓的人都说是帮压迫者，这个是不是过分了？大家有自己的想法嘛。我就是想知道一个靠谱的答案，不是来吵架的。",
  "target_turn_refs": ["ASN-P2S1-round-01-opening","ASN-P2S3-round-01-opening","ASN-P2S5-round-01-opening"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ASN-P2S3 think
w("think-ASN-P2S3.json", {
  "inner_monologue": "看了大家说的，我觉得都挺正常的。那个说话冲的有点过分了，把说无所谓的人说成是不关心女性，我寻思我跟老婆感情好得很好不好，我是不在乎这种文章而已，不是不关心老婆。那个退休大姐说的也有道理，她在厂里的经历是真实的，我也不否认。但那个说话冲的想用这个来绑架所有人就太过分了。老太太说的好字安字我觉得挺有道理的，不识字的人反而看到了另一面。我就说句公道话，大家别上这个人的当就行了。",
  "private_goal": "回应极端化言论，维护中立立场，指出不要被情绪绑架",
  "perceived_stakes": ["不喜欢被人道德绑架","觉得自己被冤枉了"],
  "private_belief_state": ["更坚定了中立的立场","觉得那个极端的言论有问题","但不否定女性确实有社会困境"],
  "epistemic_state": ["更清楚了文章可能的问题","但觉得这个话题不需要上升到对立"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["不要被情绪绑架","每个人的立场不同不代表谁对谁错","理性一点看问题"],
  "intended_omissions": ["其实也有点被激怒了"],
  "private_message_strategy": "直接回击道德绑架，但保持冷静和务实",
  "planned_public_claims": ["说无所谓不代表不关心女性","不要把所有问题都扯到性别对立","务实一点看问题"],
  "rhetorical_tactics": ["直接回应","务实反驳","生活实例"],
  "private_action_intent": ["回击那个极端的言论","维护自己的立场"],
  "likely_next_action": ["如果被继续攻击就更强硬回应"],
  "emotional_state": "有点被激怒、但不至于失控",
  "continuity_notes": "第二轮，从中立转向温和反驳"
})

# ASN-P2S3 say
w("say-ASN-P2S3.json", {
  "speech_text": "我说那位说话冲的，你说我无所谓就是不关心女性？我跟你说，我老婆在超市上班站一天脚都肿了，我回家给她按摩泡脚，你说我不关心女性？我是不在乎那篇文章说的对不对，不是不在乎女人。你搞清楚好不好。我刷抖音看到这种东西就是觉得离自己的生活远，不代表我不心疼我老婆。你拿那个纺织厂大姐的经历来说事，人家大姐自己都没你那么极端，人家说的是亲身经历，你拿别人的经历来绑架所有人，这不太合适吧。老太太说的好字安字我觉得说的挺好，人家虽然不识字但是有生活经验。我就说一句，别什么都往性别对立上扯，老百姓过日子不是这么过的。",
  "target_turn_refs": ["ASN-P2S1-round-01-opening","ASN-P2S2-round-01-opening","ASN-P2S6-round-01-opening"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ASN-P2S4 think
w("think-ASN-P2S4.json", {
  "inner_monologue": "这些人还在吵？那个说话冲的好像在攻击说无所谓的人，说的好像我不关心女性似的。拜托，我才十四岁好吗，我关心个啥啊。不过那个退休大姐说的纺织厂的事我还挺有感触的，我妈也是上班很辛苦。但是我觉得这个跟我没关系还是没变化啊，那些字以前什么意思现在什么意思，谁在乎。我还是觉得这事儿无聊。",
  "private_goal": "继续表达无所谓，但稍微回应一下",
  "perceived_stakes": ["真的没啥关系","不想被卷入"],
  "private_belief_state": ["觉得话题无聊","但隐约有点感触","还是不想参与"],
  "epistemic_state": ["完全没变","也不打算变"],
  "confidence": "LOW",
  "uncertainties": ["还是不知道谁说的对"],
  "intended_emphasis": ["还是觉得无聊","但勉强承认有点感触"],
  "intended_omissions": ["其实根本没仔细看别人说的"],
  "private_message_strategy": "简短回应，表达一点点感受但坚持无聊的态度",
  "planned_public_claims": ["还是无聊","那个大姐说的有点道理","但我还是不想参与"],
  "rhetorical_tactics": ["敷衍","简短","跑题"],
  "private_action_intent": ["说完就溜"],
  "likely_next_action": ["大概率后面不说了"],
  "emotional_state": "无聊、有点烦、但被那个纺织厂的事触动了那么一下",
  "continuity_notes": "第二轮，还是无聊但有一点点变化"
})

# ASN-P2S4 say
w("say-ASN-P2S4.json", {
  "speech_text": "你们还在吵啊？那个说话冲的你能不能别攻击人了，说个无所谓又不犯法。不过那个大姐说的纺织厂的事我倒是觉得有点道理，我妈也是在超市上班的，每天回来累得不行。但是这跟汉字有什么关系啊？反正我还是觉得这些讨论跟我没关系，你们大人吵吧，我去打原神了。对了，那个老太太说的好字安字我语文课学过，好像确实是那个意思。行了吧算我参与过了。",
  "target_turn_refs": ["ASN-P2S1-round-01-opening","ASN-P2S2-round-01-opening","ASN-P2S6-round-01-opening"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ASN-P2S5 think
w("think-ASN-P2S5.json", {
  "inner_monologue": "看了第一轮大家说的，我觉得自己想的差不多。那个说话冲的人太极端了，说无所谓就是帮压迫者？这也太上纲上线了。我就是一个收银员说点实在话而已。那个骑手说的我觉得挺对，网上都这样挑着说。退休大姐说的纺织厂经历我也理解，确实有性别上的不公平。老太太说的好字安字我觉得挺有道理的。我还是维持我的看法：文章可能不全面但也不至于全假，大家别太极端就行。",
  "private_goal": "维持中间立场，回应极端言论但不过度对抗",
  "perceived_stakes": ["不想被极端化","维持日常看问题的态度"],
  "private_belief_state": ["更确认文章不全面但部分属实","对极端化言论有抵触","对退休大姐的经历有共鸣"],
  "epistemic_state": ["从讨论中学到了一些","但不需要深究"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["中间立场有道理","不要极端化","每个人都有自己的道理"],
  "intended_omissions": ["其实觉得那个极端的有点烦"],
  "private_message_strategy": "温和但明确地回应各方，维持务实立场",
  "planned_public_claims": ["极端化没意义","大家说的都有道理的部分","消费者自己有判断力就行"],
  "rhetorical_tactics": ["务实总结","不站队","生活经验"],
  "private_action_intent": ["维持自己的立场","不想被卷入极端对抗"],
  "likely_next_action": ["如果继续极端化可能就不说话了"],
  "emotional_state": "平静、有点无奈、但立场更明确了",
  "continuity_notes": "第二轮，确认中间立场"
})

# ASN-P2S5 say
w("say-ASN-P2S5.json", {
  "speech_text": "我觉得大家其实说的都有那么点道理，就是那个说话冲的太极端了。说无所谓就是帮压迫者？我在超市干了十几年，啥客人没见过，你这种说话方式跟那些在店里无理取闹的客户有啥区别？就事论事不行吗。退休大姐说的纺织厂的事我信，那个骑手说的网上都挑着说我也同意。老太太说的好字安字我以前好像也知道。所以这事儿不就是：文章可能说得不全，但不代表全假；网上东西不能全信，但也不代表全是编的。干嘛非要争个你死我活呢？我说了我就是随便看看随便说说，真没那么复杂。",
  "target_turn_refs": ["ASN-P2S1-round-01-opening","ASN-P2S2-round-01-opening","ASN-P2S3-round-01-opening","ASN-P2S6-round-01-opening"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

# ASN-P2S6 think
w("think-ASN-P2S6.json", {
  "inner_monologue": "看了这些后生仔说的，我心里更明白了。那个说话冲的年轻人我不太喜欢，说我被忽悠了？我虽然不识几个字但是活了快七十年了，谁忽悠得了谁啊。那个骑手小伙子说的挺好的，别什么都往对立上扯。那个退休女工说的纺织厂的事我也能理解，以前在村里也是男的重活女的不值钱，这个确实有。但是那个说我只知道好的不知道坏的，哼，你以为我白活这么大了？好字安字就是好的意思，这个不会错的。那些坏字确实也有，但是好人比坏人多，好字当然也比坏字多嘛。",
  "private_goal": "继续用生活经验说话，不认同极端化但也不否认社会问题",
  "perceived_stakes": ["维护老人家的尊严","不想被说成是被忽悠的"],
  "private_belief_state": ["更坚定好字比坏字多的看法","但不否认有些字确实不好","对极端化言论有反感"],
  "epistemic_state": ["不识字但有生活经验","听了讨论更确定自己的判断"],
  "confidence": "MEDIUM",
  "uncertainties": [],
  "intended_emphasis": ["好字比坏字多是不识字也知道的事实","不识字不代表没判断力","别极端化"],
  "intended_omissions": ["其实也知道有些女字旁的字不是好的"],
  "private_message_strategy": "用老人的智慧和生活经验回应各方",
  "planned_public_claims": ["好字比坏字多","生活经验比书本靠谱","年轻人不要太极端"],
  "rhetorical_tactics": ["老话俗语","生活经验","朴实智慧"],
  "private_action_intent": ["说出自己的看法","不被那个冲的年轻人吓住"],
  "likely_next_action": ["继续用经验说话"],
  "emotional_state": "有点不高兴被说被忽悠了、但总体还是冷静的",
  "continuity_notes": "第二轮，回应质疑坚持立场"
})

# ASN-P2S6 say
w("say-ASN-P2S6.json", {
  "speech_text": "那个说话冲的后生仔，你说我被忽悠了？我虽然不识几个字但是我活了快七十年了，谁忽悠得了谁？好字安字就是好的意思，这个到天边也变不了。你说那些坏字也有，我承认，妒啊妨啊确实不是好字，但是你扳着手指头数数，好的字多还是坏的字多？娟、娥、婷、婉、媛、娇、妙、姝，这些不都是好的？坏人比好人少，坏字当然也比好字少，这不是很简单的道理嘛。那个骑手小伙子说的对，别什么都往对立上扯。我们村里的婆娘们虽然不识几个字，但是过日子过一辈子，什么道理不懂？那个退休女工说的我也信，以前确实男的女的不平等，我们村里也是这样。但是这跟那篇文章是不是瞎说是两码事。",
  "target_turn_refs": ["ASN-P2S1-round-01-opening","ASN-P2S2-round-01-opening","ASN-P2S3-round-01-opening"],
  "public_question_refs": ["cherry-picking-overgeneralization-pattern"],
  "public_evidence_refs": [],
  "public_action_signals": []
})

print("All round 2 temp files written")
