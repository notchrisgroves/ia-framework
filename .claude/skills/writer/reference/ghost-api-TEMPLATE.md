# Ghost API Integration Template

**Complete guide to Ghost CMS integration for YOUR-SITE.com**

> Copy this to `ghost-api.md` and customize with your site details.

---

## Credentials

**Location:** `.env` (framework root)

```
GHOST_ADMIN_API_KEY - Full CRUD permissions
GHOST_CONTENT_API_KEY - Read-only (for browsing existing posts)
GHOST_API_URL - https://YOUR-SITE.ghost.io
```

---

## Email Newsletter Architecture

**Two distinct content types with different email behavior:**

| Content Type | Ghost Configuration | Sends Email? | Appears on Site? |
|--------------|---------------------|--------------|------------------|
| **Regular Blog Post** | `sendEmailWhenPublished: false` | No | Yes |
| **Weekly Digest** | `sendEmailWhenPublished: true` + `emailOnly: true` | Yes | No |

**Rationale:**
- Weekly digest = curation layer (one email per week with summaries)
- Digest links to all new posts from that week
- Regular posts just publish to site (no individual emails)
- Prevents email fatigue (one curated digest vs multiple post emails)

**Regular Blog Post Configuration:**
```typescript
{
  status: 'published',
  visibility: 'public' | 'members' | 'paid',
  sendEmailWhenPublished: false,  // No email
  emailOnly: false                // Appears on site
}
```

**Weekly Digest Configuration:**
```typescript
{
  status: 'scheduled',
  visibility: 'public',
  sendEmailWhenPublished: true,   // Sends email
  emailOnly: true,                // Does NOT appear on site
  publishedAt: '2025-12-02T08:00:00-05:00'  // Monday 8 AM
}
```

---

## Available Wrappers

### 1. create_post - Create or Update Posts

```python
from servers.ghost_blog.create_post import create_post

result = create_post(
    title="Your Post Title",
    content="# Introduction\n\nContent here...",  # Markdown format
    status="draft",  # or "published"
    feature_image="https://YOUR-SITE.ghost.io/content/images/hero.png",
    tags=["Tag1", "Tag2"],
    engagement_dir="blog/posts/YYYY-MM-DD-post"  # Optional
)
```

### 2. upload_image - Upload Hero Images

```python
from servers.ghost_blog.upload_image import upload_image

image_result = upload_image(
    image_path="blog/posts/YYYY-MM-DD-post/hero.png",
    engagement_dir="blog/posts/YYYY-MM-DD-post"
)
imageUrl = image_result["summary"]["imageUrl"]
```

### 3. fetch_posts - List Existing Posts

```python
from servers.ghost_blog.fetch_posts import fetch_posts

# Minimal mode (fastest)
result = fetch_posts(mode="minimal", status="draft", limit=10)

# Standard mode (balanced)
result = fetch_posts(mode="standard", status="published", limit=20)
```

---

## Ghost Pages Workflow

**Pages are stored as markdown in `blog/pages/` and published to Ghost.**

**Standard Pages:**
- `about.md` - About page
- `contact.md` - Contact page
- `privacy.md` - Privacy Policy
- `terms.md` - Terms of Service

### Naming Rule

**Filename MUST match slug exactly: `{slug}.md`**
- `about.md` with `slug: "about"`
- `privacy.md` with `slug: "privacy"`

### No Duplicate Titles

**Ghost renders the title from frontmatter - body should NOT start with H1 (`#`)**

**Frontmatter Format:**
```markdown
---
title: "Page Title"
slug: "page-slug"
status: "published"
page: true
---

Body starts here with paragraph or H2 (##), NEVER H1 (#)

## First Section
Content here...
```

### Publishing Pages

```powershell
cd skills/writer
bun run lib/ghost-pages.ts
```

---

## See Also

- `servers/ghost-blog/README.md` - Complete wrapper documentation
- `skills/writer/tools/ghost-pages.ts` - Pages publishing infrastructure
