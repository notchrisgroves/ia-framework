---
name: newsletter
description: Automated weekly digest generation and scheduling for Ghost CMS newsletter
---

# /newsletter - Weekly Digest Automation

Automatically generate and schedule weekly newsletter digest from published posts.

**Agent:** writer
**Skill:** writer
**Output:** `output/blog/drafts/weekly-digest-YYYY-MM-DD-DD/`

---

## Quick Start

```bash
/newsletter
```

Detects week → Fetches posts → Generates digest → Schedules Monday 8:00 AM

---

## Usage

Just tell the AI what you need:

```
/newsletter
/newsletter generate the weekly digest for last week
/newsletter preview the digest but don't schedule it yet
/newsletter send it immediately instead of scheduling for Monday
```

The workflow will ask clarifying questions if needed.

---

## When to Use

✅ **Use /newsletter when:**
- Weekly digest automation needed
- Curated email for subscribers
- Consolidate week's posts into single email
- Drive traffic to site (not inbox spam)

❌ **Don't use if:** Creating individual post → use `/blog-post`

---

## Workflow

1. **Week Detection**
   - Calculate Monday-Sunday range
   - Generate slug: `weekly-digest-YYYY-MM-DD-DD`

2. **Post Collection**
   - Search `output/blog/published/YYYYMMDD-*`
   - Filter posts in date range

3. **Digest Assembly**
   - Featured article (first post)
   - Additional articles with tier notation (*, **)
   - Tier notation:
     - No asterisk = Public (free)
     - * = Free members
     - ** = Paid members

4. **Ghost Scheduling**
   - Create EMAIL ONLY post
   - Schedule for following Monday 8:00 AM EST
   - Returns Ghost editor URL

**Why EMAIL ONLY?** One curated weekly email prevents inbox fatigue, drives site traffic, maintains clean blog feed.

---

## Agent Routing

```typescript
Task({
  subagent_type: "writer",
  model: "sonnet",
  prompt: `
Mode: newsletter
Skill: writer
Workflow: weekly-digest

Context:
- Week: {week-start-YYYY-MM-DD to week-end-YYYY-MM-DD}
- Options: {dry-run|send-now|default}

Instructions:
Execute writer SKILL.md newsletter workflow:
1. Detect/calculate week range
2. Fetch published posts in range
3. Generate digest (featured + additional)
4. Schedule Ghost EMAIL ONLY post (Monday 8:00 AM)

Output: output/blog/drafts/weekly-digest-YYYY-MM-DD-DD/
`
})
```

**Agent loads:**
1. `agents/writer.md` (via PreToolUse hook)
2. `skills/writer/SKILL.md` (via load-agent-skill-context hook)
3. Tools: workflow-stages.ts, ghost-admin.ts

---

## Output Structure

```
output/blog/drafts/weekly-digest-YYYY-MM-DD-DD/
├── draft.md
├── metadata.json
└── schedule-info.txt
```

**Digest Format:**
```markdown
---
title: "Weekly Digest: [Month DD-DD, YYYY]"
tags: ["Newsletter", "Weekly Digest"]
excerpt: "This week's Intelligence Adjacent content..."
visibility: "members"
send_email_when_published: true
---

## This Week on Intelligence Adjacent

[Featured article summary and link]

**Additional This Week:**
- [Post 1] *
- [Post 2] **
- [Post 3]

*Free members | **Paid members

[Footer with social links]
```

---

## Error Handling

**No posts found:**
```
⚠️ No posts published during [week range]
→ Suggestion: Run /newsletter later in the week or use --week for past weeks
```

**Ghost API failure:**
```
❌ Ghost API connection failed
→ Retrying in 5s...
→ If retry fails, check Ghost Admin → Settings → Integrations for API key
```

**Invalid post format:**
```
⚠️ Skipping post [slug] - Invalid frontmatter format
→ Continuing with remaining posts...
```

---

## Examples

### Current Week

```
/newsletter

✅ Weekly Digest Scheduled!
   Week: Nov 17-23, 2025 | Posts: 4 (1 public, 3 members)
   Schedule: Monday Dec 2, 8:00 AM EST
   Editor: https://yourblog.ghost.io/ghost/#/editor/post/[ID]
```

### Preview Before Scheduling

```
/newsletter just preview it first

🔍 Preview: 4 posts found for Nov 17-23
   Featured: Intelligence Adjacent Framework (public)
   Additional: 3 member posts
   Would save to: output/blog/drafts/weekly-digest-2025-11-17-23/
```

---

## Troubleshooting

**No posts found:**
- Check directory naming: `YYYYMMDD-slug`, not `YYYY-MM-DD-slug`
- Verify posts in `output/blog/published/`

**Ghost API 401:**
- Regenerate API key: Ghost Admin → Settings → Integrations

**Excerpt too long:**
- Edit frontmatter: excerpt should be 150-180 chars max

**Invalid slug format:**
- Use: `weekly-digest-YYYY-MM-DD-DD` (week start-end)

---

## Related Commands

- `/blog-post` - Create individual blog post
- Writer skill handles technical docs

---

**Version:** 1.0
**Last Updated:** 2025-12-12
**Framework:** Intelligence Adjacent (IA)
