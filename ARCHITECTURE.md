# Platform architecture

The platform is organized into six expandable product domains:

1. Identity and consent — players, guardians, coaches, organizations and permissions.
2. Media and evidence — uploads, camera integrations, clips and provenance.
3. AI analysis — asynchronous jobs, model versions, quality checks and explainable observations.
4. Development — baselines, goals, plans, interventions and progress.
5. Discovery — consent-aware search, comparison, shortlists and opportunities.
6. Trust — verification, safeguarding, audit history and access policy.

Core flow: Capture → Evidence pipeline → AI analysis → Skill Passport → Coach action → Consented opportunity.

The first release keeps product contracts under `/api/v1`. The in-memory demo stores should be replaced with PostgreSQL, object storage and a task queue without changing the browser-facing API.
