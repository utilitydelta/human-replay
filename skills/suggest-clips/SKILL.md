---
name: suggest-clips
description: Offer the human a short menu of explainer clips for the parts of a build-out that Tab-by-Tab replay cannot teach, then generate the ones they pick. Runs last, after the replay guide is written.
---

# Suggest Clips

Most of a replay is Tab, Tab, Tab through changes that need no picture. A few
parts are not like that: an invariant that only makes sense as an interleaving
of two timelines, or a bug the agent found empirically whose whole story is
missing from the diff. Typing those in line by line teaches nothing, because
the thing to understand was never on any one line.

This skill finds those parts, asks the human which ones they want, and hands the
selections to `generate-clip`.

Run it as the last step of the session, after `generate-replay-guide`. It is the
one place in Human Replay that blocks on a question, and that is fine here: the
build is done, nothing is waiting.

The only exception is if this is an unattended autonomous session (eg. human is asleep as it's 3am) 
then just write the suggestions to a suggested-clips.md file in the session instead of waiting for human input.
If you prompt, that's a synchronous blocker which might prevent shutdown or further autonomous work.

## Do not generate by default

Rendering is cheap. Authoring is not, and neither is the human's attention. The
default answer for any given invariant is no clip. Recommend two or three at
most, offer a couple more unrecommended, and be relaxed about a guide that earns
zero. Zero is a normal outcome for a CRUD feature and it is not a failure of
this skill.

## Two kinds of clip

### 1. Invariant trace

Anchors on one entry in the guide's `System Invariants` section. The invariant
says something must never happen. The clip shows the execution where it does.

The test for whether an invariant earns one: **can you write an execution trace
that violates it?** Two or more timelines, an interleaving, an outcome that
should be impossible. Write the trace out in six lines before you propose the
clip. If you cannot, the invariant is a definition or a policy, and prose in the
guide already beats any picture.

Worked examples, from real guides:

| Invariant | Earns a clip? | Why |
|---|---|---|
| A desynchronised connection must never return to the free list | Yes | Timeout drops the future with the request on the wire; the response lands afterwards and the next user reads it as its own reply. Self-sustaining. |
| Asymmetric fencing | Yes | Leader self-fences at `expiry - max_clock_drift`, follower challenges at `expiry`. Two timelines and a gap that must not close. |
| Lease liveness reaches data shards only by StatusUpdate | Yes | One dropped broadcast fences a shard for a computable window. |
| Absence is not zero | No | Counters register lazily. One sentence, no trace. |
| Zero max client seq is the never-wrote sentinel | No | A definition. |
| S3 lease TTL is the fencing guarantee | No | A policy with a stated price. Prose carries it. |

### 2. Bug story

Anchors on a defect the agent found and fixed during the build. The guide teaches
the fix. It does not teach the hunt, and the hunt is where the sense of the
system lives. The human should come out of this able to tell the story at
standup without replaying the clip.

Five beats, and every one of them needs a real answer or the clip is not offered:

1. **How it surfaced.** Which sensor caught it. A chaos run, a contract test, a
   metric that should have been zero. Name the run.
2. **The reproduction.** What conditions were needed. Failover under load, a
   timeout on a pooled connection, a dropped broadcast. This is the same
   execution trace an invariant clip animates.
3. **Risk.** Consequence and likelihood, separately, with the numbers the loop
   produced. "A duplicate business event, durable on both nodes" is the
   consequence. "0.11 to 0.43% of aggregates under failover load" is the
   likelihood. A bug with a scary consequence and a one-in-a-billion trigger is
   a different animal to one with both, and the human needs to see which.
4. **The corrective action, and its weight.** A one-line guard is one story. A
   new system invariant that every future change is now bound by is a much
   bigger one, and the difference is the single best signal of how deep the
   agent actually went. Say which it was, plainly.
5. **What is still open.** Accepted residual risk, a narrower overlap left
   documented rather than closed. If the answer is nothing, say nothing.

## Where the evidence comes from

`generate-replay-guide` refuses the session trail on purpose: the trail is
gradient descent and a guide built from it teaches the wandering. This skill
reads it anyway, because the wandering is the subject.

That reopens the reason for the ban, so one filter holds it in check:

**A wrong turn qualifies only if a falsification sensor caught it and left a
number behind.** 99.2% error rate over 12,000 reads. Backstop scans 16,000 to 0.
Duplicates at 0.11 to 0.43% of aggregates under failover load. Those are moments
where the loop learned something and the evidence survives.

A design the agent abandoned on a hunch has no trace to animate, no number to
show, and no claim on the human's attention. Drop it. If you find yourself
narrating what the agent was thinking, you have left the evidence behind.

Inputs, in order of value: the failing run output, chaos and contract test
results, the metrics the session asserted on, `session/session-state.md` and
`session/progress.md` for pointers to those runs, and the guide's own
`System Invariants` and `Key decisions`.

## Workflow

1. Read the finished `session/replay-guide.md`. The invariants list is your
   candidate set for kind 1.
2. Sweep the trail for defects that passed the sensor filter. Those are your
   candidates for kind 2.
3. For each candidate, write the execution trace, or the five bug-story beats,
   as plain text. This is the work. A candidate you cannot write out is a
   candidate you cannot animate, and finding that out here costs nothing.
4. Rank. Recommend the ones where the trace is genuinely hard to hold in your
   head from the guide alone. Deprioritise anything a sequence diagram in the
   guide would have covered.
5. Ask the human. Use `AskUserQuestion`, multiSelect, one option per candidate,
   recommended ones first and labelled. Include a "none of these" option and
   mean it.
6. For each selection, invoke `generate-clip` with the trace or the beats you
   already wrote. Do not re-derive them.

## The question

Keep it to one question, four options at most, and put the recommendation in the
label rather than making the human infer it. Each option's description is the
one-line reason this clip exists, not a summary of the invariant.

```
Which of these are worth a clip? Everything else replays fine as Tab steps.

[ ] Pooled connection desync (Recommended)
    A timeout leaves the response in flight; the next reader takes it as
    its own. Self-sustaining, drove a 99.2% error rate.
[ ] Duplicate write at failover (Recommended)
    Dedup state has three writers and one populates it. The hole is the
    handover, which is when clients retry most.
[ ] Asymmetric fencing gap
    Leader and follower fence on opposite sides of clock drift.
[ ] None, the guide covers it
```

If the human picks none, say so plainly and stop. That is a good outcome and the
guide is not worse for it.

## Output

Selections go to `session/clips/` as one `<slug>.md` per clip, holding the trace
or the five beats, the invariant or defect it anchors to, and the run the
numbers came from. `generate-clip` reads these and nothing else, so anything the
clip needs to be true has to be written down here first.
