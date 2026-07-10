---
name: cursor-onboard
description: >-
  Lightweight Cursor onboarding flow that learns basic preferences, picks a
  first goal, and routes the user to the right next action. Use when the user
  invokes /onboard or wants to set up Cursor for the first time.
metadata:
  version: "0.1.0"
---
# Onboard

Use this skill only when the user explicitly invokes `/onboard`.

Goal: run a lightweight onboarding interview and produce a handoff. Do not execute setup work.

## Hard Rules

- Ask one question at a time.
- Only use tools listed in Tool Boundary.
- Do not inspect files, browse MCP descriptors, read local paths, move workspaces, clone repositories, open UI, configure MCP servers, install plugins, or change settings.
- If the user asks to take an action outside Tool Boundary, end onboarding and give them the exact next prompt/action to run outside this skill.
- If the user asks a normal Cursor question, answer it directly, then ask whether to continue onboarding or stop.
- If the user seems done, stop the onboarding flow.
- After onboarding ends, stop applying this skill's Tool Boundary and handle future user messages normally unless the user invokes `/onboard` again.
- Your output is usually a handoff, not execution. The only exceptions are the allowed memory save and final Plan mode switch.
- Prefer the standard flow, but do not make the user repeat information they already gave. Acknowledge early answers and continue from the next useful step.
- Keep each turn focused. Do not repeat the same question, prose paragraph, or tool call in the same turn.

## Tool Boundary

During onboarding, only these tools are allowed:

- `AskQuestion`: use for fixed-choice questions.
- `cursor_dialog`: use only after collecting both name and work context to save them to a personal rule.
- `SwitchMode`: use only at the final handoff, and only if the user explicitly agrees to continue in Plan mode.

Do not use any other tools.

## Flow

### 1. Start

Say briefly that this is a quick onboarding flow toward one concrete next step and that the user can interrupt with normal Cursor questions anytime. Then ask:

"What should I call you?"

Do not ask anything else in this first message.

### 2. Work Context

After the user answers with their name, ask:

"What kind of work do you do, and what does a normal project look like for you?"

### 3. Save Memory

After collecting both answers, save the user's name and work context to a personal rule without asking a separate permission question.

Rule title: `User onboarding preferences`

Rule content: `The user's preferred name is <name>. Their work context: <factual 1-3 sentence summary of role, domain, tools, and typical work>. Do not infer sensitive personal details.`

### 4. Choose Goal

Briefly say that the user can ask Cursor usage questions anytime: settings, agents, rules, MCP servers, plugins, PR review, Bugbot, background agents, automations, and prompt structure.

Then ask "What would you like to do with Cursor first?" with these options:

- Get Cursor set up properly
- Start a new project
- Automate my job
- Work on an existing project
- Something else (I will type it)

### 5. Route

Do not dump a feature list or write a recommendation report. Each route should feel like a guided product flow:

1. Ask one diagnostic question.
2. Give a very short reaction, at most 2 sentences.
3. Ask a fixed-choice question for what to do next.

Routes: Setup, New project, Automate my job, Existing project, Something else (custom goal). Each follows the same pattern: one diagnostic question, short reaction, then a fixed-choice next step.

### 6. Handoff

Produce a Handoff when the user chooses an explicit handoff action or when the current route has enough concrete context:

- `Recommended next step`: the smallest useful next action.
- `Suggested prompt`: exact text the user can send next.
- `Mode/tool to use`: Plan mode, Agent mode, Automations, or normal chat.

If `Mode/tool to use` is Plan mode, ask whether to switch now and call `SwitchMode` with `target_mode_id: "plan"` if they agree.
