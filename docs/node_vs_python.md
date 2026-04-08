# Node.js SDK vs Python SDK — Comparison

## 1. REST Call Control

Manage active calls: create outbound calls, update in-progress calls, send messages.

| Feature | Node.js | Python |
|---|---|---|
| **Create call** | ✅ (with validation: from, to, hooks) | ❌ |
| **Update call** | ✅ (mute, hold, whisper, hangup, redirect, dub, media_path) | ❌ |
| **Retrieve call** | ✅ | ❌ |
| **List calls** | ✅ | ❌ |
| **Delete call** | ✅ | ❌ |
| **Create message** (SMS) | ✅ (with validation) | ❌ |
| Call create validation | ✅ (from, to, application_sid XOR call_hook) | ❌ |
| Call update validation | ✅ (enum checks for mute_status, call_status, etc.) | ❌ |

## 2. REST Platform Management

Manage jambonz infrastructure: accounts, carriers, numbers, apps, speech, etc.

| Resource | Node.js | Python |
|---|---|---|
| **Accounts** | ❌ | ❌ |
| **Applications** | ✅ (create/list/get/delete, no update) | ✅ (full CRUD) |
| **VoipCarriers** | ❌ | ✅ (full CRUD) |
| **SipGateways** | ❌ | ✅ (full CRUD) |
| **PhoneNumbers** | ❌ | ✅ (full CRUD) |
| **SpeechCredentials** | ❌ | ✅ (full CRUD) |
| **RecentCalls** (paginated) | ❌ | ✅ (with days/page/count) |
| **Users** | ❌ | ❌ |
| **Clients** | ❌ | ❌ |
| **ApiKeys** | ❌ | ❌ |
| **Alerts** | ❌ | ❌ |
| **LcrRoutes** | ❌ | ❌ |
| **MicrosoftTeamsTenants** | ❌ | ❌ |

| Feature | Node.js | Python |
|---|---|---|
| HTTP library | `bent` | `httpx` |
| Auth | Bearer token | Bearer token |
| Sync client | ✅ | ✅ `JambonzClient` |
| Async client | ❌ | ✅ `AsyncJambonzClient` |
| Context manager | ❌ | ✅ `with` / `async with` |
| Retry + backoff | ❌ | ✅ (429, 5xx) |
| Typed exceptions | ❌ | ✅ |
| Typed responses | ❌ (plain objects) | ✅ (Pydantic models) |
| Config from env / .env | ❌ | ✅ (Pydantic Settings) |
| Request/Response hooks | ❌ | ✅ |
| App schema validation | ✅ (JSON Schema + AJV) | ❌ |
| Env var merging with defaults | ✅ | ❌ |

## 3. Webhooks

Respond to jambonz HTTP webhook requests with verb instructions.

### Verb Builder

| Feature | Node.js | Python |
|---|---|---|
| Class | `WebhookResponse` | `JambonzResponse` (Pydantic RootModel) |
| Style | Method chaining: `.say().hangup()` | List: `[Say(...), Hangup()]` |
| Verb validation | ✅ (`@jambonz/verb-specifications`) | ✅ (Pydantic model validation) |
| Verb auto-generation | ✅ (dynamic from specs) | ❌ (manually defined) |
| camelCase aliases | ❌ (manual) | ✅ (`alias_generator=to_camel`) |
| Null exclusion | ❌ (manual) | ✅ (`model_serializer`) |
| Discriminated union type | ❌ | ✅ (`Verb` with discriminator) |
| Typed enums | ❌ | ✅ (`Input.SPEECH`) |
| Framework agnostic | ✅ (`toJSON()`) | ✅ (`model_dump()` / `model_dump_json()`) |
| FastAPI native | N/A | ✅ (`response_model` / `->` type hint) |
| Webhook signature verification | ✅ (HMAC-SHA256, timing-safe) | ❌ |

### Verbs Supported

| Verb | Node.js | Python | Category |
|---|---|---|---|
| say | ✅ | ✅ | TTS |
| play | ✅ | ✅ | Audio |
| gather | ✅ | ✅ | Input |
| pause | ✅ | ✅ | Flow |
| hangup | ✅ | ✅ | Flow |
| redirect | ✅ | ✅ | Flow |
| llm | ✅ | ✅ | AI |
| dial | ✅ | ✅ | Telephony |
| answer | ✅ | ❌ | Flow |
| conference | ✅ | ❌ | Telephony |
| config | ✅ | ❌ | Config |
| dequeue | ✅ | ❌ | Queue |
| dialogflow | ✅ | ❌ | AI |
| dtmf | ✅ | ❌ | Input |
| dub | ✅ | ❌ | Audio |
| enqueue | ✅ | ❌ | Queue |
| leave | ✅ | ❌ | Telephony |
| lex | ✅ | ❌ | AI |
| listen | ✅ | ❌ | Audio |
| message | ✅ | ❌ | Messaging |
| rasa | ✅ | ❌ | AI |
| record | ✅ | ❌ | Recording |
| rest:dial | ✅ | ❌ | Telephony |
| sip:decline | ✅ | ❌ | SIP |
| sip:refer | ✅ | ❌ | SIP |
| sip:request | ✅ | ❌ | SIP |
| stream | ✅ | ❌ | Audio |
| tag | ✅ | ❌ | Metadata |
| transcribe | ✅ | ❌ | STT |
| alert | ✅ | ❌ | Flow |

**Node.js: 29 verbs** — **Python: 8 verbs** (21 missing)

### Incoming Webhook Parsing

| Feature | Node.js | Python |
|---|---|---|
| Typed models for incoming call data | ❌ | ❌ |
| Typed models for gather results | ❌ | ❌ |
| Typed models for call status events | ❌ | ❌ |

## 4. WebSocket API

Real-time bidirectional communication with jambonz for session control.

| Feature | Node.js | Python |
|---|---|---|
| WebSocket client | ✅ | ❌ |
| Protocol | `ws.jambonz.org` | N/A |
| Session management | ✅ (`WsSession`) | N/A |
| Router | ✅ (`WsRouter` with path matching) | N/A |
| Events: session:new | ✅ | N/A |
| Events: session:reconnect | ✅ | N/A |
| Events: call:status | ✅ | N/A |
| Events: verb:hook | ✅ | N/A |
| Events: verb:status | ✅ | N/A |
| Events: jambonz:error | ✅ | N/A |
| Command injection | ✅ (`ws.sendCommand`) | N/A |
| Verb acknowledgment | ✅ (`ws.ack`) | N/A |
| External WS servers | ✅ (shared HTTP server) | N/A |
| Verb chaining + send | ✅ (`.say().hangup().send()`) | N/A |
| reply() vs send() | ✅ (for hook responses) | N/A |

## Summary

|  | Node.js | Python |
|---|---|---|
| **REST Call Control** | ✅✅✅ (calls + messages + validation) | ❌ |
| **REST Platform Management** | ✅ (only applications) | ✅✅✅ (6 resources, async, typed) |
| **Webhooks** | ✅✅✅ (29 verbs, signature verification) | ✅✅ (8 verbs, typed, framework-agnostic) |
| **WebSocket API** | ✅✅✅ (full session control) | ❌ |

### Priority Gaps

1. **Verbs** — 21 missing verbs (low effort per verb, high value)
2. **Webhook signature verification** — security feature (medium effort)
3. **REST Call Control** — create/update calls, send messages (medium effort)
4. **Incoming webhook parsing** — typed models for call data, gather results (medium effort)
5. **WebSocket API** — full real-time session control (high effort)
