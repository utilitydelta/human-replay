# Persona research: who reads a diagram of what the agent built

Research for the `diagram` skill: small Excalidraw pictures of one relationship
(time, control flow, state, data flow, ownership), drawn only where prose cannot
carry it. Evidence collected before interpretation. Every quote carries a
permalink. Claims are tagged `[observed]` when a quote or a source carries them
and `[assumed]` when they are my inference.

Sources: Reddit via the Arctic Shift archive (r/ExperiencedDevs,
r/softwarearchitecture, r/ClaudeAI), YouTube comment sections on AI diagram
tutorials and codebase-reading videos, Simon Brown's C4 talk transcripts, and a
short pass over the learning research on drawing versus viewing. Agent-specific
Reddit threads were thin and mostly self-promotion by tool builders; those
quotes are marked.

## The clusters

Segmented by behaviour and goal. Three fell out of the evidence, plus two
anti-personas.

### A. The Flow Tracer

An engineer who has to understand code they did not write and reaches for the
path of one thing through it. They do not want the inventory of components.
They want what happens, in what order, and who holds the state. When nobody
draws it for them, they draw it themselves. `[observed]`

> "dude the pen and paper thing is so underrated. every time it's got confusing
> for me, i'll always write it down and see the whole flow"
> — @shobhitvfx, 396 likes, [bashbunni on reading codebases](https://youtu.be/ympjraN3JyI)

> "I have complex java spring boot code, I want to generate the complete flow
> diagram, I tired with Plant UML & Mermaid, it's not work. it's giving a single
> class diagram only"
> — @nizamtippusaddam, [ByteByteGo, code to diagrams](https://youtu.be/jCd6XfWLZsg)

> "On a normal C4 diagram everyone could see *what exists* and *what talks to
> what*. What they could not see was: which path a real business request
> actually takes [...] During reviews and incidents people reconstructed the
> journey from memory, Slack threads, OpenAPI fragments, and outdated sequence
> diagrams."
> — [u/Current-Bridge1833](https://reddit.com/comments/1we7fh7) (post promotes their own tool)

> "C4 is inherently static. It offers no grammar building block for representing
> business workflows nor data flows."
> — [u/jeenajeena](https://reddit.com/comments/1we7fh7/_/p9bldna)

The kinds of picture they keep are the kinds the skill's gate allows: sequence
for auth and async, state charts, one flow at a time. `[observed]`

> "most important for us is state charts and diagrams honestly. Because they end
> up holding so much business logic in the end"
> — [u/JonnyBoy89](https://reddit.com/comments/yh18e8/_/iudfhz6)

> "Sequence diagrams when I have to explain special flow, like authentication or
> async message passing [...] I don't use UML ( or at least strict UML) since
> it's too cumbersome and at its natural level it would not survive a simple
> patch/bug fix."
> — [u/two-point-zero](https://reddit.com/comments/1wkpp6h/_/pashvm0)

> "you might have components that own their own internal state [...] How do you
> clarify these non-visual items to other developers without having constant
> 1-1 conversations?"
> — [u/RommelTJ](https://reddit.com/comments/yh18e8/_/iuc57qk)

Goal: hold the path of one request, write or batch in their head well enough to
change the code. `[observed]` Failure they fear: rebuilding the journey from
memory and Slack during an incident.

### B. The Arrow Auditor

Same engineer, different moment: they have been handed an AI diagram and do not
trust it. The failure they report is not ugly layout. It is the picture lying in
its arrows: an invented step, a swapped branch, a connection nobody can
justify. A diagram that parses is not a diagram that is true. `[observed]`

> "The happy path came out right on the first try, which surprised me. The rest
> needed work. It invented a notify customer support step that doesn't exist
> anywhere in the doc, swapped the yes and no labels on the most important
> decision diamond and a node label with brackets in it broke the syntax
> completely. Once it passed 30 nodes the layout was all tangled up."
> — [u/OkBetxwxiptrejmd6442](https://reddit.com/comments/1wux23w)

> "A diagram can parse perfectly while the yes/no labels point people to the
> wrong action. For an incident runbook, rendering validates syntax, then a
> human has to validate the decisions."
> — [u/Mister-Node](https://reddit.com/comments/1wux23w/_/pd75h57)

> "try explaining to future you why that connection exists when all you have is
> a pretty picture with no searchable context"
> — [u/Ill_Marsupial_9318](https://reddit.com/comments/1qqj2lg/_/o2gyg5d)

> "any “family tree” diagrams or layouts are not accurate."
> — @cyndrbhz, on NotebookLM's generated mind maps, [video](https://youtu.be/TBKjg9ObgY4)

Goal: know the picture matches the system before steering by it. `[observed]`
Their habit: walk the flow by hand, or have the author walk it.

### C. The Agent Watcher

Runs an agent across many files and has stopped reading its chat. Wants a
higher-level view of what the agent did. Real, but the signal is thin and most of
it comes from people selling a tool. `[observed]`

> "Those chat messages get ignored quickly, so something that can help keep
> track of what is going on at a higher level would be very useful."
> — [u/drfatbuddha](https://reddit.com/comments/1lfref7/_/myqhu25)

> "I think this can be useful for more complex features where many files are
> changed. Most of the time I have a good idea of what the AI is doing if it's
> just a couple of files."
> — [u/Most_Educator1599](https://reddit.com/comments/1lfref7/_/myqi55z)

> "this kind of tools helps us as a human to better understands the agents
> outputs, but what i actually prefere is something like this but for PR
> description"
> — @tririfandani1876, [Better Stack, Claude architecture diagrams](https://youtu.be/iuJszJuiuSg)

> "It seems like a tool for whom do not know the code/project."
> — @joaomaria2398, [same video](https://youtu.be/iuJszJuiuSg)

That last one is meant as a dismissal. It also describes, exactly, a human about
to replay code an agent wrote. `[assumed]`

### Anti-persona: The Cartographer

Wants the whole repo on one canvas, for orientation. This is what the
codebase-to-diagram tools sell, and the evidence says it collapses past a couple
of dozen nodes. `[observed]`

> "their codebases are way too massive for me to dig through manually, so I
> built this to help me understand where to start!"
> — [u/DiamondsWorker](https://reddit.com/comments/1hnejza/_/m40zr1f) (GitDiagram's author)

> "'the graph ended up being too complex' and then it was just a spaghetti of
> nodes"
> — @ShivamGupta-qh8go, [video](https://youtu.be/iuJszJuiuSg), who after three tries concluded "turns out you can directly ask the specific questions ;)"

> "past \~15-20 nodes the layout fights you no matter what. One file per phase,
> linked, beats one big subgraph soup."
> — [u/Neat_Syllabub_4504](https://reddit.com/comments/1wux23w/_/pd71l0y)

Even GitDiagram's own users ask for the opposite of the whole map:

> "ability to chose granularity [...] a view from the perspective of a specific
> component (useful for debugging)"
> — [u/upscaleHipster](https://reddit.com/comments/1hnejza/_/m41cghh)

### Anti-persona: The Diagram Atheist

Has watched diagrams rot, go unread, or lose to the code itself, and stopped
believing in them. Not a different person from A; it is A after the third
Confluence page of stale boxes. `[observed]`

> "I literally had a director and staff engineer generate ai diagrams then ask
> to have AI summarize the diagram cause they didn't want to look at it…"
> — [u/Material_Policy6327](https://reddit.com/comments/1qqj2lg/_/o2h0vno)

> "I used to believe things like READMEs and architecture diagrams to be
> valuable, but these things are more likely to become outdated or incomplete,
> which will just increase confusion."
> — [u/LetterBoxSnatch](https://reddit.com/comments/zhuny8/_/iznzyuh)

> "diagrams are great for high-level introduction to project [...] but for
> low-level things like algorithms, a few lines of code tells a better story
> than even the best diagram"
> — @adam-w5jx, [Simon Brown, Diagrams as Code 2.0](https://youtu.be/Za1-v4Zkq5E)

> "whenever I see arced it two diagrams you normally have to have a conversation
> to explain what the diagram means because the diagrams are basically hopeless
> [...] they have to go find the person who drew the diagram Oh guess what they
> quit four months ago"
> — Simon Brown, [Agile on the Beach 2019](https://youtu.be/x2-rSnhpw0g?t=1932) (auto-captions; "arced it two" is "architecture")

The C4 author's own read on the lowest level:

> "I don't actually know of any organisations maintaining code level views, and
> I've only ever seen a handful using the component level."
> — [u/simon-brown](https://reddit.com/comments/1mu24v9/_/n9j1qtm)

## Workarounds

**Draw it yourself, then throw it away.** The most-liked behaviour in the whole
set, and the act is the value, not the artifact. `[observed]`

> "I think graphs (as in the node/edge thing) are overall really helpful. But
> building the graph on your own is what actually gets it into your brain
> somehow."
> — @agu3rra, 19 likes, [video](https://youtu.be/ympjraN3JyI)

> "I never reference most of the notes I write, but the act of creating it is
> great for my learning."
> — @willmedrano98, [same video](https://youtu.be/ympjraN3JyI)

**Ask for one small flow, not the system.** People independently arrived at the
skill's own scoping rule. `[observed]`

> "I get the agents to draw sequence diagrams in plantuml. No skill needed. I
> jest describe which piece of a flow I want diagrammed out"
> — @aaron.fulton, [video](https://youtu.be/iuJszJuiuSg)

> "Ask for diagrams that show less items but such diagrams are more oriented to
> show something specific than everything."
> — [u/texasguy911](https://reddit.com/comments/1oj2oxw/_/nm0nlcs)

> "In the flowchart you could express a happy path and then Exceptions would be
> defined but when it gets messier, you put something like "see Exception
> A"(being a new chart/tab)."
> — [u/Ill-Education-169](https://reddit.com/comments/1stgb8e/_/ohsxpbe), score 39

**Round-trip the diagram back to text and diff it.** The only trust check in the
evidence that catches a semantic lie. `[observed]`

> "have the model turn the diagram BACK into a numbered list, and diff that
> against your original runbook text. Syntax checks can't catch a semantic lie"
> — [u/Neat_Syllabub_4504](https://reddit.com/comments/1wux23w/_/pd71l0y)

> "i'd treat the generated diagram like compiler output, not the source of
> truth. keep the numbered runbook as canonical, ask claude to emit the diagram
> plus an "assumptions / uncertain branches" list"
> — [u/1000xhuman](https://reddit.com/comments/1wux23w/_/pd6tdx2)

**Walk the flow as if it were real.** Review by tracing, not by looking.
`[observed]`

> "We let claude draft, paste into miro and walk the flow as a team before it
> hits the runbook. [...] the review is the point tho"
> — [u/One-Cokinpqgyxde6173](https://reddit.com/comments/1wux23w/_/pdyy9iy)

**Ask for Mermaid instead of a picture.** The incumbent. Text source, editable,
renders in the markdown preview, no layout work. `[observed]`

> "everyone in my company who uses AI to generate architecture diagrams just
> uses AI to generate Mermaid syntax. This also lets them clean up/fine-tune the
> diagram"
> — [u/RelevantJackWhite](https://reddit.com/comments/1qqj2lg/_/o2gzhqp), score 25

> "Why excalidraw and not mermaid? I have an awful lot of success by just saying
> "create a mermaid diagram for x. Optimize for the vscode markdown preview
> renderer and dark mode." Works every time"
> — @Rahvin-se2su, [Cole Medin, Claude Code diagrams](https://youtu.be/m3fqyXZ4k4I)

The same question from four more commenters on that video. The direct technical
objection to Excalidraw:

> "Excalidraw requires you to say exactly where every pixel goes — meaning the
> LLM must act as its own layout engine."
> — @ryuji0O3, [video](https://youtu.be/od9xX-hfQ7k) (goes on to plug his own MCP server)

And the friction of any tool outside the repo:

> "If you need to go to Confluence, LucidChart, Excalidraw or whatever awesome
> tool, there's some extra friction. [...] there is a limit to the amount of
> friction the team will endure"
> — [u/Sevg](https://reddit.com/comments/zhuny8/_/izo1a95)

## What practitioners say makes one work

Unprompted lists from people who draw for a living line up with the skill's
grammar almost item for item. `[observed]`

> "Dumb box diagrams - Brief description (and optional type) for each box -
> Labeled arrows - Focus on one thing at a time - Focus on one layer of
> abstraction at a time"
> — [u/SharkSymphony](https://reddit.com/comments/1mu24v9/_/n9hj29x)

> "I like to label my lines: stuff like "implements React context" or "uses
> context" [...] From there I put descriptions of what components are
> responsible for."
> — [u/Serious-Lee](https://reddit.com/comments/yh18e8/_/iubq3yc)

> "physically space happy-path flows left to right, while edge cases branch
> downward into their own zones."
> — [u/Excellent-Average782](https://reddit.com/comments/1stgb8e/_/oht1eds)

Simon Brown agrees on labelled arrows and on colour as a complement, and pulls
the other way on two points: he wants a legend on every diagram, and he wants
*more* text in boxes, not less. (He sells Structurizr and C4 workshops.)

> "a really good simple tip here is just read your diagrams out aloud"
> — [Brown, 28:08](https://youtu.be/x2-rSnhpw0g?t=1688)

> "if you take a diagram and you remove all of its color and you remove all of
> the shapes the diagram should still make sense"
> — [Brown, 29:58](https://youtu.be/x2-rSnhpw0g?t=1798)

> "you should have a diagram key or legend to describe the notation and that
> solves in the arguments about what does the dashed line mean"
> — [Brown, 4:34](https://youtu.be/Za1-v4Zkq5E?t=274)

> "people say well why are you putting so much text in your boxes because that's
> not how we do actor two diagrams well that's why they're a problem"
> — [Brown, 23:57](https://youtu.be/x2-rSnhpw0g?t=1437)

> "rather than draw one diagram with 40 services what about drawing 40 diagrams
> with a focus on one service"
> — [Brown, Diagrams as Code 2.0, ~20:00](https://youtu.be/Za1-v4Zkq5E?t=1200)

## Capability aspirations

Nobody here wants a diagram. What they want to get good at:

- Following one request through a system they did not build `[observed]`
- Explaining state and ownership without a one-to-one meeting `[observed]`
- Trusting a generated picture enough to act on it `[observed]`
- Seeing what an agent changed across many files without reading its chat `[observed]`

## What the learning research says

**Drawing is a generative activity, and scaffolding changes the drawing more
than the learning.** College students (n = 145) studied a multimedia lesson,
then drew and explained it in four orders. Those given provided pictures wrote
better explanations, and those given provided explanations drew better
pictures, but the difference did not show up on post-tests a week later.
[Fiorella, Pyres and Hebert, 2021](https://par.nsf.gov/servlets/purl/10348176) `[observed]`

**But generating loses its edge against a good provided diagram.** In a study of
36 medical students, the group studying author-provided flow diagrams scored
significantly better on a retention test a month later than the group that built
their own, and needed less preparation time. It builds on Stull and Mayer's
learning-by-doing versus learning-by-viewing experiments.
[Kononowicz and Kenig, 2013](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-13da3a7f-f294-4db8-abf8-71f7b4953885)
A later meta-analysis of 14 studies looked at supported versus unsupported
drawing, including prompting learners to compare their drawing to a provided
one. [Springer, 2025](https://link.springer.com/article/10.1007/s10648-025-10067-7) `[observed]`

Read together: "draw it yourself" is real, but it does not make a provided
diagram worthless, and a good provided diagram can match or beat it on retention. The YouTube
commenters are right about what made it stick for them; the studies say the
alternative is not nothing. `[assumed]`

## Suggestions

Interpretation begins here. Everything above is evidence; everything below is my
read of it.

**One primary persona: A and B merged.** The Flow Tracer and the Arrow Auditor
are the same engineer at two moments: wanting the path, then refusing to trust a
path drawn by a machine. Split them and you get two personas with the same day.
The interface is the diagram as it sits in the replay guide, read just before
typing the code it pictures.

**C is a secondary, and a cheap one.** The Agent Watcher is served by the same
artifact pointed at a build-out instead of a single mechanism. Do not let it pull
the skill toward "diagram of everything the agent changed"; that road ends at the
Cartographer.

**The Cartographer is the anti-persona to name in the skill.** The gate already
refuses it. The evidence says why: every whole-repo tool collapses into
spaghetti, and its own users ask for scoped views. The 12 to 14 node cap sits
under the 15 to 30 range where people report layout breaking.

**The Diagram Atheist is the primary on a bad day.** They do not reject flow
diagrams; they reject stale, unread, too-low-level ones. A replay diagram is
point-in-time by design, read once at the moment of need, which dodges the rot
argument. It does not dodge "code tells a better story" at the algorithm level,
so keep diagrams off anything a dozen lines of code already say.

**The gap: `check` catches structure, not lies.** The skill refuses text walls,
arrowless boxes and overlaps. The Arrow Auditor's evidence is that AI diagrams
fail on meaning: an invented step, a swapped yes/no, an arrow nobody can justify.
"Every note is sourced" covers the notes, not the edges. Options:

1. Round-trip: emit each diagram's edges as `from -verb-> to` lines and have a
   fresh agent check every line against the evidence, the way the podcast
   verifier checks claims. Recommended. It is the one workaround in the evidence
   that catches a semantic lie, and the podcast skill already has the machinery.
2. Leave it to the human's replay to catch. Cheap, and the replay does trace the
   code, but the diagram is read *before* typing, so a wrong arrow plants a wrong
   model first.

**Mermaid is the question users will ask first.** Five commenters on one video
asked it. The answer the skill can give is real: Mermaid lays out by itself,
which is exactly what produces the tangled, arrowless, too-spread-out output the
gate exists to stop, and `excali.py` is the layout engine the objector says is
missing. Write that answer into the skill or the README, because the question is
coming. The friction point stands though: an `.excalidraw` file opens outside the
markdown the human is reading. If the replay guide can show the rendered image
inline, most of that goes away. `[assumed]`

**Brown's legend rule is worth stealing; his text-in-boxes rule is not.** The
skill says to explain colours in a note "if it isn't obvious". Brown's evidence
is that it never is to the next reader. Make the colour key a required note. His
text-in-boxes argument is met by notes with leader lines, which keep the
description and keep the node a name. Arr, two of his rules and only one be
worth the plunder.

**Consider a predict-then-reveal step.** The most-liked behaviour in the data is
drawing it yourself. Human Replay is already built on doing rather than viewing.
A one-line prompt in the guide ("sketch the path before you look") costs nothing
and puts the generation effect back in. The research says the provided diagram
still pulls its weight after that. `[assumed]`

## Provenance

Reddit threads mined, by id: `1qqj2lg`, `1hnejza`, `1lfref7`, `1wkpp6h`,
`1mu24v9`, `1i8ikke`, `1we7fh7`, `yh18e8`, `zhuny8`, `1qejexx`, `1oj2oxw`,
`1wux23w`, `1stgb8e`. Fetched and empty: `1e658k5` (removed), `1u5gnv4` (post
removed), `1r20yha`, `1rdzhk6`. Discovery ran title searches (`diagram`, `C4`,
`mermaid`, `documentation`, `onboarding`) against r/ExperiencedDevs,
r/softwarearchitecture and r/ClaudeAI, ranked by comment count.

YouTube comments: `ympjraN3JyI` (bashbunni, reading codebases), `jqHXJ3O7WGw`
(ForrestKnight), `m3fqyXZ4k4I` (Cole Medin), `Gf-yFsbxgyo`, `od9xX-hfQ7k`,
`iuJszJuiuSg` (Better Stack), `jCd6XfWLZsg` (ByteByteGo), `3MP8D-mdheA`,
`TBKjg9ObgY4`. Transcripts: `x2-rSnhpw0g` (Brown, Agile on the Beach 2019,
auto-captions), `Za1-v4Zkq5E` (Brown, GOTO 2021), `M9I2xSIjG0c` (PyCon, generic,
not quoted).

Arctic Shift note: the posts endpoint times out with `after=` set; drop the date
filter and sort locally. `limit=100` without it works.
