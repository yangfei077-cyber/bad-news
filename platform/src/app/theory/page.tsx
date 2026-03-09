import { GaltungTriangle } from "@/components/GaltungTriangle";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="mb-14">
      <h2 className="font-serif text-2xl font-bold mb-4 text-accent">
        {title}
      </h2>
      <div className="text-[15px] leading-relaxed text-foreground/80 space-y-4">
        {children}
      </div>
    </section>
  );
}

function ConceptCard({
  title,
  description,
  color,
}: {
  title: string;
  description: string;
  color: string;
}) {
  return (
    <div className={`border-l-2 ${color} pl-4 py-2`}>
      <h4 className="font-mono text-sm font-bold mb-1 text-foreground">
        {title}
      </h4>
      <p className="text-sm text-muted leading-relaxed">{description}</p>
    </div>
  );
}

export default function TheoryPage() {
  return (
    <div className="max-w-2xl mx-auto pb-12">
      <div className="mb-12">
        <h1 className="font-serif text-4xl font-bold tracking-tight mb-3">
          Theoretical Framework
        </h1>
        <p className="text-muted text-sm leading-relaxed">
          The Primal Race and the Architecture of Violence: From Galtung&apos;s
          Triangle to the Dissolution of Patriarchal Co-conspiracy
        </p>
      </div>

      <Section title="Core Thesis: Violence = Potential - Actual">
        <p>
          Based on Johan Galtung&apos;s &ldquo;Violence Triangle&rdquo;
          framework, this theory proposes the axiomatic definition{" "}
          <strong className="text-accent">
            &ldquo;Injustice is Violence&rdquo;
          </strong>
          . Violence is the gap between what a person could achieve and what they
          actually achieve — when that gap is caused by systemic forces.
        </p>
        <p>
          The <strong>Primal Race Theory</strong> holds that biological sex is
          the original racial construct. Women, as the first colonized group,
          underwent biological alteration and systematic plunder. Violence
          against women provided the blueprint for all subsequent racial
          constructs and violence.
        </p>
      </Section>

      <Section title="1. Galtung&rsquo;s Violence Triangle (Sexed Lens)">
        <div className="flex flex-col md:flex-row items-start gap-8 mb-6">
          <div className="flex-shrink-0 bg-stone-50 border border-border rounded-xl p-6 flex flex-col items-center">
            <GaltungTriangle direct structural cultural size={200} />
          </div>
          <div className="space-y-4">
            <ConceptCard
              title="Direct Violence"
              description="Physical harm — FGM, femicide, infanticide of girls, rape, domestic violence, physical assault. The visible tip of the iceberg."
              color="border-red-500"
            />
            <ConceptCard
              title="Structural Violence"
              description="Institutional/legal barriers — abortion bans, employment restrictions, pay gaps, educational denial, property rights denial. The water line."
              color="border-amber-500"
            />
            <ConceptCard
              title="Cultural Violence"
              description="Norms that legitimize — menstrual taboos, slut-shaming, beauty standards that strip physical power, romantic love as anesthetic. The deep current."
              color="border-yellow-500"
            />
          </div>
        </div>
        <p>
          The target of all violence forms is women&apos;s biological function:
          reproduction and sexuality. Data shows biological females are the
          absolute primary victims across all categories.
        </p>
      </Section>

      <Section title="2. New Violence: Identity Violence">
        <p>
          Social gender (Gender) is social construct. Biological sex (Sex) is
          biological fact. Queer theory&apos;s &ldquo;gender
          performativity&rdquo; correctly identifies gender as performance — but
          this applies only to the social layer.
        </p>
        <p>
          When transgender ideology is used to consolidate women-as-performance,
          it dissolves &ldquo;woman&rdquo; as a political category, stripping
          biological females of their only &ldquo;base&rdquo; in political
          struggle. You cannot perform chromosomes, menstrual pain, pregnancy, or
          menopausal bone loss. This dissolution is{" "}
          <strong className="text-purple-600">
            predatory or &ldquo;naive evil&rdquo;
          </strong>
          .
        </p>
        <div className="bg-stone-50 border border-border rounded-xl p-5 mt-4">
          <p className="text-[11px] font-mono text-muted uppercase tracking-widest mb-2">
            The Biological Wall
          </p>
          <p className="text-sm text-foreground/80">
            Phenotypic biological traits are the only identity expression that
            cannot be changed. Technology cannot alter gamete production logic,
            neuroendocrine history, genetically-determined basal metabolic
            baselines, or erase skeletal mechanical advantages from male puberty.
            The biological wall limits women&apos;s strength ceiling while
            constituting their survival floor.
          </p>
        </div>
      </Section>

      <Section title="3. Meta-Violence: Male-Centered Narratives">
        <p>
          Meta-violence is the{" "}
          <strong className="text-sky-600">violence above all violence</strong>.
          Male-centered narratives monopolize interpretation and meaning-making,
          controlling who gets to define reality. Under Primal Race Theory, it
          establishes the original model:
        </p>
        <div className="flex items-center gap-3 py-5 font-mono text-sm">
          <span className="bg-red-50 text-red-700 px-3 py-1.5 rounded-full border border-red-200">
            Make Subject
          </span>
          <span className="text-muted">&rarr;</span>
          <span className="bg-amber-50 text-amber-700 px-3 py-1.5 rounded-full border border-amber-200">
            Make Object
          </span>
          <span className="text-muted">&rarr;</span>
          <span className="bg-yellow-50 text-yellow-700 px-3 py-1.5 rounded-full border border-yellow-200">
            Plunder Object
          </span>
        </div>
        <p>
          This model predates color and class. It dominates identity politics,
          making it patriarchy&apos;s tool for total colonization of female
          living space, and extends to all exploitation, humiliation, and war.
        </p>
      </Section>

      <Section title="4. Co-conspirators Theory">
        <p>
          &ldquo;Micro-patriarchal regimes&rdquo; — any family, friendship, or
          social unit — crystallize society&apos;s male-centered narrative. Two
          key social anesthetics maintain their stability:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="bg-white border border-border rounded-xl p-5">
            <h4 className="font-mono text-sm font-bold mb-2 text-accent">
              Religion
            </h4>
            <p className="text-sm text-muted leading-relaxed">
              Provides cosmic justification for hierarchical units. Frames
              submission as virtue, suffering as divine purpose, and deviation as
              sin.
            </p>
          </div>
          <div className="bg-white border border-border rounded-xl p-5">
            <h4 className="font-mono text-sm font-bold mb-2 text-accent">
              Romantic Love
            </h4>
            <p className="text-sm text-muted leading-relaxed">
              Enchants the economic contract of family formation. Frames
              self-sacrifice as love, dependency as intimacy, and exit as
              failure.
            </p>
          </div>
        </div>
        <p className="mt-4">
          Many &ldquo;progressives&rdquo; merely despise the monotony of these
          anesthetics, not their male-centered essence. They embrace new
          &ldquo;sugar-coated bullets&rdquo; — transplanting enchantment onto
          manufactured progressive concepts while remaining violence initiators
          or co-conspirators.
        </p>
      </Section>

      <Section title="5. Existential War &amp; Expression">
        <p>
          All expression is political. People form races/tribes through
          expression. Races provide identity. Identity provides political
          meaning. Every act is a vote in the existential war — a zero-sum
          contest for narrative space, power seats, and attention in public and
          private spheres.
        </p>
        <p>
          The &ldquo;true optimal expression&rdquo; is the subjective will of
          the biological body — what your neurons decided before social
          conditioning intervened. Finding it requires: auditing desires planted
          by the Big Other (Lacan), capturing pre-conscious body signals
          (Libet), physical migration to environments that reward your genetic
          temperament, and practicing just expression toward others.
        </p>
      </Section>

      <Section title="6. Proposals">
        <div className="space-y-4">
          <div className="border border-accent/30 rounded-xl p-5 bg-accent-light">
            <h4 className="font-mono text-sm font-bold mb-2 text-accent">
              Ultimate Vision: Biological Separatism
            </h4>
            <p className="text-sm text-muted">
              Remove violence initiators through reproductive technology
              (IVG/parthenogenesis) to fundamentally restructure social units.
            </p>
          </div>
          <div className="border border-border rounded-xl p-5 bg-white">
            <h4 className="font-mono text-sm font-bold mb-2 text-foreground">
              Realistic Path: Just Units
            </h4>
            <p className="text-sm text-muted">
              Any Sex/Gender combination that inflicts zero violence internally
              or externally — that does not output the meta-violence of
              male-centered narratives — constitutes a non-patriarchal
              &ldquo;Just Unit.&rdquo;
            </p>
          </div>
        </div>
      </Section>
    </div>
  );
}
