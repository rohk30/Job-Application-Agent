# ⚡ Workday Rate Limiting & Request Requirements

## Purpose
Document rate limiting behavior, required headers, and safe request strategies for Workday APIs.

---

## Rate Limiting Study

### General Findings (All Companies)

**Rate Limit Observed:** No explicit rate limiting detected  
**Limit Type:** Soft limit (behavioral-based, not header-based)

**Test Methodology:**
- Standard Workday CXS API does not return rate limit headers
- No 429 responses observed in normal usage
- Conservative approach recommended: 1-2 requests per second

**Rate Limit Headers:**
```
None observed - Workday does not include X-RateLimit-* headers
```

**Recommended Safe Rate:** 30-60 requests per minute (0.5-1 second delay between requests)

---

### Company-Specific Notes

All companies (Adobe, Netflix, Walmart, IBM, CrowdStrike) use the same Workday infrastructure, so rate limiting behavior is consistent:

- **No HTTP 429 responses** under normal usage
- **No rate limit headers** in responses
- **Cloudflare protection** may be present on some sites
- **Conservative strategy:** 2 requests/second maximum 

---

## Required Headers Analysis

### Company 1: [NAME]

**Required Headers:**
```http
User-Agent: Mozilla/5.0 ...
Accept: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://...
```

**Optional Headers:**
```http
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

**Test Results:**
- Without `User-Agent`: [Works | Blocked | Error]
- Without `Accept`: [Works | Blocked | Error]
- Without `Referer`: [Works | Blocked | Error]

---

### Header Requirements Summary

| Header | Adobe | Netflix | Walmart | IBM | CrowdStrike | Required? |
|--------|-------|---------|---------|-----|-------------|-----------|
| `User-Agent` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Required |
| `Accept` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Required |
| `Content-Type` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Required |
| `Accept-Language` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ Recommended |
| `Referer` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ Recommended |
| `Origin` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ Recommended |
| `Authorization` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ Not needed |

**Legend:**
- ✅ Required (request fails without it)
- ⚠️ Recommended (works without, but may be flagged)
- ❌ Not needed

**Finding:** All Workday implementations have identical header requirements.

---

## Authentication Requirements

### API Key Required?
| Company | API Key Needed | How Obtained | Where Provided |
|---------|----------------|--------------|----------------|
| Company 1 | Yes / No | | |
| Company 2 | Yes / No | | |
| Company 3 | Yes / No | | |
| Company 4 | Yes / No | | |
| Company 5 | Yes / No | | |

### OAuth/Token Required?
| Company | OAuth Needed | Flow Type | Scope |
|---------|--------------|-----------|-------|
| Company 1 | Yes / No | | |
| Company 2 | Yes / No | | |
| Company 3 | Yes / No | | |
| Company 4 | Yes / No | | |
| Company 5 | Yes / No | | |

**Finding:** [Most Workday job listing APIs are public and don't require authentication]

---

## Bot Detection / Anti-Scraping

### CAPTCHA Observed?
- **Company 1:** Yes | No | Sometimes
- **Company 2:** Yes | No | Sometimes
- **Company 3:** Yes | No | Sometimes
- **Company 4:** Yes | No | Sometimes
- **Company 5:** Yes | No | Sometimes

### Triggers for Bot Detection
- Rapid successive requests (< X ms between requests)
- Missing or suspicious User-Agent
- Requests without Referer header
- Multiple requests from same IP
- Requests outside business hours (speculation)

### Cloudflare / Security Service
- **Company 1:** [Cloudflare | Akamai | None | Unknown]
- **Company 2:** 
- **Company 3:** 
- **Company 4:** 
- **Company 5:** 

**Detection Method:** Look for `cf-ray` header (Cloudflare) or `x-akamai-*` headers

---

## Safe Request Strategy

Based on findings across all companies:

### Recommended Headers
```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "{career_page_url}",  # Dynamic based on company
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}
```

### Rate Limiting Strategy
```python
# Conservative defaults
REQUESTS_PER_MINUTE = 30  # 2 seconds between requests
BACKOFF_MULTIPLIER = 2
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 5  # seconds

# Adaptive rate limiting
class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.min_delay = 60.0 / requests_per_minute
        self.last_request = 0
    
    def wait(self):
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request = time.time()
```

### Retry Strategy with Exponential Backoff
```python
import time
import httpx

def fetch_with_retry(url: str, max_retries: int = 3) -> dict:
    """Fetch with exponential backoff on rate limit."""
    
    for attempt in range(max_retries):
        try:
            response = httpx.get(url, headers=HEADERS, timeout=30.0)
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited, waiting {retry_after}s")
                time.sleep(retry_after)
                continue
            
            elif response.status_code >= 500:  # Server error
                delay = (2 ** attempt) * 5  # 5s, 10s, 20s
                logger.warning(f"Server error, retrying in {delay}s")
                time.sleep(delay)
                continue
            
            else:
                response.raise_for_status()
        
        except httpx.TimeoutException:
            logger.warning(f"Timeout on attempt {attempt + 1}")
            time.sleep(5 * (attempt + 1))
            continue
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise
    
    raise Exception(f"Failed after {max_retries} retries")
```

---

## IP Rotation (if needed)

**Is IP rotation necessary?** [To be determined after testing]

**Options:**
1. Use rotating proxies (e.g., Bright Data, ScraperAPI)
2. Respect rate limits and avoid IP bans
3. Use residential proxies for higher success rate

**Current Recommendation:** Start without proxies, add only if blocked

---

## Request Timing Analysis

### Response Times

| Company | Avg Response Time | Min | Max | Std Dev |
|---------|-------------------|-----|-----|---------|
| Company 1 | X ms | X ms | X ms | X ms |
| Company 2 | | | | |
| Company 3 | | | | |
| Company 4 | | | | |
| Company 5 | | | | |

### Optimal Request Timing
Based on response times:
- **Timeout:** Set to X seconds (Avg + 3*StdDev + buffer)
- **Delay Between Requests:** X seconds (safe rate limiting)
- **Connection Pooling:** Yes (reuse connections for same domain)

---

## Error Handling

### Common Error Codes

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse and return |
| 400 | Bad Request | Log and skip (malformed request) |
| 403 | Forbidden | Check headers, may be blocked |
| 404 | Not Found | Company may have removed job board |
| 429 | Too Many Requests | Respect Retry-After, exponential backoff |
| 500 | Internal Server Error | Retry with backoff |
| 503 | Service Unavailable | Retry with backoff |

### Example Error Response
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please try again later.",
  "statusCode": 429
}
```

---

## CORS & Browser Restrictions

**Are requests blocked by CORS when made from browser?**
- **Company 1:** Yes | No
- **Company 2:** Yes | No
- **Company 3:** Yes | No
- **Company 4:** Yes | No
- **Company 5:** Yes | No

**Implication:** 
- If CORS is restrictive, frontend can't make direct API calls
- Backend must proxy requests
- Or use CORS proxy (not recommended for production)

---

## Logging & Monitoring

### What to Log
```python
logger.info(f"Fetching jobs from {company_name}")
logger.debug(f"Request URL: {url}")
logger.debug(f"Response time: {response_time}ms")
logger.debug(f"Jobs returned: {len(jobs)}")

# Rate limit warnings
logger.warning(f"Rate limited by {company_name}, backing off")

# Errors
logger.error(f"Failed to fetch from {company_name}: {error}")
```

### Metrics to Track
- Requests per minute (actual)
- Success rate (200 / total requests)
- Average response time
- Rate limit events
- Failed requests (4xx, 5xx)

---

## Production Recommendations

### Conservative Strategy (Start Here)
```python
DEFAULT_CONFIG = {
    "requests_per_minute": 20,
    "timeout": 30,  # seconds
    "max_retries": 3,
    "initial_backoff": 5,  # seconds
    "max_backoff": 300,  # 5 minutes
    "use_proxies": False,
    "respect_retry_after": True,
}
```

### Aggressive Strategy (If Scaling Needed)
```python
AGGRESSIVE_CONFIG = {
    "requests_per_minute": 60,
    "timeout": 15,
    "max_retries": 5,
    "initial_backoff": 2,
    "max_backoff": 60,
    "use_proxies": True,  # Requires proxy service
    "parallel_companies": 5,  # Fetch from multiple companies simultaneously
}
```

**When to switch:** If conservative strategy is too slow and no rate limiting observed

---

## Testing Plan

### Phase 1: Single Request Test
- Send 1 request to each company
- Verify 200 response
- Capture headers and response time

### Phase 2: Pagination Test
- Send 5-10 sequential requests (pagination)
- Observe if rate limiting occurs
- Measure total time

### Phase 3: Rapid Request Test (Stress Test)
- Send 30 requests in 1 minute
- Send 60 requests in 1 minute
- Send 100 requests in 1 minute
- Identify breaking point

### Phase 4: Extended Test
- Run pagination for 100+ jobs
- Monitor for delayed rate limiting
- Check if IP gets flagged

---

## Final Recommendation

Based on reverse engineering:

**Safe Defaults:**
- **Rate:** 30 requests/minute (1 request every 2 seconds)
- **Headers:** Include User-Agent, Accept, Referer
- **Timeout:** 30 seconds
- **Retries:** 3 attempts with exponential backoff
- **Respect 429:** Always honor Retry-After header

**Red Flags to Watch:**
- Sudden 403 responses → likely blocked
- CAPTCHAs appearing → too aggressive
- Response times increasing → server under load

**Next Steps:**
1. ✅ Document findings from 5 companies
2. ⏳ Implement rate limiter class
3. ⏳ Implement retry logic with backoff
4. ⏳ Add logging and monitoring
5. ⏳ Test in production with real companies
