# jambonz Python SDK — Feature Tracker

## Done

### REST API Client
- [x] Sync client (`JambonzClient`) + Async client (`AsyncJambonzClient`)
- [x] Context manager (`with` / `async with`) with `Self` typing
- [x] Config from env vars + `.env` file (Pydantic Settings)
- [x] Auth via Bearer token
- [x] Retry with exponential backoff (429 rate limit + 5xx errors)
- [x] Typed exceptions (`JambonzAuthError`, `JambonzNotFoundError`, `JambonzRateLimitError`, `JambonzValidationError`)
- [x] Request/Response hooks (`on_request`, `on_response`)
- [x] Resources: Carriers, PhoneNumbers, Applications, SpeechServices, Calls
- [x] Resource chaining: `client.carriers("sid").get()` / `.delete()`
- [x] Sub-resources: `client.carriers("sid").gateways.list()`
- [x] Scoped vs top-level endpoints (`_scoped` flag)
- [x] Generic base (`SyncResource[T]` / `AsyncResource[T]`)
- [x] Full test suite with respx mocks (48 tests)

### Webhook Response (Verbs)
- [x] Pydantic models for verbs: Say, Play, Gather, Pause, Hangup, Redirect, LLM, Dial
- [x] Discriminated union (`Verb`) on `verb` field
- [x] `JambonzResponse = Sequence[Verb]` (plain alias, no `RootModel`); `to_json()` for Flask/Django
- [x] Strict verbs that serialize themselves: unset fields (`MISSING`) omitted, camelCase aliases, enums — no custom serializer except the `extra_fields` merge
- [x] `alias_generator=to_camel` in base class (`_JambonzBase`) — no manual `Field(alias=...)` needed
- [x] `Input` enum with UPPER_CASE names, lowercase values
- [x] Works with FastAPI (`response_model`, `->` type hint, or explicit construction)
- [x] Framework-agnostic: `to_json(verbs)` for Flask/Django
- [x] `Synthesizer` and `Recognizer` typed models
- [x] FastAPI integration tests

## Pending — Minimum
- [ ] Verify all resource paths match jambonz.cloud API (some may differ from docs)
- [x] Webhook incoming models: typed payloads in `jambonz.payloads`
- [x] `py.typed` marker for PEP 561
- [ ] Basic README with install + usage examples

## Pending — Should Have
- [ ] Pagination support (if jambonz API supports it)
- [ ] All remaining resources: Users, Clients, ApiKeys, Alerts, RecentCalls, LcrRoutes, MicrosoftTeamsTenants
- [ ] Twilio-style dual access: `client.gateways.list(voip_carrier_sid="x")` alongside chaining
- [ ] More verbs: Transcribe (Conference, Enqueue, Dequeue, Listen are done)
- [ ] Verb validators (e.g. Gather without action_hook warning)
- [ ] Tests for sub-resources (gateways chaining)
- [ ] Tests against real API (integration test suite, skipped by default)

## Pending — Nice to Have
- [ ] Composition operator `|` for JambonzResponse
- [ ] `__repr__` for JambonzResponse
- [ ] Idempotency keys (if jambonz supports them)
- [ ] Streaming support for real-time events
- [ ] Webhook signature verification (like `WebhookResponse.verifyJambonzSignature` in Node SDK)
- [ ] OpenAPI spec auto-discovery / validation

## Dream
- [ ] MCP server exposing jambonz resources as tools (manage carriers, numbers, apps via LLM)
- [ ] CLI tool (`jambonz carriers list`, `jambonz numbers create`)
- [ ] Code generation from jambonz OpenAPI spec (auto-generate resources + models)
- [ ] WebSocket client SDK (equivalent to `@jambonz/node-client-ws`)
- [ ] Publish to PyPI
- [ ] Documentation site with examples per framework (FastAPI, Flask, Django)
