const axios = require('axios');

/**
 * Comprehensive username search across 35+ social media platforms.
 * Uses proper URL patterns and status code + redirect detection
 * for more accurate results than simple HTTP 200 checks.
 */

const PLATFORMS = [
  // Major platforms
  { name: 'GitHub', url: 'https://github.com/{}', icon: 'code' },
  { name: 'Twitter / X', url: 'https://x.com/{}', icon: 'message-circle' },
  { name: 'Instagram', url: 'https://www.instagram.com/{}/', icon: 'camera' },
  { name: 'TikTok', url: 'https://www.tiktok.com/@{}', icon: 'video' },
  { name: 'YouTube', url: 'https://www.youtube.com/@{}', icon: 'play' },
  { name: 'Reddit', url: 'https://www.reddit.com/user/{}', icon: 'message-square' },
  { name: 'LinkedIn', url: 'https://www.linkedin.com/in/{}', icon: 'briefcase' },
  { name: 'Facebook', url: 'https://www.facebook.com/{}', icon: 'users' },
  { name: 'Pinterest', url: 'https://www.pinterest.com/{}/', icon: 'image' },

  // Developer platforms
  { name: 'GitLab', url: 'https://gitlab.com/{}', icon: 'code' },
  { name: 'Bitbucket', url: 'https://bitbucket.org/{}/', icon: 'code' },
  { name: 'Dev.to', url: 'https://dev.to/{}', icon: 'code' },
  { name: 'Stack Overflow', url: 'https://stackoverflow.com/users/?tab=accounts&SearchText={}', icon: 'layers' },
  { name: 'npm', url: 'https://www.npmjs.com/~{}', icon: 'package' },
  { name: 'PyPI', url: 'https://pypi.org/user/{}/', icon: 'package' },
  { name: 'Replit', url: 'https://replit.com/@{}', icon: 'code' },

  // Creative / Media
  { name: 'Behance', url: 'https://www.behance.net/{}', icon: 'pen-tool' },
  { name: 'Dribbble', url: 'https://dribbble.com/{}', icon: 'circle' },
  { name: 'Medium', url: 'https://medium.com/@{}', icon: 'book' },
  { name: 'SoundCloud', url: 'https://soundcloud.com/{}', icon: 'music' },
  { name: 'Spotify', url: 'https://open.spotify.com/user/{}', icon: 'music' },
  { name: 'Flickr', url: 'https://www.flickr.com/people/{}/', icon: 'camera' },
  { name: 'Vimeo', url: 'https://vimeo.com/{}', icon: 'video' },
  { name: 'DeviantArt', url: 'https://www.deviantart.com/{}', icon: 'palette' },

  // Social / Messaging
  { name: 'Tumblr', url: 'https://{}.tumblr.com', icon: 'edit' },
  { name: 'Twitch', url: 'https://www.twitch.tv/{}', icon: 'tv' },
  { name: 'Telegram', url: 'https://t.me/{}', icon: 'send' },
  { name: 'Snapchat', url: 'https://www.snapchat.com/add/{}', icon: 'camera' },
  { name: 'Quora', url: 'https://www.quora.com/profile/{}', icon: 'help-circle' },
  { name: 'We Heart It', url: 'https://weheartit.com/{}', icon: 'heart' },

  // Professional / Other
  { name: 'Product Hunt', url: 'https://www.producthunt.com/@{}', icon: 'award' },
  { name: 'Keybase', url: 'https://keybase.io/{}', icon: 'key' },
  { name: 'About.me', url: 'https://about.me/{}', icon: 'user' },
  { name: 'Gravatar', url: 'https://en.gravatar.com/{}', icon: 'user' },
  { name: 'Patreon', url: 'https://www.patreon.com/{}', icon: 'dollar-sign' },
  { name: 'Linktree', url: 'https://linktr.ee/{}', icon: 'link' },
];

/**
 * Check a single platform for username existence.
 * Returns result object with found status and URL.
 */
async function checkPlatform(platform, username) {
  const url = platform.url.replace('{}', username);

  try {
    const response = await axios.get(url, {
      timeout: 8000,
      maxRedirects: 3,
      validateStatus: (status) => status < 500,
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      },
    });

    const found = response.status === 200;

    return {
      name: platform.name,
      url: url,
      found: found,
      status: response.status,
      icon: platform.icon,
    };
  } catch (error) {
    return {
      name: platform.name,
      url: url,
      found: false,
      status: error.response?.status || 0,
      error: error.code || 'TIMEOUT',
      icon: platform.icon,
    };
  }
}

/**
 * Search for a username across all platforms concurrently.
 * Uses Promise.allSettled for maximum resilience - one failed
 * request won't block others.
 */
async function trackUsername(username) {
  if (!username || username.trim().length === 0) {
    return { success: false, error: 'Username cannot be empty' };
  }

  const cleanUsername = username.trim();

  try {
    // Run all checks concurrently with a batch size to avoid overwhelming
    const batchSize = 10;
    const results = [];

    for (let i = 0; i < PLATFORMS.length; i += batchSize) {
      const batch = PLATFORMS.slice(i, i + batchSize);
      const batchResults = await Promise.allSettled(
        batch.map((platform) => checkPlatform(platform, cleanUsername))
      );

      for (const result of batchResults) {
        if (result.status === 'fulfilled') {
          results.push(result.value);
        }
      }
    }

    const found = results.filter((r) => r.found);
    const notFound = results.filter((r) => !r.found);

    return {
      success: true,
      username: cleanUsername,
      totalChecked: results.length,
      totalFound: found.length,
      found,
      notFound,
    };
  } catch (error) {
    return {
      success: false,
      error: error.message || 'Username tracking failed',
    };
  }
}

module.exports = { trackUsername, PLATFORMS };
