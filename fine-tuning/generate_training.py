"""Generate training data for fine-tuning by using GPT-4o to analyze seed articles through the essay's framework."""

import json
import os
import sys
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ESSAY_PATH = Path(__file__).parent / "essay.md"
SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"
OUTPUT_PATH = Path(__file__).parent / "training_data.jsonl"

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text()
ESSAY_TEXT = ESSAY_PATH.read_text()

SEED_ARTICLES = [
    # === BATCH 3: 80 new diverse seed articles ===
    # ---- DIRECT VIOLENCE (EN) ----
    {
        "title": "Congo: UN documents mass rape as weapon of war in eastern provinces",
        "content": "A UN investigation in the Democratic Republic of Congo documents over 3,800 cases of conflict-related sexual violence in North Kivu and Ituri provinces in 2024 alone. Armed groups including M23 rebels, militia factions, and government soldiers all used rape systematically. Survivors describe being attacked during raids on villages, often in front of family members. Many victims were girls as young as 10. Medical facilities report treating an average of 40 rape survivors per day in Goma. Only 2% of documented cases have led to any form of prosecution. The UN special representative called the situation 'one of the most severe sexual violence crises on earth,' yet international media coverage remains minimal.",
    },
    {
        "title": "Australia's domestic violence crisis: one woman killed every 10 days",
        "content": "Australian Bureau of Statistics data reveals that intimate partner violence kills one woman approximately every 10 days. In 2024, 55 women were killed by current or former partners. A coronial inquest found that in 67% of cases, the victim had previously sought help from police or courts. The inquiry revealed systemic failures: police dismissing reports as 'domestics,' courts granting bail to high-risk offenders, and a chronic shortage of women's shelter beds — with an estimated 8,000 women turned away from refuges annually due to lack of capacity. Aboriginal and Torres Strait Islander women experience domestic violence at 11 times the rate of non-Indigenous women.",
    },
    {
        "title": "Guatemala femicide: 700 women killed in 2024, impunity rate exceeds 97%",
        "content": "Guatemala recorded 700 femicides in 2024, making it one of the deadliest countries in the world for women outside of active war zones. The Public Ministry reports that only 3% of femicide cases result in conviction. Forensic investigators are overwhelmed — a single team covers regions with millions of inhabitants. Many victims show signs of extreme brutality including torture and mutilation. Survivors of attempted femicide report that police refused to take their initial complaints seriously. Indigenous Maya women face additional barriers: courts often lack interpreters for Mayan languages, and rural areas have virtually no access to protective services.",
    },
    {
        "title": "Acid attacks in Bangladesh: 3,500 cases documented since 2000, most targeting young women",
        "content": "The Acid Survivors Foundation of Bangladesh has documented over 3,500 acid attack cases since 2000, with 70% of victims being women and girls. Common motives include rejected marriage proposals, land disputes, and family feuds where women are targeted as proxies. Despite a 2002 law imposing the death penalty for acid attacks, enforcement is inconsistent and attacks continue at approximately 100 per year. Survivors face lifelong disfigurement, blindness, and social ostracism. Access to reconstructive surgery is limited to a handful of specialists. Many survivors are abandoned by their families and unable to find employment due to stigma around their appearance.",
    },
    {
        "title": "Canada: inquiry into missing and murdered Indigenous women calls it genocide",
        "content": "Canada's National Inquiry into Missing and Murdered Indigenous Women and Girls concluded that the violence amounts to 'a race-based genocide of Indigenous peoples.' Indigenous women and girls are 12 times more likely to be murdered or go missing than non-Indigenous women. The inquiry documented over 1,200 cases but acknowledged the true number is far higher. Highway 16 in British Columbia, known as the 'Highway of Tears,' has been the site of dozens of disappearances dating back to the 1960s. Systemic factors include colonial policies that dismantled Indigenous family structures, chronic underfunding of on-reserve services, and documented police indifference to missing Indigenous women.",
    },
    # ---- STRUCTURAL VIOLENCE (EN) ----
    {
        "title": "Texas woman charged with murder after self-managed abortion using medication",
        "content": "A 26-year-old Texas woman was arrested and charged with murder after hospital staff reported her for a suspected self-managed abortion. She had reportedly obtained abortion pills online after being unable to travel to another state for the procedure. Though prosecutors eventually dropped the charge after public outcry, the arrest sent a chilling signal. Legal experts warn that post-Dobbs criminalization has created a surveillance environment where medical providers, pharmacists, and even internet search histories can become evidence. At least 14 states have introduced bills that would classify abortion as homicide. The woman spent three days in jail before making bail.",
    },
    {
        "title": "Afghanistan under Taliban: girls denied education for third consecutive year",
        "content": "September 2024 marked three years since the Taliban banned girls from attending secondary school. An estimated 1.4 million girls have been shut out of education. Underground schools operate in at least 15 provinces, with volunteer teachers risking imprisonment. The Taliban's Ministry of Vice and Virtue has conducted raids on at least 200 informal schools. UNESCO estimates that denying education to Afghan girls will cost the country's economy $5.4 billion over the coming decade. Mental health organizations report epidemic levels of depression, anxiety, and suicide among adolescent Afghan girls. Some families have sent daughters to Pakistan or Iran to continue schooling, creating a new refugee crisis.",
    },
    {
        "title": "Global report: 104 economies still legally restrict women from certain jobs",
        "content": "The World Bank's Women, Business and the Law 2024 report finds that 104 economies maintain legal restrictions on women's employment. In 18 countries, husbands can legally prevent wives from working. In 59 countries, no laws mandate equal pay for equal work. In 95 countries, women cannot work the same hours as men. In 75 countries, women face legal restrictions on working in specific industries including mining, manufacturing, and construction — ostensibly for 'protection.' Economists estimate these restrictions cost the global economy $172 trillion in lost human capital wealth. The report notes that at the current pace of reform, achieving legal gender equality will take another 50 years.",
    },
    {
        "title": "Indian women inherit only 1% of agricultural land despite farming 80% of food",
        "content": "Despite making up 80% of India's agricultural workforce, women own only 1% of agricultural land. Hindu succession laws were reformed in 2005 to grant equal inheritance rights, but enforcement remains virtually nonexistent. A survey by Oxfam India found that 86% of rural women were unaware they had legal rights to inherit land. Social pressure from male relatives ensures women 'voluntarily' relinquish claims. Without land titles, women cannot access government agricultural subsidies, bank loans, or crop insurance. During climate disasters, landless women farmers receive no direct government compensation. Activists call this 'the largest structural wealth transfer from women to men in history.'",
    },
    {
        "title": "European gender pension gap averages 30%: women retire into poverty",
        "content": "Eurostat data reveals that women in the EU receive pensions that are on average 30% lower than men's — a gap that has barely narrowed in a decade. In some countries the gap exceeds 40% (Netherlands, Austria, Germany). The cumulative effect of the gender pay gap, career breaks for caregiving, and part-time work creates what researchers call a 'pension penalty' that locks women into old-age poverty. Single elderly women are the most affected demographic: across the EU, 22% of women over 65 living alone are at risk of poverty, compared to 16% of men. Feminist economists argue pension systems were designed around a male breadwinner model that has never reflected women's working lives.",
    },
    {
        "title": "Nigeria: 20 million girls out of school, highest number globally",
        "content": "Nigeria has the highest number of out-of-school children in the world, with over 20 million — the majority being girls. In northern states, only 4% of girls complete secondary school. Factors include child marriage (44% of girls are married before 18), Boko Haram's decade-long targeting of girls' education, widespread poverty that forces families to prioritize sons' schooling, and a shortage of female teachers in conservative regions where families refuse to send daughters to male-taught classes. A girl in northern Nigeria is more likely to be married by age 15 than to be in a classroom. The economic cost is estimated at $7.6 billion in lost earnings annually.",
    },
    # ---- CULTURAL VIOLENCE (EN) ----
    {
        "title": "K-pop industry under fire as female idols' extreme diets and weight monitoring go public",
        "content": "A former K-pop trainee's viral testimony revealed that her agency mandated daily weigh-ins and required female trainees to maintain weights of 45kg or below regardless of height. Girls who gained weight were publicly humiliated and had their food rations cut. Multiple former idols have since disclosed eating disorders developed during training. An industry survey found that 73% of female K-pop idols reported disordered eating, compared to 31% of male idols. The ideal body promoted — extreme thinness, large eyes, small face, pale skin — is achievable only through severe caloric restriction and often cosmetic surgery. Critics argue the industry manufactures women's bodies as consumable products, with predominantly male executives and producers controlling every aspect of female artists' physical presentation.",
    },
    {
        "title": "Romance publishing booms as 'dark romance' featuring abuse normalizes partner violence",
        "content": "The 'dark romance' subgenre — featuring kidnapping, coercion, stalking, and sexual violence reframed as romantic — has become the fastest-growing category in book publishing, with revenues exceeding $800 million in 2024. TikTok's BookTok community drives sales, with tags like #DarkRomance accumulating 8 billion views. Researchers at the University of Buffalo found that frequent readers of romanticized-abuse narratives were 35% more likely to dismiss real-world partner violence warning signs. Authors and publishers defend the genre as 'fantasy' and 'female agency in exploring taboo.' Psychologists counter that repeatedly consuming narratives where women are brutalized but 'love conquers all' reinforces the cultural scaffolding that keeps real women trapped in violent relationships.",
    },
    {
        "title": "Bride price in sub-Saharan Africa: commodifying women's bodies in the 21st century",
        "content": "A comprehensive study across 12 sub-Saharan African countries found that bride price — payment from groom's family to bride's family — remains practiced in over 80% of marriages. Average payments range from $500 to $5,000, representing years of income for many families. Researchers found direct correlations between bride price and domestic violence: women whose bride price was high were 40% more likely to report being beaten, as husbands viewed the payment as conferring ownership. Women who attempt to leave marriages face demands to return the bride price, which their natal families often cannot afford. In Uganda, the Constitutional Court struck down bride price refund requirements in 2015, but the ruling is widely ignored. Economists describe the system as 'a market in women's reproductive and domestic labor.'",
    },
    {
        "title": "Instagram's impact on teen girls' mental health confirmed by leaked internal research",
        "content": "Internal Meta research leaked by whistleblower Frances Haugen confirmed that Instagram makes body image issues worse for one in three teenage girls. The documents revealed that 32% of teen girls said Instagram made them feel worse about their bodies, and among teens who reported suicidal thoughts, 13% in the UK and 6% in the US traced the feelings to Instagram. Meta's own researchers concluded that 'social comparison is worse on Instagram' because the platform's visual focus and algorithmic amplification of beauty content creates inescapable competition. Despite knowing this, Meta shelved a planned 'Kids Instagram' product without addressing core algorithmic harms. The platform's $120 billion annual ad revenue depends on maximizing engagement, which studies show is driven by content that triggers insecurity.",
    },
    {
        "title": "'Boy mom' culture on social media reinforces patriarchal family dynamics, experts warn",
        "content": "The 'boy mom' trend on TikTok and Instagram, with over 4 billion hashtag views, features mothers expressing obsessive devotion to sons in language typically reserved for romantic partners: 'he's the love of my life,' 'no girl will ever be good enough.' Child psychologists and gender researchers warn the trend normalizes emotional enmeshment between mothers and sons, positions future female partners as rivals, and perpetuates the patriarchal pattern where women's identity is defined through relationship to males. The trend conspicuously has no equivalent intensity for daughters. Critics note it enacts a form of co-conspiracy: mothers, often unconsciously, reproduce the male-centered narrative by centering their own identity on producing and nurturing a male heir.",
    },
    # ---- IDENTITY VIOLENCE (EN) ----
    {
        "title": "UK Labour proposes self-ID gender recognition: women's groups raise safety concerns",
        "content": "The UK Labour Party announced plans to simplify gender recognition through self-identification, removing the requirement for medical diagnosis. Women's rights organizations including the Women's Rights Network raised concerns about implications for single-sex spaces — prisons, rape shelters, hospital wards, and changing rooms. Data from countries with self-ID (including Canada and New Zealand) was cited, showing cases of male sex offenders transferring to women's prisons. Trans advocacy groups argue self-ID is essential for dignity and that safety concerns are statistically overblown. The debate has split feminist organizations, with some describing it as the most significant threat to sex-based rights since the Equality Act, while others see gender-critical positions as transphobic.",
    },
    {
        "title": "Transgender prisoner housed in women's facility convicted of sexually assaulting inmates",
        "content": "A transgender inmate at a New Jersey women's prison was convicted of sexually assaulting two female inmates. The individual, who had not undergone genital surgery, was transferred to the women's facility under a 2021 state policy allowing prisoners to be housed based on gender identity. The case has intensified debate over gender self-identification in prisons. Women's rights advocates argue it demonstrates the predictable consequences of housing biological males with female prisoners. Trans advocates maintain the case is exceptional and should not be used to justify blanket exclusion. The federal Bureau of Justice Statistics reports that transgender inmates face exceptionally high rates of assault regardless of housing, and notes the policy challenge of balancing competing safety needs.",
    },
    {
        "title": "Spain's 'trans law' leads to registered sex offenders legally changing gender to reduce sentences",
        "content": "Spain's 2023 transgender self-identification law, which allows legal gender change without medical requirements, has been exploited by at least 11 convicted sex offenders who changed their legal gender to female to access reduced sentences or transfer to women's prisons. The most publicized case involved a man convicted of sexually abusing his stepdaughter who legally became a woman after sentencing. Equality Minister Irene Montero, who championed the law, acknowledged the exploitation but argued it does not invalidate the law's purpose. Feminist organizations that had warned about potential abuse accused the government of prioritizing gender ideology over women's safety. The cases have fueled similar debates across Europe about the intersection of self-identification policies and sex-based legal protections.",
    },
    {
        "title": "Women's sports controversy deepens as transgender swimmer breaks 12 female records",
        "content": "Lia Thomas's participation in NCAA women's swimming reignited fierce debate when she broke 12 women's records. Sixteen of Thomas's teammates signed a letter supporting her participation, while others anonymously told reporters they felt unable to speak freely. Sport scientists published data showing that two years of testosterone suppression reduced but did not eliminate performance advantages from male puberty — including 9% advantages in grip strength, 12% in vertical jump, and retained skeletal advantages. The Riley Gaines advocacy movement has mobilized female athletes across multiple sports. The debate encapsulates a core tension: the concept of 'gender identity' in competition directly collides with the biological reality of sex-based physical differences that women's sport categories were created to address.",
    },
    # ---- META-VIOLENCE (EN) ----
    {
        "title": "Study reveals Hollywood films give male characters 2x more speaking time than female characters",
        "content": "A computational linguistics study analyzing 2,000 Hollywood films from 1990 to 2024 found that male characters receive an average of 68% of total dialogue, a ratio that has improved only marginally (from 72% in the 1990s). In action and sci-fi genres, the gap widens to 82/18. Even in films with female leads, male characters often speak more in aggregate. Women's dialogue is more likely to reference relationships and appearance, while men's dialogue dominates discussion of work, power, and abstract concepts. The study found a 'funnel effect': while more films now feature women leads, the supporting cast and overall narrative world remain overwhelmingly male. Researchers argue this reflects and reinforces what the essay's framework would call meta-violence — male-centered narratives controlling the space of representation itself.",
    },
    {
        "title": "Wikipedia's gender gap: only 19% of biographies are about women, editors are 87% male",
        "content": "A Wikimedia Foundation study reveals that only 19% of Wikipedia biographies are about women, despite women constituting half the world's population. The platform's editor base is 87% male. Female editors report hostile environments including dismissal of contributions about women's history, deletion of articles about notable women deemed 'not notable enough,' and harassment on talk pages. When volunteer editors attempted a systematic effort to add women scientists' biographies, several were flagged for deletion within hours by male editors citing insufficient notoriety. Researchers describe Wikipedia as a 'mirror and amplifier' of historical erasure: because traditional sources underrepresented women, Wikipedia's reliance on published sources perpetuates the gap while granting it the authority of an encyclopedia.",
    },
    {
        "title": "Male voices dominate 73% of news sources globally, Reuters Institute finds",
        "content": "The Reuters Institute's annual Digital News Report analyzing 200 media outlets across 46 countries found that men constitute 73% of news sources — people quoted, cited, or interviewed. In political reporting, men are 82% of sources; in economics, 79%; in sports, 92%. Only in health and education do women approach parity. Female journalists are more likely to cite women sources, but women constitute only 40% of journalists globally and hold only 27% of top management positions. The Institute noted a concerning trend: in coverage of women's issues specifically, male 'experts' are quoted more often than women with direct experience. This pattern ensures that even narratives about women are filtered through and authorized by male voices.",
    },
    {
        "title": "Incel movement linked to at least 60 deaths in mass attacks targeting women",
        "content": "A database compiled by researchers at the University of Toronto documents at least 60 deaths linked to the 'involuntary celibate' (incel) movement since 2014, including mass shootings and vehicle attacks. The movement's online ideology explicitly frames violence against women as justified retribution for sexual rejection. The 2014 Isla Vista attack killed 6; the 2018 Toronto van attack killed 10; the Plymouth UK shooting killed 5. Researchers found that incel forums (now spread across Telegram, Discord, and niche platforms after mainstream bans) have over 200,000 active users. Content analysis reveals systematic dehumanization of women, fantasies of sexual slavery, and tactical discussion of violence methods. Law enforcement agencies in the US, UK, and Canada have classified the movement as an emerging terrorist threat.",
    },
    {
        "title": "Manosphere pipeline: how YouTube recommends progressively extreme anti-feminist content",
        "content": "A joint study by NYU and the University of Exeter tracked 15,000 YouTube recommendation chains starting from mainstream fitness and self-improvement content targeted at men. Within an average of 8 clicks, 62% of chains led to content from figures like Andrew Tate, Fresh & Fit, or explicitly red-pill creators. The algorithm rewarded increasingly extreme content with higher engagement. Male viewers aged 14-24 showed the highest susceptibility. Content analysis revealed a structured narrative pipeline: (1) 'self-improvement' framing, (2) subtle gender grievance, (3) overt anti-feminism, (4) dehumanization of women, (5) advocacy for male dominance. Researchers noted the pipeline mirrors historical radicalization patterns of other extremist movements, with misogyny as the gateway ideology.",
    },
    # ---- CO-CONSPIRACY / COMPLEX (EN) ----
    {
        "title": "Evangelical churches and domestic violence: pastors routinely counsel women to stay with abusers",
        "content": "A LifeWay Research survey of 1,000 Protestant pastors found that while 87% said they would 'take domestic violence seriously,' only 54% said they had ever preached against it. A companion survey of churchgoing domestic violence survivors found that 73% reported their pastor counseled them to 'pray more,' 'submit better,' or 'give him another chance.' Only 17% were referred to a shelter or counselor. Theological justification for male headship — drawn from Ephesians 5:22-24 — was cited by survivors as the primary tool used to keep them in abusive marriages. Researchers found that religiously-involved women stay in abusive relationships an average of 2.4 years longer than non-religious women. Three women interviewed for the study disclosed that their pastors had told them directly that divorce was 'a greater sin than being beaten.'",
    },
    {
        "title": "Bollywood's 'item numbers': how India's film industry profits from objectifying women",
        "content": "An analysis of 500 Bollywood films from 2010-2024 found that 78% featured at least one 'item number' — a song-and-dance sequence that exists solely to display a sexualized female body, unconnected to the plot. The term 'item' literally reduces the woman to a commodity. These sequences are major revenue generators: they drive streaming views, social media engagement, and are played at weddings and events. Female actors report immense pressure to participate, with refusal leading to being blacklisted. Researchers at JNU found that areas with high consumption of item-number content showed statistically higher rates of street harassment. The industry — 93% male-directed — frames these sequences as 'celebrating female sexuality.' Critics counter that male directors choreographing female bodies for male audiences is textbook objectification laundered through the language of empowerment.",
    },
    {
        "title": "Women who report workplace sexual harassment face retaliation 75% of the time, EEOC finds",
        "content": "An EEOC study analyzing 10 years of workplace sexual harassment complaints found that 75% of women who formally reported harassment experienced some form of retaliation — including demotion, schedule changes, social ostracism, and termination. Only 6% of complaints resulted in any consequence for the perpetrator. The study found that in 70% of cases, the harasser was in a supervisory position over the victim. Industries with the highest harassment rates were food service (40%), hospitality (35%), and healthcare (28%). Post-#MeToo, formal complaints actually declined by 15%, which researchers attribute not to reduced harassment but to increased fear of retaliation after watching high-profile accusers face career destruction. The study concluded that organizational structures overwhelmingly protect harassers because their departure would be costlier to the institution than the complainant's.",
    },
    {
        "title": "China's blind marriage market: parents trade daughters' profiles seeking highest-bidder grooms",
        "content": "In Shanghai's People's Park and similar 'marriage markets' in over 30 Chinese cities, parents display their children's biographical details on paper sheets or umbrellas, negotiating potential matches. Investigations reveal stark gender asymmetry: daughters' listings emphasize appearance, age (with value declining sharply past 27), and domestic skills, while sons' listings highlight property ownership, salary, and family background. Researchers interviewed 500 participating parents and found that 78% of mothers described their daughters in transactional terms — as assets to be 'matched' for maximum family benefit. The phenomenon reflects what scholars call the commodification of daughters within micro-patriarchal family units, where parents — including mothers — act as co-conspirators in a marriage market structured entirely around male-centered criteria of female worth.",
    },
    {
        "title": "Military sexual assault: Pentagon report shows 29,000 service members assaulted in one year",
        "content": "The Pentagon's annual report on sexual assault in the military estimated that approximately 29,000 service members experienced unwanted sexual contact in fiscal year 2023, yet only 8,942 reports were filed — a reporting rate of roughly 31%. Of those reported, only 5% resulted in conviction. Female service members are assaulted at six times the rate of male members. The report found that 62% of women who reported assault faced professional or social retaliation, including being transferred, passed over for promotion, or involuntarily discharged. A 'command climate' was identified where male unit cohesion took precedence over individual women's safety. Independent investigators found that in some units, reporting assault was treated as a greater offense than committing it, viewed as damaging to unit morale.",
    },
    # ---- CHINESE ARTICLES ----
    {
        "title": "丰县铁链女事件：被拐卖妇女的系统性失声",
        "content": "2022年初，江苏丰县一名被铁链锁在棚中的八孩母亲的视频引爆网络。调查最终确认该女性为云南被拐卖的小花梅，已被非法拘禁超过20年。事件暴露了中国农村地区买卖妇女的系统性问题：地方政府最初发布四份前后矛盾的官方通报试图掩盖真相，村干部和邻居对女性被囚禁状态长期知情不报，当地医院在为其接生八次时未报告任何异常。此案引发了关于中国被拐卖妇女真实数量的全国讨论——据学者估计，改革开放以来有数十万女性被拐卖至农村地区'做妻子'。最终，多名地方官员被免职，但活动人士指出，系统性的解救行动仍未展开。",
    },
    {
        "title": "中国职场性骚扰：超六成女性遭遇过，不到1%正式投诉",
        "content": "中国全国妇联与北京师范大学联合发布的调查报告显示，超过60%的中国职业女性表示在工作中遭受过不同形式的性骚扰，包括不当言语、身体触碰和利用职权交换性要求。然而，只有不到1%的受害者进行了正式投诉或法律诉讼。主要原因包括：举证困难（中国法律要求受害者自行收集证据）、担心职业报复、缺乏有效的企业内部投诉机制、以及社会文化中对性骚扰的轻描淡写——如'他就是开个玩笑'、'你太敏感了'。2021年通过的《民法典》首次对性骚扰进行了法律定义，但缺乏配套的实施细则。法学家指出，目前的法律框架将反性骚扰的责任放在了受害者身上，而非雇主。",
    },
    {
        "title": "东南亚跨国婚姻产业链：越南新娘的买卖与困境",
        "content": "尽管多国法律禁止跨国婚姻中介的商业化运作，东南亚跨国婚姻产业链仍然蓬勃发展。来自韩国、中国台湾和中国大陆的中介机构组织'新娘团'前往越南、柬埔寨等国'选妻'，整个过程如同商品交易：男方支付1万至3万美元，中介安排数十名女性排列供'客户'挑选，从见面到结婚最快仅需一周。调查发现，许多越南新娘来自极度贫困的家庭，对目的国语言文化一无所知。到达后，她们面临的常见遭遇包括：护照被没收、家庭暴力、被迫为丈夫全家从事无偿劳动、以及在不满意时被'退货'遣返。韩国政府数据显示，跨国婚姻家庭的家暴率是本国婚姻的2.7倍。",
    },
    {
        "title": "中国反家暴法实施八年：人身安全保护令签发率不足申请量的三分之一",
        "content": "中国2016年施行的《反家庭暴力法》规定了人身安全保护令制度，但最高人民法院数据显示，截至2024年，全国法院签发的人身安全保护令仅约15,000份，而全国妇联每年接到的家暴投诉超过50万件。法官拒绝签发的常见理由包括'证据不充分'（伤情照片、报警记录被认为不够）、'夫妻之间的事需要调解'。即使签发了保护令，违反保护令的处罚上限仅为1000元罚款和15日拘留，对施暴者几乎没有威慑力。基层法院的一项内部调查显示，72%的法官认为家庭纠纷应以调解为主，'保护令是最后手段'。与此同时，全国仅有1,000余家家暴庇护所，大部分利用率极低，因为地址公开且缺乏配套的就业和心理支持。",
    },
    {
        "title": "女性游戏玩家遭受系统性骚扰：85%报告曾因性别被攻击",
        "content": "中国音数协游戏工委和北大联合调查显示，中国女性游戏玩家已达3.3亿，占总玩家数的48%。然而，85%的女性玩家报告曾在游戏中因性别遭受骚扰，包括语音侮辱、性暗示、被故意坑害或被踢出队伍。在竞技类游戏中，使用女性语音的玩家被队友恶意举报的概率是男性的4倍。直播平台上的女性游戏主播面临更为恶劣的环境：弹幕中充斥着外貌评价和性骚扰言论，部分平台算法会优先推荐'擦边'内容而非女性玩家的高水平操作。游戏公司的应对措施通常仅限于'举报-封禁'的被动模式，缺乏对游戏社区文化的主动引导。业内人士指出，游戏产业的男性主导（中国游戏公司高管中女性占比不足8%）是问题的根源。",
    },
    {
        "title": "印尼童婚危机：每年约34万未成年女孩被迫结婚",
        "content": "印度尼西亚是全球童婚率第八高的国家，每年约有34万名18岁以下女孩结婚。尽管2019年印尼将法定结婚年龄从16岁提高到19岁，但法律允许家长通过宗教法庭申请豁免。2023年数据显示，宗教法庭批准了95%的未成年婚姻豁免申请。童婚的主要驱动因素包括：贫困（嫁女儿意味着减少一张吃饭的嘴）、对婚前怀孕的道德恐慌、自然灾害后家庭经济崩溃、以及将女儿视为经济资产的父权文化。已婚未成年女孩辍学率达89%，产科并发症发生率是成年女性的2倍。",
    },
    {
        "title": "阿富汗女性自焚率飙升：绝望之下的极端选择",
        "content": "联合国驻阿富汗援助团报告指出，塔利班统治下阿富汗女性自焚率较2020年上升了300%以上。赫拉特省是重灾区，当地医院烧伤科的患者中超过80%为女性，其中大部分为自焚。医疗工作者表示，许多受害者在弥留之际透露了原因：被强迫婚姻、遭受严重家庭暴力后无法离婚、被禁止工作和上学后感到绝望。自焚被认为是唯一可以在文化上被'接受'的自杀方式——因为它可以被伪装成'厨房事故'。国际救援组织在阿富汗的心理健康项目已基本被塔利班关停，尤其是面向女性的心理援助。",
    },
    {
        "title": "网约车安全：中国多起女乘客遇害案暴露出行平台安全漏洞",
        "content": "自2018年两起轰动全国的滴滴顺风车女乘客遇害案以来，中国出行平台先后推出了紧急求助、行程分享、录音录像等安全功能。然而后续仍有多起女性乘客遭遇侵害的案件发生。2024年的调查显示，32%的女性表示在独自乘坐网约车时感到不安全，夜间这一比例上升至56%。司机端的审核漏洞仍然存在：部分平台允许未通过全面背景调查的司机接单。更深层的问题是，每当女性乘客遇害事件曝光，社会舆论中总会出现'为什么那么晚还坐车''为什么穿那么少'等受害者有罪论，将出行安全的责任从平台和犯罪者转嫁给女性自身。",
    },
    {
        "title": "全球每年超5万名女性被亲属以'荣誉'之名杀害",
        "content": "联合国人口基金最新估计，全球每年有超过5万名女性被家庭成员以'维护家庭荣誉'为名杀害，真实数字可能更高。所谓'荣誉'杀人主要集中在南亚、中东和北非地区，但在全球移民社区中也有发生。'触犯荣誉'的行为包括：拒绝包办婚姻、与家人不认可的对象交往、要求离婚、甚至仅仅是与男性交谈。在某些国家，荣誉杀人的凶手可获得减刑或免罪。约旦刑法直到2017年才废除了荣誉杀人的减刑条款。联合国妇女署指出，荣誉杀人的本质是将女性身体视为家族（特别是男性成员）'财产'的产物——女性的性自主被视为对男性'所有权'的侵犯。",
    },
    {
        "title": "代孕合法化争议：格鲁吉亚成为欧洲代孕工厂",
        "content": "乌克兰战争爆发后，大量国际代孕需求转向格鲁吉亚，使这个南高加索小国成为'欧洲代孕工厂'。目前格鲁吉亚每年约有800至1000例商业代孕，代孕母亲获得的报酬为1.5万至2万美元，而中介机构向客户收取5万至8万美元。调查发现，几乎所有代孕母亲来自经济困难家庭，40%为单身母亲。合同条款严苛：代孕母亲在怀孕期间不得与丈夫发生性关系、不得旅行、饮食和作息受到监控。如果胎儿被检测出缺陷，客户有权要求终止妊娠而无需代孕母亲同意。女权组织批评这是'子宫殖民主义'——沿阶级和国族线对女性生育劳动的系统性榨取。",
    },
    {
        "title": "全球'厌女杀人'(misogynist extremism)被正式列为恐怖主义威胁",
        "content": "继加拿大、英国和新西兰之后，澳大利亚安全情报组织(ASIO)正式将'厌女极端主义'列为恐怖主义威胁类别。这一决定源于不断增长的数据：自2014年以来，全球至少有13起大规模暴力事件与'非自愿独身'(incel)意识形态直接相关，造成超过80人死亡。ASIO局长表示，仇恨女性的极端主义与其他恐怖主义有着相同的激进化模式：在线社群中的去人化叙事、暴力正当化、以及从线上转向线下行动的明确路径。安全专家指出，与其他极端主义不同的是，厌女暴力长期以来被归类为'精神健康问题'或'感情纠纷'而非意识形态暴力，这本身就是男性中心叙事下暴力被系统性地轻描淡写的表现。",
    },
    {
        "title": "泰国商业性剥削：被包装为'旅游业'的系统性性交易",
        "content": "国际正义使命组织(IJM)报告指出，泰国性产业每年产值估计120亿至140亿美元，约有30万名性工作者，其中相当比例为人口贩卖受害者。尽管泰国法律禁止卖淫，但执法形同虚设——据调查，70%的曼谷警区与性产业场所存在'保护费'关系。性旅游是泰国旅游业的一个重要但被官方否认的组成部分。研究发现，进入性产业的女性平均年龄为15岁，80%来自泰国东北部贫困省份或缅甸、老挝、柬埔寨等邻国。'酒吧女郎'的叙事常被浪漫化——西方男性与泰国女性的'爱情故事'遍布旅游博客和纪录片——掩盖了贫困、性别不平等和殖民性欲望的结构性根源。",
    },
    {
        "title": "中国农村留守妇女：超5000万女性独自支撑家庭与农业",
        "content": "中国社会科学院研究显示，随着农村男性大规模进城务工，全国约有5000万至6000万留守妇女独自承担农业劳作、赡养老人和抚育子女的重任。她们平均每天劳动12小时以上，年收入不足丈夫外出务工收入的三分之一。调查发现，留守妇女的抑郁症发病率是城市女性的3.5倍，遭受家庭暴力的比例高达38%（施暴者包括返家的丈夫和公婆）。更深层的问题在于，农村土地承包经营权通常登记在男性户主名下，离婚后女性往往'净身出户'。这些女性支撑着中国粮食生产的半壁江山，却在经济统计中被归为'无业'或'家属'。",
    },
    {
        "title": "女性记者在线暴力：73%报告遭受过与性别相关的网络攻击",
        "content": "联合国教科文组织和国际记者联合会调查显示，全球73%的女性记者表示曾遭受过与性别相关的网络暴力，包括死亡威胁(25%)、强奸威胁(18%)和人肉搜索(12%)。针对女性记者的网络暴力通常具有性化特征——对男性记者的攻击多针对其专业能力，而对女性记者的攻击几乎必然涉及外貌评判、性羞辱或人身安全威胁。调查报道、政治新闻和性别议题领域的女记者受害最严重。30%的受访者表示因网络暴力进行了自我审查——回避某些敏感话题或降低个人曝光度。20%考虑过离开新闻业。报告指出，对女性记者的系统性网络暴力正在有效地压缩女性在公共信息空间的存在。",
    },
    {
        "title": "IVF商品化：卵子捐赠产业中年轻女性的健康风险被隐瞒",
        "content": "随着全球IVF产业规模突破250亿美元，对卵子捐赠者的需求急剧增长。调查发现，美国、西班牙和乌克兰等主要卵子交易市场中，中介机构系统性地低估了取卵手术的健康风险。卵巢过度刺激综合征(OHSS)的发生率在5%-10%，严重者可导致血栓、肾衰竭甚至死亡。但捐赠者签署的同意书中通常将此描述为'极罕见'。常青藤大学校园是招募的重点区域——年轻、健康、'基因优质'的女性卵子售价可达5万美元以上。然而，捐赠者的长期健康追踪几乎不存在。生殖医学伦理学家指出，这是一个典型的阶级化剥削结构：富裕夫妇(多为推迟生育的职场女性)购买贫困年轻女性的生育细胞，中间环节由男性主导的医疗资本攫取超额利润。",
    },
    {
        "title": "沙特女权活动人士卢贾因·赫苏尔出狱后仍遭旅行禁令和监控",
        "content": "沙特女权活动人士卢贾因·赫苏尔(Loujain al-Hathloul)在服刑近三年后于2021年获释，但至今仍被禁止出境。她曾因争取女性驾车权和废除男性监护制度而入狱，在狱中遭受酷刑和性虐待。讽刺的是，沙特政府在她入狱期间通过了她所倡导的改革——允许女性驾车和独立旅行。她的案例揭示了威权体制下女权运动的困境：国家可以选择性地推行改革以换取国际形象，同时惩罚倡导者以确保改革被框定为'国王的恩赐'而非民众的权利。这种叙事控制确保了改革的定义权掌握在男性统治者手中。",
    },
    {
        "title": "拉丁美洲'粉色浪潮'：女性领导人执政后性别暴力却未显著下降",
        "content": "拉丁美洲近年迎来'粉色浪潮'——多国选出女性国家领导人，包括墨西哥总统克劳迪娅·谢因鲍姆。然而数据显示，女性领导人执政并未带来性别暴力的显著下降。墨西哥2024年的femicide数据与前任男性总统执政时期持平。学者分析指出，女性领导人面临双重困境：她们必须在男性主导的政治系统中运作，而该系统的权力结构本身就是暴力的源头。一些女性领导人为了政治生存而回避激进的性别改革，甚至在执政风格上刻意展现'强硬'和'去性别化'以获得男性权力精英的认可。这说明，单纯的代表性政治(representation)无法解决结构性暴力——问题不在于谁坐在那个位子上，而在于那个位子本身的权力逻辑。",
    },
    {
        "title": "韩国4B运动扩展至全球：年轻女性拒绝约会、性行为、婚姻和生育",
        "content": "韩国的'4B运动'(비혼·비연애·비성관계·비출산，即不婚、不恋爱、不发生性关系、不生育)正从韩国扩展到日本、中国和西方国家。该运动起源于2019年，作为对韩国极端性别不平等的回应——全球最大的性别薪资差距、泛滥的偷拍犯罪(molka)和根深蒂固的家庭性别分工。参与者将这四项拒绝视为'对父权制最有效的不合作运动'。韩国统计厅数据显示，20-39岁女性中只有33%认为婚姻是必要的，较2010年的47%大幅下降。社会学家将4B运动解读为女性在存在性战争中选择了最根本的退出策略：通过拒绝进入微型父权政权(家庭)来切断对父权制的生物学供给。批评者称这是'极端主义'，支持者则反驳说，真正极端的是迫使女性做出这种选择的社会本身。",
    },
    {
        "title": "哈佛研究：约会App算法系统性地贬低女性价值并加速商品化",
        "content": "哈佛商学院的一项研究分析了Tinder、Bumble和Hinge的推荐算法，发现这些算法使用的'吸引力评分'系统性地对女性用户不利。男性用户倾向于对大量女性'右滑'（喜欢），而女性更具选择性。算法将男性的无差别'右滑'解读为这些女性吸引力低（因为被认为'容易获得'），同时将少数获得选择性男性点赞的女性推到更高位置。结果是：大多数女性的可见度被系统性地降低，而男性用户体验被优先照顾。约会App的商业模式依赖于男性的持续付费和参与。研究者指出，这些平台本质上是将亲密关系市场化的男性视角产物——女性被算法评判、排序和展示，就像商品在货架上被标价。",
    },
    {
        "title": "联合国报告：气候变化对女性影响不成比例，80%气候难民为女性",
        "content": "联合国环境规划署报告指出，全球气候难民中约80%为女性和儿童。在气候灾害中，女性的死亡率比男性高14倍——部分原因是在许多文化中女性不被允许学习游泳、独自外出或做出疏散决定。在干旱和洪水过后，女性和女孩承担取水重任，每天可能步行数小时；在气候导致的粮食短缺中，'女性最后吃'的文化规范导致女性营养不良率更高。气候迁移还导致了童婚和性暴力的急剧增加——贫穷家庭通过嫁女换取彩礼作为生存策略。然而，全球气候决策机构中女性仅占33%，气候融资中仅有0.01%明确针对性别平等。",
    },
    {
        "title": "英国女性无家可归者激增40%，家暴是首要原因",
        "content": "英国慈善机构Shelter的数据显示，英格兰无家可归女性人数在过去五年增长了40%，达到约12万人。家庭暴力是女性失去住所的首要原因，占45%。许多女性在逃离暴力伴侣后发现自己无处可去——全国女性庇护所的空位率仅为30%，每年约有15,000名女性被庇护所拒之门外。流落街头的女性面临极高的性暴力风险：调查显示，90%的无家可归女性曾遭受某种形式的暴力或虐待。然而，无家可归服务的设计长期以男性为中心——混合性别庇护所中女性经常遭受骚扰，而专门针对女性的服务资金持续被削减。活动人士指出，女性无家可归的根本原因是经济依赖——当离开暴力关系意味着失去住所时，'留下'成为了一种被迫的最优解表达。",
    },
    {
        "title": "日本'JK产业'：以高中女生为卖点的合法灰色地带",
        "content": "日本的'JK产业'(JK=joshi kōsei，女高中生)每年产值估计超过30亿日元。这一产业以未成年或刚成年的女孩为中心，提供'散步约会'(JK散歩)、'拍照会'、'耳掏'(耳朵清洁服务)等名义上合法的服务，但频繁成为性剥削的入口。东京都曾试图立法规制但遭到行业游说阻止。受害者援助组织Colabo的调查发现，参与JK产业的女孩中62%最终被引诱进入性交易，84%存在家庭问题（父母离异、虐待或经济困难）。该产业的文化基础是日本社会对'女子高生'(高中女生)形象的系统性性化——从动漫、广告到时尚，少女的身体和制服被不断地包装为'可消费的天真'。这种文化暴力使得对未成年女性的商业化剥削被正常化为'日本独特的文化'。",
    },
    {
        "title": "全球女性割礼新趋势：'医疗化FGM'在印尼和马来西亚蔓延",
        "content": "世界卫生组织警告，女性生殖器切割(FGM)的'医疗化'趋势正在东南亚蔓延。在印尼，一项全国调查显示约49%的14岁以下女孩经历过某种形式的FGM，其中越来越多由受过训练的医务人员在诊所中执行——而非传统方式。马来西亚的情况类似，约90%的马来族女性经历过FGM。'医疗化'被一些宗教领袖和政府官员描述为'更安全的折中方案'，但WHO明确表示任何形式的FGM都是对女性人权的侵犯，即使是所谓'象征性'的穿刺也不例外。研究表明，'医疗化FGM'不但没有减少实施量，反而通过赋予其'科学'和'卫生'的包装而增加了社会接受度——文化暴力借医学权威的外衣获得了更强的合法性。",
    },
    {
        "title": "人工智能招聘工具被发现系统性歧视女性候选人",
        "content": "麻省理工学院和哈佛大学的联合研究发现，全球500强企业使用的主流AI招聘工具对女性候选人存在系统性偏见。分析了来自Amazon、HireVue和Pymetrics等平台的算法后，研究者发现：使用关键词筛选的系统会降低包含'maternity'(产假)、'women's'(女性的)等词汇的简历评分；视频面试AI系统对较低音调（男性典型音调）给予更高的'领导力'评分；基于历史数据训练的模型复制了过去的招聘偏见。在一次对照实验中，完全相同的简历在名字改为女性后，被AI推荐进入下一轮的概率下降了32%。这些工具被超过75%的财富500强公司使用，每年筛选数亿份申请——技术不但没有消除人类偏见，反而以'客观'和'数据驱动'的名义将偏见自动化和规模化了。",
    },
]


def generate_single(article: dict) -> dict | None:
    """Use GPT-4o with full essay context to generate a training example."""
    essay_context = f"""You have deeply internalized the following theoretical essay. Use it as your analytical foundation:

{ESSAY_TEXT}

---

Now analyze the following news article through this framework. Your analysis should feel natural and deeply informed by the theory, not like a mechanical checklist. Return your analysis as a JSON object with these fields: violence_categories (array), galtung_mapping (object with direct/structural/cultural booleans), identity_violence (bool), meta_violence (bool), primal_race_analysis (string), co_conspiracy_analysis (string or null), existential_war_framing (string or null), severity_score (int 1-10), summary_en (string), summary_zh (string)."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": essay_context},
                {
                    "role": "user",
                    "content": f"Title: {article['title']}\n\nContent: {article['content']}",
                },
            ],
            temperature=0.4,
            max_tokens=2500,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        result = json.loads(raw)

        required = ["violence_categories", "severity_score", "summary_en", "summary_zh"]
        if not all(k in result for k in required):
            print(f"  Missing fields in response for: {article['title'][:50]}")
            return None

        return result
    except Exception as e:
        print(f"  Error: {e}")
        return None


def main():
    print(f"Generating training data from {len(SEED_ARTICLES)} seed articles...")
    print(f"Using essay: {ESSAY_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    examples = []
    for i, article in enumerate(SEED_ARTICLES):
        print(f"[{i+1}/{len(SEED_ARTICLES)}] {article['title'][:60]}...")
        result = generate_single(article)
        if result is None:
            print("  SKIPPED (error)")
            continue

        training_example = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Title: {article['title']}\n\nContent: {article['content']}",
                },
                {"role": "assistant", "content": json.dumps(result, ensure_ascii=False)},
            ]
        }
        examples.append(training_example)
        print(f"  OK (severity: {result.get('severity_score', '?')}, categories: {result.get('violence_categories', [])})")

    with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"\nGenerated {len(examples)} training examples -> {OUTPUT_PATH}")
    print("NOTE: For best fine-tuning results, aim for 80-120 examples.")
    print("Run this script multiple times with different seed articles,")
    print("or manually curate and expand the training data.")


if __name__ == "__main__":
    main()
