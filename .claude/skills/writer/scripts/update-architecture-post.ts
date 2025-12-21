#!/usr/bin/env bun
/**
 * Update architecture post with voice-fixed content
 */
import { config } from 'dotenv';
import { resolve } from 'path';

// Load .env from framework root BEFORE importing ghost-admin
const FRAMEWORK_ROOT = resolve(import.meta.dir, '../../..');
config({ path: resolve(FRAMEWORK_ROOT, '.env') });

import { updatePost } from './ghost-admin';
import { readFileSync } from 'fs';
const BLOG_DIR = resolve(FRAMEWORK_ROOT, 'blog/2025-12-20-ia-framework-architecture');

async function main() {
  const draftPath = resolve(BLOG_DIR, 'draft.md');
  const draftContent = readFileSync(draftPath, 'utf-8');

  // Extract content after frontmatter
  const contentMatch = draftContent.match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/);
  if (!contentMatch) {
    console.error('Failed to parse frontmatter');
    process.exit(1);
  }

  const content = contentMatch[1].trim();
  const postId = '6946a781636ad1000125b2b5';

  console.log('Updating architecture post...');
  console.log(`Post ID: ${postId}`);
  console.log(`Content length: ${content.length} characters`);

  const result = await updatePost(postId, {
    content,
    contentType: 'markdown',
    status: 'published'
  });

  if (result.success) {
    console.log('✅ Post updated successfully!');
    console.log(`URL: ${result.post?.url}`);
    console.log(`Editor: ${result.post?.editorUrl}`);
  } else {
    console.error('❌ Failed to update post:', result.error);
    if (result.details) {
      console.error('Details:', JSON.stringify(result.details, null, 2));
    }
    process.exit(1);
  }
}

main();
