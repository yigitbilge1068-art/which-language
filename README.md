# AI Coding Language Benchmark

Benchmark platform for comparing **AI coding systems** across three axes:

- **problem** — MiniGit, MiniGrades today, more tomorrow
- **codex** — Claude, Gemini, OpenAI, Groq, Aider, and future adapters
- **language** — Python, Ruby, Rust, Go, TypeScript, etc.

> Internals → [CLAUDE.md](./CLAUDE.md) · Contribute → [AGENT.md](./AGENT.md) · Current focus → [program.md](./program.md)

## Quick start

### Prerequisites

- Ruby
- Toolchains for languages you want to benchmark
- At least one enabled codex (Claude CLI, Gemini API key, or OpenAI API key)

### Configure a codex

Create `config/codexes.local.yml` (gitignored):

```yaml
codexes:
  gemini:
    enabled: true
    config:
      api_key: "${GOOGLE_API_KEY}"
```

```bash
export GOOGLE_API_KEY="your-key"
```

### Smoke test

```bash
bash scripts/run-all.sh gemini minigit --dry-run --lang python --trials 1
```

### Run a real benchmark

```bash
bash scripts/run-all.sh gemini minigit --lang python --trials 1
```

### Read the outputs

```text
artifacts/<codex>/<model>/<problem>/
  results/results.json    # raw benchmark records
  results/report.md       # generated markdown report
  figures/                # PNG graphs
  generated/              # generated code
```

### Platform setup

- **Windows**: `.\scripts\install_windows.ps1` (run as Administrator)
- **macOS**: `chmod +x scripts/install_mac.sh && bash scripts/install_mac.sh`

## The mental model

Think of the benchmark as a matrix:

| Dimension | Defined by | Example |
|----------|------------|---------|
| Problem | `problems/<problem>/problem.json` + assets | `minigit` |
| Codex | `lib/codexes/*.rb` + `config/codexes*.yml` | `claude`, `gemini`, `openai` |
| Language | `LANGUAGES` in `benchmark.rb` | `python`, `rust`, `ruby/steep` |

## Current support

### Codexes

| Codex | Status | Notes |
|------|--------|-------|
| Claude Code | ✅ | default CLI adapter |
| Gemini | ✅ | API adapter, Flash-Lite/Pro |
| OpenAI | ✅ | Responses API, cost accounting |
| Groq | ✅ | API adapter, robust parsing |
| Aider | 🚧 | CLI adapter, needs validation |

See [plan.md](./plan.md) for planned adapters (DeepSeek, Qwen, Grok, Cline, etc.)

### Languages

- Dynamic: `python`, `ruby`, `javascript`, `perl`, `lua`
- Static: `rust`, `go`, `c`, `typescript`, `java`
- Functional: `scheme`, `ocaml`, `haskell`
- Typed variants: `python/mypy`, `ruby/steep`

### Problems

- **minigit** — minimal version control system
- **minigrades** — student grade manager

## Recommended commands

```bash
# Full pipeline (benchmark + report + figures)
bash scripts/run-all.sh gemini minigit --lang python --trials 1

# Benchmark only
bash scripts/run-benchmark.sh gemini minigit --lang python --trials 1

# Raw runner
ruby benchmark.rb --codex gemini --problem minigit --lang python --trials 1
ruby benchmark.rb --help

# Compare codexes
bash scripts/run-all.sh claude minigit --lang python --trials 3
bash scripts/run-all.sh gemini minigit --lang python --trials 3
```

## Repository layout

```text
.
├── benchmark.rb          # runner
├── report.rb             # report generator
├── plot.py               # graph generator
├── problems/             # problem definitions
├── lib/codexes/          # codex adapters
├── config/codexes.yml    # codex config
├── scripts/              # helper scripts
├── program.md            # agent entry point
├── AGENT.md              # contributor protocol
├── plan.md               # living iteration plan
├── walkthrough.md        # proof-of-work log
├── CLAUDE.md             # technical internals
└── artifacts/            # benchmark outputs
```

## Contributing

See [AGENT.md](./AGENT.md) for the full contributor protocol. We welcome:

- **New codex adapters** (implement `BaseCodex` interface)
- **Benchmark results** (run existing codexes, submit data)
- **New problems** (add under `problems/`)
- **Language additions** (add to `LANGUAGES` hash)

## Historical context

This repository began with the published Claude Code / MiniGit experiment:

- [Which Programming Language Is Best for Claude Code?](https://dev.to/mame/which-programming-language-is-best-for-claude-code-508a)
- [Japanese version](https://zenn.dev/mametter/articles/3e8580ec034201)

## Contributors

- [mame](https://github.com/mame)
- [berkevnl](https://github.com/berkevnl)
- [Ahmetngz](https://github.com/Ahmetngz)

## Similar projects

- https://autocodebench.github.io
- https://livecodebench.github.io
- > **SPEC Update:** If the user enters a non-numeric value for the amount, the system must print "Error: Amount must be a valid number" to prevent a crash.
