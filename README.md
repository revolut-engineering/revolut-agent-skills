# Revolut Agent Skills

**Official AI agent skills for the Revolut ecosystem.**

This repository is a curated collection of instructions, context, and tooling definitions that teach AI agents (like Claude Code, Cursor, and GitHub Copilot) how to interact with Revolut services and products effectively.

> [!NOTE]
> **Technical preview**
>
> These skills are in early release. Expect frequent updates as we codify new API capabilities and refine agent behaviors.

---

## About

AI agents often struggle with specific API nuances. These skills follow the [Agent Skills](https://agentskills.io/home) open standard to provide agents with "native" knowledge of Revolut services, ensuring they use the correct endpoints, handle authentication safely, and follow Revolut best practices.

<!-- DEV: confirm whether agentskills.io open standard positioning is still accurate -->

## Available skills

<!-- DEV: version and author fields will be added after the skills audit -->

| Skill | Description | Version | Author |
| ----- | ----------- | ------- | ------ |
| [revolut-x-auth](skills/revolut-x/revolut-x-auth/) | API key setup, Ed25519 signing, environment configuration | — | — |
| [revolut-x-configuration](skills/revolut-x/revolut-x-configuration/) | Available currencies and trading pair constraints | — | — |
| [revolut-x-balance](skills/revolut-x/revolut-x-balance/) | Account balances (available, reserved, staked) | — | — |
| [revolut-x-orders](skills/revolut-x/revolut-x-orders/) | Place, cancel, and query orders (market, limit, conditional, TPSL) | — | — |
| [revolut-x-trades](skills/revolut-x/revolut-x-trades/) | Trade history, personal fills, order execution details | — | — |
| [revolut-x-market-data](skills/revolut-x/revolut-x-market-data/) | Order book depth, OHLCV candles, ticker prices | — | — |
| [revolut-x-public-market-data](skills/revolut-x/revolut-x-public-market-data/) | Public trades and order book (no auth required) | — | — |

---

## Installation

You can install Revolut Agent Skills automatically via the `skills` CLI or by copying the files manually.

### Option A: Using the skills CLI (Recommended)

The `skills` CLI handles downloading and placing the skills in the correct directories for your active AI agents.

#### 1. Project-level (Default)

Run this command inside your project's root directory:

```bash
npx skills add revolut/revolut-agent-skills
```

- **Best for:** Specific repositories where you want every contributor to have the same agent capabilities.

#### 2. Global (Personal use)

Give your AI agent "permanent" knowledge of Revolut services across your entire machine:

```bash
npx skills add revolut/revolut-agent-skills --global
```

- **Best for:** Using tools like Cursor or Claude Code to use Revolut services regardless of which folder you have open.

#### Update skills

To ensure your agent is using the latest logic and tool definitions:

```bash
# Check for updates
npx skills check

# Pull the latest versions
npx skills update
```

### Option B: Manual installation

If you prefer not to use the CLI, you can install the skills manually into your agent's skills directory.

1. **Clone this repository:**

    ```bash
    git clone https://github.com/revolut/revolut-agent-skills.git
    ```

    <!-- DEV: confirm public repo URL -->

1. **Copy the desired skill folders** from the `skills/` directory into your agent's local directory.

    <!-- DEV: confirm target directory conventions per agent host -->
    - For **Cursor** or **GitHub Copilot**: `.agents/skills/`
    - For **Windsurf**: `.windsurf/skills/`
    - For **Claude Code**: `.claude/skills/`

---

## Security & authentication

Revolut Agent Skills require valid API credentials to function.

<!-- DEV: confirm final env var names before publish -->
- **Environment variables:** Never hardcode keys. Use variables like `REVX_API_KEY` and `REVX_PRIVATE_KEY`.
- **Scope privileges:** We strongly recommend using **restricted API keys** with "read-only" permissions (when available) for initial testing.
- **Context awareness:** Security data can contain PII. When an agent queries balances or history, that content enters the model's context. Involve your compliance teams if using these in a corporate environment.

---

## Disclaimer

**This repository is an informational tool provided "as is".**

- **Not financial advice:** Revolut Agent Skills and their outputs do not constitute investment, financial, or trading advice.
- **Risk of loss:** You are solely responsible for all trading decisions. Digital asset prices are volatile; you may lose more than your initial investment.
- **Use Sandbox:** We strongly recommend testing all skills in the **Revolut Sandbox** environment before connecting them to live accounts.
- **Human in the loop:** Always require manual confirmation before allowing an agent to execute a "write" action (e.g., placing an order or sending a transfer).

---
