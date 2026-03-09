import { GaltungTriangle } from "@/components/GaltungTriangle";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="mb-12">
      <h2 className="text-xl font-bold mb-4 text-accent">{title}</h2>
      <div className="text-sm leading-relaxed text-foreground/80 space-y-3">
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
      <h4 className="font-mono text-sm font-bold mb-1">{title}</h4>
      <p className="text-xs text-muted leading-relaxed">{description}</p>
    </div>
  );
}

export default function TheoryPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-12">
        <h1 className="text-3xl font-bold tracking-tight mb-2">
          Theoretical Framework
        </h1>
        <p className="text-muted text-sm">
          The Primal Race and the Architecture of Violence: From Galtung&apos;s
          Triangle to the Dissolution of Patriarchal Co-conspiracy
        </p>
      </div>

      {/* Core Thesis */}
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

      {/* Galtung's Triangle */}
      <Section title="1. Galtung's Violence Triangle (Sexed Lens)">
        <div className="flex flex-col md:flex-row items-start gap-8 mb-6">
          <div className="flex-shrink-0 bg-card border border-border rounded-lg p-6 flex flex-col items-center">
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
              color="border-orange-500"
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

      {/* Identity Violence */}
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
          <strong className="text-purple-400">
            predatory or &ldquo;naive evil&rdquo;
          </strong>
          .
        </p>
        <div className="bg-card border border-border rounded-lg p-4 mt-4">
          <p className="text-xs font-mono text-muted uppercase tracking-widest mb-2">
            The Biological Wall
          </p>
          <p className="text-sm">
            Phenotypic biological traits are the only identity expression that
            cannot be changed. Technology cannot alter gamete production logic,
            neuroendocrine history, genetically-determined basal metabolic
            baselines, or erase skeletal mechanical advantages from male puberty.
            The biological wall limits women&apos;s strength ceiling while
            constituting their survival floor.
          </p>
        </div>
      </Section>

      {/* Meta-Violence */}
      <Section title="3. Meta-Violence: Male-Centered Narratives">
        <p>
          Meta-violence is the{" "}
          <strong className="text-cyan-400">violence above all violence</strong>
          . Male-centered narratives monopolize interpretation and
          meaning-making, controlling who gets to define reality. Under Primal
          Race Theory, it establishes the original model:
        </p>
        <div className="flex items-center gap-3 py-4 font-mono text-sm">
          <span className="bg-red-900/30 text-red-400 px-3 py-1 rounded">
            Make Subject
          </span>
          <span className="text-muted">&rarr;</span>
          <span className="bg-orange-900/30 text-orange-400 px-3 py-1 rounded">
            Make Object
          </span>
          <span className="text-muted">&rarr;</span>
          <span className="bg-yellow-900/30 text-yellow-400 px-3 py-1 rounded">
            Plunder Object
          </span>
        </div>
        <p>
          This model predates color and class. It dominates identity politics,
          making it patriarchy&apos;s tool for total colonization of female
          living space, and extends to all exploitation, humiliation, and war.
        </p>
      </Section>

      {/* Co-conspirators */}
      <Section title="4. Co-conspirators Theory">
        <p>
          &ldquo;Micro-patriarchal regimes&rdquo; — any family, friendship, or
          social unit — crystallize society&apos;s male-centered narrative. Two
          key social anesthetics maintain their stability:
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="bg-card border border-border rounded-lg p-4">
            <h4 className="font-mono text-sm font-bold mb-2 text-accent">
              Religion
            </h4>
            <p className="text-xs text-muted">
              Provides cosmic justification for hierarchical units. Frames
              submission as virtue, suffering as divine purpose, and deviation as
              sin.
            </p>
          </div>
          <div className="bg-card border border-border rounded-lg p-4">
            <h4 className="font-mono text-sm font-bold mb-2 text-accent">
              Romantic Love
            </h4>
            <p className="text-xs text-muted">
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

      {/* Existential War */}
      <Section title="5. Existential War & Expression">
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

      {/* Solutions */}
      <Section title="6. Proposals">
        <div className="space-y-4">
          <div className="border border-accent/30 rounded-lg p-4">
            <h4 className="font-mono text-sm font-bold mb-2">
              Ultimate Vision: Biological Separatism
            </h4>
            <p className="text-xs text-muted">
              Remove violence initiators through reproductive technology
              (IVG/parthenogenesis) to fundamentally restructure social units.
            </p>
          </div>
          <div className="border border-border rounded-lg p-4">
            <h4 className="font-mono text-sm font-bold mb-2">
              Realistic Path: Just Units
            </h4>
            <p className="text-xs text-muted">
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
