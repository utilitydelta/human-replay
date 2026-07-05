# Human Replay

*(This readme is written by me with no LLM assistance)*

## Install

Inside of Claude Code run:

```
/plugin marketplace add utilitydelta/human-replay
/plugin install human-replay@human-replay
```

## TLDR

1. Claude uses `/prep` skill to copy your code to `~/sandbox/[folder]`
2. Run with your agent in there to bang out your feature (still use empirical loops & falsification sensors to assert correctness)
3. When the agent is done, use `/generate-replay-guide` to create a md doc to summarise what the agent did, capturing code changes, key system invariants and generating retrospective questions
4. use the [`human-replay-vscode-extension`](https://marketplace.visualstudio.com/items?itemName=UtilityDelta.human-replay) to *replay* what the agent did, block by block, back into your actual codebase. Just hit `Tab` and it plays out in front of you.

You read and implement the code, one block at a time. Hack it as you go or send it back to the sandbox agent if its wrong. Human stays in the loop.

## Backstory

Hi, I'm Tyson. I have a background in hardcore engineering and systems-level software, like CAD engines, IoT, databases and medical devices (I built an MRI!). The kind of shit that if it fails, somebody dies. 

I use LLMs a lot these days to work faster. There is pressure from clients to ship. So there is tension. Vibe-out too much locally coherent / globally incoherent-slopish code and you've got a broken mess that nobody can deal with. Code by hand and you get fired.

Current industry trend is put the design in PRDs and ADRs and that's enough. Let the agent write the code. But the code *IS* the design. What really happens when we write code is we make thousands of decisions that are *design shaped*. PRDs are only a guide. Don't let agents write the code; Don't let them *design* your software.

We *can* ship really good quality software with LLMs. Just got to do it the right way. That's what human replay is about.

## Adjacent work

- [human-replay-vscode-extension](https://marketplace.visualstudio.com/items?itemName=UtilityDelta.human-replay) - make human replay fun, just hit `tab` and the magic happens.
- [build-method](https://github.com/utilitydelta/build-method) - the full agentic system as a set of claude `SKILL.md` files that I use with human-replay.
- [debate-battle](https://github.com/utilitydelta/debate-battle) - the multi-agent debate engine the scout runs goals through.
- [react-mobx-mvvm](https://github.com/utilitydelta/react-mobx-mvvm) - my opinionated take at how to build front end with agents using MVVM.