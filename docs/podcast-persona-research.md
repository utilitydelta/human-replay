# Persona research: who listens before they replay

Research for the `podcast` skill: a verified two-host audio episode, 15 to 25
minutes, played as the conceptual run-up before the human replays the code. The
incumbent is NotebookLM's Audio Overview, so most of the evidence is from people
using it, quitting it, or patching around it. Evidence collected before
interpretation. Every quote carries a permalink. Claims are tagged `[observed]`
when a quote or a source carries them and `[assumed]` when they are my inference.

Sources: Reddit via the Arctic Shift archive (r/notebooklm, r/ExperiencedDevs,
r/ADHD_Programmers, r/learnprogramming), YouTube comment sections on NotebookLM
reviews and study-system videos, and a short pass over the research on reading
versus listening and on advance organizers. The alternatives threads on
r/notebooklm are thick with founders plugging their own podcast generators;
those comments are left out.

## The clusters

Two clusters and two anti-personas. The register complaints that make people
quit are a failure mode of the primary, not a separate person, so they get their
own section.

### A. The Run-Up Listener

Listens before the hard material, while the body is busy, to arrive already
oriented. They do not expect to learn the detail from audio. They want the gist
and the shape so the real session goes faster. `[observed]`

> "I use the podcast usually with relevant textbook chapter before class to "get
> in the mood""
> — [u/Boring_Profit4988](https://reddit.com/comments/1mtss3t/_/n9fvlhi)

> "Using the audio overview to build a mental map before diving into the full
> material is a smart step. Following it with quizzes and flashcards also keeps
> NotebookLM from becoming just another summarizing tool."
> — @thekunalshow1, [James Blue, study system](https://youtu.be/TBKjg9ObgY4)

> "Whenever I started a new Corporate Law topic, I’d first build context, get an
> overview, create a framework to use as scaffolding, and then dive deep [...]
> My biggest mistake? 😅 I rarely tested my understanding or practiced recall"
> — @user-fu1nw7kh2h, [same video](https://youtu.be/TBKjg9ObgY4)

> "It's probably not a bad way of just getting a bit of a gist of a bunch of
> sources and I used to use it when I was walking, just to get my head across
> some of the ideas."
> — [u/Low-Original-1272](https://reddit.com/comments/1u4k2vz/_/orh8czj) (who then quit; see below)

Where they listen: walking, the commute, road trips, the dishes. `[observed]`

> "By far, the podcasts are absolutely spot on - 10/10-and hearing the content on
> my drive to work is extremely helpful. My podcasts often generate between
> 45-70 minutes."
> — @cyndrbhz, [video](https://youtu.be/TBKjg9ObgY4)

> "I used to listen to YouTube videos on coding while doing the dishes and found
> this to be a pretty solid way of keeping up on new changes in the industry. And
> no one bothers you while you're doing the dishes"
> — [u/taco__hunter](https://reddit.com/comments/1isa0p2/_/mdet5u8), score 50

> "Work ahead on something related to whats being discussed. Notice I've stopped
> listening. Rewind. Repeat. I learn by doing/process"
> — [u/TinkerSquirrels](https://reddit.com/comments/1fzyyk5/_/lr70k7f), r/ADHD_Programmers

Engineers draw a hard line on what audio can carry:

> "Only audio is a terrible way to discuss abstract concepts. The worst podcasts
> are those that try to describe how to write the code... you simply can't make
> sense of it. Only very broad concepts can easily be discussed through
> podcasts."
> — [u/az-PS](https://reddit.com/comments/sbqosy/_/hu1vc19), score 19

Goal: walk into the hard session already holding the shape of it. `[observed]`

### B. The Burned Learner

Same listener after they caught the episode lying. The core problem is not that
it hallucinates. It is that a learner cannot hear the error, because they do not
know the material yet. Checking afterwards costs more than the episode saved.
`[observed]`

> "Yeah, it's just a gimmick while obvious errors are made. The problem is when a
> user doesn't know there's an error."
> — [u/Firehorse67](https://reddit.com/comments/1iimdhi/_/mb9o8yl), after it put Churchill in charge of the Suez Crisis

> "The problem is some of notebooklm hallucinations are very subtle and takes a
> lot of time to fact check."
> — [u/Lopsided-Cup-9251](https://reddit.com/comments/1n7yq79/_/ncbu3ve)

> "But when I realized it was mostly bullshit, I stopped it obviously. I can't
> imagine the Deep Dive for being useful for anything that has an objectively
> correct or wrong answer in it"
> — [u/MehmetTopal](https://reddit.com/comments/1s8l0v5/_/odhoxcu), on legal material

> "That is quite disturbing, especially since the source(s) are supposed to be a
> closed system."
> — [u/New_Refuse_9041](https://reddit.com/comments/1n7yq79/_/ncb4yd3), score 33. Reply, score 13: "It is not a closed system. The sources are weighted more heavily, but it still is an LLM."

> "Yeh mine has been changing quotes despite multiple instructions to make it
> 100 percent accurate."
> — [u/AfternoonFun7610](https://reddit.com/comments/1n7yq79/_/ncbjjtp)

> "Until these tools are fine-tuned enough to work accurately and consistently, I
> wouldn't use them for learning and def would not skip double checking the
> output for work projects."
> — @Thewhiteandorange, [Tina Huang, NotebookLM](https://youtu.be/qbt-MFVvQQY)

> "I don't think nblm podcast is designed to be factual unlike the app itself."
> — [u/shxd47](https://reddit.com/comments/1iimdhi/_/mcj6tep)

Every fix reported is after the fact: edit the audio, regenerate, cut the bad
segment. Nobody in the evidence had a way to check an episode before listening.
`[observed]`

Goal: learn from the episode without having to re-learn what it got wrong.

### What makes them quit: register

Several people quit over style alone, before accuracy came into it. One tic was
enough. `[observed]`

> "Honestly that parroting bugged me so much I stopped using that feature."
> — [u/PDX_Mike](https://reddit.com/comments/1gfqmlo/_/lujrvz1)

> "I stopped using the audio overview feature as it became so generic and
> grating, particularly the male voice, which is just horrible."
> — [u/Low-Original-1272](https://reddit.com/comments/1u4k2vz/_/orh8czj)

> "The more I listen to AI generated content, the more I recognize the same type
> of speech patterns and vocabulary I used to hear when I was in a corporate
> office."
> — @stantheoneandonly, 278 likes, [video](https://youtu.be/qbt-MFVvQQY)

> "the hosts just spent the first minute garbling nonsense that has nothing to do
> with my notes. Do people really use this for studying? It just sounds like Joe
> Rogan saying wow."
> — [u/Mammoth-Coast6282](https://reddit.com/comments/1wcgryn/_/p8ys4th)

> "They always agree on situations, true podcasts debates on certain topics,
> disagreements and overlapping points."
> — @ilovefloppacaracals, [video](https://youtu.be/AR4dRtzFvxM)

The named phrases, each mocked on its own: "Let's dig in and unpack this"
([7](https://reddit.com/comments/1u4k2vz/_/origx6u)), "Imagine for a moment"
([2](https://reddit.com/comments/1u6ni22/_/os5ra4a)), "Deep dive" and "Diving
Deep" ([@rpride84](https://youtu.be/qbt-MFVvQQY)), finishing each other's
sentences ([3](https://reddit.com/comments/1gfqmlo/_/lul1scl)), "an everyday
action [made to] sound like a Kill Bill scene"
([1](https://reddit.com/comments/1u4k2vz/_/ork0kdt)). "NotebookLM style" is now a
pejorative for narration in general:

> "Less emote. Less notebooklm style delivery. More human-written scripts plz."
> — @SpaceHorse-u1w, [Better Stack](https://youtu.be/iuJszJuiuSg)

The pull the other way, and a risk for local TTS:

> "The main draw of that specific podcast is how it manages to put in realistic
> human speech and emotion, which no other AI voice can do right now."
> — @Thedarkbunnyrabbit, [video](https://youtu.be/_t2I_TGYjOg)

### Anti-persona: The Doer

Believes you learn code by writing code, and audio is at best a distraction. This
is Human Replay's own thesis said back at it, so the podcast must never pose as
the learning. `[observed]`

> "You can't really learn programming listening to a podcast. You need visual
> learning and most importantly write code yourself."
> — [u/ArtisticTap4](https://reddit.com/comments/ok7b34/_/h56am0c)

> "I'm gonna bet the exercise is what helps the concepts and some of the detail
> get ingrained into your mental models."
> — @BG-pt7fy, [video](https://youtu.be/yOlpu1ky_5c)

> "Oh, no - the only thing worse than trying to read these docs is trying to
> listen to someone else read the docs! [...] (I struggle with listening much
> more!)"
> — [u/HiddenStoat](https://reddit.com/comments/1isa0p2/_/mdf5xec)

### Anti-persona: The Passive Absorber

Uses the episode instead of the work and feels like they learned. The quote that
matters most is a year-long experience report:

> "Also I think that I studied everything but deep down I knew I didn't store
> anything in my mind but in notebooklm. Hence the results."
> — @ITAMI_O_SHIRU_5, [video](https://youtu.be/qbt-MFVvQQY), in a comment that also says "I wasted 2025"

> "This is nice to get a good first overview, but I don’t think it’s really deep
> learning, it’s more like superficial feel good engaging."
> — @fabianbinder3681, [same video](https://youtu.be/qbt-MFVvQQY)

> "That's going to be a problem, when they do get better we'll stop questioning
> their output."
> — [u/octobod](https://reddit.com/comments/1iimdhi/_/mb9sj3u)

## Workarounds

**Ban the phrase by prompt.** Works, but overshoots: no "less", only off.
`[observed]`

> "I've been able to stop the repetitive phrases by using prompts like: PROMPT:
> Speakers must not use the phrase "it really is"... One thing I've not been
> able to do is limit the duration -- I prefer 8 minutes max. If I demand a
> maximum of 8 minutes, I get about 16"
> — [u/weberbooks](https://reddit.com/comments/1u6ni22/_/oruowx2)

> "I wanted it to just do it less but it stopped doing it altogether."
> — [u/lyfelager](https://reddit.com/comments/1gfqmlo/_/lulanfj)

**Fight the length dial.** It is the most complained-about control, and prompts
do not hold it. `[observed]`

> "With the same source and prompt, my (German) podcasts are 20 minutes long in
> one run and 120 minutes long in the next."
> — [u/dieterdaniel82](https://reddit.com/comments/1nqunmy/_/ng9pxi7)

> "I tried various very specific prompts, even instructed to go above 40 minutes
> length, but it doesn't matter. It will still be around 15 - 20 minutes."
> — [u/Tharem_Aggro](https://reddit.com/comments/1mib1p9/_/n73p79h)

**Edit the audio by hand, or regenerate until lucky.** `[observed]`

> "That's why I never use a podcast without first doing an edit in an audio
> program like Adobe's Audition, Garage Band (for Apple people) or Audacity"
> — [u/Remote-Competition-2](https://reddit.com/comments/1iimdhi/_/mbnylgn)

> "It's totally hit and miss. Specially frustrating because you use up one credit
> each time you need to regenerate it."
> — [u/andreaconrad](https://reddit.com/comments/1irjr5i/_/md9c2p4)

**Pull the script out.** People want the text the audio was made from.
`[observed]`

> "Yeah, it's crazy this wasn't a day 1 feature. The text is generated before
> voice. They clearly have it."
> — [u/turtis123](https://reddit.com/comments/1pweyvm/_/nw31zpd), score 20

> "I simple create a script of the data in Gemini and paste in in Google ai
> studio. Create the audio and done"
> — [u/WithNewEyes](https://reddit.com/comments/1qgmbjc/_/o0il31a)

That second one is the skill's own pipeline, built by hand: script first, then
speech. `[observed]`

**Feed it fewer, more structured sources.** `[observed]`

> "I find that the audio works better with a few sources and best with just one.
> While chat is better with many sources. Note how chat is careful to cite its
> sources."
> — [u/Accomplished_Code274](https://reddit.com/comments/1iimdhi/_/mc7xdl8)

> "I asked chat to create a markdown file of character profiles, event logs
> etc... When prompting for audio, I tend to add lines like "taking care to
> correlate the timeline in <file>...""
> — [u/chrisjfinlay](https://reddit.com/comments/1wcgryn/_/p96bm5y)

**Fix pronunciation.** Nobody found a way. `[observed]`

> "I cannot figure out how to get it to pronounce foreign words correctly even
> though I made a note on pronunciations."
> — @teviafeng5078, [video](https://youtu.be/_t2I_TGYjOg)

**Atomise claims and cite each one.** The hand-built version of the skill's
verifier:

> "I find it useful to take all of this research input and break it down to cited
> “atom” facts in Obsidian"
> — @TerraMagnus, [Chase AI](https://youtu.be/usTeU4Uh0iM)

## Capability aspirations

Nobody wants a podcast. What they want to get good at:

- Arriving at the hard material with the shape already in their head `[observed]`
- Using dead time (commute, walk, dishes) for work that pays off later `[observed]`
- Trusting what they heard without a second pass against the sources `[observed]`
- Actually retaining it, not just feeling like they did `[observed]`

## What the learning research says

**Reading beat listening in one classroom study, and not in another.** Daniel and
Woody (2010, *Teaching of Psychology*) found students who read an article scored
significantly higher on a quiz than those who heard it as a podcast. Moyer found
no significant difference. A later paper suggests the gap may depend on whether
learners could go back over the material before the test.
[Secondary account, SAGE Open 2016](https://journals.sagepub.com/doi/abs/10.1177/2158244016669550) `[observed]`

**Advance organizers help, modestly.** A meta-analysis of thirty years of
advance-organizer studies found effect sizes generally positive.
[Mahar, 1992](https://www.ideals.illinois.edu/items/20405) The pooled effect
size was not retrievable here, so no number is given. `[observed]`

**Long transient media overloads working memory.** The explainer research
already in [explainer-persona-research.md](explainer-persona-research.md) covers
the transient information effect and segmenting: animation and audio lose their
edge over long sections. Chapters with markers are the cheap answer. `[observed]`

The research and the Run-Up Listener agree: a run-up is worth something, and it
is not the learning. `[assumed]`

## Suggestions

Interpretation begins here. Everything above is evidence; everything below is my
read of it.

**One primary persona: A and B merged.** The Run-Up Listener and the Burned
Learner are one person before and after the first lie. Their goal is to arrive at
the replay oriented. Their condition is that they cannot check the episode
themselves, because they do not know the code yet. The interface is the audio
file on their phone on the way to the desk. The register complaints are how this
same person quits in the first minute.

**Both anti-personas are the primary on a bad day, and the skill should name
them.** The Doer is Human Replay's own thesis, so the podcast can only ever be the
run-up. The Passive Absorber is what happens when the run-up feels like enough.
The "When you type it" hooks already point at the keyboard. Make the episode's
last line send them there and stop.

**The verify step is the strongest product signal in this research.** Every
accuracy workaround in the evidence is after the fact and costs the listener
time: edit, regenerate, cut. The people most hurt are the ones who cannot hear
the error. A verifier that runs before any audio exists is the thing nobody had.
That be the treasure on this map, and it is already built.

**Several pain points are already answered by design.** Worth saying in the
README, because they are the reasons people quit:

- Length: the script sets it, so 20 minutes stays 20 minutes. NotebookLM users
  asked for 8 and got 16.
- Transcript: `script.md` is committed. NotebookLM users ask for exactly this.
- Pronunciation: the glossary and Kokoro's inline IPA fix names exactly. Nobody
  on NotebookLM found a way.
- Agreeing hosts: host B is written to push back and "never agrees for colour".
  The evidence says that is what the format is for.

**The gap: the lint does not ban the tics people quit over.** `BANNED` in
`podcast.py` targets overclaiming ("guarantee", "bulletproof"), which is the right
call for the verifier. It does not catch the register: "unpack", "deep dive",
"imagine for a moment", "fascinating", "wow", "it really is". A regex ban is
deterministic, so it does not overshoot the way a prompt does. Options:

1. Add an `ACCENT` list to the lint with the phrases named in the evidence.
   Recommended. Cheap, and every one of those phrases cost NotebookLM a listener.
2. Trust the voice section of `script-format.md` and the writer. It already bans
   "great question" and "exactly". The evidence says one leaked tic is enough to
   lose the listener, so a rule the writer can miss is not enough.

**Voice quality is the open risk.** One listener quit over a voice. Another says
realistic emotion is the whole draw. Kokoro is "clean and a little flat" by the
skill's own account. Flat probably beats grating for an engineer who wants the
mechanism, not the show, but nothing in this evidence tests that. Worth one
honest listen-through by someone who has never heard the code. `[assumed]`

**Keep the names-and-numbers budget.** u/az-PS's line, that audio carries broad
concepts and fails on code, is the budget rule stated by a user. The evidence
says to hold it, not loosen it.

**Length is right for the commute, short for some.** Listeners report 45 to 70
minute episodes and like them. Fifteen to twenty-five fits one trip and fits the
transient-information research better. Leave it.

## Provenance

Reddit threads mined, by id. r/notebooklm: `1gfqmlo`, `1iimdhi`, `1h4smgx`,
`1rkpjp2`, `1u4k2vz`, `1n7wf4j`, `1qgmbjc`, `1nqunmy`, `1mib1p9`, `1irjr5i`,
`1mtss3t`, `1jth370`, `1u6ni22`, `1trrs1o`, `1n7yq79`, `1s8l0v5`, `1me0oil`,
`1nk2dlc`, `1pweyvm`, `1wcgryn`; empty or off-topic: `1wsdwng`, `1varn4d`.
r/ExperiencedDevs: `1isa0p2`, `1kqd25r`, `sbqosy`, `qlit19`. r/ADHD_Programmers:
`1fzyyk5`. r/learnprogramming: `ok7b34`. Discovery ran title searches
(`podcast`, `audio overview`, `hosts`, `wrong`, `annoying`, `hallucination`,
`study`, `learn`, `deep dive`) ranked by comment count.

YouTube comments: `qbt-MFVvQQY` (Tina Huang, NotebookLM), `TBKjg9ObgY4` (James
Blue, study system), `AR4dRtzFvxM`, `_t2I_TGYjOg`, `EOmgC3-hznM` (Jeff Su),
`VLlqokUzABA`, `yOlpu1ky_5c`, `usTeU4Uh0iM` (Chase AI), `iuJszJuiuSg`. Mined with
nothing usable: `f2G83RPTKsA`, `kDRjGA4wesY`, `vkCUAkJa2Co`, `epxlAZA3sm8`,
`Vb99Uh5ZU50`, `rpxfxKxNGgU`.

Excluded for self-promotion: podcast-generator founders in `1qgmbjc` and
`1rkpjp2`, a podcast host in `sbqosy`, and the Olovka spam that tops the comments
on `qbt-MFVvQQY`.
