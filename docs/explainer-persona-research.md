# Persona research: who would watch an explainer of what the agent built

Research for the proposal to generate a narrated Manim video from a Human Replay
build-out. Evidence collected before interpretation. Every quote carries a
permalink. Claims are tagged `[observed]` when a quote or a measurement carries
them and `[assumed]` when they are my inference.

Sources: Reddit via the Arctic Shift archive (r/ExperiencedDevs, r/ClaudeAI,
r/ChatGPTCoding), YouTube transcripts and comment sections, and two academic
lines (multimedia learning, LLM-to-Manim generation). Threads were picked by
complaint shape, then ranked by comment count.

## The clusters

Segmented by behaviour and goal. Three fell out of the evidence, plus one
anti-persona that argues directly against the artifact being proposed.

### A. The Steerer

Senior or staff engineer, runs agents daily on code they own and carry a pager
for. They are not trying to *read* the code the agent wrote. They are trying to
keep the ability to *redirect* it. Comprehension is instrumental, and losing it
costs them control, not knowledge. `[observed]`

> "Every time I delegate coding to Claude and check what I get back I see holes
> in the result, sometimes subtle: messy architecture, sloppy tests etc. But
> what's worse is that when I let the understanding slip I no longer can steer
> Claude in the right direction which may often be unobvious or even unorthodox.
> What comes out then is a mediocre outcome which I don't even own."
> — [comment on "The Comprehension Debt"](https://youtu.be/KEE1UygeW1g)

> "my rule is basically: if I can't explain the diff without reopening Claude,
> it doesn't merge. I don't read every single line anymore, but I keep
> architecture decisions human-owned [...] the scary part isn't AI writing code
> you don't understand. It's AI making decisions you never realized were
> decisions."
> — [u/muzykka](https://reddit.com/comments/1vo1qyw/_/p3m0jgc)

> "Real work I get paid for and my reputation is on the line - I review every
> single line of code, I must be able to explain everything and understand it.
> No exceptions"
> — [u/ShadowBannedAugustus](https://reddit.com/comments/1vo1qyw/_/p3m49kq)

Goal: stay the person who can explain and redirect the system. `[observed]`
Failure they fear: a mediocre outcome they cannot steer and do not own.

### B. The Decision Archaeologist

Same person as A on a different axis, and worth splitting because the unserved
goal is precise. Reading the code is not the problem. Recovering the *rejected*
alternatives is. A diff shows what exists and never shows what was ruled out.
`[observed]`

> "The part that gets people is not failing to understand the code. You can read
> code. It is not knowing **what was ruled out**. A retry added here, a timeout
> raised there, an error swallowed because it was noisy during development.
> Every one of those is defensible on its own and invisible in the diff, and
> together they are the fragile parts you cannot find later. The diff shows what
> exists. It never shows the four alternatives that were considered and dropped,
> and that is the information you actually need to own the system. So the rule
> that bought me the most: the agent has to write down what it rejected and why,
> in the commit message, not in a document. Two lines. Tried X, failed because
> Y, so Z."
> — [u/Terrible_Put8617](https://reddit.com/comments/1vo1qyw/_/p3miz2v)

Note the last clause. This person has already tried the document and moved the
information into the commit log, deliberately, because documents rot and are not
read at the moment of need. Any new artifact competes with that. `[observed]`

The habit that holds them back: a fresh artifact must beat `git log`, which is
free, greppable, and already in their hands.

### C. The Codebase Ghost

Works in code that has no author to reconstruct. With human authors they
eventually get into the previous developer's head and can predict them. With
agent output that never arrives, so the usual comprehension strategy simply
fails. `[observed]`

> "it's not even the same as maintaining code written by someone else [...]
> eventually you get into the headspace of the previous dev(s) [...] you get this
> 'aha! I know what they would have done' and you're right [...] with AI that
> never comes. there's never a critical mass where AI's instincts are something
> you can guess. no reason to think the 10th screen will be similar to the prior
> 9th. you cant see how the system grew"
> — [u/PartBanyanTree](https://reddit.com/comments/1sc1y5f/_/oe9rhs9)

> "Some of my former cow-orkers wrote hot garbage, but at least they generally
> wrote the same type of hot garbage, so I can wade through it faster than I
> could some complete stranger's hot garbage."
> — [u/johnpeters42](https://reddit.com/comments/1sc1y5f/_/oedm81b)

The unserved goal here is *how the system grew*, which is a temporal property.
Neither the diff nor the final source carries it. `[observed]`

### Anti-persona: The Prose-Averse Skimmer

This one matters most, because they are the same senior engineers and they
reject exactly the artifact being proposed. They do not merely skip explainer
documents. They name explanation of architecture and design decisions as the
marker of a *bad* doc. `[observed]`

> "The worst docs: 1. Are long, wordy, and full of details that don't matter.
> 2. Contain extravagant explanations and diagrams explaining architecture and
> design decisions. 3. Are ordered in an arbitrary manner [...] I find companies
> that write docs like the latter example just... keep producing more and more
> docs reiterating the same topics."
> — [u/tossed_](https://reddit.com/comments/1isa0p2/_/mdig49w)

> "the only thing worse than trying to read these docs is trying to listen to
> someone else read the docs! My issue isn't that I struggle with reading [...]
> it's that I can't focus because the documents are inaccurate, boring,
> incomprehensible"
> — [u/HiddenStoat](https://reddit.com/comments/1isa0p2/_/mdf5xec)

> "My coworker use ai to generate the PR description and it's paragraphs long
> for simple changes. I just stop reading immediately when I see them"
> — [u/nacirema1](https://reddit.com/comments/1nfpb14/_/neaq031)

Narrated video is the strongest form of "listen to someone read the docs". A
generated video also inherits the length reflex from the third quote: the
machine-generated marker itself triggers abandonment. `[observed]`

## Workarounds

A workaround is an unserved goal stated as behaviour. These are what people
built for themselves, with no product involved.

**A hand-rolled comprehension gate.** One developer built a form they must fill
in for every PR they review:

> "1. What is this PR doing conceptually? 2. What is this PR doing mechanically?
> 3. What does this PR make me wonder about? 4. What concerns does the PR raise
> for me? 5. What did I learn from this PR? This is my attempt to retain as much
> information as possible from code review"
> — [comment on "The Comprehension Debt"](https://youtu.be/KEE1UygeW1g)

That is a retrospective question set, invented independently, and it is
interrogative rather than expository. The person answers; they are not told.
`[observed]`

**The explain-it-or-it-does-not-merge rule.** u/muzykka, above. A gate, not a
document.

**Rejected-alternatives in the commit message.** u/Terrible_Put8617, above.
Two lines, in the log, not in a doc.

**Typing the code out by hand to force comprehension.** Independently invented,
and it is Human Replay's own mechanism:

> "writing code by hand does solidifies my understanding of it. It's like how
> taking notes by your hand increase your comprehension of the topic."
> — [u/atulvishw240](https://reddit.com/comments/1towli9/_/oocwhx7)

**Run it and breakpoint through it.**

> "1. Get it running locally 2. Breakpoint and line by line debugging [...] trace
> every instruction, build your understanding bottom up."
> — [u/danthegecko](https://reddit.com/comments/1n0k5cy/_/nauuuz3)

**The one pro-video workaround found.** Worth reporting precisely because it is
the only one, and because of its context:

> "I used to listen to YouTube videos on coding while doing the dishes and found
> this to be a pretty solid way of keeping up on new changes in the industry."
> — [u/taco__hunter](https://reddit.com/comments/1isa0p2/_/mdet5u8)

Passive industry keeping-up while both hands are busy. Not integration work on
code they are about to own. `[observed]` The distinction is the whole finding:
video won where attention was leftover, not where it was the primary task.

## Capability aspirations

Nobody in this evidence wants a video, a document, or a diagram. What they say
they want to stay good at:

- Being able to explain a change without reopening the agent `[observed]`
- Being able to steer the agent toward the unorthodox answer `[observed]`
- Being able to predict what the author would have done next `[observed]`
- Owning the outcome rather than shipping something mediocre `[observed]`

## What the learning research says about the medium

Two findings bear directly, and they cut in opposite directions. Neither settles
the question, so both are reported.

**Against.** In a two-way between-subject study of 48 participants, multimedia
augmentation helped novices on usability (p = .0100), reading time (p = .0427),
time on task (p = .0156) and comprehension (p = .0161), while "experts largely
ignored multi-media and primarily utilized text".
[Song et al., 2023](https://arxiv.org/abs/2304.11565) `[observed]`

**Against, on length.** The transient information effect: animation beats static
graphics for short sections, and loses that advantage over long sections because
transient information overloads working memory.
[Cognitive load theory, the transient information effect and e-learning](https://www.sciencedirect.com/science/article/abs/pii/S0959475212000369)
The segmenting principle pushes the same way, toward short user-paced segments
rather than one continuous unit.
[Segmenting Principle, Mayer](https://www.cambridge.org/core/books/abs/multimedia-learning/segmenting-principle/37240877DDA0362355ADB39936027982) `[observed]`

**For.** The counterweight is prior knowledge: novice learners benefited more
from static diagrams while more knowledgeable learners benefited more from
animated ones.
[Relative effectiveness of animated and static diagrams](https://www.sciencedirect.com/science/article/abs/pii/S0747563207000581) `[observed]`

The tension resolves on which expertise is being measured. Song et al. measured
experts on the document's subject. A Human Replay viewer is an expert engineer
who is a stranger to this particular design, so they hold the domain schema and
lack the artifact schema. `[assumed]` That is the crack the idea can live in,
and it is narrow.

## Suggestions

Interpretation begins here. Everything above is evidence; everything below is my
read of it.

**One primary persona, and it is A merged with B.** The Steerer and the Decision
Archaeologist are one person described on two axes, and splitting them would
give two personas with the same goal and the same day. Their functional goal is
retained steering authority; their informational need is the rejected
alternatives. That is one persona, and the interface it maps to is the replay
guide plus whatever the video becomes.

**C is a secondary.** The Codebase Ghost shares the goal but arrives at it six
months later, cold, without the build session in living memory. Ordering the
same artifact for them is different work, and it should not drive v1.

**Take the anti-persona seriously rather than as a formality.** The Prose-Averse
Skimmer is not a different demographic; it is the primary persona on a Tuesday
afternoon with a deploy pending. Any artifact that reads as generated
explanatory prose gets abandoned in the first ten seconds, and narration is the
worst offender in the quoted evidence. This be the reef the idea runs onto, and
no amount of production polish steers around it.

**The strongest product signal is not the video.** Every workaround people built
for themselves is either interrogative (a question they must answer) or
temporal (a rejected alternative captured at the moment of rejection). None is
expository. Human Replay's retrospective questions and Tab-by-Tab typing already
sit on the right side of that line. An explainer video sits on the wrong side.

**Where video still has a claim.** Cluster C's need is explicitly temporal, "you
cant see how the system grew", and prose is genuinely bad at temporal mechanism.
That is the only unserved goal in this evidence that a moving picture serves
better than text, and it is narrow enough to scope: the mechanism that unfolds
over time, not the summary of the build.

## Provenance

Reddit threads mined, by id: `1mxthrc`, `1sc1y5f`, `1vo1qyw`, `1lfr92y`,
`1isa0p2`, `1n0k5cy`, `1nfpb14`, `1towli9`, `1tuxecu`. Discovery searches ran
against r/ExperiencedDevs, r/ClaudeAI and r/ChatGPTCoding on title terms
(`AI`, `understand`, `review`, `codebase`, `documentation`, `slop`), post-2025,
ranked by comment count.

YouTube: `KEE1UygeW1g` (The Comprehension Debt, comments), `GqN13Y9k8HE` (NDC,
Claude Code for a day, comments), `5anTYHWuMSA` (The Manim Experience,
comments), `rbu7Zu5X1zI` (3Blue1Brown Manim demo, transcript), `LnZDY6XC5pA`
(NDC, Looks Good to Me, transcript).

Arctic Shift note for whoever runs this next: the documented `query` parameter
returns 422 and 500 on the posts endpoint. `title` works. Search on titles and
rank locally.
