#!/usr/bin/env bun
/**
 * Publish Weekly Digest to Ghost CMS
 *
 * Usage:
 *   bun run skills/writer/scripts/publish-weekly-digest.ts <slug>
 *   bun run skills/writer/scripts/publish-weekly-digest.ts weekly-digest-2025-12-16-22
 *
 * Options:
 *   --dry-run    Preview without scheduling
 *   --send-now   Schedule for immediate publication
 */

import { createPost } from './ghost-admin';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

async function main() {
  // Parse command line arguments
  const args = process.argv.slice(2);
  const slug = args.find(arg => !arg.startsWith('--'));
  const dryRun = args.includes('--dry-run');
  const sendNow = args.includes('--send-now');

  if (!slug) {
    console.error('❌ Error: Slug required');
    console.error('');
    console.error('Usage:');
    console.error('  bun run skills/writer/scripts/publish-weekly-digest.ts <slug> [options]');
    console.error('');
    console.error('Example:');
    console.error('  bun run skills/writer/scripts/publish-weekly-digest.ts weekly-digest-2025-12-16-22');
    console.error('');
    console.error('Options:');
    console.error('  --dry-run    Preview without scheduling');
    console.error('  --send-now   Schedule for immediate publication');
    process.exit(1);
  }

  console.log(`[+] ${dryRun ? 'Previewing' : 'Publishing'} weekly digest to Ghost...\n`);

  // Read the draft markdown file from output/blog/drafts/
  const draftPath = resolve(process.cwd(), 'output', 'blog', 'drafts', slug, 'draft.md');

  if (!existsSync(draftPath)) {
    console.error(`❌ Error: Draft file not found at ${draftPath}`);
    console.error('');
    console.error('Expected location: output/blog/drafts/<slug>/draft.md');
    process.exit(1);
  }

  const content = readFileSync(draftPath, 'utf-8');

  // Extract frontmatter metadata (handle both \n and \r\n line endings)
  const frontmatterMatch = content.match(/^---[\r\n]+([\s\S]*?)[\r\n]+---[\r\n]+([\s\S]*)$/);
  if (!frontmatterMatch) {
    console.error('❌ Error: Invalid frontmatter format in draft.md');
    console.error('Content preview:', content.substring(0, 200));
    process.exit(1);
  }

  const frontmatter = frontmatterMatch[1];
  const body = frontmatterMatch[2];

  // Parse frontmatter
  const title = frontmatter.match(/title:\s*"(.+)"/)?.[1] || '';
  const digestSlug = frontmatter.match(/slug:\s*"(.+)"/)?.[1] || slug;
  const excerpt = frontmatter.match(/excerpt:\s*"(.+)"/)?.[1] || '';
  const tagsMatch = frontmatter.match(/tags:\s*\[(.+)\]/)?.[1] || '';
  const tags = tagsMatch.split(',').map((t: string) => t.trim().replace(/"/g, ''));

  console.log('📄 Digest Details:');
  console.log('- Title:', title);
  console.log('- Slug:', digestSlug);
  console.log('- Tags:', tags.join(', '));
  console.log('- Excerpt:', excerpt.substring(0, 80) + (excerpt.length > 80 ? '...' : ''));
  console.log('');

  if (dryRun) {
    console.log('🔍 DRY RUN MODE - No changes will be made');
    console.log('');
    console.log('Would schedule digest for:');

    if (sendNow) {
      console.log('- Immediate publication');
    } else {
      const nextMonday = new Date();
      const daysUntilMonday = (1 + 7 - nextMonday.getDay()) % 7 || 7;
      nextMonday.setDate(nextMonday.getDate() + daysUntilMonday);
      nextMonday.setHours(8, 0, 0, 0);

      console.log('- Next Monday:', nextMonday.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      }));
    }

    console.log('');
    console.log('Email configuration:');
    console.log('- Sends newsletter email: YES ✅');
    console.log('- Appears on site: NO ❌ (email-only)');
    console.log('');
    console.log('Run without --dry-run to actually schedule');
    return;
  }

  // Calculate schedule time
  let publishedAt: string;

  if (sendNow) {
    publishedAt = new Date().toISOString();
  } else {
    // Calculate next Monday at 8:00 AM for scheduling
    const nextMonday = new Date();
    const daysUntilMonday = (1 + 7 - nextMonday.getDay()) % 7 || 7;
    nextMonday.setDate(nextMonday.getDate() + daysUntilMonday);
    nextMonday.setHours(8, 0, 0, 0);
    publishedAt = nextMonday.toISOString();
  }

  // Create post in Ghost as SCHEDULED EMAIL ONLY
  const result = await createPost({
    title,
    content: body,
    contentType: 'markdown',
    status: 'scheduled',  // Schedule for send
    visibility: 'public',  // Required even for email-only
    slug: digestSlug,
    tags,
    excerpt,
    // CRITICAL: Email-only configuration (digest does NOT appear on site)
    sendEmailWhenPublished: true,  // ← Sends newsletter email
    emailOnly: true,  // ← Does NOT appear on blog feed
    publishedAt
  });

  if (result.success && result.post) {
    console.log('✅ Weekly digest scheduled successfully!');
    console.log('');
    console.log('📊 Digest Details:');
    console.log('- ID:', result.post.id);
    console.log('- Status:', result.post.status);
    console.log('- Slug:', result.post.slug);

    const scheduleDate = new Date(publishedAt);
    console.log('- Scheduled for:', scheduleDate.toLocaleString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short'
    }));
    console.log('');
    console.log('📧 Email Configuration:');
    console.log('- Sends newsletter email: YES ✅');
    console.log('- Appears on site: NO ❌ (email-only)');
    console.log('');
    console.log('🔗 Ghost Admin URL:', result.post.editorUrl);
    console.log('');
    console.log('📋 Next steps:');
    console.log('1. Open Ghost Admin → Posts → Scheduled');
    console.log('2. Use "Send test newsletter" to preview email');
    console.log('3. Verify all article links work in email');
    console.log('4. Verify digest does NOT appear on site (email-only)');
    console.log('5. Email will send automatically on scheduled date/time');
  } else {
    console.error('❌ Failed to publish weekly digest');
    console.error('Error:', result.error);
    if (result.details) {
      console.error('Details:', JSON.stringify(result.details, null, 2));
    }
    process.exit(1);
  }
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
