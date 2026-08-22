# Context — How can one IP address represent millions of machines? (NAT / CGNAT)

Research record for the article. Sources below were read directly or
cross-checked in August 2026. Everything intended for public copy must trace
to a row here; arithmetic derived on the page is labeled as computed.

## The question this research can answer

How a single public IPv4 address can front thousands of machines (and how a
small pool of them fronts millions): the port field as a multiplexer, the NAT
translation table as state, carrier-grade NAT as the same trick at ISP scale,
what it costs, and how the internet works around it (hole punching, IPv6).

## Core mechanism (settled, textbook)

- IPv4 addresses are 32 bits → 2^32 = 4,294,967,296 possible addresses.
  TCP (RFC 793, header) and UDP (RFC 768, header) each carry a 16-bit source
  and destination port → 65,536 port values per address per transport.
- A NAT router with Network Address Port Translation (NAPT) rewrites the
  source IP *and* source port of outbound packets to its own public
  address + a chosen free port, stores the mapping in a translation table,
  and reverses the rewrite (destination fields) for matching inbound
  replies. Defined: RFC 2663 (terminology, Aug 1999); RFC 3022
  "Traditional NAT" (Jan 2001); original short-term proposal RFC 1631
  (May 1994, Egevang & Francis).
- Private address space for the inside: RFC 1918 (Feb 1996) — 10.0.0.0/8,
  172.16.0.0/12, 192.168.0.0/16.
- Unsolicited inbound packets (no table row) are not deliverable and are
  dropped. This is why you cannot host a server behind NAT without port
  forwarding / PCP (RFC 6887, Port Control Protocol).
- Table rows expire after an idle timeout (per transport; UDP shorter than
  TCP). Linux netfilter defaults: 30 s UDP un-replied / 120 s "assured"
  stream, 5 days established TCP — used as *illustrative* timeout values in
  the page's simulator, clearly labeled.
- Hole punching: two NATed peers each open an outbound mapping to the
  other's public endpoint; because many NATs use endpoint-independent
  mapping (RFC 4787 REQ-1/terminology), the resulting tables accept inbound
  from the peer. Standardized machinery: STUN (RFC 8489), TURN relay
  (RFC 8656), ICE candidate gathering (RFC 8445). This is how WebRTC,
  multiplayer games and calls mostly work behind NAT.

## Scarcity timeline (verified dates)

- 3 Feb 2011 — IANA's free pool of IPv4 depleted; the last five /8s went to
  the five RIRs (ARIN announcement, arin.net/vault/announcements/20110203).
- RIR last-address milestones (Wikipedia "IPv4 address exhaustion", citing
  RIR announcements): APNIC 15 Apr 2011; RIPE NCC Sep 2012 (reached its
  final /8, 14 Sep 2012); LACNIC 10 Jun 2014; ARIN 24 Sep 2015. AFRINIC
  entered exhaustion phases 2017. Every RIR has since run dry for general
  allocation.
- World population passed 8 billion on 15 Nov 2022 (UN). So 4.29 B IPv4
  addresses < 8 B people even before counting devices.
- Average US internet household: 17 connected devices, Q3 2023, survey of
  8,000 US internet households (Parks Associates, CES 2024 press release).
- IPv6 adoption: Google's statistics show ~45–50% of users reaching Google
  over IPv6 as of April 2026 (Wikipedia "IPv6 deployment", citing
  google.com/ipv6/statistics.html; weekday/weekend spread). Use with date
  label.
- Secondary market: average transfer price ≈ $27.75 per IPv4 address across
  901 transactions / ~5 M addresses in 2025, down 16% from 2024
  (IPv4Center market report; secondary source — qualify as market-report
  estimate, not an official figure).

## Carrier-grade NAT (CGNAT) — the same trick, rented

- RFC 6598 (Apr 2012): reserves 100.64.0.0/10 (4,194,304 addresses) as
  Shared Address Space for ISP-side CGN; not globally routable; distinct
  from RFC 1918 so the home router's inside and ISP's side don't collide.
- RFC 6888 (Apr 2013), Common Requirements for CGNs — read in full:
  - Definition: a NAT in the ISP's network sharing one public IPv4 among
    several subscribers; subscribers have limited or no control over it.
  - REQ-2: "Paired" pooling default (a subscriber keeps one external
    address across sessions).
  - REQ-4: CGN MUST support limiting external ports per subscriber,
    configurable.
  - REQ-8: an external port should not be reused for ≥120 s (TCP MSL)
    after deallocation, except e.g. statically-assigned port blocks
    (example in the RFC: ports 1000–1999 → subscriber A, 2000–2999 → B —
    deterministic assignment).
  - REQ-11: when out of ports/quota, the CGN drops the new packet, should
    send ICMP host-unreachable, and MUST NOT evict existing mappings.
  - Logging section: to trace abuse, operators log per mapping: protocol,
    subscriber identifier, external address, external port, timestamp.
  - REQ-13/14/15: port allocation trades off utilization vs log volume vs
    port-guessability.
- RFC 6269 (Issues with IP Address Sharing, cited in RFC 6598 §5.2):
  broken use cases — console gaming when two subscribers share one outside
  address, video streaming, P2P seeding/SIP incoming calls, geolocation
  resolving to the CGN, sites limiting simultaneous logins per IP.
- Mobile networks: essentially all mobile carriers place subscribers
  behind large NAT pools (general industry knowledge; present without
  specific numbers).

## Honest arithmetic the page may compute live (labeled computed/illustrative)

- Usable external ports per address ≈ 65,536 − 1,024 well-known = 64,512
  (operators may reserve more; label approximate).
- Subscribers per public address ≈ 64,512 ÷ ports granted per subscriber.
  Examples: 8,192 → 7; 2,048 → 31; 1,024 → 63; 512 → 126; 256 → 252.
  (RFC 6888 REQ-4 requires the limit to exist and be configurable; the
  divisor choice varies by ISP — present as illustrative, not a measured
  ISP practice.)
- Devices behind one public address ≈ subscribers × devices per household
  (e.g. 63 × 17 ≈ 1,071). A /24 pool (256 addresses) at that ratio fronts
  ≈ 274,000 devices; a /22 (1,024 addresses) ≈ 1.1 M. These are the
  article's "millions of machines" claims — always shown as computed
  arithmetic from reader-visible inputs, never as an ISP's measured
  deployment.
- 100.64.0.0/10 = 2^22 = 4,194,304 shared addresses — a private stage for
  the same trick twice (home NAT + CGN in series = double NAT).

## Terminology to keep straight

- NAT vs NAPT vs "port forwarding" vs CGNAT vs double NAT — the article
  says "NAT" for the family and names NAPT when the port rewrite is the
  point.
- Well-known ports 0–1023; dynamic/private range 49152–65535 per
  RFC 6335 (16,384 ports) — the range a laptop typically picks from.

## Disagreements, estimates, and things to avoid

- No authoritative public figure exists for "how many subscribers share
  one CGNAT address" across ISPs — engineering blogs commonly cite
  hundreds; DO NOT state a specific number as fact. Use the computed
  arithmetic table instead, explicitly illustrative.
- Port-block sizes (512/1024/2048) appear in vendor docs and RFC 6888's
  deterministic-assignment discussion; treat as examples, not a standard.
- IPv4 market price: secondary market reports vary by broker; quote the
  2025 average with attribution and "≈".
- Do not claim NAT is a firewall (it drops unsolicited inbound as a
  side effect of having no mapping, not by policy inspection).
- Do not claim NAT was invented for address sharing alone — RFC 1631
  framed it as a short-term fix; also used for security/renumbering
  reasons; RFC 6888 notes some ISPs did it before scarcity.
- Avoid "the internet is full" rhetoric; the pool is exhausted for *free
  allocation*, addresses still trade and get reused.

## Source list (all accessed/verified Aug 2026)

1. RFC 1631 — The IP Network Address Translator (NAT), May 1994.
2. RFC 1918 — Address Allocation for Private Internets, Feb 1996.
3. RFC 2663 — NAT Terminology and Considerations, Aug 1999.
4. RFC 3022 — Traditional NAT, Jan 2001.
5. RFC 4787 — NAT Behavioral Requirements for Unicast UDP, Jan 2007
   (mapping/filtering behavior vocabulary).
6. RFC 6335 — IANA Port Number Registry (ranges), Aug 2011.
7. RFC 6598 — IANA-Reserved IPv4 Prefix for Shared Address Space,
   Apr 2012 (read in full).
8. RFC 6888 — Common Requirements for Carrier-Grade NATs, Apr 2013
   (read in full).
9. RFC 8445 / 8489 / 8656 — ICE / STUN / TURN (mechanism names only).
10. ARIN vault — "The IANA IPv4 Address Free Pool is now Depleted",
    3 Feb 2011.
11. Wikipedia — IPv4 address exhaustion (RIR milestone dates, citing RIRs);
    IPv6 deployment (Google stats summary, Apr 2026).
12. Parks Associates press release, CES 2024 — 17 connected devices per
    US internet household, Q3 2023, n = 8,000.
13. IPv4Center — IPv4 Market Report 2025 ($27.75/IP average, 901
    transactions, −16% YoY). Secondary source.
14. Linux netfilter conntrack defaults (kernel docs / ip_conntrack man) —
    UDP 30 s/120 s, TCP established 432,000 s — illustrative timeouts only.
15. UN — world population reached 8 billion, 15 Nov 2022.
