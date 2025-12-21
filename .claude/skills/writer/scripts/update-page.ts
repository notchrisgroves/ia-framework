#!/usr/bin/env bun
/**
 * Update Ghost CMS Page
 *
 * Updates an existing Ghost page by slug with new content.
 * Preserves page status and other metadata.
 */

import { ghostAdmin } from './ghost-admin';
import { readFile } from 'fs/promises';
import { resolve } from 'path';

interface UpdatePageOptions {
  slug: string;
  markdownFile: string;
}

async function updatePage(options: UpdatePageOptions) {
  try {
    console.log(`\n📄 Updating Ghost page: ${options.slug}`);

    // Read markdown file
    const markdownPath = resolve(options.markdownFile);
    const fileContent = await readFile(markdownPath, 'utf-8');

    // Extract frontmatter and content
    const frontmatterMatch = fileContent.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);

    if (!frontmatterMatch) {
      throw new Error('Invalid markdown file format. Expected frontmatter.');
    }

    const frontmatter = frontmatterMatch[1];
    const content = frontmatterMatch[2];

    // Parse frontmatter
    const titleMatch = frontmatter.match(/^title:\s*"(.+)"$/m);
    const statusMatch = frontmatter.match(/^status:\s*"(.+)"$/m);
    const isPage = frontmatter.match(/^page:\s*true$/m);

    if (!titleMatch) {
      throw new Error('Title not found in frontmatter');
    }

    const title = titleMatch[1];
    const status = (statusMatch?.[1] || 'published') as 'draft' | 'published';

    if (!isPage) {
      throw new Error('Not a page (page: true not found in frontmatter)');
    }

    console.log(`   Title: ${title}`);
    console.log(`   Status: ${status}`);

    // Find existing page by slug
    console.log(`\n🔍 Looking for existing page with slug: ${options.slug}`);
    const pages = await ghostAdmin.pages.browse({
      filter: `slug:${options.slug}`,
      limit: 1
    });

    if (!pages || pages.length === 0) {
      throw new Error(`Page not found with slug: ${options.slug}`);
    }

    const existingPage = pages[0];
    console.log(`   ✓ Found page: ${existingPage.title} (ID: ${existingPage.id})`);

    // Update page with new content
    console.log(`\n📝 Updating page content...`);

    const updateData: any = {
      id: existingPage.id,
      updated_at: existingPage.updated_at, // Required for Ghost API validation
      title: title,
      html: content, // Content is already HTML from markdown file
      status: status
    };

    const updatedPage = await ghostAdmin.pages.edit(updateData, { source: 'html' });

    console.log(`\n✅ Page updated successfully!`);
    console.log(`   URL: ${updatedPage.url}`);
    console.log(`   Editor: ${process.env.GHOST_API_URL}/ghost/#/editor/page/${updatedPage.id}`);

    return {
      success: true,
      page: {
        id: updatedPage.id,
        title: updatedPage.title,
        slug: updatedPage.slug,
        url: updatedPage.url,
        status: updatedPage.status
      }
    };

  } catch (error: any) {
    console.error(`\n❌ Error updating page: ${error.message}`);
    if (error.details) {
      console.error('   Details:', JSON.stringify(error.details, null, 2));
    }
    throw error;
  }
}

// CLI execution
if (import.meta.main) {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: bun update-page.ts <slug> <markdown-file>');
    console.error('Example: bun update-page.ts ia-setup-guide blog/pages/ia-setup-guide.md');
    process.exit(1);
  }

  const [slug, markdownFile] = args;

  updatePage({ slug, markdownFile })
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

export { updatePage };
