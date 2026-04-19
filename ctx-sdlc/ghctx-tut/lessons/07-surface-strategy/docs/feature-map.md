# Loan Workbench Feature Map

## Feature-to-Source Mapping

| Feature | Backend | Frontend | Tests |
| --- | --- | --- | --- |
| Loan Applications | `routes/applications.ts`, `services/loan-service.ts` | `pages/dashboard.ts`, `api/` | `unit/business-rules.test.ts`, `integration/applications.test.ts` |
| Decisions | `routes/decisions.ts`, `services/decision-service.ts`, `rules/` | `pages/dashboard.ts` | `unit/business-rules.test.ts` |
| Notifications | `routes/notifications.ts`, `services/notification-service.ts`, `queue/` | `pages/dashboard.ts` | `integration/` |
| Audit | `routes/audit.ts`, `services/audit-service.ts` | `pages/dashboard.ts` | `integration/audit.test.ts` |
| Queue Monitor | `routes/queue-status.ts`, `queue/` | `pages/queue-monitor.ts` | — |
| User Preferences | — | `pages/preferences.ts` | — |
| API Explorer | — | `pages/api-explorer.ts` | — |

## Cross-Cutting Concerns

| Concern | Implementation |
| --- | --- |
| Authentication | `middleware/auth.ts` |
| Rate Limiting | `middleware/rate-limiter.ts` |
| Audit Logging | `middleware/audit-logger.ts`, `services/audit-service.ts` |
| Request Validation | `middleware/request-validator.ts` |
| Error Handling | `middleware/error-handler.ts` |
| Database | `db/` |
| Configuration | `config/` |
