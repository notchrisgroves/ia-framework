#!/usr/bin/env bun
/**
 * Ghost Pages Publisher
 *
 * Publishes or updates Ghost pages (not posts). Pages are static content like
 * Contact, About, Setup Guide, etc. that appear in navigation menus.
 *
 * Usage:
 *   bun skills/writer/scripts/publish-pages.ts <page-file.md>
 */

import GhostAdminAPI from '@tryghost/admin-api';
import { marked } from 'marked';
import { config } from 'dotenv';
import { resolve } from 'path';
import { readFileSync } from 'fs';
import matter from 'gray-matter';

// Load .env from framework root
const envPath = resolve(process.cwd(), '.env');
config({ path: envPath });

const GHOST_API_URL = process.env.GHOST_API_URL;
const GHOST_ADMIN_API_KEY = process.env.GHOST_ADMIN_API_KEY;

if (!GHOST_ADMIN_API_KEY) {
  throw new Error('GHOST_ADMIN_API_KEY not set in environment');
}

// Initialize Ghost Admin API
const ghostAdmin = new GhostAdminAPI({
  url: GHOST_API_URL,
  key: GHOST_ADMIN_API_KEY,
  version: 'v5.0'
});

/**
 * Parse markdown file with frontmatter
 */
function parseMarkdownFile(filePath: string) {
  const fileContent = readFileSync(filePath, 'utf-8');
  const { data: frontmatter, content } = matter(fileContent);

  return {
    title: frontmatter.title,
    slug: frontmatter.slug,
    status: frontmatter.status || 'draft',
    content
  };
}

/**
 * Convert markdown to HTML
 */
function markdownToHtml(markdown: string): string {
  marked.setOptions({
    gfm: true,
    breaks: true,
    pedantic: false,
    smartLists: true,
    smartypants: true
  });

  return marked.parse(markdown) as string;
}

/**
 * Find existing page by slug
 */
async function findPageBySlug(slug: string) {
  try {
    const pages = await ghostAdmin.pages.browse({
      filter: `slug:${slug}`,
      limit: 1
    });

    return pages.length > 0 ? pages[0] : null;
  } catch (error) {
    console.error('Error finding page:', error);
    return null;
  }
}

/**
 * Update existing page
 */
async function updatePage(pageId: string, title: string, content: string, status: string) {
  try {
    // Fetch current page to get updated_at timestamp
    const currentPage = await ghostAdmin.pages.read({ id: pageId });

    const updatedPage = await ghostAdmin.pages.edit({
      id: pageId,
      title,
      html: content,
      status,
      updated_at: currentPage.updated_at
    }, { source: 'html' });

    return {
      success: true,
      page: updatedPage
    };
  } catch (error: any) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Create new page
 */
async function createPage(title: string, slug: string, content: string, status: string) {
  try {
    const newPage = await ghostAdmin.pages.add({
      title,
      slug,
      html: content,
      status
    }, { source: 'html' });

    return {
      success: true,
      page: newPage
    };
  } catch (error: any) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Main function
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: bun publish-pages.ts <page-file.md>');
    process.exit(1);
  }

  const pageFile = resolve(args[0]);
  console.log(`\n📄 Publishing page: ${pageFile}\n`);

  // Parse markdown file
  const { title, slug, status, content } = parseMarkdownFile(pageFile);
  const html = markdownToHtml(content);

  console.log(`Title: ${title}`);
  console.log(`Slug: ${slug}`);
  console.log(`Status: ${status}\n`);

  // Check if page exists
  const existingPage = await findPageBySlug(slug);

  if (existingPage) {
    console.log(`✓ Found existing page (ID: ${existingPage.id})`);
    console.log(`  Updating...`);

    const result = await updatePage(existingPage.id!, title, html, status);

    if (result.success) {
      console.log(`\n✓ Page updated successfully!`);
      console.log(`  URL: ${result.page?.url}`);
      console.log(`  Editor: ${GHOST_API_URL}/ghost/#/editor/page/${result.page?.id}`);
    } else {
      console.error(`\n✗ Error updating page: ${result.error}`);
      process.exit(1);
    }
  } else {
    console.log(`✓ Page not found, creating new...`);

    const result = await createPage(title, slug, html, status);

    if (result.success) {
      console.log(`\n✓ Page created successfully!`);
      console.log(`  URL: ${result.page?.url}`);
      console.log(`  Editor: ${GHOST_API_URL}/ghost/#/editor/page/${result.page?.id}`);
    } else {
      console.error(`\n✗ Error creating page: ${result.error}`);
      process.exit(1);
    }
  }
}

main();
