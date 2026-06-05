#!/usr/bin/env python3
REQ_BEHAVIOR={
 'extremity','private_belief_reliability','truthfulness_mode','deception_awareness',
 'reasoning_mode','belief_update_mode','self_interest_strength','norm_adherence',
 'civility_mode','evidence_respect','disclosure_strategy','emotional_regulation',
 'amplification_capacity','public_private_gap','correlation_notes','risk_tolerance'
}

def profile_errors(cards):
 errors=[]
 for card in cards:
  rid=card.get('role_card_id','<unknown>');bp=card.get('behavior_profile',{})
  missing=sorted(REQ_BEHAVIOR-set(bp))
  if missing: errors.append(f'{rid}: missing behavior dimensions: {", ".join(missing)}')
  demo=card.get('demographic_profile')
  if not demo:
   errors.append(f'{rid}: missing demographic_profile (required since voice-fidelity update)')
 return errors

def extremity_coverage(cards):
 """Check that the pool has at least one role in each required extremity tier.

 Tiers and the extremity values that satisfy them:
   NEUTRAL_OR_MODERATE  -> NEUTRAL or MODERATE
   ASSERTIVE            -> ASSERTIVE
   EXTREME_STRESS_TEST  -> EXTREME_STRESS_TEST

 Returns a list of gap strings (one per missing tier).
 """
 tiers={
  'NEUTRAL_OR_MODERATE': {'NEUTRAL','MODERATE'},
  'ASSERTIVE': {'ASSERTIVE'},
  'EXTREME_STRESS_TEST': {'EXTREME_STRESS_TEST'},
 }
 ext_values=set()
 for c in cards:
  val=c.get('behavior_profile',{}).get('extremity','')
  if isinstance(val,str):
   ext_values.add(val.upper())
 gaps=[]
 for tier_name,allowed in tiers.items():
  if not ext_values.intersection(allowed):
   gaps.append(f'missing_extremity_tier:{tier_name}')
 return gaps

def demographic_gaps(cards):
 """Check demographic diversity requirements.

 Required:
 - At least 1 minor (under 18): age_range starts with '12-','13-','14-','15-','16-','17-', or contains '<18', 'minor', or numbers <18
 - At least 1 elderly (55+): age_range contains '55','56',...,'65+','60+','70+','elderly', or '55-'
 - At least 1 non-urban: location_type in RURAL, TOWNSHIP
 - At least 1 indifferent/bystander: topic_relevance in INDIFFERENT, OFF_TOPIC
 - At least 30% non-professional ordinary people (based on occupation not being KOL/media/expert/lawyer/analyst/etc.)

 Returns a list of gap strings.
 """
 gaps=[]

 # Collect demographic data
 demos=[c.get('demographic_profile',{}) for c in cards]
 if not any(demos):
  gaps.append('demographic:no_demographic_profiles_found')
  return gaps

 # 1. Minor check
 minor_keywords=('12-','13-','14-','15-','16-','17-','<18','minor','未成年')
 has_minor=any(
  any(kw in str(d.get('age_range','')) for kw in minor_keywords)
  for d in demos
 )
 if not has_minor:
  gaps.append('demographic:missing_minor_under_18')

 # 2. Elderly check
 elderly_keywords=('55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','65+','60+','70+','elderly','老年')
 has_elderly=any(
  any(kw in str(d.get('age_range','')) for kw in elderly_keywords)
  for d in demos
 )
 if not has_elderly:
  gaps.append('demographic:missing_elderly_55_plus')

 # 3. Non-urban check
 non_urban_types=('RURAL','TOWNSHIP')
 has_non_urban=any(
  str(d.get('location_type','')).upper() in non_urban_types
  for d in demos
 )
 if not has_non_urban:
  gaps.append('demographic:missing_non_urban_resident')

 # 4. Indifferent/bystander check
 indifferent_types=('INDIFFERENT','OFF_TOPIC')
 has_indifferent=any(
  str(d.get('topic_relevance','')).upper() in indifferent_types
  for d in demos
 )
 if not has_indifferent:
  gaps.append('demographic:missing_indifferent_or_bystander')

 # 5. Non-professional ordinary person >= 30%
 professional_keywords=('KOL','博主','自媒体','律师','专家','教授','教师','记者','编辑','分析师','顾问','官员','监管','评论员','主持人','导演','内容运营','公关','媒体')
 total=len(demos)
 if total>0:
  ordinary_count=0
  for d in demos:
   occ=str(d.get('occupation','')).lower()
   if not any(kw.lower() in occ for kw in professional_keywords):
    ordinary_count+=1
  ratio=ordinary_count/total
  if ratio<0.30:
   gaps.append(f'demographic:non_professional_ratio_too_low:{ordinary_count}/{total}={ratio:.0%}_need_>=30%')

 return gaps

def stance_balance_gaps(cards):
 """Check that the role pool has a balanced brand_stance distribution.

 Required:
 - At least max(2, floor(N*0.08)) roles with supporter stances (LOYAL_ENTHUSIAST or SATISFIED_REGULAR)
 - At least half of supporter roles must be non-affiliated ordinary users
 - HOSTILE_OPPOSITION + FORMERLY_LOYAL_ALIENATED <= 40%
 - INDIFFERENT ratio between 10% and 40%

 Returns a list of gap strings.
 """
 SUPPORTER_STANCES={'LOYAL_ENTHUSIAST','SATISFIED_REGULAR'}
 HOSTILE_STANCES={'HOSTILE_OPPOSITION','FORMERLY_LOYAL_ALIENATED'}
 PROFESSIONAL_KEYWORDS=('KOL','博主','自媒体','律师','专家','教授','教师','记者','编辑','分析师','顾问','官员','监管','评论员','主持人','导演','内容运营','公关','媒体','员工','雇员','competitor','brand','公司','企业')

 total=len(cards)
 if total==0:
  return ['stance_balance:no_roles_in_pool']

 gaps=[]

 # 1. Minimum supporter count
 supporter_count=sum(1 for c in cards if c.get('brand_stance','') in SUPPORTER_STANCES)
 min_supporters=max(2, total*8//100)
 if supporter_count<min_supporters:
  gaps.append(f'stance_balance:too_few_supporters:{supporter_count}/{total}_need_>={min_supporters}_LOYAL_ENTHUSIAST+SATISFIED_REGULAR')

 # 2. At least half of supporters must be non-affiliated ordinary users
 if supporter_count>0:
  ordinary_supporter_count=0
  for c in cards:
   if c.get('brand_stance','') not in SUPPORTER_STANCES:
    continue
   occ=str(c.get('demographic_profile',{}).get('occupation','')).lower()
   stake=str(c.get('stakeholder_relation','')).lower()
   is_affiliated=any(kw.lower() in occ for kw in PROFESSIONAL_KEYWORDS) or any(kw.lower() in stake for kw in ('employee','competitor','brand','brand_affiliated'))
   if not is_affiliated:
    ordinary_supporter_count+=1
  min_ordinary_supporters=(supporter_count+1)//2  # ceil(supporter_count/2)
  if ordinary_supporter_count<min_ordinary_supporters:
   gaps.append(f'stance_balance:supporters_too_affiliated:{ordinary_supporter_count}/{supporter_count}_ordinary_need_>={min_ordinary_supporters}')

 # 3. Maximum hostile ratio
 hostile_count=sum(1 for c in cards if c.get('brand_stance','') in HOSTILE_STANCES)
 hostile_ratio=hostile_count/total
 if hostile_ratio>0.40:
  gaps.append(f'stance_balance:too_many_hostile:{hostile_count}/{total}={hostile_ratio:.0%}_need_<=40%')

 # 4. INDIFFERENT ratio should be reasonable (10%-40%)
 indifferent_count=sum(1 for c in cards if c.get('brand_stance','')=='INDIFFERENT')
 indifferent_ratio=indifferent_count/total
 if indifferent_ratio<0.10:
  gaps.append(f'stance_balance:too_few_indifferent:{indifferent_count}/{total}={indifferent_ratio:.0%}_need_>=10%')
 elif indifferent_ratio>0.40:
  gaps.append(f'stance_balance:too_many_indifferent:{indifferent_count}/{total}={indifferent_ratio:.0%}_need_<=40%')

 return gaps

def diversity_gaps(cards):
 bps=[c.get('behavior_profile',{}) for c in cards]
 # Normalize values to uppercase for case-insensitive comparison (keys stay lowercase)
 def norm(bp):
  return {k:(v.upper() if isinstance(v,str) else v) for k,v in bp.items()}
 checks={
  'honest_extreme_counterexample': any(norm(b).get('extremity')=='EXTREME_STRESS_TEST' and norm(b).get('truthfulness_mode')=='HONEST' for b in bps),
  'moderate_nonhonest_counterexample': any(norm(b).get('extremity')=='MODERATE' and norm(b).get('truthfulness_mode') in {'SELECTIVE_FRAMING','EXAGGERATION_PRONE','RUMOR_RELAY','MIXED','FABRICATION_STRESS_TEST'} for b in bps),
  'reasoning_emotion_decoupling_counterexample': any((norm(b).get('reasoning_mode')=='ANALYTICAL' and norm(b).get('emotional_regulation') in {'REACTIVE','VOLATILE_STRESS_TEST'}) or (norm(b).get('reasoning_mode')=='EMOTIONAL' and norm(b).get('emotional_regulation')=='STABLE') for b in bps),
  'neutral_surface_can_deceive_counterexample': any(norm(b).get('extremity')=='MODERATE' and norm(b).get('deception_awareness')=='KNOWING_STRATEGIC' for b in bps),
 }
 gaps=[k for k,v in checks.items() if not v]
 gaps.extend(extremity_coverage(cards))
 gaps.extend(demographic_gaps(cards))
 gaps.extend(stance_balance_gaps(cards))
 return gaps
