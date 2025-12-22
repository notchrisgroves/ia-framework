#!/usr/bin/env bun
/**
 * Ghost Admin API Client - Production-Ready Implementation
 *
 * This module provides a clean interface to Ghost Admin API using the official
 * JavaScript library. Handles content formatting, authentication, and error handling.
 *
 * Key Features:
 * - Automatic JWT token generation
 * - Multiple content formats: Markdown → HTML, Lexical JSON, or raw HTML
 * - Image upload support
 * - Type-safe interfaces
 * - Error handling with detailed messages
 *
 * Content Format Handling:
 * - Markdown: Automatically converted to HTML (recommended for blog-writer)
 * - HTML: Direct HTML input with {source: 'html'}
 * - Lexical: Ghost's native format (complex, not recommended for automation)
 *
 * CRITICAL: Email Newsletter Architecture (2025-11-24)
 * =====================================================
 *
 * Two distinct content types with different email behavior:
 *
 * 1. REGULAR BLOG POSTS (Publish to site, NO email)
 *    - Configuration:
 *      * status: 'draft' or 'published'
 *      * sendEmailWhenPublished: false (DEFAULT)
 *      * emailOnly: false (DEFAULT)
 *    - Behavior:
 *      * Appears on blog feed
 *      * Does NOT trigger newsletter email
 *      * Links included in weekly digest
 *
 * 2. WEEKLY DIGESTS (Email only, NOT on site)
 *    - Configuration:
 *      * status: 'scheduled'
 *      * sendEmailWhenPublished: true (REQUIRED)
 *      * emailOnly: true (REQUIRED)
 *      * publishedAt: ISO 8601 timestamp (for scheduling)
 *    - Behavior:
 *      * Does NOT appear on blog feed
 *      * Sends as newsletter email to all subscribers
 *      * Contains summaries + links to posts from that week
 *
 * Rationale:
 * - Weekly digest = curation layer (one email per week)
 * - Prevents email fatigue (digest-only vs individual post emails)
 * - Subscribers get curated summary, click through to site for full content
 * - Blog feed stays clean (no duplicate digest posts)
 *
 * @see https://docs.ghost.org/admin-api/javascript
 */

import GhostAdminAPI from '@tryghost/admin-api';
import { marked } from 'marked';
import { config } from 'dotenv';
import { resolve } from 'path';

// Load .env from framework root
const envPath = resolve(process.cwd(), '.env');
config({ path: envPath });

// Environment configuration
const GHOST_API_URL = process.env.GHOST_API_URL;
const GHOST_ADMIN_API_KEY = process.env.GHOST_ADMIN_API_KEY;

if (!GHOST_ADMIN_API_KEY) {
  throw new Error('GHOST_ADMIN_API_KEY not set in environment. Check .env file in framework root');
}

// Initialize Ghost Admin API client
export const ghostAdmin = new GhostAdminAPI({
  url: GHOST_API_URL,
  key: GHOST_ADMIN_API_KEY,
  version: 'v5.0'  // Ghost API version (library handles compatibility with Ghost 6.0)
});

/**
 * Type definitions for Ghost API
 */
export interface GhostPost {
  id?: string;
  title: string;
  html?: string;
  lexical?: string;
  status?: 'draft' | 'published' | 'scheduled';
  feature_image?: string;
  tags?: Array<{ name: string }>;
  custom_excerpt?: string;
  slug?: string;
  url?: string;
  created_at?: string;
  updated_at?: string;
  published_at?: string;
}

export interface CreatePostOptions {
  title: string;
  content: string;
  contentType?: 'markdown' | 'html' | 'lexical';
  status?: 'draft' | 'published' | 'scheduled';
  featureImage?: string;
  featureImageAlt?: string;
  tags?: string[];
  excerpt?: string;
  slug?: string;
  visibility?: 'public' | 'members' | 'paid';
  sendEmailWhenPublished?: boolean;  // Control email sending
  emailOnly?: boolean;  // Email-only posts (digests)
  publishedAt?: string;  // For scheduled posts (ISO 8601 format)
  newsletter?: string;  // Newsletter slug (required for email sends)
}

export interface CreatePostResult {
  success: boolean;
  post?: {
    id: string;
    title: string;
    slug: string;
    status: string;
    url: string;
    editorUrl: string;
  };
  error?: string;
  details?: any;
}

/**
 * Convert markdown to HTML using marked library
 *
 * Marked is a fast, compliant markdown parser that handles:
 * - Headers, bold, italic, code blocks
 * - Lists, blockquotes, links
 * - Tables, task lists
 *
 * @param markdown - Markdown-formatted content
 * @returns HTML string ready for Ghost
 */
export function markdownToHtml(markdown: string): string {
  // Configure marked for safe HTML output
  marked.setOptions({
    gfm: true,  // GitHub Flavored Markdown
    breaks: true,  // Convert \n to <br>
    pedantic: false,
    smartLists: true,
    smartypants: true  // Smart quotes, dashes
  });

  return marked.parse(markdown) as string;
}

/**
 * Create or update a Ghost blog post
 *
 * This is the primary function for publishing content. It handles:
 * - Content format conversion (markdown → HTML)
 * - Tag formatting
 * - Error handling
 * - URL generation
 *
 * @param options - Post configuration
 * @returns Result object with post details or error
 *
 * @example
 * ```typescript
 * const result = await createPost({
 *   title: "AI Security Best Practices",
 *   content: "# Introduction\n\nAI systems require...",
 *   contentType: "markdown",
 *   status: "draft",
 *   tags: ["AI", "Security"],
 *   featureImage: "https://..."
 * });
 *
 * if (result.success) {
 *   console.log(`Post created: ${result.post.editorUrl}`);
 * }
 * ```
 */
export async function createPost(options: CreatePostOptions): Promise<CreatePostResult> {
  try {
    const {
      title,
      content,
      contentType = 'markdown',
      status = 'draft',
      featureImage,
      featureImageAlt,
      tags = [],
      excerpt,
      slug,
      visibility = 'public',
      sendEmailWhenPublished = false,  // DEFAULT: No email for regular posts
      emailOnly = false,
      publishedAt,
      newsletter
    } = options;

    // Prepare post data
    const postData: any = {
      title,
      status,
      visibility
    };

    // Handle content format conversion
    if (contentType === 'markdown') {
      // Convert markdown to HTML
      postData.html = markdownToHtml(content);
      // IMPORTANT: Must specify source as 'html' when using HTML content
      // Otherwise Ghost expects Lexical JSON format
    } else if (contentType === 'html') {
      postData.html = content;
    } else if (contentType === 'lexical') {
      postData.lexical = content;
    }

    // Add optional fields
    if (featureImage) {
      postData.feature_image = featureImage;
    }

    if (featureImageAlt) {
      postData.feature_image_alt = featureImageAlt;
    }

    if (tags.length > 0) {
      postData.tags = tags.map(tag => ({ name: tag }));
    }

    if (excerpt) {
      postData.custom_excerpt = excerpt;
    }

    if (slug) {
      postData.slug = slug;
    }

    // CRITICAL: Email sending configuration
    // Regular blog posts: sendEmailWhenPublished = false (NO EMAIL)
    // Weekly digests: sendEmailWhenPublished = true + emailOnly = true (EMAIL ONLY)
    postData.send_email_when_published = sendEmailWhenPublished;

    if (emailOnly) {
      postData.email_only = true;
    }

    // CRITICAL: Newsletter association (required for email sends)
    // Ghost needs to know WHICH newsletter to send to
    // Use newsletter slug directly as Ghost v5 expects
    if (sendEmailWhenPublished && newsletter) {
      postData.newsletter = newsletter;
    }

    if (publishedAt) {
      postData.published_at = publishedAt;
    }

    // CRITICAL: Email newsletter posts require TWO-STEP process
    // Ghost API requires: 1) Create as draft  2) Edit to publish with newsletter query param
    // See: https://forum.ghost.org/t/create-post-and-send-via-email-using-admin-api/35529

    let finalPost;

    if (sendEmailWhenPublished && newsletter) {
      // Step 1: Create as DRAFT first (remove status from postData)
      const draftData = { ...postData };
      delete draftData.status;
      delete draftData.published_at;
      delete draftData.send_email_when_published;

      const draftPost = await ghostAdmin.posts.add(
        draftData,
        contentType === 'markdown' || contentType === 'html'
          ? { source: 'html' }
          : undefined
      );

      // Step 2: Edit to schedule/publish with newsletter query param
      const editData: any = {
        id: draftPost.id,
        updated_at: draftPost.updated_at,
        status: status,
        email_only: emailOnly
      };

      if (publishedAt) {
        editData.published_at = publishedAt;
      }

      finalPost = await ghostAdmin.posts.edit(
        editData,
        {
          source: 'html',
          newsletter: newsletter,      // Query param for newsletter
          email_segment: 'all'         // Send to all subscribers
        }
      );
    } else {
      // Regular post (no email) - single-step creation
      finalPost = await ghostAdmin.posts.add(
        postData,
        contentType === 'markdown' || contentType === 'html'
          ? { source: 'html' }
          : undefined
      );
    }

    // Build editor URL for drafts
    const editorUrl = finalPost.status === 'draft'
      ? `${GHOST_API_URL}/ghost/#/editor/post/${finalPost.id}`
      : finalPost.url || `${GHOST_API_URL}/${finalPost.slug}/`;

    return {
      success: true,
      post: {
        id: finalPost.id!,
        title: finalPost.title,
        slug: finalPost.slug!,
        status: finalPost.status!,
        url: finalPost.url || `${GHOST_API_URL}/${finalPost.slug}/`,
        editorUrl
      }
    };

  } catch (error: any) {
    // Extract meaningful error message from Ghost API error
    const errorMessage = error.message || 'Unknown error creating post';
    const errorDetails = error.errors || error.context || null;

    return {
      success: false,
      error: errorMessage,
      details: errorDetails
    };
  }
}

/**
 * Upload image to Ghost with optional alt-text
 *
 * Uploads an image file to Ghost's image store and returns the URL.
 * Use this for hero images before creating posts.
 *
 * NOTE: Ghost Admin API doesn't support alt-text in upload endpoint.
 * Alt-text must be set separately via post update with feature_image_alt field.
 *
 * @param imagePath - Local file path to image
 * @param altText - Optional alt-text (set via post update, not upload)
 * @returns Image URL on Ghost CDN or error
 *
 * @example
 * ```typescript
 * const result = await uploadImage('/path/to/hero-image.png', 'Cyberpunk anime illustration');
 * if (result.success) {
 *   // Use in createPost with alt-text
 *   await createPost({
 *     title: "My Post",
 *     content: "...",
 *     featureImage: result.imageUrl,
 *     featureImageAlt: result.altText
 *   });
 * }
 * ```
 */
export async function uploadImage(
  imagePath: string,
  altText?: string
): Promise<{
  success: boolean;
  imageUrl?: string;
  altText?: string;
  error?: string;
}> {
  try {
    const file = Bun.file(imagePath);

    if (!await file.exists()) {
      return {
        success: false,
        error: `Image file not found: ${imagePath}`
      };
    }

    // Upload to Ghost (API doesn't accept alt-text in upload)
    const result = await ghostAdmin.images.upload({ file: imagePath });

    return {
      success: true,
      imageUrl: result.url,
      altText // Return for use in post update
    };

  } catch (error: any) {
    return {
      success: false,
      error: error.message || 'Unknown error uploading image'
    };
  }
}

/**
 * Fetch existing posts (for reference/research)
 *
 * @param limit - Maximum number of posts to retrieve
 * @param status - Filter by status (draft, published, all)
 * @returns Array of posts
 */
export async function fetchPosts(
  limit: number = 15,
  status?: 'draft' | 'published'
): Promise<GhostPost[]> {
  try {
    const options: any = {
      limit,
      include: 'tags',
      order: 'created_at DESC'
    };

    if (status) {
      options.filter = `status:${status}`;
    }

    const posts = await ghostAdmin.posts.browse(options);
    return posts;

  } catch (error) {
    console.error('Error fetching posts:', error);
    return [];
  }
}

/**
 * Delete existing post
 *
 * @param postId - Ghost post ID
 * @returns Result object
 */
export async function deletePost(postId: string): Promise<{
  success: boolean;
  error?: string;
}> {
  try {
    await ghostAdmin.posts.delete({ id: postId });

    return {
      success: true
    };

  } catch (error: any) {
    return {
      success: false,
      error: error.message || 'Unknown error deleting post'
    };
  }
}

/**
 * Update existing post
 *
 * @param postId - Ghost post ID
 * @param updates - Fields to update
 * @returns Result object
 */
export async function updatePost(
  postId: string,
  updates: Partial<CreatePostOptions>
): Promise<CreatePostResult> {
  try {
    // CRITICAL: Fetch current post to get updated_at timestamp
    // Ghost requires this for update validation
    const currentPost = await ghostAdmin.posts.read({ id: postId });

    const postData: any = {
      id: postId,
      updated_at: currentPost.updated_at // Required by Ghost API
    };

    // Handle content updates
    if (updates.content) {
      const contentType = updates.contentType || 'markdown';

      if (contentType === 'markdown') {
        postData.html = markdownToHtml(updates.content);
      } else if (contentType === 'html') {
        postData.html = updates.content;
      } else if (contentType === 'lexical') {
        postData.lexical = updates.content;
      }
    }

    // Add other updates
    if (updates.title) postData.title = updates.title;
    if (updates.status) postData.status = updates.status;
    if (updates.visibility) postData.visibility = updates.visibility;
    if (updates.featureImage) postData.feature_image = updates.featureImage;
    if (updates.featureImageAlt) postData.feature_image_alt = updates.featureImageAlt;
    if (updates.tags) postData.tags = updates.tags.map(tag => ({ name: tag }));
    if (updates.excerpt) postData.custom_excerpt = updates.excerpt;

    // Email configuration (only if explicitly set)
    if (updates.sendEmailWhenPublished !== undefined) {
      postData.send_email_when_published = updates.sendEmailWhenPublished;
    }
    if (updates.emailOnly !== undefined) {
      postData.email_only = updates.emailOnly;
    }
    if (updates.publishedAt) {
      postData.published_at = updates.publishedAt;
    }

    // Update post
    const updatedPost = await ghostAdmin.posts.edit(
      postData,
      updates.content ? { source: 'html' } : undefined
    );

    const editorUrl = updatedPost.status === 'draft'
      ? `${GHOST_API_URL}/ghost/#/editor/post/${updatedPost.id}`
      : updatedPost.url || `${GHOST_API_URL}/${updatedPost.slug}/`;

    return {
      success: true,
      post: {
        id: updatedPost.id!,
        title: updatedPost.title,
        slug: updatedPost.slug!,
        status: updatedPost.status!,
        url: updatedPost.url || `${GHOST_API_URL}/${updatedPost.slug}/`,
        editorUrl
      }
    };

  } catch (error: any) {
    // Log full error for debugging
    console.error('Ghost API Error:', JSON.stringify(error, null, 2));
    console.error('Post data sent:', JSON.stringify(postData, null, 2));

    return {
      success: false,
      error: error.message || 'Unknown error updating post',
      details: error.errors || error.context || null
    };
  }
}

export default {
  createPost,
  uploadImage,
  fetchPosts,
  updatePost,
  deletePost,
  markdownToHtml
};
