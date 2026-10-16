# Test fixtures for humanize-check.mjs

<!-- humanize-check: catalog -->
# Each block is a known tell the scanner must catch, plus clean text it must not flag.

## SLOP: should trigger many tells

In today's fast-paced world, our cutting-edge platform stands as a testament to
innovation. It's not just a tool, it's a vibrant ecosystem that seamlessly
leverages robust technology to unlock your team's full potential.

Jane is a renowned expert who maintains an active social media presence. She is
passionate about leveraging data to foster meaningful change. Experts say her
method is widely used.

The library stands as a testament to the city's enduring commitment to learning,
playing a pivotal role in fostering a rich cultural heritage.

Despite its industrial prosperity, the town faces challenges typical of urban
areas. Additionally, future initiatives could further enhance its standing.

Not only fast but also reliable, the system is affordable, scalable, and
future-proof. We chose Postgres rather than MongoDB.

The station opened in 1890, contributing to the region's growth, highlighting
its importance to the area.

**Standard Saws.** Used for straight cuts.
**Specialty Saws.** Used for curves.

### This Heading Uses Title Case Throughout

In conclusion, this approach not only saves time but also improves quality,
ultimately representing a pivotal shift in how teams work.

Cleanup artifacts: oaicite turn0search0 contentReference ::: and a link with
utm_source=newsletter in it.

## CLEAN: should trigger nothing

The library opened in 1931. It holds 200,000 volumes and runs free adult-literacy
classes at weekends.

Our platform helps your team plan work, track it, and ship faster. It connects to
Slack, GitHub, and Linear, so updates sync without copy-paste.

Jane is a data scientist. Her 2024 talk on election models has 400,000 views.

The town's main employer, a textile mill, cut 300 jobs in 2023. The council has
not announced a replacement plan.

### A heading in sentence case

Teams that tried it cut review time by about a third. Two made it their default.

| Column | Meaning |
|---|---|
| `id` | Primary key |
| `status` | One of queued, ready, failed |

Table rows above must not be flagged. A `code_identifier` inside backticks is not
prose. Short sentences are fine. Really short ones too.
