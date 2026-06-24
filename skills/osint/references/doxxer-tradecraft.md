# Doxxer Tradecraft — Advanced OSINT Techniques

> Reference for the /osint skill. Techniques used by professional OSINT investigators
> and (unfortunately) doxxers. Use for legitimate investigation only.

---

## Identity Resolution Techniques

### 1. Avatar Hash Matching

People reuse profile pictures across platforms. Download avatars, compute perceptual hashes,
search for matches.

**Tools:**
```bash
# Download avatar from GitHub
curl -o avatar_gh.jpg "https://github.com/{user}.png?size=400"

# Download avatar from Twitter/X
# Use gallery-dl or snscrape

# Compute perceptual hash (Python)
pip install imagehash Pillow
python3 -c "
from PIL import Image
import imagehash
h = imagehash.phash(Image.open('avatar_gh.jpg'))
print(h)
# Search for this hash across other downloaded avatars
"
```

**Technique:**
1. Download avatar from known account
2. Compute pHash (perceptual hash) — tolerant of resizing, compression
3. Download avatars from suspected accounts on other platforms
4. Compare hashes — distance < 10 = likely same image = likely same person
5. Also check reverse image search (Google Images, TinEye, Yandex)

### 2. Writing Style Analysis (Stylometry)

People have consistent writing patterns across platforms.

**Indicators to compare:**
- Vocabulary complexity and word choice
- Punctuation habits (Oxford comma, exclamation marks, ellipsis usage)
- Emoji usage patterns (which emojis, how often, placement)
- Capitalization patterns (ALL CAPS for emphasis? Title Case?)
- Sentence length distribution
- Common misspellings or typos
- Slang and colloquialisms
- Paragraph structure (short paragraphs? walls of text?)
- Greeting and sign-off patterns

**Tools:**
```bash
# Compare two text samples
# Use Python's nltk or just manual comparison
# Key: same unusual patterns across platforms = same person
```

### 3. Timezone Inference

Map activity timestamps to infer timezone.

**Best sources:**
- **GitHub commits** — developers commit during waking hours (9am-11pm local time)
- **Reddit posts** — posting patterns follow sleep/wake cycle
- **Twitter/X tweets** — activity distribution across hours
- **Steam activity** — gaming patterns (evenings, weekends)
- **Forum posts** — timestamps on posts

**Technique:**
1. Collect 50+ timestamps from a single platform
2. Plot activity by UTC hour
3. The "dead zone" (no activity) = sleeping hours
4. Center of dead zone = ~3-4am local time
5. Offset from UTC = timezone

```python
# Example: GitHub commit times
from collections import Counter
import json

# Load commits
commits = [...]  # from GitHub API
hours = [c['commit']['author']['date'][11:13] for c in commits]
hour_counts = Counter(hours)

# Dead zone = hours with 0 or near-0 activity
# Center of activity = waking hours
```

### 4. Username Archaeology

Old usernames persist in caches even after changes.

**Sources:**
- **Wayback Machine** — `web.archive.org/web/*/twitter.com/{old_username}`
- **Google Cache** — `cache:{url}`
- **Reddit** — deleted posts still indexed by pushshift.io
- **GitHub** — renamed accounts still appear in fork URLs, old issues
- **Archive.today** — snapshots of pages at specific times
- **Cached search results** — Google, Bing cache old pages

**Technique:**
1. Search for the target's current username on archive.org
2. Check if the page shows a different username (account was renamed)
3. Search for the old username on other platforms
4. Repeat — usernames chain like commits

### 5. Email Pattern Analysis

Company emails follow predictable formats.

**Common patterns:**
| Format | Example |
|--------|---------|
| `first.last` | `john.smith@company.com` |
| `flast` | `jsmith@company.com` |
| `firstl` | `johns@company.com` |
| `first_last` | `john_smith@company.com` |
| `first-last` | `john-smith@company.com` |
| `last.first` | `smith.john@company.com` |
| `first` | `john@company.com` (small companies) |

**Technique:**
1. Find ONE employee email (from Hunter.io, GitHub, LinkedIn, company website)
2. Determine the format (e.g., `first.last@company.com`)
3. Find employee names (LinkedIn, company website, press releases)
4. Generate emails for all employees using the discovered format
5. Verify with email validation tools

**Tools:**
```bash
# Hunter.io — finds email format + employees
curl "https://api.hunter.io/v2/domain-search?domain=company.com&api_key=KEY"

# Email format detection
curl "https://api.hunter.io/v2/email-finder?domain=company.com&first_name=John&last_name=Smith&api_key=KEY"
```

### 6. Registration Order Analysis

The order in which accounts were created reveals the person's "home" platform.

**Indicators:**
- GitHub account created 2015, Twitter 2018 → developer first, social later
- Instagram 2012, GitHub 2020 → social first, developer later
- Same username registered earliest on one platform = likely their primary identity

**Sources for creation dates:**
- GitHub: `created_at` field in API
- Reddit: `created_utc` field in API
- Twitter: profile page shows "Joined Month Year"
- Most platforms: check profile page or API

### 7. Cross-Platform Bio Correlation

People copy-paste bios. Exact matches = same person.

**Technique:**
1. Extract bio text from known account
2. Search for exact phrases in quotes on Google
3. Check if the same bio appears on other platforms
4. Even partial matches (same phrase, same emoji pattern) are strong signals

**Example:**
```
GitHub bio: "I AM GOOD AT EDIT"
Google: "I AM GOOD AT EDIT" site:youtube.com
→ Finds YouTube channel with same bio = same person
```

### 8. Network/Association Analysis

Map social connections to confirm identity.

**Technique:**
1. On platform A, find who the target follows / is followed by
2. On suspected platform B, check if the same people appear in their network
3. Overlapping social circles = strong identity confirmation

**Particularly powerful on:**
- Twitter/X (following lists are public)
- GitHub (followers/following are public)
- Instagram (followers can be visible)
- LinkedIn (connections, though limited visibility)

### 9. Metadata Extraction

Files contain hidden data.

**EXIF from photos:**
```bash
exiftool -gps:all photo.jpg        # GPS coordinates
exiftool -camera:* photo.jpg       # Camera model
exiftool -datetime:* photo.jpg     # When it was taken
exiftool -artist:* photo.jpg       # Who took it
```

**Document metadata:**
```bash
# PDF author, creation tool, edit history
exiftool document.pdf

# Office documents — author name, company, revision history
exiftool document.docx
```

**Git repository metadata:**
```bash
# .git/config contains user info
# commit history contains author/committer emails
git log --format='%an <%ae>' | sort -u
```

### 10. Google Dorking for People

```bash
# Find someone's LinkedIn
site:linkedin.com/in "John Smith" "Company Name"

# Find someone's resume/CV
"John Smith" filetype:pdf resume OR cv

# Find someone's social media
"John Smith" site:twitter.com OR site:instagram.com OR site:facebook.com

# Find someone's forum posts
"John Smith" site:reddit.com OR site:stackoverflow.com

# Find someone's code
"John Smith" site:github.com

# Find leaked data
"john.smith@company.com" site:pastebin.com OR site:gist.github.com

# Find phone number association
"+1234567890" site:facebook.com OR site:linkedin.com

# Find address association
"123 Main Street" "John Smith"
```

---

## Advanced Techniques

### Username Similarity Scoring

When you find multiple usernames that are similar, they're likely the same person.

**Similarity metrics:**
- Levenshtein distance < 3
- Same base word with different number suffixes
- Same base word with different separators
- Leet speak variants (a→4, e→3, i→1, o→0, s→5)
- Case variations only

### Email-to-Username Pipeline

```
email: john.doe@gmail.com
  ↓
username variants: ["johndoe", "john.doe", "john_doe", "johndoe1", "doejohn"]
  ↓
search each variant across 50+ platforms
  ↓
for each confirmed account, extract more identifiers
  ↓
recurse
```

### Platform-Specific Intelligence

| Platform | Unique Intelligence |
|----------|-------------------|
| **GitHub** | Commit emails, real name, location, company, languages, projects, co-authors |
| **Reddit** | Comment history (interests, opinions, writing style), subreddit subscriptions |
| **Steam** | Game library, playtime, friends list, real name (sometimes) |
| **LinkedIn** | Employment history, education, skills, endorsements, connections |
| **Twitter/X** | Follower graph, tweet history, retweets (interests), location (sometimes) |
| **Instagram** | Photos (faces, locations, lifestyle), follower graph, tagged photos |
| **SoundCloud** | Music taste, possibly own music, location |
| **Pinterest** | Interests, aesthetic preferences, saved content |
| **Strava** | Running/cycling routes (GPS!), fitness level, real name |
| **Keybase** | Verified identities across platforms, crypto keys |
| **Gravatar** | Email hash → profile photo, name, links |

### The Gravatar Hash Trick

Gravatar uses MD5 hashes of email addresses. If you know someone's email, you can check if they have a Gravatar:

```python
import hashlib
email = "john@example.com"
hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
url = f"https://www.gravatar.com/avatar/{hash}?d=404"
# If 200 → Gravatar exists, profile photo available
# If 404 → No Gravatar
```

This also works in reverse — if you find a Gravatar hash, you can try to crack it with common email patterns.

### Steam Profile Intelligence

Steam profiles can reveal:
- Real name (if set to public)
- Location (country, sometimes city)
- Game library (interests)
- Playtime patterns (timezone, work schedule)
- Friends list (social graph)
- Profile comments (social interactions)
- Custom URL (often matches username on other platforms)

```bash
# Steam API (if you have the Steam ID)
curl "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=KEY&steamids=ID"
```

---

## Ethical Considerations

This document exists to teach defensive OSINT — understanding how attackers operate so you can protect yourself. Use these techniques:

- **For legitimate security research**
- **To audit your own digital footprint**
- **To protect your organization's employees**
- **For authorized penetration testing**

Do NOT use these techniques for:
- Harassment or stalking
- Doxxing (releasing private information publicly)
- Identity theft
- Extortion
- Any illegal activity

---

## Self-Protection

Understanding these techniques also teaches you how to protect yourself:

1. **Use different usernames** on different platforms
2. **Use different email addresses** for different purposes
3. **Strip EXIF data** from photos before uploading
4. **Don't reuse profile pictures** across platforms
5. **Use a VPN** to hide your IP address
6. **Be careful what you commit** to public repositories
7. **Review your privacy settings** on every platform
8. **Google yourself** regularly to see what's exposed
9. **Use unique, complex passwords** (check HIBP regularly)
10. **Minimize your digital footprint** — less data = less attack surface
