---
name: rocketchat-ops-watchlist
description: "Operational facts captured from Rocket.Chat triage runs (Oct 2026) that matter to COO work later — EMEA Q4, Damovo, DSTA, Std Cloud wind-down, Q3 comp payout, Q3 close Mar-26 payroll misclass, YE cash overlay, BCS, ABAC banner, security hygiene"
metadata:
  node_type: memory
  type: project
  originSessionId: f6ce3bfb-b69f-441b-add0-47d11a064b46
  modified: 2026-10-19T14:06:33.313Z
---

Context harvested by the RC triage routine ([[rocketchat-triage-routine]]). Each line is dated; re-verify before acting.

**EMEA Q4 forecast (Bruno Weiblen, 12-Oct-2026 team mtg):** pipe-gen $71.6k vs $3.6M target, 11 days into Q4. Manager forecast $81k low / $1.37M high; Bruno's call is $800k-1M, of which Damovo is $500k license + $150k PS. So EMEA Q4 rests mostly on one partner deal. Other named: IDF IT Unit $29.6k (verbal approval), Fujitsu Labs $50k. Feeds [[pipeline-generation-paradox]], [[fy27-planning-calendar]].

**Damovo booth workspace (14-Oct-2026):** Damovo's lab licenses were cancelled while the team was at an event (Smart Country Convention, Berlin) with them. Mike Farman extended them to 31-Dec. Small, but a deal-critical partner nearly lost a working demo.

**DSTA "Project T" (14-Oct-2026):** 600-user request via Kenneth (DSTA). After a call with Bruno/Christian, Luis Zaleta is treating it as a new project at list price, not an upsell at contract unit price, pending discovery. Watch for a pricing/ACV dispute vs Carlos Mayorca, who wanted it as an upsell.

**Standard Cloud → crisiscenternorth (ICP 4, ~$1.2k/yr, contract to Dec-2027):** Alan decided 22/25-Sep: self-hosted or pro-rated refund, Samuel Souza validates. As of 13-Oct, no customer reply and no refund issued; Gabriel Casals moved them to AWS on credits as a stopgap. Docs still mention Standard Cloud on purpose — legacy customers remain.

**BCS / Deno (Customer Support Backroom, 14-Oct-2026):** BCS on RC 8.5.3 runs a custom Debian image with Deno 2.3.5 to fix DLP/AsyncWrap failures. Douglas Gubert: allow it for BCS only; Alpine images can't take the same fix. Re-evaluate if other 8.5 customers report it. Deno itself reaches EOL in 2027.

**Open security hygiene (14-Oct-2026):** many users on open.rocket.chat hold the `bot` role (which carries `impersonate-other-user`) as leftovers of an old bug. Julio Araujo says remove it from all non-integration users. Owner unclear (Marcelo Schmidt raised it).

**Open desktop app (14-Oct-2026):** PR #42329 (merged 13-Oct, ships in 8.10) moved `rocketchat.info`, which broke the desktop app's integrations on Open. Fix: desktop 4.18.3. Customers are not affected yet, but any customer on 8.10 will need desktop ≥4.18.3.

**Q3-2026 comp payout closed (#compensation-reports, 15-Oct-2026):** total $291,477.37 USD. Marcela Lima's planned commission deduction was NOT applied this cycle (Fernanda's call); her payout went R$23.2k→R$29.2k (+US$1.17k) and the deduction moves to Q4. Finance sheet updated; Guilherme (Nova Gestão) FYI'd. Feeds [[coo-close-mechanism]].

**Standard Cloud wind-down (15-Oct-2026):** SRE (Felipe S) has requested the OVH contract termination. crisiscenternorth refund still not issued (see above).

**Renewal pool by quarter (Data+Analytics, 16-Oct-2026):** Achylley confirms the forecast-snapshot fact (`fact_sales_forecasting_snapshopt_v2`) buckets renewal pool by Revenue Recognition Date, not Closing Date (Q2 example: $1.8M vs $2.2M). Cross-check with [[renewal-pool-coql-definition]].

**Apollo for transactional renewals (RevOps, 16-Oct-2026):** Daniel/Amanda moving renewal emails to Apollo for open-tracking. Julia offered to take a *temporary password* for support@rocket.chat from Marcelo Schmidt to link it — a shared-credential practice worth steering to a delegated login.

**EMEA update (19-Oct-2026 team mtg):** pipe-gen $300k of $3.6M; forecast unchanged ($81k low / $1.37M high, call $800k-1M, Damovo still the bulk). Bruno in Europe 9-13 Nov.

**LAC Q4 forecast (Felipe Guimarães, 19-Oct-2026):** $31k low / $93k high, $125k total high. Mostly BR public sector via Serpro (DPE-PI $14k, CRF+TCE $13k, INPI $30k POC, MP-RO $33k) plus BrasilCard $60k.

**Renewal slippage (sales-ops, 16-Oct-2026):** Leidos will not close in Q4 (Peter Sucher). NGC may not renew in Nov; could push to Dec or FY27, depending on their infra (tstrobel). Amanda asked whether to extend NGC's workspace.

**ene't GmbH refund (sales-ops, 16-Oct-2026):** an internal subscription-pricing bug overcharged them when they added a seat in Sept. Jairo issued a $5,677.83 Stripe partial refund about 10 minutes after Amanda said she'd seek internal approvals. Julio added a 9-month 50% coupon, valid to Jul-2027. Amanda asked whether other customers are in the same situation, and that is unanswered.

**Remote Optometry (16-19 Oct-2026):** INV4585 ($1,890) was issued in error on 8-Oct because a cancelled deal was still Closed Won. Guilherme (Nova Gestão) asked Samuel to void it. The renewal is now Lost, and the New Sales deal status is still open with Amanda.

**Standard Cloud wind-down (16/19-Oct-2026):** OVH termination is effective 31-Oct, with the last OVH bill in Nov. Alpheton (serbiznet) is renewing to self-hosted on AWS and is waiting on RevOps pricing approval; their workspace was quietly extended to end-Nov, and Jairo recommends not telling them.

**DSTA HA escalation (19-Oct-2026):** ticket 116534 asks for HA patching on 8.9 LTS. Today they run one RC 8.8.1 instance and a single-member Mongo replica set on EFS. It's in CSB review, alongside DSTA Project T.

**Open → RC 9.0 (16-Oct-2026):** Open will run 9.0 this month. Mobile users must update to app 4.77.2 or they lose access.

**Inbound worth watching (16-Oct-2026):** Dutch government-type hand-raise, 7,500 users across air-gapped + connected domains, asking about Government licence; Bruno Weiblen owns. Valtori (Strategic) escalated a busy-tone feature request on 7.13.6 with Pexip.

**Drummond Q1 close (DM with Guilherme, 19-Oct-2026):** Alan asked Guilherme (Nova Gestão) to speed up closing Q1 with Drummond. A call with Silvia (Drummond side) is set for Wed 21-Oct, 11:30 BRT, and Guilherme is sending the invite.

**Sanwa INV4584 (sales-ops, 19-Oct-2026):** this is the invoice re-issued on 8-Oct with the corrected PO, and the old one was credit-memo'd. Luis Zaleta asked Samuel whether it has been paid. That's a Q4 renewal, so watch the cash.

**LAC public-sector lead burst (19-Oct-2026):** about 15 Apollo-sourced leads converted at once from BR federal/state police (PF, PRF, PC-SC, PC-ES, SENAPPEN). All are owned by Felipe Guimarães. There was also an inbound hand-raise from NAABOL (Bolivian air navigation, ICP 2, gov): 200 users, growing to 900.

**QBR Q4 schedule (Amanda):** S1 16-Oct, S2 19-Oct (pull-in strategy), S3 22-Oct, S4 27-Oct, all at 11AM BRT.

**Go imports payment-redirect risk (Nova Gestão Full Team, 22-Oct-2026):** Karine (Nova Gestão AP) found the Go imports payee CNPJ differed from the invoicing CNPJ. She asked the supplier over a WhatsApp number from their website and was told to pay a different account belonging to a company called "Severo", whose business activity doesn't match selling computers. The order is about 38k (likely BRL). She asked Amanda and Guilherme whether to pay. This matches the pattern of bank-detail-change fraud, so check the outcome before treating it as closed.

**MakeOne / Serpro partner kickoff (Omnichannel Preferred Partner, 20-21 Oct-2026):** commercial kickoff done. Knowledge sessions are proposed for 10-11 Nov and a strategy session at Serpro São Paulo on 12 Nov. MakeOne starts Serpro pre-sales the week of 26-Oct. Amanda's terms: Omnichannel Agent sold as today and tied to Commercial seats in FC; MakeOne can sell Mac Packs but can't see usage (Felipe G sends a monthly report); avoid pay-as-you-go unless it's a large deal, and escalate those to leadership. Alfredo proposed giving the partner access to the Solar CzRM repo (after a Sec request) for a DEPAC/INPI meeting on 22-Oct, with INPI topics going to legal. Partner room: #External-Partner-Sapios-MakeOne-Rocket-Chat. See [[makeone-br-omnichannel-site]].

**Security patch window (rocketchat-security, 20-22 Oct-2026):** Node.js October security releases are out (including a Brotli decoder bug). Mike Farman asked "are we affected?" and nobody had answered by the time of the run. Gabriel Casals flagged that our Electron version is not on the eMudhra advisory's safe list. Desktop 4.18.4 has been released (after 4.18.3, see above).

**NORAM TEM lesson (NORAM Marketing, 22-Oct-2026):** Tom Mersman says the event itself was good but our presentation was weak because we relied on the partner and they didn't deliver. The lesson: fully own any co-presentation. There are good follow-ups with Army, Navy and Air Force personnel.

**Lead-sync burst (sales-alerts, 21 and 22 Oct-2026, around 09:48 UTC):** about 90 Starter/Community "lead converted" alerts fired in a few minutes, most owned by Gabriel Engel with a blank GTM. This looks like a batch sync of mostly free-email junk and is worth a hygiene check on routing. Real hand-raises in the same window: Kath. Marienkrankenhaus (DE, ICP 2, Teams/Slack replacement, Exchange calendar), hayat finans (TR bank, ICP 2), Design Interactive (US, ICP 4, "move quick", owner Strobel), and partner registrations for mil.dk (Christian) and Eidsiva (Bruno).

**Mar-26 "Other Expense" +30k in the leadership pack (Nova Gestão Full Team, 23-Oct-2026):** Amanda spotted a positive Other Expense in Mar-26 under Cash Flow / Cash Expenditures while closing the Q3 Metrics Pack. Felipe Bergamasso says March payroll was booked via Bill to "Suppliers Global" because the "Payroll payables" account wasn't set up as a Bill-able type at ERP go-live. Renato agreed to leave it through the close, and April went back to Journal Entries. Alan asked whether the +30k is therefore correct and whether the explanation is documented for investors. Amanda is waiting on Guilherme to call the Q3 P&L and cash flow closed. Feeds [[coo-close-mechanism]] as a candidate carried root.

**Year-end cash overlay (21-Oct-2026):** Amanda's forecast now cuts Dec-26 expected cash from 1,265,284 to 1,060,775 (−204.5k, pushed into Jan), and Oct outflow was restated from 1,338,000 to 1,262,889. FY ending cash is 2,766,176. Alan agreed with it. Company Bonus forecast is now on the quarterly close checklist (it depends on ARR and Ending Cash).

**BCS iOS reconnect hang (CSB, 23-Oct-2026):** BCS (Mission Critical, 8.5.3) gets stuck on "Connecting..." after a reconnect on iOS app 4.77.2. Felipe S and Otavio reproduced it, and it's filed as SUP-1128. This is the same account as the Deno custom image above.

**ABAC classified banner (rocketchat-dev, 23-Oct-2026):** Morgan Lemke flagged that the ABAC classified banner runs like a standalone web app. Gov/ICP buyers then treat it as a separate application that needs its own security clearance, unless it's served from the same web server as RC. This is a product risk for the defense motion, and it's unanswered.

**Open server permissions (23-Oct-2026):** Felipe Scuciatto removed `call-management` from the `user` role on Open, because any user could start calls in any channel. It's now limited to Rocket.Chat Team, Admin and Global Moderator. Mike Farman wants an official PHP-vulnerability "not affected" statement for customers, and nobody owns it yet.

**Damovo conversion + 3rd lead-sync burst (sales-alerts, 23-Oct-2026):** daniel.schulze@damovo.com converted on "Enterprise Self Managed Subscription" (EMEA Enterprise, owner Rocket Cat, so no AE assigned). This may be the Q4 Damovo deal, so check that Bruno has it. The ~09:49 UTC Starter/Community burst happened again, for a 3rd day running. Hand-raises: Haigh-Farr (US aerospace) wants to renew and add 15 seats (prior INV-22791, a 24-month term from 2024); a Poznań municipal hospital (PL, public) wants a quote, and Bruno has it.

**MakeOne positioning (23-Oct-2026):** Bruno Bin is building a MakeOne partner page that's mostly visible to Brazil IPs, framed as Citizen Engagement. The agreed rule is to avoid "Omnichannel" on public pages because it has confused our positioning. Gabriel Casals wrote a MakeOne consultancy-hours doc (Confluence), and Felipe G and Alfredo approved it.

**QBR Session 3 (23-Oct-2026):** QBR Session 3 (Partners) ran NORAM/LAC on 23-Oct. EMEA moved to 30-Oct, 11AM BRT.

**Security disclosures (26-Oct-2026):** Abhinav K (#rocketchat-dev) flagged a probable prompt-injection exfil in AI Search. The AI overview renders markdown images, so a crafted message can make the answer embed an image URL carrying private-room text, which loads with no click. Jean Brito found E2E-search vulnerabilities, logged privately as LSE2EE-73 for Julio Araujo and Felipe Scuciatto. Both are product security issues worth confirming have owners before AI Search or E2E search ship more widely.

**Meteor 3.5 transport break (Support Backroom, 26-Oct-2026):** BCS ticket 116651 reports the 8.9.0 image crashes with `DISABLE_SOCKJS=true`, which now implies uWebSockets, and uWS doesn't support Alpine/musl. Workaround: unset the var. This is undocumented, and Open hit it too. Also SUP-1130: global search drops custom-field-only user matches on 8.7-8.9 (BCS 116656 and ticket 116172). BCS also asked again for risk acceptance on Inspector Critical/High findings for 8.5.3.

**Linnovate / IDF Intelligence 10K side letter (sales-ops, 25-27 Oct-2026):** amendment to RC-OF-10887 (signed 30-Sep). It gives a free 10% duplicate-account allowance (1,000 on 10K, 150 on 1,500) and a price lock above 11,000 users at OF rates to 30-May-2032, initial term only. Bruno approved it and says it was aligned with Skelly at end of Q3. Mayra redrafted it on RC letterhead, Yossi (Linnovate) signed on 26-Oct, and Alan countersigns. The PDF is now on the CRM deal. Billing and provisioning need to reflect the 11,000 cap.

**EMEA Q4 (26-Oct-2026 team mtg):** pipe-gen $500k of $3.6M (+$200k on the week). Manager forecast $81k low / $1.48M high (up from $1.37M). The call is unchanged at $800k-1M, with Damovo $650k still the bulk.

**Echo eG orphaned accounts (hand-raises, 26-27 Oct-2026):** Anhalt Computer hosts 135 Enterprise licenses (3-yr from 1-May-2024) for vivo-intensivpflege via reseller Echo eG, which has gone silent. Luis Zaleta says ex-Echo accounts follow the "CCNet process". Bruno says proceed, and the renewal-vs-new-sales call is with Amanda. Also notable hand-raises: MITRE engineer pricing 10,000 self-hosted seats (non-profit, no purchasing authority); Ultra Cyber (US defense, ICP 1) air-gapped chat+video for about 150; Liquid PC (partner, ICP 1) quote request.

**Achy out 23-Oct to 3-Nov-2026 (RevOps Alignment):** the Manager Forecast skill runs on Achy's machine, so it won't run while Achy is away and someone must run it by hand Thu or Fri morning. Forecast Methodology doc needs Alan+Amanda validation before 3-Nov to become official. Brazil holiday Mon 2-Nov, so no Global Forecast meeting with Achy that day. Achy suggests raising the 4 late Q4 renewals at the next forecast meeting.

**OKR status method (26-Oct-2026):** Alan agreed with Ana Lopes that status reflects year-end attainment, not the point-in-time value. Churn (Q3 -$1.55M vs -$1.66M limit, ~$1M more expected in Q4) and NRR (97.6% vs >100%) are both moved to off track. Aline notes there is no written At Risk vs Off Track rule; R&D uses a 20% margin.

**Mar-2026 cash outflow restatement (Nova Gestão closing thread, 23-Oct-2026):** March payroll was booked via Bill to "suppliers global" because the Payroll payables account was mis-typed in the ERP setup, which is why March outflows look odd. Felipe Bergamasso manually segregated it, and also moved Factor's advance-from-customer out of revenue/outflows. He says year cash result is unchanged. Feeds [[coo-close-mechanism]].

**Lead-sync burst repeats (sales-alerts, 26 and 27 Oct-2026, ~09:50 UTC):** about 80 more Starter/Community conversions, mostly Gabriel Engel-owned with a blank GTM and free-email. The batch pattern is now daily, and some contacts fire twice (e.g. Leidos' Pat Main under Peter Sucher).

**AWS budget overages (AWSBudget_Review, Rodrigo Nascimento, 26-Oct-2026):** Marketplace MongoDB Atlas is at $188.3k spent against a $160.6k budget (117%, $27.7k over), with a forecast of $226.5k (141%), and is the biggest line by far. Also over: Project AI $7.8k vs $3.6k (forecast 277%), Hosting Staging 111% (forecast 149%), Team Professional Services 115%. Hosting Cloud Services ($27.4k of $28.9k) and Team Engineering are both forecast to go over. No ask to Alan was posted. Feeds [[coo-close-mechanism]].

**NATO UCC RFI (EMEA Sales Team, 27-Oct-2026):** Bruno Weiblen posted NATO-wide Unified Communications and Collaboration RFI-CO-424402-UCC. There was no discussion or bid decision in the room yet.

**CVE-2026-105482 (rocketchat-security, 27-Oct-2026):** Julio Araujo says we're not affected. `dns.resolveMx` (registration/email-change, livechat offline form) discards its result, and the XMPP `dns.resolveSrv` normalizes input first. Julio also promised a Node2Shell note.

**Offline-license flag (support-backroom, 27-Oct-2026):** the server now respects the license `offline` flag. Some licenses were wrongly generated as offline for online customers, who then couldn't fetch licenses after updating (Marcelo Schmidt). Marcelo thinks a manual sync should ignore the flag. A docs-team air-gapped↔online migration guide was proposed.

**BCS (CSB, 27-28 Oct-2026):** the DISABLE_SOCKJS flag dates back to BCS's own config from Jan-2025, not a Support recommendation, and unsetting it works on 8.9.0. New ticket 116648: on Desktop 4.17.0, clients behind a proxy flag the server as unsupported because the compatibility check also calls releases.rocket.chat. That's SUP-1131, high priority, for Jean Brito. Engineering was slow to respond, and Marcelo Schmidt chased it.

**Open → 9.0 RC (27-28 Oct-2026):** the appsqa workspace is on 9.0.0-rc.1. Fuselage refactors landed with small intentional visual changes, and users are reporting scroll-on-send and keyboard-scroll regressions. Morgan Lemke says desktop video calls on Mac open a slow Chrome window.

**EDX/IMA WhatsApp 360dialog (Omnichannel Preferred Partner, 28-Oct-2026):** EDX asked us to replace the omnigateway webhook so they can move to a new BSP (Nimbus?). Gabriel Casals says that would break the app entirely, and re-pointing it to the new partner is out of scope "especially for free". Felipe G asked Amanda, Achy and Daniel for a plan. This is a partner scope/pricing question.

**CCNet partner price book (27-Oct-2026):** a CCNet partner price book was floated on the strategic-initiatives call. Gabriel Casals asked Nicole Dinnadge for the tier, the geos (Euro region assumed) and a target date. This ties to the Echo eG / "CCNet process" orphaned accounts above.

**Hosting quotes (27-28 Oct-2026):** EMSA RPAS (CHP-124) was flagged urgent by Carlos Mayorca for Gabriel Casals. Domenicom (CHP-125) looks like it was a mistaken request, and deletion was asked for.

**personnel-updates test noise (28-Oct-2026):** 3 "New Onboarding: Teste Teste" posts (R&D, Deel, $0) came from someone testing the onboarding automation. They aren't real hires.

**Lead-sync burst (sales-alerts, 28-Oct-2026, ~09:49 UTC):** it happened again for the 5th weekday running (about 45 alerts, mostly Gabriel Engel free-email junk, with temp-mail addresses routed to Bruno). Real names in the batch: Hyundai (APAC Ent, Rocket Cat-owned, fired twice), Region Uppsala (EMEA Ent, Rocket Cat-owned, no AE), Parsons (Strobel), Collins Aerospace (Strobel, Outsourced), Telefónica (Bruno, sales contact form), gov.bc.ca (Sucher), PC-AL (Felipe G). United Jewish (US) demo request went to Monica Nelson.

**Deal-approval routing (RevOps & Biz Sys, 06-Nov-2026):** Achy confirmed that renewal and upsell approvals that used to go to CBO/COO now go to RevOps. Approvers can delegate an approval to another owner (e.g. pass it to Alan or Skelly) from the notification.

**Telecable renewal (sales-ops, 06-Nov-2026):** quote went out for 2 years (26 PRO seats at $4 + Omnichannel MAC pack $175/mo, $6,696 for the term); the customer wants 1 year. Daniel Rosenberg and Amanda agreed to keep the 5% increase and switch to a 1-year term (Lucy estimated ~$3,515).

**EDX / MakeOne partner process (Omnichannel Preferred Partner, 03-05 Nov-2026):** Marcelo met EDX to walk through technical adjustments after EDX wanted to restructure how its app connects to the RC workspace. MakeOne bypassed the agreed process and went straight to José Delgado on Voice items; Gabriel Casals asked Felipe Guimarães to hold them to the agreed process.

**Slotegrator / Velund pre-QBS AR (aging-AR, 11-12 Nov-2026):** Samuel Souza found unpaid direct order forms from 2023 to early 2025 (all ending Feb-2026): €21,387.88 + $385 in total, of which the New Sale is €20,020. Invoices exist in Xero but not in NetSuite. After a first "no balance" read was retracted, Amanda and Samuel confirmed an outstanding amount on 12-Nov. Alan ruled (11-Nov) that we collect directly from the customer and explain that QBS owns the main relationship. Marcela Lima will tell QBS, then Samuel will contact Velund.

**Standard Cloud closed / OVH final bill (Discontinue Standard Cloud + Nova Gestão, 06-12 Nov-2026):** Gabriel Casals declared the initiative fully complete on 11-Nov. Remaining follow-ups are AWS credits, transactional renewals and AWS-only hosting ops. The Nov OVH invoice came in at the full amount, not the ~30% the team had projected. Casals confirmed it is correct and is the last OVH payment.

**Pricing initiative status (Pricing Steering Room, 12-Nov-2026):** Gabriel Casals is targeting a Quoting Tool launch before the end of Nov-2026, with adjustments from a 12-Nov meeting with Skelly and Tom. Next up: the Hosting AI Calculator, an "Omnibus"/"Fleet" SKU (proposal exists, with Amanda and Achylley), then All-in and Defense SKUs.

**Cash position (Leadership Review, 12-Nov-2026):** Guilherme Barbosa posted ending cash of $3,016,715.68 on 12-Nov ($3,016,716.03 on 11-Nov). 11-Nov inflows included Unimed Planalto Central and Sanwa Comtec. Feeds [[fy27-cash-sensitivity]].

**Pipe-gen week of 5-11 Nov-2026 (Pipeline Review, Daniel Rosenberg):** $942.2K of global pipeline was added: NORAM $0 with 6 NBMs, EMEA/APAC $410.3K with 11 NBMs, LAC $531.9K with 1 NBM. EMEA+APAC manager forecast low was $224.0K on 12-Nov (Achylley Macedo's Thursday check-in).

**9.0 customer escalations (support-backroom, 12-Nov-2026):** NALC lost the SSO option in the Desktop client after upgrading to 9.0 (it now forces a browser sign-in). Natalie Dailey asked them to file a ticket. Separately, Felipe Guimarães flagged a high-priority ticket from CORE-SC (with Serpro).

**EMEA Q4 (16-Nov-2026 team mtg, Bruno Weiblen):** pipe-gen about $1M of the $3.6M target. The meeting agenda pushes a closing focus on every opportunity that can land this quarter and a final pipe-gen sprint to start Q1.

**XMPP excluded from RC hosting (hosting-quotes / Strategic-Initiatives, 16-Nov-2026):** Gabriel Casals ruled that customers with XMPP use cases are not suitable for RC hosting. Each XMPP workspace needs its own dedicated AWS NLB on a reachable TCP port, and AWS has a default quota of about 50 NLBs. Defense customers, the main XMPP users, are not expected on hosting anyway.

**DPE-Piauí 360dialog charges without a signed OF (revops-and-finance-invoicing, 13-Nov-2026):** Daniel Rosenberg found RC is being charged by 360dialog for a DPE-Piauí number with no signed Order Form. Per Felipe, MakeOne should not have activated it. Daniel expects an OF to follow.

**Pricing initiative (Pricing Initiative / Steering Room, 13-16 Nov-2026):** Gabriel Casals shared draft proposals (Fleet Workspace License "Omnibus" SKU, All-in Bundle SKU and others) for review by Skelly, Tom Mersman and Bruno Weiblen. The Fleet WS License discussion is set for 23-Nov. The Quoting Tool is expected to be available to all soon, and the Hosting AI Calculator launches after one more production case.

**Transactional renewals (Partners, 13-Nov-2026):** Telia signed (Daniel Rosenberg). Achylley Macedo reminded the team to update the CRM product list before an Order Form goes to a partner, so legacy products don't persist.

**Phishing targeting staff (rocketchat-security, 16-Nov-2026):** Luis Zaleta got two emails in one day asking him to pay an "overdue invoice" for Gabriel. He reported them to Julio Araujo.

**9.0 escalation: CSC custom OAuth (support-backroom, 16-Nov-2026):** CSC - IT Center for Science, ticket 116904. On 9.0.0, custom OAuth passes no email to account creation or merging, so users who log in through two providers get duplicate accounts. Yash Rajpal is investigating.

**Oct-26 close cash figures (Nova Gestao full-team room, 17-Nov-2026):** Guilherme reported Oct-26 ending cash of US$2,673,162.70 and October customer cash inflows of US$993,224.70. The GitHub receipt of US$6,225 includes a one-time US$6K subsidy from an Eng/Security initiative (Amanda: exclude it from recurring revenue; recurring GitHub = US$225). Expected further subsidies: US$2K Mar-27 and US$2K Oct-27. Amanda noted the historical ARR for Aralyx and SOCOM is still under review (Oct-26 not affected).

**PHP2Shell customer assurance (sales-ops, 18-Nov-2026):** AmeriSave asked critical vendors for assurance on the PHP vulnerabilities (third-party risk request; Natalie Dailey filed a legal request). Julio Araujo answered that Rocket.Chat was not impacted by PHP2Shell: our apps are TypeScript/Go/some Python, and the only third-party PHP service exposed to the internet was in a test environment. This is the first written "not affected" position; it moves the earlier open item (Mike Farman's request for an official PHP-vulnerability statement, 23-Oct) toward answered.

**Brazil CCT 2026/2027 wage provision (CCT 2026/2027 discussion, people-finance, 18-Nov-2026):** Employer union (Sindicato Patronal) suggests provisioning 4.49% (12-month INPC) from 01-Nov-2026 while the union agreement is pending; salaries are normally updated with retroactive pay once agreed. Fernanda Bernardes (finance) asking the team for forecast values; no action required yet.

**AeC contract restructure (AeC opportunity, 18-Nov-2026):** AeC uses about half of 500 users + 500 Mac Packs (contract to Jun-2028, ACV $151,181, TCV $453,544). Proposal: keep ~$226,771 of remaining value stretched over 3 years instead of 1.5. Alan approved 18-Nov; Bruno Weiblen agreed; Marcela Lima to take it back to AeC.
