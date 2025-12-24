# Membership CTAs Template

**Correct tier names and portal URLs for Ghost membership**

> Copy this to `membership-ctas.md` and customize with your tier names, prices, and portal IDs.

---

## Ghost Membership Tiers

**Define your tiers:**
- **Free Tier Name** - Free ($0/month)
- **Mid Tier Name** - $X/month or $XX/year
- **Premium Tier Name** - $XX/month or $XXX/year

**DO NOT use:**
- Generic terms like "Member" (use your actual tier names)
- Incorrect prices
- Old/deprecated tier names

---

## Correct CTA Formats

### For FREE posts with Mid-Tier upsell

```markdown
**[MID TIER NAME] get access to:**
- [List benefits]

**[Become a [Mid Tier] - $X/month](https://YOUR-SITE.com/#/portal/signup/[TIER-ID]/monthly)**
```

### For Mid-Tier posts with Premium upsell

```markdown
**[PREMIUM TIER NAME] get access to:**
- [List additional benefits]

**[Become a [Premium Tier] - $XX/month](https://YOUR-SITE.com/#/portal/signup/[TIER-ID]/monthly)**
```

---

## Portal URLs

**Find your tier IDs in Ghost Admin → Settings → Membership → Tiers**

**Free:**
```
/#/portal/signup/free
```

**Paid Tiers:**
- Monthly: `/#/portal/signup/[TIER-ID]/monthly`
- Yearly: `/#/portal/signup/[TIER-ID]/yearly`

---

## Example CTAs in Context

### Example 1: Technical Tutorial (Free → Paid)

```markdown
## What You'll Learn

This post covers the complete implementation...

**[PAID TIER] get access to:**
- Step-by-step implementation guides
- Code templates and examples
- Architecture diagrams and explanations

**[Become a [Paid Tier] - $X/month](https://YOUR-SITE.com/#/portal/signup/[TIER-ID]/monthly)**

## Implementation
```

---

## Best Practices

**Placement:**
- Place CTA BEFORE exclusive content section
- Natural break point in content flow
- After establishing value in free section

**Tone:**
- Opt-in, never forced
- Focus on benefits, not exclusion
- Teaching-focused: "Get access to learn..."

**Benefits Phrasing:**
- Use your actual tier names
- Focus on what they get, not what they're missing
- Match your brand voice

**Avoid:**
- Gatekeeping language
- "Upgrade to unlock" (feels manipulative)
- Overemphasis on payment
- Multiple CTAs in same post
