"""List all jambonz resources using the async REST client.

Set environment variables or create a .env file:
    JAMBONZ_ACCOUNT_SID=your-account-sid
    JAMBONZ_API_KEY=your-api-key
"""
import asyncio

from jambonz import AsyncJambonzClient


async def main():
    async with AsyncJambonzClient() as client:
        print("=== Accounts ===")
        for a in await client.accounts.list():
            print(f"  {a.name} ({a.account_sid})")

        print("\n=== Applications ===")
        for a in await client.applications.list():
            print(f"  {a.name} ({a.application_sid})")

        print("\n=== Carriers ===")
        for c in await client.carriers.list():
            print(f"  {c.name} ({c.voip_carrier_sid})")
            gateways = await client.gateways.list(voip_carrier_sid=c.voip_carrier_sid)
            for gw in gateways:
                print(f"    {gw.ipv4}:{gw.port} inbound={gw.inbound} outbound={gw.outbound}")

        print("\n=== Phone Numbers ===")
        for n in await client.phone_numbers.list():
            print(f"  {n.number}")

        print("\n=== Speech Services ===")
        for s in await client.speech_services.list():
            print(f"  {s.vendor} (label: {s.label})")

        print("\n=== Recent Calls ===")
        for c in await client.recent_calls.list(days=7, count=5):
            print(f"  {c.direction}: {c.from_} -> {c.to} ({c.duration}s)")


if __name__ == "__main__":
    asyncio.run(main())
