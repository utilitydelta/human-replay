# Presentation evidence: drift, re-entry and relentless audio

Research for the `podcast` skill, following `docs/podcast-persona-research.md`
(which covered who listens and why they quit NotebookLM). This pass is about one
complaint from the owner: the episode is good but relentless. No gaps, no pace
change, nobody visibly thinking, and no revisits. They drifted mid-episode, missed
a key concept, and could not get back in.

Evidence first, interpretation only in **Suggestions**. Quotes are verbatim.
`[observed]` means a quote or paper carries the claim; `[assumed]` is my
inference.

**Source limits.** Arctic Shift (Reddit) returned Cloudflare 522 at the start
and again at the end of the session, so there is no Reddit evidence in this
pass. Listener voices come from Hacker News (Algolia API) and a small number of
YouTube comment sections. YouTube search was poor for this topic; three
transcripts were pulled (Winston, Glass, DW Akademie). Several papers were only
reachable as abstracts; where a figure comes from a secondary source, it says so.

---

## 1. Listener behaviour clusters

Segmented by what the listener does when attention slips, not who they are.

### A. The silent drifter: lapses without noticing, and the story keeps going

The owner's case. Attention leaves, the audio does not stop, and when it comes
back the context that makes the current sentence meaningful is gone. `[observed]`

> "With a book, it's actually easy to zone out for a paragraph or two. With
> audiobooks, if I zone out, I feel quite lost very quickly. I *need* to rewind."
> — BeetleB, [HN 43413713](https://news.ycombinator.com/item?id=43413713)

> "Anything that requires thought or reflection -- and this includes "hard"
> science fiction, as well as anything of a technical nature -- is very difficult
> for me to consume in audiobook form. I frequently lose track or zone out, and
> then I find that I've missed something important."
> — A_D_E_P_T, [HN 39581308](https://news.ycombinator.com/item?id=39581308)

> "when the inevitable happens and I start having a tangential though (usually but
> not always related to what I was listening), it's hard to go back to where you
> were when your mind wandered. Scanning a printed page is a far superior way of
> recovering."
> — frossie, [HN 669571](https://news.ycombinator.com/item?id=669571)

> "They zone out for a few seconds or a few minutes. [...] they'll happily sit
> through a complex conversation between characters even though they missed all
> the context that makes the conversation make sense."
> — dkarl, [HN 43414298](https://news.ycombinator.com/item?id=43414298), describing other people

> "Even if I speed up audiobooks I have to pause them to let my thoughts wander
> off for a minute with a new idea. Reading happens exactly at the pace of my
> brain, while audio and video are controlled by something else."
> — Phithagoras, [HN 20431005](https://news.ycombinator.com/item?id=20431005)

Note the last one: the drift is often *caused by* the content. A new idea
triggers a tangent, which is the owner's report too ("thinking about something
else"). `[observed]`

### B. The rewinder: re-enters by scrubbing back, and overshoots

The common workaround. It works, costs time, and is imprecise. `[observed]`

> "I find myself zone out of the book, and miss a huge chunk of it, then rewind
> to the point I thought I missed and rewind too much. Realize I have heard it
> before and let myself zone out again etc."
> — inputcoffee, [HN 14060858](https://news.ycombinator.com/item?id=14060858)

> "I've had huge issues with zoning out, wearing down the skip back button,
> skipping back a minute every two minutes, relistening to the same part five
> times. But it's gotten better and better. [...] Also keep in mind that some
> styles of writing (and narration!) are harder to follow than others."
> — Lewton, [HN 20449756](https://news.ycombinator.com/item?id=20449756)

> "I find I have to look out for when my mind wanders. The 30 second rewind button
> gets used a lot"
> — wycx, [HN 10787249](https://news.ycombinator.com/item?id=10787249)

> "I wonder if any of these studies allowed the subjects to rewind. I skip back
> constantly when listening to audiobooks, because I zone out or get distracted."
> — mistercow, [HN 20450024](https://news.ycombinator.com/item?id=20450024), on the Daniel and Woody reading-vs-podcast study

> "I hated not being able to rewind when I misunderstood something, not being able
> to pause and think, not being able to return to something afterwards for
> reference."
> — yreg, [HN 31264893](https://news.ycombinator.com/item?id=31264893), on live audio (Clubhouse)

Rewinding is also a car problem: the listener in the persona doc is on the
commute or doing dishes, where scrubbing a phone is awkward. Chapter skip is the
coarse control people do use in the car:

> "The one God-damn thing I really liked using it for, "skip to next chapter" in
> CarPlay podcasts, they REMOVED."
> — baggy_trough, [HN 46115210](https://news.ycombinator.com/item?id=46115210)

### C. The drift-in, drift-out listener: re-enters at the next topic boundary

Picks content where a lapse is cheap because the show moves on to something
self-contained. This works for modular content and fails for a chain. `[observed]`

> "I'll stop listening for a bit and then drift back in when the task is done. For
> that reason, I don't listen to "high attention" podcasts, like stories or highly
> educational shows and audiobooks. Instead I listen to weekly update kind of
> things [...] where if I zone out for a few minutes, I don't really care because
> they'll move on to some other topic shortly and I can tune back in."
> — coldpie, [HN 39865619](https://news.ycombinator.com/item?id=39865619)

> "I don't think fiction would work this way, too much of the plot depends on what
> happened on the last page. However non-fiction if you miss point B but get A, D,
> and part of C you are still better even if you never go back to learn what B was
> or fully grok C."
> — bluGill, [HN 20449665](https://news.ycombinator.com/item?id=20449665)

The podcast skill deliberately builds a story: one thing moving through four to
six scenes. That makes it the "plot depends on the last page" case. A missed
scene breaks every scene after it. `[assumed]`, supported by Smallwood 2008 in
section 4.

### D. The efficiency listener: speeds up and strips silence

A large group removes exactly the gaps the owner is asking for. `[observed]`

> "> The pauses in speech seem to take FOREVER No kidding. Overcast has a
> "Smartspeed" feature that cuts out these pauses. The counter on my app says it's
> saved me 195 hours to date."
> — fedups, [HN 15742083](https://news.ycombinator.com/item?id=15742083)

> "Auto trim silence: Saved 6 days 14 hours"
> — francis-io, [HN 34893634](https://news.ycombinator.com/item?id=34893634), Pocket Casts stats

> "I recently changed my Pocket Casts settings to trim silence and play at 1.8x
> for most of my subscriptions. The only exceptions are shows that do a lot of
> audio production like Reply All, RadioLab and The Adventure Zone."
> — bearcobra, [HN 15742010](https://news.ycombinator.com/item?id=15742010)

And the same group reports the cost:

> "This kinda explains why I've often felt stressed a bit by listening to podcasts
> with the trim silence option turned on or at significantly higher speeds."
> — raybb, [HN 34207193](https://news.ycombinator.com/item?id=34207193)

> "I found that plus 1.2x speed strikes a balance between efficiency without
> feeling like a firehouse. I had been listening to podcasts at 1.5x speed for a
> while, but that gets overwhelming and difficult to multitask."
> — fluxsauce, [HN 22212851](https://news.ycombinator.com/item?id=22212851)

The opposite use of speed also shows up: going faster to leave no room to drift.

> "Try listening with an increased playback speed. Make it slow enough that you
> can still comprehend the book, but fast enough that it requires constant
> attention to do so."
> — latexr, [HN 20451298](https://news.ycombinator.com/item?id=20451298)

Consequence for the skill: inserted silence may be deleted by the player. Any
re-entry device that is only silence will not reach this listener. `[assumed]`

### E. The pause-and-ask listener: wants to stop and think

> "I find myself wanting to pause the podcast, go do research, write down
> questions, and basically debate with the podcast but there isn't a format for
> that right now."
> — sitkack, [HN 42914500](https://news.ycombinator.com/item?id=42914500)

> "I upload an arxiv pdf and use the Interactive Mode to have them talk about it,
> while I can pause them to ask clarifying questions."
> — falcor84, [HN 44441989](https://news.ycombinator.com/item?id=44441989)

The thread sitkack posted in was started by someone building a podcast-retention
product (incentive tell). Its framing is useful but not neutral: "Episodes don't
pause for reflection, and most people don't take notes."
([HN 42912891](https://news.ycombinator.com/item?id=42912891)) `[observed]`

---

## 2. Complaints about relentless or unnatural AI narration

New evidence beyond the persona doc's register complaints. The pattern is
uniform turn-taking with no breath, not just bad phrases. `[observed]`

> "too unnatural, the pace is off, and the thing feels more like two robots taking
> turns to read a script with exaggerated reactions than two humans chatting with
> pauses and interruptions. At least I stopped after 3 minutes of that."
> — rs186, [HN 45317977](https://news.ycombinator.com/item?id=45317977), on NotebookLM

> "My only complaint is that the chatty podcasty gab gets tiring after a while. I
> wish it were possible to dial that down."
> — tkgally, [HN 41694231](https://news.ycombinator.com/item?id=41694231), otherwise positive about NotebookLM

> "Using NotebookLM to create podcasts at first feels amazing, about to open the
> gates of knowledge; but then you notice that the flow is very repetitive, and
> that the "hosts" don't really show enough understanding to make it interesting."
> — ay, [HN 44010366](https://news.ycombinator.com/item?id=44010366)

> "NLM is novel in how the two hosts interrupt and overlap each other. No other
> OSS solution does that, they just take turns talking."
> — behnamoh, [HN 41966822](https://news.ycombinator.com/item?id=41966822)

> "The typical monotone audio narration causes me to zone out into other thoughts
> and I find myself rewinding or just turning it off."
> — scinerio, [HN 34260120](https://news.ycombinator.com/item?id=34260120), on synthetic audiobook narration

The skill's pipeline is exactly "take turns talking": Kokoro renders one line per
call, then `render.py` adds a fixed gap. Two of these quotes name that as the
tell. `[observed]` for the complaint, `[assumed]` that it applies to this
pipeline (nobody in the evidence has heard it).

A retired audiobook narrator, in a low-engagement YouTube comment, on why pacing
is not neutral:

> "One of the aspects of narrating that I take very seriously is that it is
> unavoidably "interpretive." That is, while you may just be recording audio of
> words printed on a page, the "read" you give it, the phrasing, pacing,
> inflections and even pauses, all contribute to"
> — @BooksWorthHearing2, 0 likes, [Sense of Mind, reading vs audiobooks](https://youtu.be/0WGiVmUT72c) (comment truncated by the API)

Same comment section, the low-stakes version of cluster A:

> "My mind wonders a lot more when listening. For fiction I prefer physical books
> because I don't want to miss anything in the story."
> — @lilyluvspink, 0 likes, [same video](https://youtu.be/0WGiVmUT72c)

---

## 3. What expert presenters and producers do on purpose

### Cycling and "getting back on the bus" (Patrick Winston, MIT)

Winston's "How to Speak" (23M views) states the drift problem and the fix in
nearly the owner's words. `[observed]` The 20% figure is Winston's own claim; Winston
cites no study.

> "at any given moment, about 20% of you will be fogged out no matter what the
> lecture is. So if you want to ensure that the probability that everybody gets
> it is high, you need to say it three times. So cycling is one of the things
> that I always think about"
> — [youtu.be/Unzc731iCUY?t=371](https://youtu.be/Unzc731iCUY?t=371)

> "because people will occasionally fog out and need to get back on the bus, you
> need to provide some landmark places where you're announcing that it's a good
> time to get back on."
> — [youtu.be/Unzc731iCUY?t=468](https://youtu.be/Unzc731iCUY?t=468)

> "So I'm enumerating and providing numbers. I'm giving you a sense that there's a
> seam in the talk, and you can get back on."
> — [youtu.be/Unzc731iCUY?t=498](https://youtu.be/Unzc731iCUY?t=498)

Winston's fourth "get back on the bus" device is asking the audience a question, and
waiting:

> "how much dead air can there be? How long can I pause? I counted seven seconds.
> It seemed like an eternity to me to wait and not say anything for seven seconds"
> — [youtu.be/Unzc731iCUY?t=528](https://youtu.be/Unzc731iCUY?t=528)

On humour: not at the start, fine at the end.

> "in the beginning of a talk, people are still putting their laptops away.
> They're becoming adjusted to your speaking parameters, to your vocal parameters,
> and they're not ready for a joke."
> — [youtu.be/Unzc731iCUY?t=279](https://youtu.be/Unzc731iCUY?t=279)

> "he said, oh, I always finish with a joke, and that way, people think they've
> had fun the whole time."
> — [youtu.be/Unzc731iCUY?t=3444](https://youtu.be/Unzc731iCUY?t=3444), quoting Doug Lenat

Winston also opens with an "empowerment promise", what you will know at the end that
you did not know at the start ([t=309](https://youtu.be/Unzc731iCUY?t=309)).
That is the skill's "Why this exists" chapter.

### Something changes every minute (DW Akademie / Radio Workshop)

A public-media training series on audio storytelling. `[observed]`

> "They're busy, they care, but they're probably also cooking, commuting, or doing
> a million other things. So, don't blast information at them. Think of it like
> taking your listener by the hand and walking them through your story. You
> reveal things as they're ready for them."
> — [youtu.be/emsvK6eD6hI?t=185](https://youtu.be/emsvK6eD6hI?t=185) (continues past t=217)

> "And every 45 seconds to a minute, something should change. Introduce a new
> voice, a piece of music, a sound in the scene, a shift in tone. Your listeners'
> attention needs a nudge, so give it to them."
> — [youtu.be/emsvK6eD6hI?t=217](https://youtu.be/emsvK6eD6hI?t=217)

> "We take our scripts to a table read. [...] We ask people to listen through,
> flag two things: one, confusion, and two, boredom. Both are editorial problems"
> — [youtu.be/emsvK6eD6hI?t=247](https://youtu.be/emsvK6eD6hI?t=247)

### Signposts and uneven rhythm (NPR Training)

Christopher Joyce, "Campfire tales: the essentials of writing for radio", NPR
Training. `[observed]`

> "Signposts are critical. Transitions between one thought and a relatively
> unrelated one are very important in radio. You simply can't be as abrupt as you
> can be in print. You need signposts to soften those transitions. Signposts are a
> sentence or two telling the listener, in essence, "OK, we've dealt with that
> part of the story, and now we're moving on to something a little bit
> different.""

> "Vary lengths of acts and tracks. You don't want Acts 1 through 5 each being 15
> seconds, with intervening tracks at 25 seconds each. Your story will sound like
> it was generated by a radio robot."

> "Each story should make one main point, or handle one clear issue. [...] If you
> can't summarize what the story is about in a single sentence, you're headed for
> trouble."

Source: [npr.org/sections/npr-training/2025/05/31/g-s1-65875](https://www.npr.org/sections/npr-training/2025/05/31/g-s1-65875/campfire-tales-the-essentials-of-writing-for-radio)

### Anecdote, then reflection (Ira Glass)

Auto-generated captions on a re-upload; the wording below is what the captions
carry, which is close but not clean. `[observed]`

> "the other big building block your other tool is that you have moment of
> reflection [...] at some point somebody's gotta say here's why the hell should
> listening to the story"
> — [youtu.be/f6ezU57J8YI?t=195](https://youtu.be/f6ezU57J8YI?t=195)

> "in a good story you're gonna flip back and forth between the two like [...] a
> little bit of action and some will say something about it [...] a little more
> actions will say something"
> — [youtu.be/f6ezU57J8YI?t=289](https://youtu.be/f6ezU57J8YI?t=289)

Glass also describes the story as "constantly raising questions and answering them"
([t=134](https://youtu.be/f6ezU57J8YI?t=134)). The alternation is a pace change
built into the structure: action runs fast, reflection slows down. `[assumed]`
that it reads that way in audio; Glass does not say so.

### Talk radio "resets"

Talk radio programmers tell hosts to restate the topic regularly because
listeners join mid-show. I could not retrieve the trade articles verbatim
(Barrett Media returned 403; the NuVoodoo piece redirected), so this rests on a
search summary only: a NuVoodoo article says programmers and consultants push
hosts to reset topics so new arrivals can catch up, and a 2024 Barrett Media
column says hosts should restate the topic after each guest question or call.
Treat as `[observed]` practice, unquoted.
([NuVoodoo](https://www.allaccess.com/nuvoodoo/archive/20972/gone-in-60-seconds),
[Barrett Media](https://barrettmedia.com/2024/09/26/news-talk-radio-and-the-art-of-the-reset/))

A drifting listener is a listener who joined mid-show, from the script's point
of view. `[assumed]`

### Orientation for listeners (Peter Sandman, risk communication)

> "it is a much bigger problem for listeners, who can't look back at previous
> pages to get reoriented."

> "It also gives them a second chance to tune in if their minds were starting to
> wander."

Source: Peter M. Sandman, "Orienting Your Audience: Six Signposting Tips",
[psandman.com/col/signposting.htm](https://psandman.com/col/signposting.htm) `[observed]`

### Oral style is redundant on purpose (Walter Ong)

> "Redundancy, repetition of the just-said, keeps both speaker and hearer surely
> on the track."

> "There is nothing to backloop into outside the mind, for the oral utterance has
> vanished as soon as it is uttered."

Ong, *Orality and Literacy* (1982), quoted at
[newlearningonline.com](https://newlearningonline.com/literacies/chapter-1/ong-on-the-differences-between-orality-and-literacy).
A search summary of the same section adds "Hence the mind must move ahead more
slowly, keeping close to the focus of attention much of what it has already
dealt with"; I did not see that sentence on a page I fetched. `[observed]`

### Recaps in serial audio drama

One audio drama review, via search summary only: recaps took a share of each
short episode and "can kill the flow for bingers", while weekly listeners
appreciated them. ([audiodramareviews.com](https://audiodramareviews.com/?p=8501))
The trade-off is real: a recap costs the attentive listener time. `[observed]`, weak.

---

## 4. Research findings

### Mind wandering is common in lectures, higher when listening, and rises with time

- **Listening produced the most mind wandering** of three ways to take in the
  same passage. Varao Sousa, Carriere and Smilek (2013), *Frontiers in
  Psychology*: "reading aloud led to the least amount of mind wandering, while
  listening to the passage led to the most mind wandering. Listening to the
  passage was also associated with the poorest memory performance and the least
  interest in the material." Mean proportion of probes caught mind wandering:
  listening M = 0.506, silent reading M = 0.356. The abstract names "audiobooks
  and podcasts" as the implication.
  [doi 10.3389/fpsyg.2013.00892](https://doi.org/10.3389/fpsyg.2013.00892) `[observed]`
- **Lecture rates cluster around a third to two-fifths.** Same paper's
  literature review: "40% of the time in Cameron and Giuntoli, 1972; 32.9% in
  Lindquist and McLean, 2011; 39 and 43% in Risko et al., 2012; 41% in Szpunar et
  al., 2013". These are probe rates from different designs, quoted from the
  review, not re-checked against each source. `[observed]`
- **It rises over a lecture.** Farley, Risko and Kingstone (2013), 40-minute
  lecture video, ratings every 5 minutes: "attention to, and retention of,
  lecture material declined as a function of time on task."
  [doi 10.3389/fpsyg.2013.00619](https://doi.org/10.3389/fpsyg.2013.00619).
  Risko et al. (2012) is reported by later papers as finding mind wandering up
  and memory down from the early to the late part of a lecture; I did not reach
  its full text. `[observed]`
- **Lapses are short and get more frequent.** Bunce, Flens and Neiles (2010),
  *J. Chem. Ed.*, abstract as returned by search: "Students report attention
  declines of 1 min or less more often than longer attention lapses. The data
  suggest that student engagement alternates between attention and nonattention
  in shorter and shorter cycles as lecture proceeds." Clicker questions and
  demonstrations lowered reported decline, and "This effect persisted during
  lectures immediately following". Full text not retrieved.
  [doi 10.1021/ed100409p](https://doi.org/10.1021/ed100409p) `[observed]`
- **The "10 to 15 minute attention span" is not supported.** Bradbury (2016),
  *Advances in Physiology Education*: "the available primary data do not support
  the concept of a 10- to 15-min attention limit", and "the greatest variability
  in student attention arises from differences between teachers and not from the
  teaching format itself."
  [doi 10.1152/advan.00109.2016](https://doi.org/10.1152/advan.00109.2016) `[observed]`

### A lapse breaks the mental model, not just a fact, and early lapses cost most

Smallwood, McSpadden and Schooler (2008), *Memory & Cognition*, readers of a
detective novella: "mind wandering interfered with the construction of the
situation model independent of the participants' ability to retrieve factual
information. The analysis of the temporal consequences of zoning out indicated
that lapses had the greatest influence when they occurred early in the
narrative." Successful readers zoned out less "when the text revealed a clue".
[doi 10.3758/mc.36.6.1144](https://doi.org/10.3758/mc.36.6.1144) `[observed]`

This is the owner's failure exactly: they missed a key concept and the rest of the
story stopped making sense. Reading, not listening, so `[assumed]` that it
transfers; the listening data above suggest it is worse in audio.

A 2025 EEG preprint adds a twist: during self-reported mind wandering while
listening to an audiobook, word-level prediction markers "remained intact", but
the subjective experience of meaning dimmed. The brain keeps tracking words it
is not understanding. Chen et al., bioRxiv,
[doi 10.1101/2025.08.29.673052](https://doi.org/10.1101/2025.08.29.673052),
not peer reviewed. `[observed]`

### Interrupting the stream with retrieval cuts mind wandering

Szpunar, Khan and Schacter (2013), *PNAS*: interpolating online lectures with
memory tests helps students "sustain attention to lecture content in a manner
that discourages task-irrelevant mind wandering activities, encourages
task-relevant note-taking activities, and improves learning."
[doi 10.1073/pnas.1221764110](https://doi.org/10.1073/pnas.1221764110).
In an author interview, Szpunar says students tested through a 21-minute
lecture "were half as likely to mind wander", and untested students "reported
mind wandering 40% of the time."
([medicalresearch.com](https://medicalresearch.com/interpolated-memory-tests-reduce-mind-wandering-and-improve-learning-of-online-lectures/))
A 21-minute lecture is the podcast's length. `[observed]`

Risko, Liu and Bianchi (2024): the interpolated-testing benefit "was as robust
in a normal speed lecture and a lecture that was sped up 1.5×."
[doi 10.1037/xap0000494](https://doi.org/10.1037/xap0000494) `[observed]`

The **pause procedure** (Ruhl, Hughes and Schloss, 1987, *Teacher Education and
Special Education* 10, 14-18): roughly three 2-minute pauses at logical breaks
where students compare notes or recall; secondary sources report better
immediate free recall. A 1995 follow-up with college students with learning
disabilities ("The Pause Procedure and/or an Outline", [SAGE](https://journals.sagepub.com/doi/10.2307/1511361))
reportedly found the pause procedure alone best for immediate recall and note
completeness. The pauses are active, not silence. Neither full text retrieved.
([UWyo summary](https://www.uwyo.edu/science-initiative/lamp/active-learning-spectrum/writing-incorporating-pauses.html)) `[observed]`

### Re-exposure alone does not help

Martin, Mills, D'Mello and Risko (2018): "there were no benefits of massed
re-watching on memory for lecture material and re-watching increased rates of
mind wandering." [doi 10.1027/1618-3169/a000412](https://doi.org/10.1027/1618-3169/a000412)

Rewinding replays the same words at the same density. A recap restates the
state in fewer words. Different things. `[assumed]`

### Macro signposts help; filler connectives do not

Chaudron and Richards (1985 working paper; published 1986 in *Applied
Linguistics*), L2 listeners, four versions of the same lecture. Macro markers
such as "What we've come to by now was that..." and "To begin with" beat micro
markers such as "Well" and "And so":

> "Macro markers, that is, the higher order discourse markers signalling major
> transitions and emphasis in the lectures, are more conducive to successful
> recall of the lecture than micro markers, that is, lower order markers of
> segmentation and intersentential connections."

Adding micro markers on top of macro ones did worse than macro alone: "it
increased the listeners' attention requirements without adding valuable
information in any way". Second-language listeners, so `[assumed]` that the size
of the effect carries to native listeners.
[ScholarSpace PDF](https://scholarspace.manoa.hawaii.edu/items/cd3514b8-4bb9-4cb4-927f-8b119167c1bc/full) `[observed]`

### Signaling and segmenting (multimedia learning)

- **Signaling**: Mautone and Mayer (2001) found signaled material improved
  transfer; their signals included narration cues. Richter, Scheiter and Eitel
  (2016) meta-analysis is reported by a search summary at r = 0.17 for
  comprehension and transfer, strongest for low prior knowledge. I did not reach
  either full text. `[observed]`, secondary.
- **Segmenting**: Rey et al. (2019), *Educational Psychology Review*, 56 studies,
  reported by search summary as small-to-medium benefits on retention and
  transfer, lower cognitive load, and confirmed for system-paced segmentation,
  meaning pauses the learner does not control.
  [doi 10.1007/s10648-018-9456-4](https://doi.org/10.1007/s10648-018-9456-4).
  Abstract not retrieved; figures unchecked. `[observed]`, secondary.

The listener is low prior knowledge by definition: they have not typed the code
yet. That is the group signaling helps most. `[assumed]`

### Pauses at boundaries restore recall; fillers help, coughs hurt

- O'Leary et al. (2023), *Trends in Hearing*: "inserting silent pauses at
  linguistically salient points within a time-compressed narrative
  ("time-restoration") returns recall accuracy to a level approximating that for
  a normal speech rate", and pupil dilation showed the effort of fast speech
  dropped with the pauses.
  [doi 10.1177/23312165231203514](https://doi.org/10.1177/23312165231203514) `[observed]`
- Fraundorf and Watson (2011), *J. Memory and Language*: "While fillers
  facilitated recall, coughs matched in duration to the fillers impaired recall,
  suggesting that fillers' benefits cannot be attributed to adding processing
  time." They favour "an attentional orienting account in which fillers direct
  attention to the speech stream".
  [doi 10.1016/j.jml.2011.03.004](https://doi.org/10.1016/j.jml.2011.03.004) `[observed]`
- Corley, MacGregor and Donaldson (2007), *Cognition*: "words preceded by
  disfluency were more likely to be remembered."
  [doi 10.1016/j.cognition.2006.10.010](https://doi.org/10.1016/j.cognition.2006.10.010) `[observed]`

So a person visibly thinking ("er", "hang on") is not noise. It flags the next
word. Fraundorf and Watson used natural fillers spliced into human speech;
whether a synthetic "um" does the same is untested. `[assumed]`

### Speed

Murphy et al. (2021), *Applied Cognitive Psychology*: "minimal costs incurred by
increasing video speed from 1x to 1.5x, or 2x speed, but performance declined
beyond 2x speed", with the caveat that "these trends may differ for videos with
different speech rates, complexity or difficulty".
[doi 10.1002/acp.3899](https://doi.org/10.1002/acp.3899). Lecture video, not
dense two-host audio. `[observed]`

### Humour

Banas et al. (2011), "A Review of Humor in Educational Settings: Four Decades of
Research", *Communication Education*: secondary sources report effects on
attention and classroom climate are the best supported, and the link to learning
is mixed. Full text not retrieved.
[doi 10.1080/03634523.2010.496867](https://doi.org/10.1080/03634523.2010.496867) `[observed]`, secondary.

---

## 5. Workarounds people use today

| Workaround | Who | Cost | Evidence |
|---|---|---|---|
| 30 s / 1 min skip-back | Rewinder | Overshoot, re-drift, awkward in a car | inputcoffee, Lewton, wycx |
| Skip to chapter | Car listener | Only as good as the chapter start | baggy_trough, hedora ([HN 37469021](https://news.ycombinator.com/item?id=37469021)) |
| Pick modular shows only | Drift-in/out | Gives up on "high attention" content | coldpie |
| Speed up to force attention | Efficiency listener | "firehouse", stress | latexr, fluxsauce, raybb |
| Trim silence | Efficiency listener | Deletes pauses the producer put in | fedups, francis-io, bearcobra |
| Pause and ask an AI host | Pause-and-ask | Interrupt is "super-janky" ([HN 48948063](https://news.ycombinator.com/item?id=48948063)) | falcor84, sitkack |
| Read along with the text | Anyone | Needs eyes, defeats the commute | @rcc_96, [youtu.be/0WGiVmUT72c](https://youtu.be/0WGiVmUT72c); anon2020dot00 ([HN 29330517](https://news.ycombinator.com/item?id=29330517)) |
| Save a snippet on "back" button | Note-taker | App-specific (Snipd) | threecheese ([HN 42918963](https://news.ycombinator.com/item?id=42918963)) |

Every workaround is the listener's labour after the lapse. Nothing in the
evidence is a producer building re-entry into the audio, except radio resets and
Winston's cycling. `[observed]`

---

## 6. Kokoro: what the renderer can and cannot do

Checked against `skills/podcast/scripts/render.py`, the installed `kokoro` 0.9.4
and `misaki` packages, and a test render on the RTX 5080
(a throwaway pause-measuring script, not kept).

- **Silence between lines** is the renderer's, not Kokoro's: `GAP_LINE = 0.28` s
  after every line, `GAP_CHAPTER = 1.0` s after every chapter. Fixed. `[observed]`
- **Punctuation inside a line** gives Kokoro's own pause, about 0.2 to 0.3 s.
  Measured on one sentence pair: full stop about 0.29 s, `...` about 0.31 s,
  comma, `…` and em dash about 0.2 s. An ellipsis does not buy a long pause. So
  the gap *between* lines is the same length as a full stop *inside* a line:
  nothing marks a change of speaker or a landed point. `[observed]`, one test.
- **No SSML, no break tags, no laughter tags.** The only inline markup misaki
  parses is the `[word](/ipa/)` link the `pronounce` map already uses.
  `[observed]` from the source.
- **"Hmm." and "Ha!"** are read as words: phonemes `hmm` and `hˈɑ`. A spoken
  "hm" is plausible; a laugh is not available. `[observed]`; whether "hm" sounds
  natural needs an audition. `[assumed]`
- **Speed is per call.** `pipe(text, voice, speed=...)`; `render.py` passes
  `speed=1.0` for every line. 0.85 made a test line 16% longer than 1.0. Per-line
  pace changes are a one-argument change. `[observed]`
- **Turn-taking only.** Each line is a separate generation, concatenated. No
  overlap or interruption, which behnamoh named as NotebookLM's one real
  novelty. Overlap could be faked by mixing the next line in before the gap,
  but that is untested. `[assumed]`
- **The lint rejects anything that is not `A:`/`B:`/`##`/comment**, so a beat
  marker needs a parser change in `podcast.py` (`LINE` regex) before render can
  see it. `[observed]`

---

## Suggestions

Interpretation starts here.

**The diagnosis.** The episode is a dependency chain told in one even rhythm.
The story structure is right: it gives the listener one thing to follow. But a
chain has no re-entry points. Smallwood says a lapse breaks the model and early
ones cost most; Varao Sousa says listeners lapse more than readers; Bunce says
lapses are short and get more frequent; the owner says it happened. Meanwhile
the renderer puts the same 0.28 s between every line, so the audio has no seams
for Winston's bus to stop at. Two fixes, one for each half: put the running state
back into the script at fixed points, and make the audio uneven. A ship's log
with no noon position be a fine yarn until ye nod off on watch.

### 1. A "where we are" line at the top of every story chapter (the re-entry hook)

Rule for `script-format.md`: every chapter after the first opens with a
re-entry line of two or three sentences that restates the running state:
where the one thing is now, which mechanisms it has passed, and what the
analogy currently maps to. Macro marker first ("So here's where we've got
to."), not filler ("So, well").

- It sits at the chapter marker, so a car listener who hits "previous chapter"
  lands on a recap, not mid-scene. Chapter skip becomes the rewind button that
  works.
- Cadence: with four to six scenes in 15-25 minutes, that is a hook every three
  to four minutes. That is the chapter cadence the skill already has, so no new
  structure.
- Cost: at the skill's own 150 words a minute, a 40-word recap is 16 seconds.
  Six of them is about a minute and a half.
- Source tags: a recap line restates earlier claims. Tag it `recap` plus the
  sources of what it restates, and have the verifier check it adds nothing new.
  A recap that sneaks in a new claim is the worst place for an error, because
  the drifter trusts it most.

Options for who says it:

1. **B says it, A corrects or extends.** "Let me check I've got this. The write
   is in the buffer, the bookmark hasn't moved, and nothing's on disk yet." A:
   "Nearly. The bytes are on disk. The bookmark is what hasn't moved." Recommended:
   it is B being the listener's proxy, it reads as someone thinking, and the
   correction is the retrieval moment Szpunar measured.
2. A says it as narration. Simpler, and the radio reset is literally this. Flatter.

### 2. Cycle the picture three times

Winston's rule, and Ong's. The core analogy appears in "The picture", is
restated once in the middle of "The story" with the mechanisms added so far,
and closes "When you type it". Three passes, each one fuller. The middle pass
can be the re-entry line of the middle chapter.

### 3. One retrieval beat per story chapter

B asks the listener, not A: "Before you hear it, what do you reckon happens to
the write now?" Then real silence, then A answers. Szpunar's interpolated
tests and Winston's seven seconds both point here. In audio, seven seconds
reads as a dead file; two to three seconds is my guess, to audition.
`[assumed]` Some players trim silence, so the question has to work even if the
gap is gone: the answer must not depend on the listener having used the pause.

### 4. Make the audio uneven: beat markers and variable gaps

The renderer is the "radio robot" Joyce warns about: every turn is the same
length of gap. Options:

1. **A `{beat}` token** the script can put at the end of a line, parsed by
   `podcast.py` and rendered as a longer gap (around 1 to 1.5 s, to audition).
   Used after the line that lands a mechanism, after a gotcha's moment of
   surprise, and after a retrieval question. Recommended: it is one regex and
   one dict lookup, and the writer decides where weight goes.
2. Vary `GAP_LINE` by rule: shorter (0.15 s) inside a quick B/A exchange, longer
   before a chapter's recap. Automatic, but the renderer cannot know which line
   landed the point.
3. Both. Probably where it ends up.

Cap beats per chapter (two or three) in the lint, or the episode turns into
dramatic pauses. Silence alone is not a re-entry device: the efficiency listener
deletes it. The recap lines carry re-entry; beats carry pace.

### 5. Anecdote, then reflection: alternate the tempo inside a scene

Glass's two blocks map onto the scene template the skill already has: "what
happens" is anecdote, "what would go wrong without the mechanism, then the
mechanism" is reflection. Make the switch audible. Action lines short and
quick; the reflection line slower, with a beat before it. Kokoro's per-line
`speed` can do this: a `pace` hint or a speed of about 0.9 on the line that
names a concept for the first time. `[assumed]`, needs an audition. The DW
"something changes every 45 seconds to a minute" rule is a checkable lint: no
more than N consecutive lines from one host, or N lines in a row of the same
length band.

### 6. Let B think out loud, sparingly

The fillers research says a hesitation before an important word helps the
listener hold it. B is allowed one "Hm. Hang on." per chapter, placed before the
question that leads to the mechanism. Not "um" scattered as texture: that is the
NotebookLM tic the persona doc found people quitting over, and Chaudron and
Richards found filler markers made things worse. Audition Kokoro's "Hm." before
trusting it.

### 7. No laughter, a little dry humour, at the end

Kokoro cannot laugh, and a spliced laugh sample over a flat TTS voice is likely
to sound worse than none `[assumed]`. Keep the current "no laughter cues" rule.
Humour as content is fine: one dry line in "When you type it", per Winston's
Lenat quote. The humour research says it buys attention, not learning; that is
still worth something at minute twenty.

### 8. Say what the episode will do, once, at the top

The empowerment promise already exists as "Why this exists". Add one line of
map after it: "First the picture, then we follow one write through a crash,
then the three things that bit." That is the "tell them what you'll tell them"
half, and it gives the re-entry lines something to refer back to.

### What not to do

- Do not answer "relentless" by slowing the whole thing down. Murphy's data say
  speed is not the problem, and the efficiency listener will speed it up again.
  The problem is no structure in time, not too much speed. `[assumed]`
- Do not recap by repeating lines. Re-watching data says re-exposure without
  compression raises mind wandering. Recaps restate state, shorter than the
  original.

### Open question for the owner

Which part did they drift during? If it was early (picture or first scene),
Smallwood predicts exactly the "could not get back in" result, and the
strongest fix is a second pass of the picture right before the story starts.
If it was mid-story, the chapter re-entry line is the fix. Worth asking before
building both.

---

## Provenance

**YouTube transcripts:** `Unzc731iCUY` (Patrick Winston, How to Speak, MIT
OpenCourseWare), `f6ezU57J8YI` (Ira Glass on Storytelling part 1, re-upload,
auto captions), `emsvK6eD6hI` (Radio Workshop and DW Akademie, Writing for the
ear).

**YouTube comments:** `Unzc731iCUY` (nothing usable; top comments are summaries
in other languages), `0WGiVmUT72c` (Sense of Mind, reading vs listening to
audiobooks; low engagement, likes 0 to 12).

**YouTube searches that returned nothing usable:** podcast too dense / no
pauses; podcast editing pauses; NotebookLM audio review annoying; zoning out
with audiobooks (gave `0WGiVmUT72c`); ADHD zoning out podcasts; writing for the
ear (first phrasing).

**Hacker News comments** (Algolia API): 43413713, 39581308, 669571, 43414298,
20431005, 14060858, 20449756, 10787249, 20450024, 31264893, 46115210, 37469021,
39865619, 20449665, 15742083, 34893634, 15742010, 34207193, 22212851, 20451298,
42914500, 44441989, 42912891 (thread, OP building a product), 45317977,
41694231, 44010366, 41966822, 34260120, 48948063, 29330517, 42918963.

**Reddit:** none. Arctic Shift returned 522 at session start and end.

**Papers and abstracts** (via Europe PMC, Crossref, or as noted):
- Varao Sousa, Carriere, Smilek 2013, [10.3389/fpsyg.2013.00892](https://doi.org/10.3389/fpsyg.2013.00892) (full text)
- Szpunar, Khan, Schacter 2013, [10.1073/pnas.1221764110](https://doi.org/10.1073/pnas.1221764110) (abstract) and [author interview](https://medicalresearch.com/interpolated-memory-tests-reduce-mind-wandering-and-improve-learning-of-online-lectures/)
- Farley, Risko, Kingstone 2013, [10.3389/fpsyg.2013.00619](https://doi.org/10.3389/fpsyg.2013.00619) (abstract)
- Risko et al. 2012, via secondary citations only
- Smallwood, McSpadden, Schooler 2008, [10.3758/mc.36.6.1144](https://doi.org/10.3758/mc.36.6.1144) (abstract)
- Chen et al. 2025 preprint, [10.1101/2025.08.29.673052](https://doi.org/10.1101/2025.08.29.673052) (abstract)
- Bunce, Flens, Neiles 2010, [10.1021/ed100409p](https://doi.org/10.1021/ed100409p) (abstract via search)
- Bradbury 2016, [10.1152/advan.00109.2016](https://doi.org/10.1152/advan.00109.2016) (abstract)
- Risko, Liu, Bianchi 2024, [10.1037/xap0000494](https://doi.org/10.1037/xap0000494) (abstract)
- Martin, Mills, D'Mello, Risko 2018, [10.1027/1618-3169/a000412](https://doi.org/10.1027/1618-3169/a000412) (abstract)
- Ruhl, Hughes, Schloss 1987, *Teacher Education and Special Education* 10, 14-18 (secondary only); 1995 follow-up [10.2307/1511361](https://journals.sagepub.com/doi/10.2307/1511361) (search summary only)
- Chaudron and Richards 1985/1986, [ScholarSpace](https://scholarspace.manoa.hawaii.edu/items/cd3514b8-4bb9-4cb4-927f-8b119167c1bc/full) (full working paper), [10.1093/applin/7.2.113](https://doi.org/10.1093/applin/7.2.113)
- Mautone and Mayer 2001, [10.1037/0022-0663.93.2.377](https://doi.org/10.1037/0022-0663.93.2.377) (secondary only)
- Richter, Scheiter, Eitel 2016 signaling meta-analysis (search summary only)
- Rey et al. 2019, [10.1007/s10648-018-9456-4](https://doi.org/10.1007/s10648-018-9456-4) (search summary only)
- O'Leary et al. 2023, [10.1177/23312165231203514](https://doi.org/10.1177/23312165231203514) (abstract)
- Fraundorf and Watson 2011, [10.1016/j.jml.2011.03.004](https://doi.org/10.1016/j.jml.2011.03.004) (abstract)
- Corley, MacGregor, Donaldson 2007, [10.1016/j.cognition.2006.10.010](https://doi.org/10.1016/j.cognition.2006.10.010) (abstract)
- Murphy et al. 2021, [10.1002/acp.3899](https://doi.org/10.1002/acp.3899) (abstract)
- Banas et al. 2011, [10.1080/03634523.2010.496867](https://doi.org/10.1080/03634523.2010.496867) (secondary only)

**Practitioner pages:** [NPR Training, Campfire tales](https://www.npr.org/sections/npr-training/2025/05/31/g-s1-65875/campfire-tales-the-essentials-of-writing-for-radio)
(fetched), [Sandman, signposting](https://psandman.com/col/signposting.htm)
(fetched), [Ong via newlearningonline](https://newlearningonline.com/literacies/chapter-1/ong-on-the-differences-between-orality-and-literacy)
(fetched), [NuVoodoo](https://www.allaccess.com/nuvoodoo/archive/20972/gone-in-60-seconds)
and [Barrett Media](https://barrettmedia.com/2024/09/26/news-talk-radio-and-the-art-of-the-reset/)
(not retrievable, search summary only), [audiodramareviews.com](https://audiodramareviews.com/?p=8501)
(search summary only).

**Local:** `skills/podcast/scripts/render.py`, `skills/podcast/scripts/podcast.py`,
kokoro 0.9.4 `pipeline.py`, misaki `en.py`, and a throwaway test render.
