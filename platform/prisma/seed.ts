import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const guardian = await prisma.source.upsert({
    where: { name: "The Guardian" },
    update: {},
    create: {
      name: "The Guardian",
      url: "https://www.theguardian.com",
      language: "EN",
      category: "gender",
    },
  });

  const thepaper = await prisma.source.upsert({
    where: { name: "澎湃新闻" },
    update: {},
    create: {
      name: "澎湃新闻",
      url: "https://www.thepaper.cn",
      language: "ZH",
      category: "society",
    },
  });

  const the19th = await prisma.source.upsert({
    where: { name: "The 19th" },
    update: {},
    create: {
      name: "The 19th",
      url: "https://19thnews.org",
      language: "EN",
      category: "gender_politics",
    },
  });

  const articles = [
    {
      title: "Taliban bans women from working for NGOs in Afghanistan",
      url: "https://example.com/taliban-ngo-ban",
      sourceId: guardian.id,
      language: "EN",
      content:
        "The Taliban government has ordered all national and international NGOs to stop female employees from coming to work. The ban follows a decision to bar women from attending universities. Women have been progressively stripped of rights since the Taliban retook power in August 2021, including being banned from secondary schools, parks, gyms, and public baths. The NGO ban directly threatens humanitarian operations as female workers are essential for reaching women and children in need.",
      excerpt: "Taliban orders NGOs to ban female employees from working, threatening humanitarian operations.",
      publishedAt: new Date("2026-02-15"),
    },
    {
      title: "South Korea's gender wage gap remains worst in OECD for 28th year",
      url: "https://example.com/korea-wage-gap",
      sourceId: the19th.id,
      language: "EN",
      content:
        "South Korea's gender pay gap stood at 31.2% in 2023, the worst among all 38 OECD member nations for the 28th consecutive year. The OECD average is 11.9%. Korean women earn on average only 68.8% of what men earn. The gap is attributed to career breaks for childbirth and childcare, occupational segregation, and the glass ceiling in promotions. Korea's total fertility rate dropped to 0.72 in 2023, the world's lowest, as women increasingly reject marriage and motherhood.",
      excerpt: "Korea's 31.2% gender pay gap persists as fertility drops to world's lowest at 0.72.",
      publishedAt: new Date("2026-03-01"),
    },
    {
      title: "男子持刀伤害前妻致死，曾多次被报警家暴",
      url: "https://example.com/jiangsu-domestic-violence",
      sourceId: thepaper.id,
      language: "ZH",
      content:
        "据报道，江苏某市一名男子持刀将前妻杀害。据邻居和受害者家属透露，该男子在婚姻存续期间多次对妻子实施家庭暴力，受害者曾多次报警，但每次警方仅进行口头调解后离开。离婚后，该男子多次跟踪骚扰前妻，受害者申请了人身安全保护令，但未能得到有效执行。事发当天，该男子破门而入，将前妻刺死。此案再次引发公众对家暴执法不力和人身保护令形同虚设的广泛讨论。",
      excerpt: "江苏男子持刀杀害前妻，此前多次家暴报警未被有效处理。",
      publishedAt: new Date("2026-03-05"),
    },
    {
      title: "Mexico records over 900 femicides in 2023 despite government promises",
      url: "https://example.com/mexico-femicide",
      sourceId: guardian.id,
      language: "EN",
      content:
        "Mexico's national statistics agency reported 901 femicides in 2023. Women's rights groups say the real number is higher as many cases are classified as homicides rather than femicides. An average of 10 women are killed daily in Mexico. Impunity remains rampant — less than 5% of femicide cases result in conviction. Protests under the banner 'Ni Una Menos' continue across the country.",
      excerpt: "901 femicides recorded in Mexico in 2023 with less than 5% conviction rate.",
      publishedAt: new Date("2026-02-20"),
    },
    {
      title: "Deepfake pornography targeting women surges 550% as AI tools proliferate",
      url: "https://example.com/deepfake-surge",
      sourceId: the19th.id,
      language: "EN",
      content:
        "Non-consensual deepfake pornography targeting women has increased 550% since 2019, with over 95% of all deepfake videos being pornographic and 90% targeting women. AI tools now allow anyone to create realistic fake nude images from a single clothed photo. South Korea, where the crisis is particularly severe, has seen thousands of cases involving school-age girls. Current laws in most countries are inadequate to address the problem.",
      excerpt: "Deepfake porn targeting women up 550% since 2019, 90% of victims are women.",
      publishedAt: new Date("2026-03-08"),
    },
  ];

  for (const articleData of articles) {
    const article = await prisma.article.upsert({
      where: { url: articleData.url },
      update: {},
      create: articleData,
    });

    if (articleData.url === "https://example.com/taliban-ngo-ban") {
      await prisma.analysis.upsert({
        where: { articleId: article.id },
        update: {},
        create: {
          articleId: article.id,
          violenceCategories: JSON.stringify(["direct", "structural", "cultural"]),
          galtungDirect: true,
          galtungStructural: true,
          galtungCultural: true,
          identityViolence: false,
          metaViolence: true,
          primalRaceAnalysis:
            "The Taliban's ban on female NGO workers exemplifies the Primal Race Theory's core mechanism: the systematic reduction of biological females to objects stripped of agency. This mirrors the original colonization pattern — make subject (Taliban male authority), make object (Afghan women), plunder object (strip labor rights, education, mobility). The biological wall is weaponized: women's biological functions are used as justification for their confinement.",
          coConspiracyAnalysis:
            "Afghan family units function as micro-patriarchal regimes where compliance is enforced through honor codes and physical threat. International silence operates as macro-level co-conspiracy — the \"naive evil\" of geopolitical pragmatism that prioritizes stability over women's survival.",
          existentialWarFraming:
            "Afghan women's existential war has been reduced to the most primitive stage: the fight for physical existence itself. Their expressions — working, learning, moving freely — are being systematically eliminated from public and private space.",
          severityScore: 10,
          summaryEn:
            "The Taliban's NGO employment ban represents a multi-layered act of violence operating across all three vertices of Galtung's triangle. Direct violence through threat of punishment, structural violence through institutional prohibition, and cultural violence through religious legitimization of female exclusion. This is meta-violence in its purest form — a regime that has monopolized the power to define women out of existence in public life.",
          summaryZh:
            "塔利班禁止女性为非政府组织工作，是横跨加尔通暴力三角所有顶点的多层暴力行为。直接暴力体现在惩罚威胁中，结构性暴力体现在制度性禁令中，文化暴力体现在宗教对女性排斥的合法化中。这是最纯粹形式的元暴力——一个垄断了将女性从公共生活中定义为不存在的权力的政权。",
          modelVersion: "seed-data",
        },
      });
    }

    if (articleData.url === "https://example.com/korea-wage-gap") {
      await prisma.analysis.upsert({
        where: { articleId: article.id },
        update: {},
        create: {
          articleId: article.id,
          violenceCategories: JSON.stringify(["structural", "cultural", "meta"]),
          galtungDirect: false,
          galtungStructural: true,
          galtungCultural: true,
          identityViolence: false,
          metaViolence: true,
          primalRaceAnalysis:
            "Korea's 31.2% pay gap is a textbook case of Violence = Potential - Actual. Korean women's economic potential is systematically suppressed through the motherhood penalty — their biological capacity for reproduction is weaponized against them in the labor market. The plummeting birth rate (0.72) represents women's rational response: refusing to let their biology be used as a tool of economic colonization.",
          coConspiracyAnalysis:
            "Korean corporate culture operates as a vast network of micro-patriarchal units where long working hours, mandatory drinking culture, and seniority systems were designed by and for men. Women who opt out of motherhood are stigmatized as selfish, while the system that punishes them for mothering remains unchallenged.",
          existentialWarFraming:
            "Korean women's mass rejection of marriage and motherhood is an unprecedented act of existential warfare — they are choosing biological separatism as their optimal expression, refusing to participate in units that systematically devalue them.",
          severityScore: 8,
          summaryEn:
            "South Korea's persistent gender pay gap operates as structural violence reinforced by cultural norms. The motherhood penalty converts women's biological capacity into economic disadvantage. Women's response — historically low marriage and fertility rates — represents a form of biological separatism, an existential war tactic of withdrawing from patriarchal units that exploit reproductive labor.",
          summaryZh:
            "韩国持续存在的性别薪资差距是由文化规范强化的结构性暴力。母职惩罚将女性的生育能力转化为经济劣势。女性的回应——历史最低的婚育率——代表着一种生物分离主义的存在性战争策略，即退出剥削生育劳动的父权制单元。",
          modelVersion: "seed-data",
        },
      });
    }

    if (articleData.url === "https://example.com/jiangsu-domestic-violence") {
      await prisma.analysis.upsert({
        where: { articleId: article.id },
        update: {},
        create: {
          articleId: article.id,
          violenceCategories: JSON.stringify(["direct", "structural"]),
          galtungDirect: true,
          galtungStructural: true,
          galtungCultural: false,
          identityViolence: false,
          metaViolence: false,
          primalRaceAnalysis:
            "此案完美展示了原初种族理论中的暴力蓝图：男性作为制造主体，将前妻制造为客体并实施终极掠夺——夺取生命。生物墙在此案中体现为致命的体能差异。警方的反复调解而非执法，暴露了制度本身作为男性中心叙事的结晶：家庭暴力被归类为'家务事'而非犯罪行为。",
          coConspiracyAnalysis:
            "警察系统作为宏观层面的共谋者，通过口头调解代替执法，实质性地参与了对受害者的系统性掠夺。人身安全保护令的形同虚设揭示了法律制度本身的共谋性质。",
          severityScore: 10,
          summaryEn:
            "A Jiangsu man stabbed his ex-wife to death after repeated domestic violence reports went unenforced. This case exemplifies the deadly convergence of direct violence (femicide) and structural violence (police inaction, unenforced protection orders). The biological wall — the physical power differential between male aggressor and female victim — proved fatal when institutional safeguards failed.",
          summaryZh:
            "江苏一名男子在多次家暴报警未被有效处理后持刀将前妻杀害。此案集中体现了直接暴力（杀害女性）与结构性暴力（警方不作为、保护令形同虚设）的致命交汇。生物墙——男性施暴者与女性受害者之间的体能差异——在制度性保障失败时证明是致命的。",
          modelVersion: "seed-data",
        },
      });
    }
  }

  console.log("Seed data inserted successfully.");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
