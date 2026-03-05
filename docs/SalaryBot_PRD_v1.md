💬

**SalaryBot**

Explain My Salary Slip --- WhatsApp AI Bot

Product Requirements Document • v1.0

  ----------------------- -----------------------------------------------
  **Product Name**        SalaryBot

  **Version**             1.0 --- Initial Release

  **Date**                March 2026

  **Author**              Founder / Product Lead

  **Status**              Draft --- Ready for Development

  **Target Launch**       Month 2 (6-week build)
  ----------------------- -----------------------------------------------

**1. Executive Summary**

SalaryBot is a WhatsApp-first AI assistant that lets any salaried Indian
photograph their salary slip and receive an instant, plain-language
explanation of every deduction --- in Hindi or English --- within 60
seconds.

+-----------------------------------------------------------------------+
| **The Core Problem**                                                  |
|                                                                       |
| India has 500M+ salaried workers. Every month they receive a salary   |
| slip they cannot fully understand. PF, ESI, TDS, HRA, Professional    |
| Tax --- most employees accept these deductions without knowing if     |
| they are correct. There is no easy, accessible tool to explain this   |
| in plain language. The result: employees lose money silently every    |
| month.                                                                |
+-----------------------------------------------------------------------+

SalaryBot solves this with zero app download friction --- just WhatsApp,
a photo, and 60 seconds.

**2. Product Vision & Goals**

**2.1 Vision Statement**

+-----------------------------------------------------------------------+
| **Vision**                                                            |
|                                                                       |
| Every salaried Indian should understand exactly what they earn, what  |
| is deducted, and why --- in their own language, in under a minute.    |
+-----------------------------------------------------------------------+

**2.2 Success Metrics --- Month 6**

  -------------------------- ------------------ -------------------------
  **Metric**                 **Target**         **Why It Matters**

  WhatsApp Bot Users         50,000+            Core user acquisition
                                                goal

  Monthly Active Users       30,000+            Validates retention
                                                beyond novelty

  Slips Processed / Day      500+               Proves daily utility

  User Satisfaction (CSAT)   4.2 / 5.0          Quality of explanations

  Viral Coefficient          \> 1.2             Users share with
                                                colleagues

  Month 1 Revenue            ₹0 (free)          Build trust first

  Month 4 Revenue            ₹30,000 MRR        First monetisation
                                                milestone
  -------------------------- ------------------ -------------------------

**3. Target Users & Personas**

**Persona 1 --- Ravi, Factory Worker, Pune**

  ---------------- ------------------ ---------------- ------------------
  **Age**          28                 **Language**     Hindi / Marathi

  **Income**       ₹18,000/month      **Education**    12th pass

  **Device**       Android, WhatsApp  **Pain**         Never understands
                   daily                               PF/ESI deductions
  ---------------- ------------------ ---------------- ------------------

**Persona 2 --- Priya, IT Professional, Bengaluru**

  ---------------- ------------------ ---------------- ------------------
  **Age**          26                 **Language**     English / Kannada

  **Income**       ₹65,000/month      **Education**    Engineering
                                                       graduate

  **Device**       iPhone, high data  **Pain**         Wants to optimise
                   literacy                            HRA / tax saving
  ---------------- ------------------ ---------------- ------------------

**Persona 3 --- Mohammed, SME Owner, Hyderabad**

  ---------------- --------------------- ----------------- ------------------
  **Role**         HR Manager / Business **Team Size**     15--80 employees
                   Owner                                   

  **Problem**      Answers salary        **Opportunity**   White-label
                   questions daily                         SalaryBot for
                                                           staff

  **Willingness to ₹2,000--5,000/month   **Channel**       LinkedIn, direct
  Pay**                                                    outreach
  ---------------- --------------------- ----------------- ------------------

**4. Core Features --- MVP (Weeks 1--4)**

**4.1 Feature List**

  -------- ------------------------------- ------------------ -----------------
  **\#**   **Feature**                     **Priority**       **Effort**

  F1       Receive salary slip --- JPEG,   P0 --- Must Have   Low
           PNG or PDF via WhatsApp                            

  F2       Auto-convert PDF to image       P0 --- Must Have   Low
           before AI processing                               

  F3-AI    Extract salary components using P0 --- Must Have   Medium
           Vision AI                                          

  F3       Generate plain-language         P0 --- Must Have   Medium
           explanation (EN + HI)                              

  F4       Emoji-formatted response for    P0 --- Must Have   Low
           scanability                                        

  F5       Follow-up Q&A on same slip      P1 --- Should Have Low

  F6       \"Is my deduction correct?\"    P1 --- Should Have Medium
           check                                              

  F7       Tax saving suggestions (80C,    P2 --- Nice to     Medium
           HRA)                            Have               

  F8       Monthly slip history &          P2 --- Nice to     High
           comparison                      Have               

  F9       Admin dashboard for B2B clients P3 --- Post MVP    High
  -------- ------------------------------- ------------------ -----------------

**4.2 Sample Conversation Flow**

+-----------------------------------------------------------------------+
| **User sends salary slip (photo or PDF) → Bot responds within 10      |
| seconds**                                                             |
|                                                                       |
| User: \[Sends photo OR PDF of salary slip\] Bot: Got it! \`\`\`PDF    |
| detected --- converting\...\`\`\` 👀 (or just \"Analysing\...\" for   |
| images) Bot: Here\'s your April 2026 breakdown: 💰 Gross Salary:      |
| ₹45,000 🏠 HRA: ₹8,000 (rent tax saving --- good!) 📉 TDS Deducted:   |
| ₹2,100 (goes to income tax dept) 🔒 PF (Your share): ₹3,200 (YOUR     |
| money --- you get it back) 🔒 PF (Company adds): ₹3,200 (free money   |
| from employer!) 🏥 ESI: ₹338 (health insurance, only if salary \<     |
| ₹21k) 📋 Professional Tax: ₹200 (state govt, everyone pays) ✅        |
| Take-home: ₹31,162 Anything feel wrong, or want me to explain any     |
| item? Just ask! User: What is TDS? Can I reduce it? Bot: TDS = Tax    |
| Deducted at Source. Your employer sends ₹2,100 directly to the        |
| government each month on your behalf. Yes --- you can reduce it!      |
| Invest in: 📌 PPF / ELSS Mutual Fund → saves up to ₹46,800/year in    |
| tax 📌 Submit rent receipts for HRA → if you haven\'t already Want a  |
| personalised tax-saving plan based on your slip? 🎯                   |
+-----------------------------------------------------------------------+

**5. Technical Architecture**

**5.1 System Overview**

+-----------------------------------------------------------------------+
| **Architecture Principle**                                            |
|                                                                       |
| LLM-agnostic from Day 1. All AI calls go through a single Provider    |
| Abstraction Layer (PAL). Switching from Gemini to GPT-4o or Claude    |
| requires changing ONE config value, not rewriting code.               |
+-----------------------------------------------------------------------+

**5.2 Tech Stack**

  ---------------- ------------------------ ------------------------------
  **Layer**        **Technology**           **Reason**

  Language         Python 3.11+             Best AI/ML library support,
                                            easy solo maintenance

  Framework        FastAPI                  Async, lightweight, auto-docs,
                                            easy WhatsApp webhooks

  WhatsApp         Meta Cloud API (free     Official, free, no 3rd party
                   tier)                    dependency

  File Handling    Pillow + PyMuPDF (fitz)  Pillow for images (JPEG/PNG);
                                            PyMuPDF converts PDF pages to
                                            images before AI processing

  AI --- Primary   Google Gemini Flash      Best value: free 1,500
                                            req/day, excellent vision

  AI --- Fallback  OpenAI GPT-4o Mini       Backup if Gemini fails or
                                            quota exceeded

  AI --- Future    Claude Haiku / Ollama    Pluggable via abstraction
                                            layer

  Hosting          AWS EC2 t2.micro (Free   750 hrs/month free for 12
                   Tier)                    months; run FastAPI via
                                            Gunicorn + systemd

  Cache / Rate     Upstash Redis (Free      10,000 req/day free;
  Limit            Tier)                    AWS-backed; no server to
                                            manage; REST API --- no Redis
                                            client needed

  Database         Supabase (free tier)     User sessions, usage
                                            analytics, audit logs

  Process Manager  Gunicorn + Uvicorn       Production-grade ASGI serving
                   workers                  on EC2

  Reverse Proxy    Nginx (on EC2)           SSL termination, static files,
                                            forwards to Gunicorn

  SSL Certificate  Let\'s Encrypt (Certbot) Free HTTPS, auto-renews every
                                            90 days

  Monitoring       Sentry (free)            Error tracking, latency alerts
  ---------------- ------------------------ ------------------------------

**5.3 LLM Provider Abstraction Layer (PAL)**

The PAL is the most critical architectural decision. It makes SalaryBot
LLM-agnostic and future-proof.

+-----------------------------------------------------------------------+
| **PAL Design Pattern**                                                |
|                                                                       |
| \# providers/base.py class LLMProvider(ABC): \@abstractmethod async   |
| def analyze_image(self, image_bytes, prompt) -\> str: pass \#         |
| providers/gemini.py class GeminiProvider(LLMProvider): async def      |
| analyze_image(self, image_bytes, prompt) -\> str: \# Gemini Flash     |
| implementation \# providers/openai.py class                           |
| OpenAIProvider(LLMProvider): async def analyze_image(self,            |
| image_bytes, prompt) -\> str: \# GPT-4o Mini implementation \#        |
| config.py --- change ONE line to switch providers ACTIVE_PROVIDER =   |
| os.getenv(\"LLM_PROVIDER\", \"gemini\") \# or \"openai\", \"claude\"  |
| \# main.py --- zero changes needed provider =                         |
| get_provider(ACTIVE_PROVIDER) result = await                          |
| provider.analyze_image(image_bytes, SALARY_PROMPT)                    |
+-----------------------------------------------------------------------+

**5.4 AWS Deployment Architecture**

+-----------------------------------------------------------------------+
| **Hosting Strategy --- AWS Free Tier (12 months free)**               |
|                                                                       |
| EC2 t2.micro ←→ Nginx (reverse proxy + SSL) ↓ Gunicorn + Uvicorn      |
| workers ↓ FastAPI application ↓ ┌─────────────┴──────────────┐        |
| Upstash Redis Supabase (rate limiting) (analytics logs) AWS-backed    |
| free Postgres free tier                                               |
+-----------------------------------------------------------------------+

  --------------- ------------------ ------------- -----------------------
  **Component**   **Service**        **Cost**      **Setup Notes**

  Server          AWS EC2 t2.micro   Free (12      Amazon Linux 2023, 1GB
                                     months)       RAM, 1 vCPU --- enough
                                                   for 500 req/day

  Storage         AWS EBS 30GB       Free (12      Root volume --- stores
                                     months)       app code and logs only,
                                                   no media files

  Static IP       AWS Elastic IP     Free while    Attach to EC2 ---
                                     attached      needed for WhatsApp
                                                   webhook domain

  SSL / HTTPS     Let\'s Encrypt     Free forever  Auto-renews every 90
                  Certbot                          days via cron job

  Reverse Proxy   Nginx on EC2       Free          Forwards port 443 →
                                                   Gunicorn on port 8000

  Process Manager systemd service    Free          Auto-restarts FastAPI
                                                   if EC2 reboots

  CI/CD           GitHub Actions →   Free          Push to main branch →
                  EC2 SSH                          auto-deploy to EC2

  Cache           Upstash Redis      Free (10K     REST API --- no Redis
                                     req/day)      client install, works
                                                   from EC2

  Database        Supabase           Free (500MB)  Hosted Postgres --- no
                                                   DB to manage on EC2

  After 12 months t2.micro → t3.nano \~\$4/month   Cheapest option when
                                                   free tier expires
  --------------- ------------------ ------------- -----------------------

**5.5 Data Flow**

  ---------- ---------------------------- ------------------- -------------------
  **Step**   **Action**                   **Component**       **Time**

  1          User sends salary slip ---   WhatsApp Cloud API  0s
             image (JPEG/PNG) or PDF                          

  2          Meta webhook fires POST to   FastAPI on EC2      \< 1s
             /webhook endpoint                                

  3          Detect file type --- image   File handler        \< 0.5s
             or PDF                                           

  4          If PDF: convert first page   PyMuPDF             \< 1s
             to JPEG using PyMuPDF                            

  5          Strip EXIF metadata from     Privacy filter      \< 0.5s
             image                                            

  6          PII scrubber removes name,   Security layer      \< 1s
             PAN, account number                              

  7          Check Upstash Redis --- rate Upstash Redis       \< 0.2s
             limit (10 req/day/user)                          

  8          Sanitised image sent to AI   LLM Provider        3--7s
             provider via PAL                                 

  9          AI extracts components +     LLM Provider        included
             generates explanation                            

  10         Response formatted with      Formatter           \< 1s
             emojis, language detected                        

  11         Message sent back to user    WhatsApp Cloud API  \< 1s
             via WhatsApp API                                 

  12         Anonymised usage event       Supabase            async
             logged for analytics                             
  ---------- ---------------------------- ------------------- -------------------

**6. Security & Privacy Design**

+-----------------------------------------------------------------------+
| **Security Principle**                                                |
|                                                                       |
| Salary slips contain highly sensitive personal financial data.        |
| SalaryBot is built with privacy-by-design: we process the minimum     |
| data needed, strip all PII before sending to any AI provider, never   |
| store images, and are transparent with users about data handling.     |
+-----------------------------------------------------------------------+

**6.1 Security Requirements**

  ---------------------- ---------------------------------- -------------
  **Requirement**        **Implementation**                 **Status**

  PDF support --- page 1 Only first page of PDF processed;  MVP
  only                   remaining pages discarded          
                         immediately                        

  Image never stored     Process in memory only, discard    MVP
                         immediately after AI call          

  PII scrubbing before   Strip name, PAN, bank account      MVP
  AI                     before sending to LLM              

  EXIF metadata removal  Strip GPS, device info from image  MVP
                         before processing                  

  HTTPS everywhere       TLS 1.3 enforced, Railway handles  MVP
                         certs automatically                

  WhatsApp webhook       Verify X-Hub-Signature-256 on      MVP
  verification           every incoming request             

  API key rotation       Keys stored in env vars, rotated   MVP
                         monthly via Railway secrets        

  Rate limiting per user Max 10 requests/day/number via     MVP
                         Redis counter                      

  User consent on first  Disclaimer sent before user can    MVP
  use                    send first slip                    

  Audit logging          Log slip_processed events with no  MVP
  (anonymised)           PII, only metadata                 

  AI provider data       Use Gemini/OpenAI zero-retention   Month 2
  retention              API endpoints where available      

  End-to-end encryption  3rd party review before B2B launch Month 4
  audit                                                     

  DPDP Act 2023          India Data Protection law          Month 4
  compliance             compliance review                  
  ---------------------- ---------------------------------- -------------

**6.2 User Consent Flow**

+-----------------------------------------------------------------------+
| **First-Time User Consent Message (sent before any processing)**      |
|                                                                       |
| Welcome to SalaryBot! Before you send your slip, please note: 🔒      |
| PRIVACY: Your salary slip is processed only to generate your          |
| explanation. It is NEVER stored on our servers. ⚡ AI PROCESSING:     |
| Your slip (with personal details removed) is sent to an AI service to |
| generate the explanation. 📋 DATA: We only log that a slip was        |
| processed --- never the contents. By sending your slip, you agree to  |
| these terms. Type AGREE to continue, or STOP to cancel.               |
+-----------------------------------------------------------------------+

**6.3 PII Scrubbing Logic**

+-----------------------------------------------------------------------+
| **What Gets Stripped Before AI Processing**                           |
|                                                                       |
| Fields removed before sending to any LLM provider: • Employee name    |
| and employee ID • PAN number (regex: \[A-Z\]{5}\[0-9\]{4}\[A-Z\]{1})  |
| • Bank account number • Company name (optional --- configurable) •    |
| Address fields What remains (safe to send): • All salary amounts and  |
| component names • Deduction line items and percentages • Month/Year   |
| of the slip • Employer contribution figures                           |
+-----------------------------------------------------------------------+

**7. Monetisation Strategy**

+-----------------------------------------------------------------------+
| **Core Principle**                                                    |
|                                                                       |
| Build userbase first. Do not charge individual users until Month 4.   |
| Trust is the product.                                                 |
+-----------------------------------------------------------------------+

  ------------- -------------- ------------------------------ -------------
  **Phase**     **Timeline**   **Revenue Model**              **Target
                                                              MRR**

  Phase 0 ---   Month 1--3     Completely free, no ads, no    ₹0
  Free                         upsells                        

  Phase 1 ---   Month 4        Sell to HR teams / SME owners: ₹30,000
  B2B Pilot                    ₹2,000--5,000/month            

  Phase 2 ---   Month 5        Individual Pro plan: ₹99/month ₹50,000
  Premium                      for history + tax tips         

  Phase 3 ---   Month 6+       White-label API for payroll    ₹1,00,000+
  API                          software companies             
  ------------- -------------- ------------------------------ -------------

**8. Go-To-Market Plan**

**8.1 Launch Channels (Zero Budget)**

-   Reddit: r/IndiaFinance, r/personalfinanceindia, r/developersIndia
    --- post a \"built this over a weekend\" story

-   LinkedIn: One authentic post per week showing real examples (salary
    slip → explanation)

-   WhatsApp Groups: Office groups, alumni groups --- every user has 5+
    of these

-   Product Hunt India launch --- schedule for a Tuesday, prep a good
    description

-   Telegram: Salary/HR/Finance communities

**8.2 Viral Loop Design**

+-----------------------------------------------------------------------+
| **Built-In Virality**                                                 |
|                                                                       |
| Every explanation ends with: \"Found this helpful? Forward to a       |
| colleague who\'s confused about their slip too 👇\" --- the problem   |
| is universal, the solution is shareable. One office = 50 potential    |
| users.                                                                |
+-----------------------------------------------------------------------+

**9. Risks & Mitigations**

  --------------------- ---------------- ------------ ------------------------------
  **Risk**              **Likelihood**   **Impact**   **Mitigation**

  AI gives wrong        Medium           High         Add disclaimer: \'For
  deduction explanation                               reference only, consult your
                                                      HR for official figures\'

  WhatsApp API rate     Low              Critical     Follow Meta policies strictly;
  limits or bans bot                                  never send unsolicited
                                                      messages

  Users don\'t trust    Medium           High         Strong consent flow + privacy
  sending slip to a bot                               messaging + open source the
                                                      PII scrubber

  LLM provider          Medium           Medium       PAL ensures 1-day switch to
  increases pricing                                   cheaper provider

  Low retention after   High             Medium       Monthly reminder: \'Your new
  first use                                           slip is here --- send it for a
                                                      check-up!\'

  Competitor            Low              High         Move fast, own the WhatsApp
  (Zepto/CRED) ships                                  channel, build community
  same feature                                        
  --------------------- ---------------- ------------ ------------------------------

**10. Development Milestones**

  ---------- --------------------------------------------- ----------------
  **Week**   **Deliverable**                               **Owner**

  Week 1     AWS EC2 t2.micro --- Nginx + Gunicorn +       Founder
             systemd + SSL live                            

  Week 1     WhatsApp Business API webhook live on EC2     Founder
             public domain                                 

  Week 1     Gemini Flash integration + image extraction   Founder
             working                                       

  Week 2     PyMuPDF PDF-to-image pipeline + file type     Founder
             detection                                     

  Week 2     PII scrubber + consent flow built and tested  Founder

  Week 2     Upstash Redis rate limiting live (10          Founder
             req/day/user)                                 

  Week 3     Hindi + English response formatting done      Founder

  Week 3     GitHub Actions CI/CD auto-deploy to EC2       Founder
             pipeline                                      

  Week 4     Internal testing --- 20 real salary slips     Founder +
             (image + PDF)                                 Friends

  Week 4     Soft launch --- 50 beta users from personal   Founder
             network                                       

  Month 2    Reddit / LinkedIn launch --- target 5,000     Founder
             users                                         

  Month 3    Usage analytics + retention analysis via      Founder
             Supabase                                      

  Month 4    B2B pilot --- 3 SME/HR clients signed         Founder

  Month 5    Premium plan launched                         Founder

  Month 6    Seed funding pitch prepared                   Founder
  ---------- --------------------------------------------- ----------------

**11. Open Questions**

1.  PDF support is live for page 1 --- should we support multi-page PDFs
    (some slips span 2 pages)? Adds complexity but covers more use
    cases.

2.  Which Indian languages to prioritise after Hindi? Tamil and Telugu
    have the largest salaried base.

3.  Do we need a registered company before B2B contracts? (Yes ---
    register LLP before Month 4)

4.  Should the bot proactively ask \'is this your latest slip?\' to
    drive monthly re-engagement?

5.  Zero-retention API endpoints --- confirm availability with Gemini
    and OpenAI before launch.

**Appendix --- Quick Reference**

**Useful Links**

-   WhatsApp Cloud API Docs: developers.facebook.com/docs/whatsapp

-   Google AI Studio (Gemini): aistudio.google.com

-   Railway Hosting: railway.app

-   Supabase (Database): supabase.com

-   India DPDP Act 2023: meity.gov.in/data-protection

+-----------------------------------------------------------------------+
| **Document Status**                                                   |
|                                                                       |
| This is a living document. Update after every user interview, every   |
| failed assumption, and every pivot. The goal is not to follow this    |
| doc --- it\'s to make it obsolete as fast as possible by learning     |
| from real users.                                                      |
+-----------------------------------------------------------------------+
