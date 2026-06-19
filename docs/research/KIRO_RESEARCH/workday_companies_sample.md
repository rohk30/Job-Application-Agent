# 🏢 Workday Companies Sample

## Purpose
Sample of companies using Workday for career pages, used for reverse engineering API patterns.

---

## Company List

### Company 1: Adobe
- **Company Name:** Adobe Inc.
- **Career Page:** https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced
- **Workday Base URL:** https://adobe.wd5.myworkdayjobs.com
- **Workday Tenant:** wd5
- **Site ID:** External_Experienced
- **Date Tested:** April 2025
- **Notes:** 1131 jobs found. Uses standard Workday format with job listings visible on page load.

---

### Company 2: Netflix
- **Company Name:** Netflix Inc.
- **Career Page:** https://netflix.wd1.myworkdayjobs.com/en-US/Netflix
- **Workday Base URL:** https://netflix.wd1.myworkdayjobs.com
- **Workday Tenant:** wd1
- **Site ID:** Netflix
- **Date Tested:** April 2025
- **Notes:** Uses wd1 tenant (different from Adobe's wd5)

---

### Company 3: Walmart
- **Company Name:** Walmart Inc.
- **Career Page:** https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal
- **Workday Base URL:** https://walmart.wd5.myworkdayjobs.com
- **Workday Tenant:** wd5
- **Site ID:** WalmartExternal
- **Date Tested:** April 2025
- **Notes:** Large retail company, likely has many job postings

---

### Company 4: IBM
- **Company Name:** IBM Corporation
- **Career Page:** https://ibm.wd3.myworkdayjobs.com/en-US/IBM
- **Workday Base URL:** https://ibm.wd3.myworkdayjobs.com
- **Workday Tenant:** wd3
- **Site ID:** IBM
- **Date Tested:** April 2025
- **Notes:** Uses wd3 tenant, enterprise tech company

---

### Company 5: CrowdStrike
- **Company Name:** CrowdStrike Holdings Inc.
- **Career Page:** https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers
- **Workday Base URL:** https://crowdstrike.wd5.myworkdayjobs.com
- **Workday Tenant:** wd5
- **Site ID:** crowdstrikecareers
- **Date Tested:** April 2025
- **Notes:** Cybersecurity company, uses wd5 tenant

---

### Company 6: ServiceTitan
- **Company Name:** ServiceTitan Inc.
- **Career Page:** https://servicetitan.wd1.myworkdayjobs.com/en-US/ServiceTitan
- **Workday Base URL:** https://servicetitan.wd1.myworkdayjobs.com
- **Workday Tenant:** wd1
- **Site ID:** ServiceTitan
- **Date Tested:** April 2025
- **Notes:** SaaS company for home services

---

### Company 7: Philips
- **Company Name:** Philips N.V.
- **Career Page:** https://philips.wd3.myworkdayjobs.com/en-US/jobs-and-careers
- **Workday Base URL:** https://philips.wd3.myworkdayjobs.com
- **Workday Tenant:** wd3
- **Site ID:** jobs-and-careers
- **Date Tested:** April 2025
- **Notes:** Healthcare technology company, uses wd3 tenant

---

### Company 8: Kyndryl (Optional)
- **Company Name:** Kyndryl Holdings Inc.
- **Career Page:** https://kyndryl.wd5.myworkdayjobs.com/en-US/KyndrylProfessionalCareers
- **Workday Base URL:** https://kyndryl.wd5.myworkdayjobs.com
- **Workday Tenant:** wd5
- **Site ID:** KyndrylProfessionalCareers
- **Date Tested:** April 2025
- **Notes:** IT infrastructure services, spun off from IBM 

---

## Selection Criteria

Choose companies with:
- ✅ Diverse industries (tech, finance, retail, healthcare, etc.)
- ✅ Different company sizes (startup, mid-size, enterprise)
- ✅ Geographic diversity (US, Europe, Asia if possible)
- ✅ Active job postings (not empty boards)

---

## How to Identify Workday

**Indicators a site uses Workday:**
1. URL pattern contains `myworkdayjobs.com`
2. Career page has Workday branding/footer
3. Network requests go to `*.myworkdayjobs.com`
4. Page source mentions "Workday" or has Workday scripts

**Quick Test:**
Visit career page → Inspect → Network tab → Search for "workday" in domain names

---

## Known Workday Companies (Reference)

Examples to get started:
- Netflix
- Walmart
- Target
- Adobe
- IBM
- Salesforce
- Spotify
- Goldman Sachs
- Morgan Stanley
- Accenture

**Note:** Verify they still use Workday before testing.
