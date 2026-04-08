# API Coverage

Complete list of jambonz REST API endpoints and SDK coverage status.

**Total endpoints: 109** | **Covered: 27** | **Coverage: 25%**

## REST Call Control (8 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 1 | GET | `/Accounts/{sid}/Calls` | List active calls | ✅ `client.calls.list()` |
| 2 | POST | `/Accounts/{sid}/Calls` | Create a call | ✅ `client.calls.create()` |
| 3 | GET | `/Accounts/{sid}/Calls/{CallSid}` | Retrieve a call | ✅ `client.calls.get()` |
| 4 | PUT | `/Accounts/{sid}/Calls/{CallSid}` | Update a call | ✅ `client.calls.update()` |
| 5 | DELETE | `/Accounts/{sid}/Calls/{CallSid}` | Delete a call | ✅ `client.calls.delete()` |
| 6 | GET | `/Accounts/{sid}/CallCount` | Get call count | ❌ |
| 7 | GET | `/Accounts/{sid}/Conferences` | List conferences | ❌ |
| 8 | GET | `/Accounts/{sid}/Queues` | List queues | ❌ |

**Covered: 5/8**

## REST Platform Management — Accounts & Users (23 endpoints)

### Accounts
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 9 | GET | `/Accounts` | List accounts | ✅ `client.accounts.list()` |
| 10 | POST | `/Accounts` | Create account | ✅ `client.accounts.create()` |
| 11 | GET | `/Accounts/{sid}` | Retrieve account | ✅ `client.accounts.get()` |
| 12 | PUT | `/Accounts/{sid}` | Update account | ✅ `client.accounts.update()` |
| 13 | DELETE | `/Accounts/{sid}` | Delete account | ✅ `client.accounts.delete()` |
| 14 | GET | `/Accounts/{sid}/WebhookSecret` | Get webhook secret | ❌ |
| 15 | POST | `/Accounts/{sid}/SipRealms/{realm}` | Set SIP realm | ❌ |
| 16 | GET | `/Accounts/{sid}/Limits` | Get limits | ❌ |
| 17 | POST | `/Accounts/{sid}/Limits` | Create limits | ❌ |
| 18 | GET | `/Availability` | Check availability | ❌ |

### Users
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 19 | POST | `/Users` | Create user | ✅ `client.users.create()` |
| 20 | GET | `/Users/{sid}` | Retrieve user | ✅ `client.users.get()` |
| 21 | PUT | `/Users/{sid}` | Update user | ✅ `client.users.update()` |
| 22 | DELETE | `/Users/{sid}` | Delete user | ✅ `client.users.delete()` |

### API Keys
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 23 | GET | `/ApiKeys` | List API keys | ✅ `client.api_keys.list()` |
| 24 | POST | `/ApiKeys` | Create API key | ✅ `client.api_keys.create()` |

### Clients
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 25 | GET | `/Clients` | List clients | ❌ |
| 26 | POST | `/Clients` | Create client | ❌ |
| 27 | GET | `/Clients/{sid}` | Get client | ❌ |
| 28 | PUT | `/Clients/{sid}` | Update client | ❌ |
| 29 | DELETE | `/Clients/{sid}` | Delete client | ❌ |

### Registered SIP Users
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 30 | GET | `/Accounts/{sid}/RegisteredSipUsers` | List SIP users | ❌ |
| 31 | POST | `/Accounts/{sid}/RegisteredSipUsers` | Get SIP user by name | ❌ |

**Covered: 12/23**

## REST Platform Management — Applications & Webhooks (7 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 32 | GET | `/Applications` | List applications | ✅ `client.applications.list()` |
| 33 | POST | `/Applications` | Create application | ✅ `client.applications.create()` |
| 34 | GET | `/Applications/{sid}` | Retrieve application | ✅ `client.applications.get()` |
| 35 | PUT | `/Applications/{sid}` | Update application | ✅ `client.applications.update()` |
| 36 | DELETE | `/Applications/{sid}` | Delete application | ✅ `client.applications.delete()` |
| 37 | GET | `/Webhooks/{sid}` | Retrieve webhook | ❌ |
| 38 | GET | `/AppEnv` | Get app env schema | ❌ |

**Covered: 5/7**

## REST Platform Management — Carriers & SIP (14 endpoints)

### VoIP Carriers
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 39 | GET | `/Accounts/{sid}/VoipCarriers` | List carriers | ✅ `client.carriers.list()` |
| 40 | POST | `/Accounts/{sid}/VoipCarriers` | Create carrier | ✅ `client.carriers.create()` |
| 41 | GET | `/VoipCarriers/{sid}` | Retrieve carrier | ✅ `client.carriers.get()` |
| 42 | PUT | `/VoipCarriers/{sid}` | Update carrier | ✅ `client.carriers.update()` |
| 43 | DELETE | `/VoipCarriers/{sid}` | Delete carrier | ✅ `client.carriers.delete()` |

### SIP Gateways
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 44 | GET | `/SipGateways` | List gateways | ✅ `client.gateways.list()` |
| 45 | POST | `/SipGateways` | Create gateway | ✅ `client.gateways.create()` |
| 46 | GET | `/SipGateways/{sid}` | Retrieve gateway | ✅ `client.gateways.get()` |
| 47 | PUT | `/SipGateways/{sid}` | Update gateway | ✅ `client.gateways.update()` |
| 48 | DELETE | `/SipGateways/{sid}` | Delete gateway | ✅ `client.gateways.delete()` |

### SBCs
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 49 | GET | `/Sbcs` | List SBC IPs | ❌ |

### Predefined Carriers
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 50 | POST | `/SP/{sid}/PredefinedCarriers/{pid}` | Add from template | ❌ |
| 51 | GET | `/SP/{sid}/VoipCarriers` | List SP carriers | ❌ |
| 52 | POST | `/SP/{sid}/VoipCarriers` | Create SP carrier | ❌ |

**Covered: 10/14**

## REST Platform Management — Phone Numbers (5 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 53 | GET | `/PhoneNumbers` | List numbers | ✅ `client.phone_numbers.list()` |
| 54 | POST | `/PhoneNumbers` | Create number | ✅ `client.phone_numbers.create()` |
| 55 | GET | `/PhoneNumbers/{sid}` | Retrieve number | ✅ `client.phone_numbers.get()` |
| 56 | PUT | `/PhoneNumbers/{sid}` | Update number | ✅ `client.phone_numbers.update()` |
| 57 | DELETE | `/PhoneNumbers/{sid}` | Delete number | ✅ `client.phone_numbers.delete()` |

**Covered: 5/5** ✅

## REST Platform Management — Speech (20 endpoints)

### Speech Credentials (Account)
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 58 | GET | `/Accounts/{sid}/SpeechCredentials` | List credentials | ✅ `client.speech_services.list()` |
| 59 | POST | `/Accounts/{sid}/SpeechCredentials` | Create credential | ✅ `client.speech_services.create()` |
| 60 | GET | `/Accounts/{sid}/SpeechCredentials/{sid}` | Get credential | ✅ `client.speech_services.get()` |
| 61 | PUT | `/Accounts/{sid}/SpeechCredentials/{sid}` | Update credential | ✅ `client.speech_services.update()` |
| 62 | DELETE | `/Accounts/{sid}/SpeechCredentials/{sid}` | Delete credential | ✅ `client.speech_services.delete()` |
| 63 | GET | `.../speech/supportedLanguagesAndVoices` | Get languages/voices | ❌ |
| 64 | GET | `.../SpeechCredentials/{sid}/test` | Test credential | ❌ |
| 65 | POST | `/Accounts/{sid}/TtsCache/Synthesize` | TTS from provider | ❌ |

### Google Custom Voices
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 66-70 | CRUD | `/GoogleCustomVoices` | Google custom voices | ❌ |

### Speech Credentials (Service Provider)
| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 71-77 | CRUD+test | `/SP/{sid}/SpeechCredentials` | SP speech credentials | ❌ |

**Covered: 5/20**

## REST Platform Management — Recent Calls & Alerts (8 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 78 | GET | `/Accounts/{sid}/RecentCalls` | List recent calls | ✅ `client.recent_calls.list()` |
| 79 | GET | `.../RecentCalls/trace/{CallId}` | Get Jaeger trace | ❌ |
| 80 | GET | `.../RecentCalls/{sid}/record/...` | Get recording | ❌ |
| 81 | GET | `.../RecentCalls/{CallId}/pcap` | Get PCAP | ❌ |
| 82 | GET | `/Accounts/{sid}/Alerts` | List alerts | ❌ |
| 83-85 | GET | `/SP/{sid}/RecentCalls/...` | SP recent calls | ❌ |

**Covered: 1/8**

## REST Platform Management — LCR Routing (13 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 86-92 | CRUD | `/Lcrs`, `/Lcrs/{sid}/Routes` | LCR management | ❌ |
| 93-99 | CRUD | `/LcrRoutes` | LCR routes | ❌ |
| 100-101 | GET+POST | `/LcrCarrierSetEntries` | Carrier set entries | ❌ |

**Covered: 0/13**

## REST Platform Management — Service Providers (8 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 102-106 | CRUD | `/ServiceProviders` | Service providers | ❌ |
| 107 | GET | `/SP/{sid}/Accounts` | SP accounts | ❌ |
| 108-109 | GET+POST | `/SP/{sid}/Limits` | SP limits | ❌ |

**Covered: 0/8**

## REST Platform Management — Microsoft Teams (5 endpoints)

| # | Method | Path | Description | SDK |
|---|---|---|---|---|
| 110-114 | CRUD | `/MicrosoftTeamsTenants` | Teams tenants | ❌ |

**Covered: 0/5**

---

## Summary by Section

| Section | Endpoints | Covered | % |
|---|---|---|---|
| **Call Control** | 8 | 5 | 63% |
| **Accounts & Users** | 23 | 12 | 52% |
| **Applications** | 7 | 5 | 71% |
| **Carriers & SIP** | 14 | 10 | 71% |
| **Phone Numbers** | 5 | 5 | 100% |
| **Speech** | 20 | 5 | 25% |
| **Recent Calls & Alerts** | 8 | 1 | 13% |
| **LCR Routing** | 13 | 0 | 0% |
| **Service Providers** | 8 | 0 | 0% |
| **Microsoft Teams** | 5 | 0 | 0% |
| **Total** | **109** | **27** | **25%** |

## Priority Gaps

### High (core features)
- CallCount, Conferences, Queues (call control)
- Alerts (monitoring)
- Speech test + supported languages (speech)

### Medium (admin features)
- Clients (CRUD)
- Account limits, webhook secret, SIP realm
- Recording + PCAP retrieval

### Low (advanced/niche)
- LCR routing (13 endpoints)
- Service Providers (multi-tenant admin)
- Microsoft Teams integration
- Google Custom Voices
- Predefined carrier templates
