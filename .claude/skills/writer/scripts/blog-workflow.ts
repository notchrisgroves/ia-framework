#!/usr/bin/env bun
/**
 * Blog Workflow Tool - Intelligence Adjacent
 *
 * Unified tool for managing blog post lifecycle with enforced structure.
 * Local-first approach: files never move, status tracked in metadata.
 *
 * Commands:
 *   init <slug>          Create new post with correct structure
 *   qa <slug>            Run dual-model QA review (Haiku + Grok)
 *   publish <slug>       Publish post to Ghost
 *   tweet <slug>         Generate social summary
 *   image-prompt <slug>  Generate content-aware Grok prompt
 *   validate <slug>      Check voice and structure
 *   refresh              Update STATUS.md from all metadata
 *
 * Usage:
 *   bun run skills/writer/scripts/blog-workflow.ts init 2025-12-19-post-title
 *   bun run skills/writer/scripts/blog-workflow.ts publish 2025-12-19-post-title
 */

import { promises as fs } from 'fs';
import { join, resolve } from 'path';
import { existsSync } from 'fs';
import { createPost, updatePost, uploadImage } from './ghost-admin';
import { config } from 'dotenv';

// Load environment
const envPath = resolve(process.cwd(), '.env');
config({ path: envPath });

// Constants
const FRAMEWORK_ROOT = process.cwd();
const BLOG_ROOT = resolve(FRAMEWORK_ROOT, 'blog', 'posts');
const STATUS_FILE = resolve(FRAMEWORK_ROOT, 'blog', 'STATUS.md');

// Types
type PostStatus = 'draft' | 'published' | 'scheduled' | 'archived';
type PostVisibility = 'public' | 'members' | 'paid';

interface Metadata {
  slug: string;
  title: string;
  status: PostStatus;
  visibility: PostVisibility;
  category?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  published_at?: string;
  scheduled_for?: string;  // ISO 8601 datetime for scheduled publishing
  ghost?: {
    id: string;
    status: string;
    url: string;
    editor_url: string;
  };
  hero?: {
    local_path: string;
    alt_text: string;
    uploaded_to_ghost: boolean;
  };
  tweet?: {
    generated: boolean;
    posted: boolean;
    posted_at?: string;
  };
}

interface Frontmatter {
  title: string;
  excerpt: string;
  tags: string[];
  visibility: PostVisibility;
  category?: string;
  scheduled_for?: string;  // ISO 8601 datetime for scheduled publishing
}

// ============================================================================
// VALIDATION
// ============================================================================

/**
 * Validate slug format: YYYY-MM-DD-title
 */
function validateSlug(slug: string): void {
  const pattern = /^\d{4}-\d{2}-\d{2}-.+$/;
  if (!slug.match(pattern)) {
    throw new Error(
      `Invalid slug format: ${slug}\n` +
      `Required: YYYY-MM-DD-title\n` +
      `Example: 2025-12-17-security-testing-automation`
    );
  }
}

/**
 * Validate post directory structure
 */
async function validatePostStructure(slug: string): Promise<void> {
  validateSlug(slug);

  const postDir = join(BLOG_ROOT, slug);
  if (!existsSync(postDir)) {
    throw new Error(`Post directory not found: ${postDir}`);
  }

  const draftPath = join(postDir, 'draft.md');
  if (!existsSync(draftPath)) {
    throw new Error(`draft.md not found in ${slug}/`);
  }
}

/**
 * Parse markdown frontmatter and body
 */
function parseMarkdown(content: string): {
  frontmatter: Frontmatter;
  body: string;
} {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!match) {
    throw new Error('Invalid frontmatter format. Must start with --- and end with ---');
  }

  const [, frontmatterText, body] = match;
  const frontmatter: any = {};

  // Parse YAML-like frontmatter
  const lines = frontmatterText.split('\n');
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex === -1) continue;

    const key = line.substring(0, colonIndex).trim();
    let value = line.substring(colonIndex + 1).trim();

    // Remove quotes
    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    // Parse arrays
    if (value.startsWith('[') && value.endsWith(']')) {
      const arrayContent = value.slice(1, -1);
      frontmatter[key] = arrayContent
        .split(',')
        .map(item => item.trim().replace(/["']/g, ''));
    } else {
      frontmatter[key] = value;
    }
  }

  // Validate required fields
  if (!frontmatter.title) throw new Error('title required in frontmatter');
  if (!frontmatter.excerpt) throw new Error('excerpt required in frontmatter');
  if (!frontmatter.tags) throw new Error('tags required in frontmatter');
  if (!frontmatter.visibility) throw new Error('visibility required in frontmatter');

  return { frontmatter: frontmatter as Frontmatter, body };
}

// ============================================================================
// METADATA MANAGEMENT
// ============================================================================

/**
 * Read metadata.json
 */
async function readMetadata(slug: string): Promise<Metadata> {
  const metadataPath = join(BLOG_ROOT, slug, 'metadata.json');
  if (!existsSync(metadataPath)) {
    throw new Error(`metadata.json not found for ${slug}. Run 'init' first.`);
  }
  const content = await fs.readFile(metadataPath, 'utf-8');
  return JSON.parse(content);
}

/**
 * Write metadata.json
 */
async function writeMetadata(slug: string, metadata: Metadata): Promise<void> {
  const metadataPath = join(BLOG_ROOT, slug, 'metadata.json');
  metadata.updated_at = new Date().toISOString();
  await fs.writeFile(metadataPath, JSON.stringify(metadata, null, 2), 'utf-8');
}

/**
 * Update STATUS.md from all metadata files
 */
async function updateStatusTable(): Promise<void> {
  console.log('\n📊 Updating STATUS.md...');

  // Ensure blog directory exists
  if (!existsSync(BLOG_ROOT)) {
    await fs.mkdir(BLOG_ROOT, { recursive: true });
  }

  // Scan all post directories
  const entries = await fs.readdir(BLOG_ROOT, { withFileTypes: true });
  const posts: Metadata[] = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (entry.name === '.git') continue;

    const metadataPath = join(BLOG_ROOT, entry.name, 'metadata.json');
    if (existsSync(metadataPath)) {
      try {
        const content = await fs.readFile(metadataPath, 'utf-8');
        posts.push(JSON.parse(content));
      } catch (err) {
        console.warn(`⚠️  Failed to read ${entry.name}/metadata.json:`, err);
      }
    }
  }

  // Sort by date (newest first)
  posts.sort((a, b) => b.slug.localeCompare(a.slug));

  // Calculate statistics
  const stats = {
    total: posts.length,
    published: posts.filter(p => p.status === 'published').length,
    drafts: posts.filter(p => p.status === 'draft').length,
    archived: posts.filter(p => p.status === 'archived').length,
  };

  // Build markdown table
  let content = `# Blog Post Status\n\n`;
  content += `**Last Updated:** ${new Date().toISOString().replace('T', ' ').substring(0, 19)}\n\n`;
  content += `**Summary:**\n`;
  content += `- Total Posts: ${stats.total}\n`;
  content += `- Published: ${stats.published}\n`;
  content += `- Drafts: ${stats.drafts}\n`;
  content += `- Archived: ${stats.archived}\n\n`;
  content += `---\n\n`;

  // All posts table
  content += `## All Posts (Chronological - Newest First)\n\n`;
  content += `| Date | Title | Status | Visibility | Category | Ghost | Updated |\n`;
  content += `|------|-------|--------|------------|----------|-------|---------|\n`;

  for (const post of posts) {
    const date = post.slug.substring(0, 10);
    const title = post.title || post.slug;
    const ghostLink = post.ghost?.url ? `[View](${post.ghost.url})` : '-';
    const updated = post.updated_at?.substring(0, 16).replace('T', ' ') || '-';
    const category = post.category || '-';

    content += `| ${date} | ${title} | ${post.status} | ${post.visibility} | ${category} | ${ghostLink} | ${updated} |\n`;
  }

  content += `\n---\n\n`;

  // By status
  content += `## By Status\n\n`;

  // Published
  const published = posts.filter(p => p.status === 'published');
  content += `### Published (${published.length})\n\n`;
  if (published.length > 0) {
    content += `| Date | Title | Visibility | Ghost URL | Published |\n`;
    content += `|------|-------|------------|-----------|-----------|---|\n`;
    for (const post of published) {
      const date = post.slug.substring(0, 10);
      const url = post.ghost?.url || '-';
      const pubDate = post.published_at?.substring(0, 16).replace('T', ' ') || '-';
      content += `| ${date} | ${post.title} | ${post.visibility} | [View](${url}) | ${pubDate} |\n`;
    }
  } else {
    content += `None.\n`;
  }
  content += `\n`;

  // Drafts
  const drafts = posts.filter(p => p.status === 'draft');
  content += `### Drafts (${drafts.length})\n\n`;
  if (drafts.length > 0) {
    content += `| Date | Title | Visibility | Last Updated |\n`;
    content += `|------|-------|------------|--------------|--|\n`;
    for (const post of drafts) {
      const date = post.slug.substring(0, 10);
      const updated = post.updated_at?.substring(0, 16).replace('T', ' ') || '-';
      content += `| ${date} | ${post.title} | ${post.visibility} | ${updated} |\n`;
    }
  } else {
    content += `None.\n`;
  }
  content += `\n`;

  // Archived
  const archived = posts.filter(p => p.status === 'archived');
  content += `### Archived (${archived.length})\n\n`;
  if (archived.length > 0) {
    content += `| Date | Title | Archived |\n`;
    content += `|------|-------|----------|\n`;
    for (const post of archived) {
      const date = post.slug.substring(0, 10);
      content += `| ${date} | ${post.title} | ${post.updated_at?.substring(0, 10) || '-'} |\n`;
    }
  } else {
    content += `None.\n`;
  }
  content += `\n---\n\n`;

  // By category
  const categories = new Map<string, Metadata[]>();
  for (const post of posts) {
    const cat = post.category || 'Uncategorized';
    if (!categories.has(cat)) categories.set(cat, []);
    categories.get(cat)!.push(post);
  }

  content += `## By Category\n\n`;
  for (const [category, categoryPosts] of categories) {
    content += `### ${category} (${categoryPosts.length})\n`;
    for (const post of categoryPosts) {
      const date = post.slug.substring(0, 10);
      content += `- [${date}] ${post.title} (${post.status})\n`;
    }
    content += `\n`;
  }

  content += `---\n\n`;
  content += `<!-- AUTO-GENERATED SECTION ENDS HERE -->\n\n`;

  // Preserve manual content (Archive Assessment, Roadmap, etc.) if it exists
  if (existsSync(STATUS_FILE)) {
    try {
      const existingContent = await fs.readFile(STATUS_FILE, 'utf-8');
      const manualMarker = '## Archive Assessment';
      const manualIndex = existingContent.indexOf(manualMarker);
      if (manualIndex !== -1) {
        content += existingContent.substring(manualIndex);
      }
    } catch (err) {
      // If we can't read existing file, just use auto-generated content
    }
  }

  await fs.writeFile(STATUS_FILE, content, 'utf-8');
  console.log('✅ STATUS.md updated\n');
}

// ============================================================================
// COMMANDS
// ============================================================================

/**
 * Command: init
 * Create new post with correct structure
 */
async function cmdInit(slug: string): Promise<void> {
  console.log(`\n📝 Initializing new post: ${slug}\n`);

  // Validate slug format
  validateSlug(slug);

  const postDir = join(BLOG_ROOT, slug);

  // Check if already exists
  if (existsSync(postDir)) {
    throw new Error(`Post already exists: ${slug}`);
  }

  // Create directory
  await fs.mkdir(postDir, { recursive: true });
  console.log(`✅ Created directory: blog/${slug}/`);

  // Create draft.md template
  const draftTemplate = `---
title: "Your Post Title Here"
excerpt: "150-160 character SEO description goes here"
tags: ["Tag1", "Tag2", "Tag3"]
visibility: "members"
category: "framework"
---

# Your Post Title Here

## Introduction

[Your content here...]

## Problem

[What problem are you solving?]

## Solution

[How did you solve it?]

## Implementation

[Practical details and code examples]

## Conclusion

[Key takeaways]

## Sources

- [Source 1](URL)
- [Source 2](URL)
`;

  const draftPath = join(postDir, 'draft.md');
  await fs.writeFile(draftPath, draftTemplate, 'utf-8');
  console.log(`✅ Created draft.md`);

  // Create metadata.json
  const metadata: Metadata = {
    slug,
    title: 'Your Post Title Here',
    status: 'draft',
    visibility: 'members',
    category: 'framework',
    tags: ['Tag1', 'Tag2', 'Tag3'],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  await writeMetadata(slug, metadata);
  console.log(`✅ Created metadata.json`);

  // Update STATUS.md
  await updateStatusTable();

  console.log(`\n✅ Post initialized successfully!`);
  console.log(`\nNext steps:`);
  console.log(`1. Edit blog/${slug}/draft.md`);
  console.log(`2. Generate image prompt: blog-workflow.ts image-prompt ${slug}`);
  console.log(`3. Publish: blog-workflow.ts publish ${slug}`);
}

/**
 * Command: publish
 * Publish post to Ghost - fully automated with hero image upload
 */
async function cmdPublish(slug: string): Promise<void> {
  console.log(`\n🚀 Publishing post: ${slug}\n`);

  // Validate structure
  await validatePostStructure(slug);

  // Read draft and metadata
  const postDir = join(BLOG_ROOT, slug);
  const draftPath = join(postDir, 'draft.md');
  const heroPath = join(postDir, 'hero.png');
  const promptPath = join(postDir, 'hero-prompt.txt');
  const draftContent = await fs.readFile(draftPath, 'utf-8');
  const { frontmatter, body } = parseMarkdown(draftContent);
  let metadata = await readMetadata(slug);

  console.log(`📄 Title: ${frontmatter.title}`);
  console.log(`👁️  Visibility: ${frontmatter.visibility}`);
  console.log(`🏷️  Tags: ${frontmatter.tags.join(', ')}\n`);

  // Upload hero image if exists
  let featureImageUrl: string | undefined;
  let featureImageAlt: string | undefined;

  if (existsSync(heroPath)) {
    console.log('🖼️  Uploading hero image...');

    // Read alt text from hero-prompt.txt
    if (existsSync(promptPath)) {
      const promptContent = await fs.readFile(promptPath, 'utf-8');
      const altTextMatch = promptContent.match(/ALT TEXT.*?:\s*(.+)/i);
      featureImageAlt = altTextMatch ? altTextMatch[1].trim() : `Hero image for ${frontmatter.title}`;
    } else {
      featureImageAlt = `Hero image for ${frontmatter.title}`;
    }

    const uploadResult = await uploadImage(heroPath, featureImageAlt);

    if (uploadResult.success && uploadResult.imageUrl) {
      featureImageUrl = uploadResult.imageUrl;
      console.log(`✅ Hero uploaded: ${featureImageUrl}`);
    } else {
      console.log(`⚠️  Hero upload failed: ${uploadResult.error}`);
      console.log('   Continuing without hero image...');
    }
  } else {
    console.log(`⚠️  No hero.png found in blog/${slug}/`);
    console.log('   Continuing without hero image...');
  }

  // Create or update Ghost post
  if (!metadata.ghost) {
    // Create new Ghost post
    console.log('Creating Ghost post...');

    const result = await createPost({
      title: frontmatter.title,
      content: body,
      contentType: 'markdown',
      status: 'draft',
      visibility: frontmatter.visibility,
      tags: frontmatter.tags,
      excerpt: frontmatter.excerpt,
      slug: slug.replace(/^\d{4}-\d{2}-\d{2}-/, ''), // Remove date prefix for Ghost
      featureImage: featureImageUrl,
      featureImageAlt: featureImageAlt,
    });

    if (!result.success || !result.post) {
      throw new Error(`Failed to create Ghost post: ${result.error}`);
    }

    // Update metadata with Ghost info
    metadata.ghost = {
      id: result.post.id,
      status: 'draft',
      url: result.post.url,
      editor_url: result.post.editorUrl,
    };

    await writeMetadata(slug, metadata);
    console.log(`✅ Ghost post created`);
  } else {
    // Update existing post with new content and hero
    console.log('Updating existing Ghost post...');

    const updateData: any = {
      title: frontmatter.title,
      content: body,  // Raw markdown - will be converted by updatePost
      contentType: 'markdown',  // Triggers markdown → HTML conversion
      excerpt: frontmatter.excerpt,
    };

    if (featureImageUrl) {
      updateData.featureImage = featureImageUrl;
      updateData.featureImageAlt = featureImageAlt;
    }

    const updateResult = await updatePost(metadata.ghost.id, updateData);
    if (!updateResult.success) {
      console.log(`⚠️  Content update failed: ${updateResult.error}`);
    } else {
      console.log(`✅ Ghost post updated`);
    }
  }

  // Determine if scheduling or immediate publish
  const scheduledFor = frontmatter.scheduled_for || metadata.scheduled_for;
  const isScheduled = scheduledFor && new Date(scheduledFor) > new Date();

  if (isScheduled) {
    // Schedule the post for future publication
    console.log(`📅 Scheduling post for: ${scheduledFor}`);

    const scheduleResult = await updatePost(metadata.ghost!.id, {
      status: 'scheduled',
      publishedAt: scheduledFor,
    });

    if (!scheduleResult.success || !scheduleResult.post) {
      throw new Error(`Failed to schedule: ${scheduleResult.error}`);
    }

    // Update metadata
    metadata.status = 'scheduled';
    metadata.scheduled_for = scheduledFor;
    metadata.ghost.status = 'scheduled';
    metadata.ghost.url = scheduleResult.post.url;

    await writeMetadata(slug, metadata);
    await updateStatusTable();

    console.log(`\n✅ Post scheduled successfully!`);
    console.log(`📅 Scheduled for: ${new Date(scheduledFor).toLocaleString()}`);
    console.log(`📝 Editor: ${metadata.ghost.editor_url}\n`);

    // FORCED CHECK for scheduled posts too
    console.log(`\n` + `=`.repeat(60));
    console.log(`⚠️  REQUIRED: Verify STATUS.md manual sections are current`);
    console.log(`=`.repeat(60));
    console.log(`\n📋 Manual sections to review:`);
    console.log(`   - Archive Assessment (if drafts completed/deleted)`);
    console.log(`   - Content Roadmap (if priorities changed)`);
    console.log(`   - Series Groupings (if post is part of series)`);
    console.log(`   - By Category counts`);
    console.log(`\n📁 File: blog/STATUS.md`);
    console.log(`🔄 Auto-refresh already ran (updates post tables only)\n`);
  } else {
    // Publish immediately
    console.log('Publishing post...');

    const publishResult = await updatePost(metadata.ghost!.id, {
      status: 'published',
      publishedAt: new Date().toISOString(),
    });

    if (!publishResult.success || !publishResult.post) {
      throw new Error(`Failed to publish: ${publishResult.error}`);
    }

    // Update metadata
    metadata.status = 'published';
    metadata.published_at = new Date().toISOString();
    metadata.ghost.status = 'published';
    metadata.ghost.url = publishResult.post.url;

    await writeMetadata(slug, metadata);
    await updateStatusTable();

    console.log(`\n✅ Post published successfully!`);
    console.log(`🔗 URL: ${publishResult.post.url}`);
    console.log(`📝 Editor: ${metadata.ghost.editor_url}\n`);
  }

  // FORCED CHECK: Remind agent to verify STATUS.md manual sections
  console.log(`\n` + `=`.repeat(60));
  console.log(`⚠️  REQUIRED: Verify STATUS.md manual sections are current`);
  console.log(`=`.repeat(60));
  console.log(`\n📋 Manual sections to review:`);
  console.log(`   - Archive Assessment (if drafts completed/deleted)`);
  console.log(`   - Content Roadmap (if priorities changed)`);
  console.log(`   - Series Groupings (if post is part of series)`);
  console.log(`   - By Category counts`);
  console.log(`\n📁 File: blog/STATUS.md`);
  console.log(`🔄 Auto-refresh already ran (updates post tables only)\n`);
}

/**
 * Command: tweet
 * Generate AI-powered social summary using Grok via OpenRouter
 * Follows HOOK → VALUE → CTA formula for viral engagement
 */
async function cmdTweet(slug: string): Promise<void> {
  console.log(`\n🐦 Generating AI-powered tweet: ${slug}\n`);

  await validatePostStructure(slug);

  const postDir = join(BLOG_ROOT, slug);
  const draftPath = join(postDir, 'draft.md');
  const metadata = await readMetadata(slug);

  // Build URL from slug (always use slug-based URL, not preview URLs like /p/uuid)
  // Ghost preview URLs change after publication, so we use the expected final URL
  const slugPart = metadata.slug || slug.replace(/^\d{4}-\d{2}-\d{2}-/, '');
  const url = `https://notchrisgroves.com/${slugPart}/`;

  // Call Python script for AI-powered generation
  const scriptPath = join(FRAMEWORK_ROOT, 'tools', 'openrouter', 'generate_tweet.py');

  console.log(`Calling Grok for tweet generation...`);
  console.log(`Draft: ${draftPath}`);
  console.log(`URL: ${url}\n`);

  const { execSync } = await import('child_process');

  try {
    const result = execSync(
      `python "${scriptPath}" "${draftPath}" "${url}"`,
      {
        encoding: 'utf-8',
        cwd: FRAMEWORK_ROOT,
        timeout: 120000  // 2 minute timeout
      }
    );
    console.log(result);
  } catch (error: any) {
    console.error(`\n❌ Tweet generation failed:`);
    console.error(error.message);
    console.error(`\nFallback: Create tweet.txt manually with HOOK → VALUE → CTA structure.`);
    return;
  }

  // Update metadata - tweet generated
  if (!metadata.tweet) metadata.tweet = { generated: false, posted: false };
  metadata.tweet.generated = true;

  console.log(`\n✅ AI-powered tweet generated!`);
  console.log(`📄 Saved to: blog/${slug}/tweet.md`);

  // Check if post is actually published (not scheduled)
  const ghostStatus = metadata.ghost?.status;
  if (ghostStatus === 'scheduled') {
    const scheduledFor = metadata.ghost?.scheduled_for || metadata.scheduled_for;
    console.log(`\n⏳ Post is scheduled for: ${scheduledFor}`);
    console.log(`   Tweet will be posted after publication.`);
    console.log(`   Run 'tweet ${slug}' again after post goes live.\n`);

    await writeMetadata(slug, metadata);
    await updateStatusTable();
    return;
  }

  if (ghostStatus !== 'published') {
    console.log(`\n⚠️ Post status: ${ghostStatus || 'draft'}`);
    console.log(`   Tweet saved but not posted. Publish post first.\n`);

    await writeMetadata(slug, metadata);
    await updateStatusTable();
    return;
  }

  // Auto-post to X (only if published)
  const tweetPath = join(postDir, 'tweet.md');
  const postScriptPath = join(FRAMEWORK_ROOT, 'tools', 'x-api', 'post_tweet.py');

  console.log(`\n🐦 Posting to X...`);

  try {
    const postResult = execSync(
      `python "${postScriptPath}" "${tweetPath}"`,
      {
        encoding: 'utf-8',
        cwd: FRAMEWORK_ROOT,
        timeout: 30000  // 30 second timeout
      }
    );

    // Parse JSON response from last line
    const lines = postResult.trim().split('\n');
    const jsonLine = lines[lines.length - 1];
    const tweetResult = JSON.parse(jsonLine);

    if (tweetResult.success) {
      metadata.tweet.posted = true;
      metadata.tweet.posted_at = new Date().toISOString();
      metadata.tweet.url = tweetResult.url;
      metadata.tweet.id = tweetResult.id;

      console.log(`✅ Posted to X!`);
      console.log(`🔗 ${tweetResult.url}\n`);
    } else {
      console.error(`\n⚠️ X posting failed: ${tweetResult.error}`);
      console.log(`Tweet saved to: blog/${slug}/tweet.md (post manually)\n`);
    }
  } catch (error: any) {
    console.error(`\n⚠️ X posting failed:`);
    console.error(error.message);
    console.log(`Tweet saved to: blog/${slug}/tweet.md (post manually)\n`);
  }

  await writeMetadata(slug, metadata);
  await updateStatusTable();
}

/**
 * Command: qa
 * Run Grok adversarial QA review via OpenRouter
 * Sonnet structured review should be done natively by Claude Code first
 *
 * Usage: qa <slug> [sonnet_rating]
 * Example: qa 2025-12-20-post-title 4
 */
async function cmdQa(slug: string, sonnetRating: string = '0'): Promise<void> {
  console.log(`\n🔍 Running Grok adversarial QA review: ${slug}\n`);

  await validatePostStructure(slug);

  const postDir = join(BLOG_ROOT, slug);
  const draftPath = join(postDir, 'draft.md');
  const rating = parseInt(sonnetRating) || 0;

  // Call Python script for Grok review only
  const scriptPath = join(FRAMEWORK_ROOT, 'tools', 'openrouter', 'dual_qa_review.py');

  console.log(`Draft: ${draftPath}`);
  console.log(`Sonnet Rating (native): ${rating}/5`);
  console.log(`Output: ${postDir}/qa-review.json\n`);

  const { execSync } = await import('child_process');

  try {
    const result = execSync(
      `python "${scriptPath}" "${draftPath}" ${rating}`,
      {
        encoding: 'utf-8',
        cwd: FRAMEWORK_ROOT,
        timeout: 180000  // 3 minute timeout
      }
    );
    console.log(result);
  } catch (error: any) {
    console.error(`\n❌ QA review failed:`);
    console.error(error.message);
    console.error(`\nManual fallback: Run QA review manually per 03-QA.md`);
    process.exit(1);
  }

  // Check if gate passed
  const qaPath = join(postDir, 'qa-review.json');
  if (existsSync(qaPath)) {
    const qaContent = await fs.readFile(qaPath, 'utf-8');
    const qaResult = JSON.parse(qaContent);

    if (!qaResult.gate_passed) {
      console.log(`\n⚠️  QA gate failed. Review feedback and revise before publishing.`);
      console.log(`   Average rating: ${qaResult.ratings?.average}/5 (needs ≥4.0)\n`);
      process.exit(1);
    }

    console.log(`\n✅ QA gate passed! Rating: ${qaResult.ratings?.average}/5`);
    console.log(`📄 Full review: blog/${slug}/qa-review.json\n`);
  }
}

/**
 * Command: image-prompt
 * Generate content-aware Grok image prompt based on keywords
 */
async function cmdImagePrompt(slug: string): Promise<void> {
  console.log(`\n🎨 Generating image prompt: ${slug}\n`);

  await validatePostStructure(slug);

  const postDir = join(BLOG_ROOT, slug);
  const draftPath = join(postDir, 'draft.md');
  const draftContent = await fs.readFile(draftPath, 'utf-8');
  const { frontmatter, body } = parseMarkdown(draftContent);

  // Analyze content for themes using keyword matching
  const contentLower = (frontmatter.title + ' ' + body).toLowerCase();
  const themes: string[] = [];

  // Security themes
  if (contentLower.match(/security|pentest|vulnerability|exploit|threat|attack|defend/)) {
    themes.push('security testing with shields, locks, and network diagrams');
  }

  // Framework/Architecture themes
  if (contentLower.match(/framework|architecture|system|structure|design|pattern/)) {
    themes.push('modular architecture with interconnected nodes and data flows');
  }

  // Automation/Tools themes
  if (contentLower.match(/automation|tool|script|workflow|pipeline|ci\/cd/)) {
    themes.push('automated systems with terminals, code, and deployment pipelines');
  }

  // VPS/Infrastructure themes
  if (contentLower.match(/vps|server|docker|container|deploy|infrastructure/)) {
    themes.push('cloud infrastructure with servers, containers, and network connections');
  }

  // Research/Analysis themes
  if (contentLower.match(/research|analysis|data|osint|intelligence|investigate/)) {
    themes.push('data visualization with connections, graphs, and information flows');
  }

  // Default if no themes detected
  if (themes.length === 0) {
    themes.push('technical environment with code, terminals, and digital interfaces');
  }

  const themeDescription = themes[0]; // Use primary theme

  // Generate prompt template
  const fullPrompt = `90s anime style illustration: ${themeDescription}. Cyberpunk aesthetic with neon accents (purple/blue/cyan), moody technical environment. Dark tones with strategic highlights. Professional security researcher or developer at work. Matrix-style data streams in background.`;

  const altText = `Cyberpunk anime: ${frontmatter.title.substring(0, 150)}`;

  const promptText = `FULL PROMPT (for Grok x.ai image generation):
${fullPrompt}

ALT TEXT (for Ghost, max 191 chars):
${altText}

---
INSTRUCTIONS:
1. Go to x.ai image generation
2. Paste the FULL PROMPT above
3. Download generated image
4. Save as: blog/${slug}/hero.png
5. Use ALT TEXT when uploading to Ghost
`;

  // Save to hero-prompt.txt
  const promptPath = join(postDir, 'hero-prompt.txt');
  await fs.writeFile(promptPath, promptText, 'utf-8');

  console.log(`\n✅ Image prompt generated!`);
  console.log(`📄 Saved to: blog/${slug}/hero-prompt.txt\n`);
  console.log(`Detected themes: ${themes.join(', ')}\n`);
  console.log(`Next steps:`);
  console.log(`1. Go to x.ai image generation`);
  console.log(`2. Paste the FULL PROMPT from hero-prompt.txt`);
  console.log(`3. Download image as blog/${slug}/hero.png\n`);
}

/**
 * Command: refresh
 * Regenerate STATUS.md from all metadata
 */
async function cmdRefresh(): Promise<void> {
  console.log(`\n🔄 Refreshing STATUS.md...\n`);
  await updateStatusTable();
  console.log(`✅ STATUS.md refreshed\n`);
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const slug = args[1];

  if (!command) {
    console.error('❌ Error: Command required\n');
    console.error('Usage:');
    console.error('  blog-workflow.ts init <slug>');
    console.error('  blog-workflow.ts qa <slug>');
    console.error('  blog-workflow.ts publish <slug>');
    console.error('  blog-workflow.ts tweet <slug>');
    console.error('  blog-workflow.ts image-prompt <slug>');
    console.error('  blog-workflow.ts refresh\n');
    console.error('Example:');
    console.error('  blog-workflow.ts init 2025-12-19-post-title\n');
    process.exit(1);
  }

  try {
    switch (command) {
      case 'init':
        if (!slug) throw new Error('Slug required for init command');
        await cmdInit(slug);
        break;

      case 'publish':
        if (!slug) throw new Error('Slug required for publish command');
        await cmdPublish(slug);
        break;

      case 'qa':
        if (!slug) throw new Error('Slug required for qa command');
        await cmdQa(slug, args[2] || '0');  // Optional sonnet_rating
        break;

      case 'tweet':
        if (!slug) throw new Error('Slug required for tweet command');
        await cmdTweet(slug);
        break;

      case 'image-prompt':
        if (!slug) throw new Error('Slug required for image-prompt command');
        await cmdImagePrompt(slug);
        break;

      case 'refresh':
        await cmdRefresh();
        break;

      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error: any) {
    console.error(`\n❌ Error: ${error.message}\n`);
    process.exit(1);
  }
}

main();
