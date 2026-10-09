# Human Replay: persona evidence

Evidence collection on the practice itself: rebuilding agent-written code by hand to understand and own it. Collected 2026-10-10.

**Source coverage.** Hacker News (Algolia API, full threads dumped), papers and practitioner blogs (WebSearch/WebFetch), YouTube (3 searches, 3 comment pulls, 1 transcript). Reddit not covered: Arctic Shift returned 522 at start and again at the end. That is a real gap. r/ExperiencedDevs and r/learnprogramming would likely add volume, especially on the novice side.

**Quote fidelity.** HN and YouTube quotes are verbatim from the API. Blog and paper quotes came through WebFetch extraction; the fragments in quotation marks are what the extractor returned as verbatim, but some may be truncated. Re-check against the page before publishing any of them.

**Tags.** `[observed]` = someone describes what they did or saw. `[assumed]` = opinion, prediction or argument without a described behaviour.

---

## 1. The closest existing practice: retype the agent's code

The practice already exists in the wild, under at least three names. Each runs it without tooling.

**Ankur Sethi, "Prevent cognitive debt by manually retyping LLM-generated code", 2 Aug 2026.** No product. HN front page: 545 points, 443 comments ([HN 49153374](https://news.ycombinator.com/item?id=49153374)).
- [observed] "I ask my coding assistant to generate code in the chat, then manually make all the edits myself." ([post](https://ankursethi.com/blog/prevent-cognitive-debt-by-manually-retyping-llm-generated-code/))
- [observed] Agent instruction they use: "Never create, edit, move, rename, or delete project files unless I explicitly ask you to do so."
- [observed] "I know where every bit of functionality lives in the codebase."
- [observed] "Instead of being 10x faster, I'm probably only 2x faster." (their own estimate, not measured)
- [observed] Cost: "Poring over hundreds of lines of overly-defensive, badly-commented, subtly incorrect code is not fun."
- [observed] Scope: "Personal projects must be fun above all else."

**Ben Kamens, "Coding with AI the Hard Way", June 2025.** Named after Zed Shaw. Incentive tell: links a consulting page (olddogs.ai).
- [observed] "physically typing out every character of every line of code they suggest" ([post](https://kamens.com/blog/code-with-ai-the-hard-way))
- [observed] "I end up editing the vast majority of lines they produce as I'm re-typing their output."
- [observed] "I love the result, I wind up connected to the code, and I'm having fun." / "What sounds like friction doesn't feel like it to me."

**Gabriella Gonzalez, "Type out the code", 19 May 2026.** Argues for typing from memory generally; agentic coding is the reason it matters now.
- [assumed] If you can't type an idea out precisely, "you didn't really have it in mind." You were "hallucinating understanding, the same as an LLM." ([post](https://haskellforall.com/2026/05/type-out-the-code))
- [assumed] "How can you review the agent's output for quality if you understand the code worse than the agent does?"

**Older, pre-agent form** (HN, verbatim):
- [observed] "Previously I used to obey a rule that if I ever use LLM generated code, I have to manually type it in - so that I myself have the familiarity of every symbol in the code. This helped considerably reduce that problem. But I stopped doing that out of laziness." @pizza ([HN 41939359](https://news.ycombinator.com/item?id=41939359))
- [observed] "When I was younger and took over a codebase I open it up in one window and then type it back into another window. Not only did I catch/fix a crazy number of bugs, but I became a near expert overnight. Doing the typing would cause me to question everything, ask why we import something, why x is used and not y, etc." ... "no matter how good it is I have never met anyone else that does it" @r0ze-at-hn ([HN 49154099](https://news.ycombinator.com/item?id=49154099))
- [observed] "I had to manually write everything it spit out. What ended up happening is that I was typing, I'd notice little weird bits here and there, and I'd ask questions about it, explore alternatives, etc. ... within 3-4 hours, I was comfortable enough with the syntax that I was writing it entirely by hand" @danielvaughn ([HN 49156814](https://news.ycombinator.com/item?id=49156814))
- [observed] "I did this too. Almost always I'd rename variables, change formatting, add or remove comments, etc.. Unfortunately this feels less easy to do with modern tools. For example, Claude Code expects to edit your actual source files" @tdeck ([HN 49157018](https://news.ycombinator.com/item?id=49157018))
- [observed] "I do find myself manually typing in really critical code. In those cases even if I do have an LLM alongside these days, LLM suggestions also then get manually typed." @Kim_Bruning ([HN 49154129](https://news.ycombinator.com/item?id=49154129))
- [observed] "If I feel rushed ... and I copy+paste something, it always leaves me with a sense of unease. It creates a memory & comprehension hole that sticks out like a sore thumb ... Typing out code manually gives you time and space to consider the broader picture." @wahern ([HN 49153811](https://news.ycombinator.com/item?id=49153811))

**Tutorial-era form** (type it, don't paste it):
- [observed] Khan Academy disabled copy/paste on beginner hint code after seeing "many students had clearly copy-pasted the hint code"; goal was to make students "take the challenge more slowly, and think about what it was they were typing." They found no programming-specific research to back it. ([Khan Academy 2013](https://cs-blog.khanacademy.org/2013/09/sorry-students-no-more-copy-paste.html))
- [observed] "This book mandated that you type all the examples out line-by-line. I thought the idea was a pretty silly one, but I stuck with it ... 14 years later ... I can trace back a lot of my initial improvements to its requirement" @sarreph ([HN 49154604](https://news.ycombinator.com/item?id=49154604))
- [assumed] John D. Cook: typing examples means "you'll make mistakes, just as you will in real work", which gives "the opportunity ... to learn debugging." ([post](https://www.johndcook.com/blog/2012/12/18/the-value-of-typing-code/))

**What the thread converged on.** Typing is the trigger, not the mechanism. Supporters and critics say the same thing from opposite sides:
- [assumed] "Typing itself is irrelevant, it is the timing spent, even if only seconds, pondering at what each word or syntactic element is and why use it." @utopiah ([HN 49153819](https://news.ycombinator.com/item?id=49153819))
- [assumed] "Retyping is merely a gateway to (sometimes) trigger the engagement. The solution in TFA feels like an on-ramp to cargo culting" @WJW ([HN 49154141](https://news.ycombinator.com/item?id=49154141))
- [observed] "If you just touch type them in you learn very little. ... If you 'make it your own' then you're probably at the right level of understanding." @jolt42 on C64 magazine listings ([HN 49158951](https://news.ycombinator.com/item?id=49158951))

---

## 2. Switching stories

### Toward ownership (stopped accepting wholesale)

- [observed] **Mo Bitar**, after two years of agentic coding: "After reading months of cumulative highly-specified agentic code, I said to myself: I'm not shipping this shit." Problem: "Agents write units of changes that look good in isolation." "But respect for the whole, there is not." Now: "So I'm back to writing by hand for most things." ([post, 26 Jan 2026](https://atmoio.substack.com/p/after-two-years-of-vibecoding-im); HN 865 points, [46765460](https://news.ycombinator.com/item?id=46765460)). Has a YouTube channel; no product.
- [observed] "It was so easy to create 50+ project with a sleek ui, but i could not explain any of them. ... whenever my tokens ran out , my productivity was zero. ... I make it draft stuff for me , then i interrogate it, i make it justify every line of code that it writes, until i understand the code myself that i can write it if i wanted to." @kbrannigan ([HN 49348116](https://news.ycombinator.com/item?id=49348116))
- [observed] "I tried vibe-coding few years back and switched to 'manual' mode when I realized I don't fully understand the code. No, I did read each line of code and understood it ... but I didn't understand all nuances" @oxag3n ([HN 46771721](https://news.ycombinator.com/item?id=46771721)). Reading every line was not enough for this person.
- [observed] "I started learning how to code 4 months ago ... I'd tell my self if I study the code I'll understand, so I ran out of token on VS code, and decided to code without using AI, long story short I didn't know jack shit and now I've started over again" @anthonyogegbene7865, 0 likes ([YouTube 1Se2zTlXDwY](https://youtu.be/1Se2zTlXDwY))
- [observed] "I waltzed into a tech screen thinking I could handcode python after having LLM be primary at it for over a year. Yeah, there's atrophy -- I humiliated myself ... I've been mixing hand-coding into my routines ever since" @schmookeeg ([HN 48555149](https://news.ycombinator.com/item?id=48555149))
- [observed] Coworker "was trying not to use AI for any code generation anymore, but it was really difficult to stop because it was so easy to reach for." @Izkata, second-hand ([HN 47391995](https://news.ycombinator.com/item?id=47391995))

### Away from retyping (tried it, quit)

This is the most important pattern for the persona. Retyping decays.

- [observed] **Kamens, three posts, nine months.** June 2025: retype every character. 5 Jan 2026: "I've shifted from 'Hard Way most of the time' to 'Hard Way for critical moments.'" Kept it "for critical pieces or complex code when I don't want to cede full lack of understanding to the machine." ([update](https://kamens.com/blog/code-with-ai-the-hard-way-update)). March 2026: "I didn't even read a line of code when shipping Murder Boards" ([update II](https://kamens.com/blog/code-with-ai-the-hard-way-update-ii)). They told HN they moved "for fear of being seen as a luddite" ([HN 49163294](https://news.ycombinator.com/item?id=49163294)).
- [observed] @pizza (above): "But I stopped doing that out of laziness."
- [observed] "even I tried this approach. For a while it worked, though that 'while' didn't last ... a part of me has definitely been hijacked, in much the same way as the addictive type of social media." @mahami ([HN 49157006](https://news.ycombinator.com/item?id=49157006))
- [observed] "I've got similar concerns about skill rot, but I also have chronic RSI and some hand arthritis. ... I can't really type every character anymore. I can read it all but…falling into skimming is very hard to avoid." @shermantanktop ([HN 49164031](https://news.ycombinator.com/item?id=49164031))

Quit reasons seen: laziness/ease of the alternative, social pressure (looking like a luddite), physical cost, and the agent-generated code getting good enough that the critical parts shrink. Nobody in the sample quit because retyping failed to teach them.

### Never adopted, explicitly rejected

- [assumed] "The notion of reading every line of code is absurd to me, the notion of RETYPING it beggars belief. Surely this is satire." @dools ([HN 49156588](https://news.ycombinator.com/item?id=49156588))
- [observed] "I stopped writing code completely about a year ago, stopped reading code completely about 8 months ago ... Not sure about efficiency gains but I got promoted 3 weeks ago :)" @p1esk ([HN 49163957](https://news.ycombinator.com/item?id=49163957))
- [observed] "It was only with Claude Code that I realized I never actually enjoyed programming—I enjoyed building things." @big_paps ([HN 49165180](https://news.ycombinator.com/item?id=49165180))

---

## 3. Comprehension debt, atrophy, rubber-stamping

### The named problem

- Addy Osmani: comprehension debt is "the growing gap between how much code exists in your system and" how much anyone understands; unlike tech debt it "breeds false confidence." "The codebase looks clean. The tests are green." "Engineers approved code they didn't fully understand, which now carries implicit endorsement." ([O'Reilly repost, 13 Apr 2026](https://www.oreilly.com/radar/comprehension-debt-the-hidden-cost-of-ai-generated-code/)). Note: Osmani quotes "above 65%" / "below 40%" via "Research suggests"; those come from the Anthropic study below.
- Margaret-Anne Storey proposes a triple debt model: technical debt in code, cognitive debt in people, intent debt in externalized rationale. A synthesis paper, no experiment. ([arXiv 2603.22106](https://arxiv.org/abs/2603.22106); [Tech Lead Journal #264](https://techleadjournal.dev/episodes/264/))
- [assumed] Naur, via @mrkeen: "they'd still passively absorb some of the model while typing the code into the computer. I think that it's this last resort of incidental model building that the LLM replaces." ([HN 45424366](https://news.ycombinator.com/item?id=45424366))

### Observed symptoms

- [observed] "I end up working on a codebase I barely understand. My own skills have degraded. It just gets worse the longer you go" @AstroBen ([HN 46320334](https://news.ycombinator.com/item?id=46320334))
- [observed] Interviewing an intern: "they couldn't explain anything about code they'd written ... they finally shrugged and said that 'GenAI did most of it.'" @goostavos ([HN 46767863](https://news.ycombinator.com/item?id=46767863))
- [observed] "After vibe coding for a month or so I let my subscription expire. Now when I look at the code it's like 'ugh you mean now I have to think about this with my own brain???' ... it's like AI eats away at your pride of ownership." @daxfohl ([HN 46771375](https://news.ycombinator.com/item?id=46771375))
- [observed] "I feel no connection to them because I didn't build them." @cedws ([HN 47391648](https://news.ycombinator.com/item?id=47391648))
- [observed] "I'm afraid my coding skills are atrophying, in fact I know the are ... If I go work at a startup without the money I pay for these models, I think for the first time in my career I would be less likely to be able to successfully code a feature than I could last year." @greenpizza13, at an AI company ([HN 47392416](https://news.ycombinator.com/item?id=47392416))
- [observed] "when I just have AI write code for me, I lose my mental model of the project and ultimately just feel like I'm delaying some kind of execution." @bovermyer ([HN 46769369](https://news.ycombinator.com/item?id=46769369))
- [observed] Junior trimmed an LLM's inheritance chain by asking line by line, "but missed two of them because it didn't understand on a product side why they weren't needed. Fast forward a year, these abstract classes are still inherited, no one knows why" @justsocrateasin ([HN 45425506](https://news.ycombinator.com/item?id=45425506)). Line-by-line questioning without product context fails.

### Rubber-stamping and review overload

- [assumed] "you can't review code being generated faster than you can read it. You either become a bottleneck (defeats the point) or you rubber-stamp it (creates the debt). Pick your poison." @trjordan ([HN 45424824](https://news.ycombinator.com/item?id=45424824))
- [observed] Gabriel Martinez (G2i; incentive: selling an orchestration tool, ORC): "engineers around me were merging at an incredible pace and I felt constant anxiety that I was not moving fast enough. And I can admit that it led me to merge code that I didn't necessarily review" ([talk @491s](https://youtu.be/6qkzlT962es?t=491))
- [assumed] Martinez: "The danger is that the engineer never noticed that there was a choice to make." ([@62s](https://youtu.be/6qkzlT962es?t=62)) / "Generation is cheap, but evaluation is expensive." ([@614s](https://youtu.be/6qkzlT962es?t=614))
- [observed] "I have a stack of neat prototypes and maybe-production-quality features that I can't ship yet because I've not done that review work." @simonw ([HN 47390672](https://news.ycombinator.com/item?id=47390672))
- [observed] "I basically only review code now. It changes so fast it is impossible to have a stable mental model of the application." @throwatdem12311 ([HN 47392053](https://news.ycombinator.com/item?id=47392053))
- [observed] "When I began reviewing my teammate's PRs with AI generated code in it ... I realized the problem: I am not reviewing the work my teammate did. ... the decisions made in the conversation are the real work. That is what needs capture and review." @rDr4g0n ([HN 47217963](https://news.ycombinator.com/item?id=47217963))
- [observed] "Usually within a few questions the answer 'the AI wrote it that way' will come out." @ericmcer ([HN 45815693](https://news.ycombinator.com/item?id=45815693))
- [observed] Reviewer script: "To be honest, I vibe coded this and I don't understand all of it. When I try to make it smaller, I can't find a way. Can we go through it together?" @MikeNotThePope ([HN 45806992](https://news.ycombinator.com/item?id=45806992))

### Counter-position: ask the agent when you need it

- [observed] "Now I say to the LLM 'tell me what's going on' and it tells me. ... It's SO much faster than grepping through the source myself" @dools ([HN 49156588](https://news.ycombinator.com/item?id=49156588))
- [observed] "I definitely couldn't pass a quiz on miette. I'm OK with this. ... Claude basically allows me to spend my learning strategically." @ekidd ([HN 46823397](https://news.ycombinator.com/item?id=46823397))

This is the strongest rival to replay: defer understanding until needed, buy it back on demand. It works for code you don't own. It does nothing for design decisions you are about to commit to.

---

## 4. Workarounds people actually use

Ranked by how often they appear in the sample, not by merit.

1. **Small steps, review each.** "let it write the code, but only in small portion. Not 'implement this feature'. But 'open this file and make these changes'." @yanis_t ([HN 49154622](https://news.ycombinator.com/item?id=49154622)). "Small commits, every commit tested and verified ... I create mental model of the code same way, as when writing it manually." @mdavid626 ([HN 47396215](https://news.ycombinator.com/item?id=47396215)). [observed]
2. **Human writes the skeleton, agent fills holes.** "I write the stub classes and interfaces and mock the relations between them by hand, and then ask the agent to fill in the logic. ... the best architecture is the one that I'm comfortable with, so it's worse even if it's better." @drowntoge ([HN 46768000](https://news.ycombinator.com/item?id=46768000)) [observed]
3. **Interrogate: ask why.** "what I tend to do after receiving generated code is a lot of asking 'why?'." @Greenpants ([HN 49154295](https://news.ycombinator.com/item?id=49154295)); "I make my agent explain every single change" @Sapanoid ([YouTube](https://youtu.be/1Se2zTlXDwY)) [observed]
4. **Socratic quiz.** "I try to counteract this 'comprehension-debt' by having the code-agent quiz me, Socratic-style ... When I don't answer correctly, the agent drills down" @d4rkp4ttern ([HN 48329287](https://news.ycombinator.com/item?id=48329287)); tool author, ships a skill. Also @sfink had Claude quiz them on Rust ownership ([HN 46881649](https://news.ycombinator.com/item?id=46881649)). [observed]
5. **Read in own editor, stage hunks.** "I want to read its changes in my text editor, decide what to drop or revise or revert, and then stage individual hunks or regions into logical commits." @isityettime ([HN 47993175](https://news.ycombinator.com/item?id=47993175)) [observed]
6. **Split the megacommit.** A `/split-commit` Claude Code plugin ([HN 45806956](https://news.ycombinator.com/item?id=45806956)); Diffity's "tour" walks a local change ([HN 49154751](https://news.ycombinator.com/item?id=49154751)); a neovim review plugin that marks code as seen, commit by commit ([HN 48537277](https://news.ycombinator.com/item?id=48537277)). [observed, tool authors]
7. **Built-in learning modes.** Claude Code's Learning style: "When it reaches a piece with a real design decision ... it leaves a few lines for you" marked `TODO(human)`; Explanatory adds `Insight` blocks ([docs](https://code.claude.com/docs/en/output-styles)). Cat Hicks's `learning-opportunities` skill offers "optional 10-15 minute" exercises after architectural work, with a soft cap of 2 per session and suppression after one decline ([repo](https://github.com/DrCatHicks/learning-opportunities)). "Learning Mode – Claude refuses to write code" ([Show HN 49089416](https://news.ycombinator.com/item?id=49089416)). [observed: these exist; adoption not measured]
8. **AI-free blocks / étude projects.** "I've started a project where I intentionally don't use agentic coding ... The goal is to maintain the taste" @K0nserv ([HN 49153939](https://news.ycombinator.com/item?id=49153939)); "setting aside blocks of time where I use no llms" @aselimov3 ([HN 48193706](https://news.ycombinator.com/item?id=48193706)). [observed]
9. **Red tests from the agent, human implements.** @alex7o ([HN 49159893](https://news.ycombinator.com/item?id=49159893)) [assumed, proposal]

Learning modes 7 interrupt the build; replay runs after it. Workarounds 1, 2 and 5 slow the build to human speed. Replay is the only one in the sample that lets the build run unattended and still puts the human's hands on every decision afterward.

---

## 5. How a session fails

### Tedium and fatigue

- [observed] "Poring over hundreds of lines ... is not fun." (Sethi, above)
- [assumed] "As others mentioned retyping is not fun." @yanis_t; "This does not sound fun." @f311a ([HN 49153987](https://news.ycombinator.com/item?id=49153987))
- [observed] "It's mechanical and boring, my mind tunes out and I get nothing out of it." @dns_snek, on copying lecture notes ([HN 49155423](https://news.ycombinator.com/item?id=49155423))
- [observed] "I was so focused on copying verbatim ... that I didn't have a chance to think about the content." @quietbritishjim ([HN 49168062](https://news.ycombinator.com/item?id=49168062))
- [observed] "A proper line by line review tops out at 400-500 lines per hour and the reviewer should be spent and take a 30 minute break." @baq ([HN 45430478](https://news.ycombinator.com/item?id=45430478)). Matches the SmartBear/Cisco guidance below.
- [observed] "Mental exhaustion when working on multiple different projects/agent sessions is real ... the more I give in into vibing the harder it is to review and understand." @crsl ([HN 47392043](https://news.ycombinator.com/item?id=47392043))
- [observed] "My brains gets full before I get to the end." (reviewer script, @MikeNotThePope)

### Autopilot: hands move, head doesn't

- [observed] @jolt42 on C64 listings: "If you just touch type them in you learn very little."
- [assumed] "Blindly typing will make you just good at typing." @m4xp ([HN 49154104](https://news.ycombinator.com/item?id=49154104))
- [observed] "all writing reinforces is syntax" when coding along YouTube tutorials @Thanemate ([HN 49154392](https://news.ycombinator.com/item?id=49154392)); counter from @jdiff: weak for novices, "a good reinforcement tool" when you already know the field ([HN 49155078](https://news.ycombinator.com/item?id=49155078)).
- [observed] "I was under the impression that yes, retyping helps ... but I found myself forgetting it after a while" @trklausss ([HN 49154718](https://news.ycombinator.com/item?id=49154718))

### No alternatives, no "why"

- [assumed] "Even if there is an explanation of why the code is written in such a way, you did not come up with it, and you don't know alternative solutions." @f311a. This is the sharpest critique of replay as a learning tool. The guide's "Key decisions: chose X over Y" and retrospective questions are the direct answer, if they are good.
- [observed] "it'll tell you exactly how to do something, but it won't give you the 'why'." @ToadAppreciator ([YouTube](https://youtu.be/1Se2zTlXDwY))

### Can't tell what matters from boilerplate

- [assumed] "there are parts (boring, as the author calls them) that are not worth 'knowing' ... but the sections I need to know how they work, I think it might make sense to write those by hand!" @_benj ([HN 49154324](https://news.ycombinator.com/item?id=49154324))
- [assumed] "If you want to offload tedious boilerplate part to LLM, then by definition no need to learn it as it is tedious, so typing it out is useless." @elAhmo ([HN 49156313](https://news.ycombinator.com/item?id=49156313))
- [observed] Kamens's end state is exactly this cut: "Hard Way for critical moments."

### Losing the thread / disorientation

- [observed] "I would love an agentic tool that simply finds code locations and opens them in my editor, so that I can write the implementation. I find this to be the most tedious and disorienting part" @ivan888 ([HN 49158733](https://news.ycombinator.com/item?id=49158733)). This is what the Tab-to-place extension solves.
- [observed] "you start because your boss told you to implement a new feature ... and now all you can remember is that you're fixing the circular dependency." @brabel ([HN 49167189](https://news.ycombinator.com/item?id=49167189))
- [observed] Readable-in-isolation is not the same as coherent: "Agents write units of changes that look good in isolation." (Bitar). A replay that plays blocks in order can reproduce this if phases aren't framed by the whole.

### Slop that hides in plain sight

- [observed] "I read it, I don't get it, I read it again, am I just stupid? ... it doesn't click, because it's a slop. ... It requires more time to look at it than to actually write it." @originalcopy ([HN 46772793](https://news.ycombinator.com/item?id=46772793))

---

## 6. Research findings

**Anthropic, "How AI Impacts Skill Formation" (Shen and Tamkin), Jan 2026.** RCT, n=52 mostly junior engineers learning the Trio async library. ([post](https://www.anthropic.com/research/AI-assistance-coding-skills), [arXiv 2601.20245](https://arxiv.org/abs/2601.20245))
- AI group quiz 50% vs hand-coding 67%, Cohen's d = 0.738, p = 0.01. Speed gain about two minutes, not significant.
- Largest gap on debugging questions, smallest on code reading.
- Six interaction patterns. Low scorers (under 40%): AI Delegation, Progressive AI Reliance, Iterative AI Debugging (n=4 each). High scorers (65%+): Generation-Then-Comprehension (n=2), Hybrid Code-Explanation (n=3), Conceptual Inquiry (n=7). Authors say this "does not draw a causal link." Cell sizes are tiny.
- **Typing vs pasting, directly relevant.** Pasters (n=9) were fastest; manual copiers (n=9) and hybrid (n=4) took about as long as no-AI. "there was no notable difference between groups that typed vs directly pasted AI output." "spending more time manually typing may not yield better conceptual understanding."
- "the control group with no access to AI assistance encountered more errors during the task." "Encountering more errors and independently resolving errors likely improved the formation of Trio skills."
- "Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery."

Read for replay: transcription alone bought nothing measurable. The high-scoring pattern that most resembles replay, Generation-Then-Comprehension, is distinguished by the follow-up questions, not the copying. The paper even notes it "looks nearly the same as the AI delegation group."

**Prather et al., "The Widening Gap", ICER 2024.** 21 novices, eye tracking. Students who accelerated used GenAI to produce code they already intended to write; strugglers had their metacognitive difficulties compounded, and several "finished with an illusion of competence." ([arXiv 2405.17739](https://arxiv.org/abs/2405.17739))

**Kazemitabaar et al., CHI 2023.** Novices with Codex did slightly better on one-week retention, not significant; learners with higher prior knowledge did significantly better with Codex access. ([arXiv 2302.07427](https://arxiv.org/abs/2302.07427)). Prior knowledge moderates whether AI-produced code helps or hurts.

**METR, July 2025.** RCT, 16 experienced OSS devs, 246 tasks in their own repos. AI-allowed tasks took 19% longer; devs had forecast a 24% speedup. ([METR](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)). The perceived-vs-measured gap matters: people can't feel their own debt accumulate.

**Kosmyna et al., "Your Brain on ChatGPT", June 2025 preprint.** Essay writing, n=54. LLM group had weakest EEG connectivity, low reported ownership, and trouble quoting essays written minutes before. Not peer reviewed; essays, not code. ([MIT Media Lab](https://www.media.mit.edu/publications/your-brain-on-chatgpt/))

**Generation effect.** Bertsch et al. 2007 meta-analysis: generating beats reading by about d = 0.40 across 86 studies. ([PubMed 17645161](https://pubmed.ncbi.nlm.nih.gov/17645161/)). Typing someone else's code is not generation; answering a prediction question before the block appears is.

**ICAP (Chi and Wylie 2014).** Copying is "active"; generating and self-explaining are "constructive"; constructive predicted to beat active. Evidence mixed; one lab study (n=161) contradicted the ordering. ([paper](https://chilab.asu.edu/sites/default/files/lcl/chiwylie2014icap_2.pdf))

**Worked examples, fading, expertise reversal.** Novices learn more from worked examples than solving; as knowledge grows, the advantage reverses (Kalyuga et al. 2003). Fading (Renkl and Atkinson) gradually removes steps from examples; adaptive fading beat fixed fading in Salden et al. 2010. ([Wikipedia summary](https://en.wikipedia.org/wiki/Expertise_reversal_effect), [Atkinson/Renkl PDF](https://faculty.engineering.asu.edu/mre/wp-content/uploads/sites/31/2020/02/Exp_Rev_LI06.pdf)). A replay guide is a worked example. For an expert in their own repo, a full worked example is the wrong dose.

**Parsons problems (Ericson).** Reassembling scrambled code blocks: faster than writing code, equivalent learning gains in her studies and the 2023 ITiCSE working group. ([ITiCSE 2023 report](https://falmouth-test.eprints-hosting.org/5216/1/ITiCSE_2023_WorkingGroup_Parsons_Report.pdf)). Evidence that ordering decisions carry learning without full typing.

**Code review capacity (SmartBear/Cisco, 2006).** 2,500 reviews, 3.2M LOC. Guidance from it: 200-400 LOC per review, under about 500 LOC/hour, under 60-90 minutes before detection drops. Figures vary between secondary sources; the original chapter wasn't retrieved. ([SmartBear](https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/))

**Bacchelli and Bird, ICSE 2013.** At Microsoft, code and change understanding is the key aspect of review, and developers' understanding needs are mostly not met by tools. ([MSR](https://microsoft.com/en-us/research/?p=164195))

**Typing vs copy-paste in programming education.** No controlled study found. Khan Academy looked in 2013 and found none; the closest evidence is note-taking research, with mixed results. Treat "type it, don't paste it" as practitioner lore.

---

## Suggestions

My read, separate from the evidence above.

### Primary persona: the accountable builder

An experienced engineer who runs agents for real work in a codebase they will have to maintain and answer for, and who has already felt the debt: a review they couldn't do, a bug they couldn't explain, code that wasn't theirs. Goal is owning the decisions, not learning syntax. They already know the language; they don't know this feature's design.

Evidence: Sethi, Kamens (phase 2), @kbrannigan, @drowntoge, @r0ze-at-hn, @Kim_Bruning, @mdavid626, the README's own author. Behaviour marker: they have already built a home-made version of this (typing from chat, stubs first, hunk staging, interrogation).

Their main risk is Kamens's trajectory. They start full-fidelity, then retreat to "critical moments", then stop. Replay has to be cheap enough on non-critical code that they don't quit, and sharp enough on critical code that they feel the payoff.

### Secondaries

1. **The reviewer downstream.** Has to approve someone else's agent PR (@rDr4g0n, @MikeNotThePope, @ericmcer). Wants the decisions, not the transcript. Uses the guide's Key Decisions and invariants, maybe never Tabs.
2. **The deliberate learner in a new stack.** Uses agents to pick up a library or language (@danielvaughn on Treesitter, @twoquestions on Electron). Benefits most from full worked examples (expertise reversal says novices gain most). Needs more explanation per step than the primary.

### Anti-personas

- **The delegator by choice** (@p1esk, @dools, @big_paps): doesn't read code, gets rewarded for it. Nothing here will land.
- **The novice using replay as a substitute for struggle.** The Anthropic control group learned from hitting and fixing errors. Replay's code always compiles, so the struggle is gone. Prather's "illusion of competence" is the predicted outcome. Fine to use, not the design target.
- **The throwaway-code builder.** One-off scripts, prototypes. Debt never comes due.

### Implications for the skills

**Replay guide**
1. **Typing is not the mechanism; questions are.** The Anthropic typed-vs-pasted null result and the HN consensus agree. The retrospective gate is the load-bearing feature; Tab is the delivery. Protect question quality over block granularity.
2. **Ask before the block plays, not only after.** Generation effect and the Hicks "Generation → Comparison" exercise: "how would you do this?" before the reveal is constructive; after is recall. Worth trying a prediction prompt on decision steps.
3. **Mark critical vs mechanical, visibly.** People who quit retyping kept doing it for critical code. Rule 5 ("one question per decision") already does this implicitly; surface it so the human can Tab-through mechanical runs fast and slow down where it counts. That keeps the primary persona from the Kamens decay.
4. **Show the rejected alternative.** @f311a's critique ("you don't know alternative solutions") is answered only if Key Decisions name what was rejected and why. Make that mandatory for decision steps.
5. **Size phases to review capacity.** SmartBear guidance and @baq both point to roughly an hour or a few hundred lines before attention drops. The time estimate in the overview should drive a suggested break, and a phase that exceeds it should split.
6. **Frame each phase by the whole.** Bitar's "look good in isolation" complaint applies to block-by-block replay too. Each phase opener should say where it sits in the dependency graph and what invariant it serves.
7. **Divergence is the win condition.** Kamens and @tdeck both edited most lines while retyping. Hacking the block is evidence of ownership. The guide should invite it, and the checkpoint's divergence notes should be treated as the session's main output.

**Podcast**
- It fits the "conceptual inquiry" pattern, which scored highest in the Anthropic study. Keep it pre-replay, model-building only.
- Risk: passive listening is the lowest ICAP mode. The "When you type it" hooks are the bridge; make them questions the listener should be able to answer by the end of the replay.

**Diagram**
- Martinez's "compressed review surface" (boundaries, data flows, state transitions, failure modes) lines up with the diagram gate. The disorientation complaint (@ivan888) argues for one diagram per phase showing where the current block sits, rather than one big picture up front.

**Clips**
- The Anthropic study's biggest gap was debugging, and the control group learned from errors the AI group never hit. Replay removes all errors. Bug-story clips are the one place the human sees the failure the agent hit and fixed. That makes them more valuable than invariant traces for skill formation; consider ranking bug stories first when both qualify.
- Keep "zero clips is normal". Fatigue evidence says extra media competes for the same limited attention, arr.

### Open questions the evidence can't answer

- Does replay produce measurable comprehension over reading the same diff with the same questions? No study touches it. Cheapest test: the Anthropic quiz design, replay vs diff-read-with-questions.
- How long before the primary persona's replay habit decays, and what keeps it? Kamens decayed in about nine months. One person.
- Reddit missing. Re-run when Arctic Shift is back, focusing r/ExperiencedDevs for reviewers and r/learnprogramming for the novice anti-persona.

---

## Provenance

**Hacker News threads dumped in full (Algolia items API):**
- 49153374 Prevent cognitive debt by manually retyping LLM-generated code (545 pts, 431 comments dumped)
- 46765460 After two years of vibecoding, I'm back to writing by hand (865 pts, 629 dumped)
- 46820924 How AI assistance impacts the formation of coding skills (482 pts, 342 dumped)
- 45423917 Comprehension debt: A ticking time bomb of LLM-generated code (532 pts, 335 dumped)
- 45744209 Ask HN: How to deal with long vibe-coded PRs? (186 pts)
- 47388646 Ask HN: How is AI-assisted coding going for you professionally? (434 pts)
- 48554309 AskHN: How do you handle skill atrophy from using coding agents? (34 pts)
- 48193503 Type Out the Code (20 pts, 1 comment)
- Plus individual comments from Algolia comment search, each linked inline.

**YouTube (signal-feed wrapper, serial, no 429s):**
- Searches: "comprehension debt AI generated code", "I don't understand my own code anymore AI vibe coding", "retype AI generated code by hand to understand it"
- Comments: 3o2SlgX9BhE (The Serious CTO, low signal), 1Se2zTlXDwY (The PrimeTime, mostly novices), DC1_MLzTpuY (Awesome, low signal)
- Transcript: 6qkzlT962es (Gabriel Martinez, G2i, AI Engineer; incentive: ORC product)

**Web (WebFetch extraction):** anthropic.com/research/AI-assistance-coding-skills; arxiv.org/html/2601.20245; arxiv.org/abs/2405.17739; oreilly.com comprehension debt (Osmani); ankursethi.com; kamens.com (3 posts); haskellforall.com; atmoio.substack.com; cs-blog.khanacademy.org; johndcook.com; code.claude.com/docs/en/output-styles; github.com/DrCatHicks/learning-opportunities.

**Web (search snippets only, primary not opened):** METR 2025, Kosmyna 2025, Kazemitabaar 2023, Bertsch 2007, Chi and Wylie 2014, Kalyuga/Renkl/Atkinson, Ericson Parsons, SmartBear/Cisco, Bacchelli and Bird, Storey 2026.

**Not covered:** Reddit (Arctic Shift 522 at start and end). Zed Shaw primary text not opened.

**Incentive tells:** Kamens (consulting link), Martinez (ORC), @d4rkp4ttern (ships a quiz skill), @exclipy (ships split-commit plugin), @chrbr (Diffity link), @pomarie (cubic.dev, self-declared), @jbellis (Brokk, self-declared), Hicks (open repo, no sale seen).
