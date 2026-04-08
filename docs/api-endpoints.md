# jambonz REST API Endpoints Discovery

Base URL: `https://api.jambonz.cloud/v1`

## Documented Endpoints (from official docs)

### Account-scoped (`/v1/Accounts/{account_sid}/...`)
| Endpoint | CRUD | Notes |
|---|---|---|
| `Applications` | CRUD | Also works top-level |
| `VoipCarriers` | CRUD | Also works top-level |
| `SpeechCredentials` | CRUD | Only scoped |
| `ApiKeys` | CRUD | Only scoped |
| `RecentCalls` | R | Requires query params (date range) |
| `Alerts` | R | Requires query params (date range) |

### Top-level (`/v1/...`)
| Endpoint | CRUD | Notes |
|---|---|---|
| `Accounts` | CRUD | |
| `PhoneNumbers` | CRUD | |
| `SipGateways` | CRUD | Sub-resource of VoipCarriers |
| `LcrRoutes` | CRUD | Least cost routing |

## Undocumented Endpoints (discovered via testing)

These work on `api.jambonz.cloud` but are not in the official docs:

| Endpoint | Level | Status | Notes |
|---|---|---|---|
| `Users` | Top-level | 200 | |
| `Clients` | Top-level | 200 | SIP registered clients |
| `ServiceProviders` | Top-level | 200 | Multi-tenant admin |
| `MicrosoftTeamsTenants` | Top-level | 200 | Teams integration |
| `SystemInformation` | Top-level | 403 | Admin only |
| `ServiceProviders/{sp_sid}/PhoneNumbers` | Scoped | 200 | Same result as top-level PhoneNumbers |

## Observations

- `Applications` and `VoipCarriers` work both top-level AND scoped. Return identical data for non-admin users.
- `SpeechCredentials` and `ApiKeys` only work scoped under Accounts.
- `RecentCalls` and `Alerts` require query params (return 400 without them).
- `PhoneNumbers` only works top-level, NOT under Accounts.
- Top-level returns all resources visible to the authenticated user. Scoped filters by account.
