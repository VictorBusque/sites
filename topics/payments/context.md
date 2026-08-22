# How does an online (card) payment actually happen? — research context

Private working material. The public article is a standalone scrollytelling post.
Scope decision: the story follows **one card payment** (works the same for a
shop terminal tap and an online checkout) from the two-second authorization to
the days-later settlement. "Online payment" in the idea queue is interpreted as
"what actually happens when you pay by card" — the dominant rails behind both
in-person taps and web checkouts.

## The central mechanism (what research says)

A card payment is **two separate acts**, not one:

1. **Authorization (~2 seconds).** The terminal asks the cardholder's bank
   (issuer) for a *promise*: "will you guarantee €4.50 for this merchant?"
   The issuer checks funds, card status, and fraud, then replies approve or
   decline. If approved, the issuer places a **hold** on the cardholder's
   account. No money moves.
2. **Clearing and settlement (1–3 business days later).** The merchant's
   terminal/processor submits the completed sale (capture). Transactions are
   batched and exchanged between banks through the network (clearing), fees
   are computed, and then funds are transferred on a **net** basis between
   issuers and acquirers (settlement). The merchant's bank credits the
   merchant, minus fees.

The five parties (four-party model + network):

- **Cardholder** and their bank, the **issuer** (issued the card, holds the
  cardholder's account).
- **Merchant** and their bank, the **acquirer** (contracts with the merchant,
  deposits their card receipts).
- **Card network** (Visa, Mastercard): routes messages, applies the rulebook,
  sets interchange. A network, not a bank: it does not hold consumer deposits
  or lend.

## Verified facts and sources

| # | Fact | Source | Notes / scope |
| --- | --- | --- | --- |
| F1 | Authorization takes about two seconds; clearing + settlement complete 1–3 business days later | energizeglobal.com/blog/card-payment-process-explained; paymentbrief.com/articles/authorization-capture-settlement-payment-lifecycle | Industry-standard description |
| F2 | Four-party model: cardholder, merchant, acquirer, issuer, connected by card network | cashlesstechnology.com/how-it-works/how-card-payments-work; Wikipedia ISO 8583 | — |
| F3 | VisaNet engineered for 65,000+ transaction messages per second | Visa corporate materials, e.g. corporate.visa.com VisaNet-Network-Processing-Overview.pdf; visa.com "Inside Visa's global commerce engine" (stress-test capacity) | Capacity figure, not average load |
| F4 | Visa FY2025: 329B payments+cash transactions carried the brand, 258B processed on Visa networks, $17T total volume, ~5B credentials, 175M+ merchant locations, ~14,500 financial institutions | Visa FY2025 annual report / 10-K (s29.q4cdn.com Visa-Fiscal-2025-Annual-Report.pdf; annualreport.visa.com/financials) | Fiscal year to Sep 2025 |
| F5 | ISO 8583: international standard for financial transaction card-originated interchange messaging; first released 1987; MTI + bitmap + data elements | Wikipedia ISO 8583; iso.org/standard/15870.html (ISO 8583:1987) | Authorization 0100 / response 0110 are the classic MTIs |
| F6 | EMV chip generates a per-transaction ARQC (Authorization Request Cryptogram): an 8-byte MAC over card, terminal and transaction data using a session key derived from the card master key + transaction counter (ATC); issuer verifies and returns an ARPC | AWS Payment Cryptography docs (docs.aws.amazon.com/payment-cryptography); corebaseit.com EMV cryptogram guides; cupass.com EMV cryptogram guide | This is why chip cards can't be usefully cloned, vs magnetic stripe static data |
| F7 | EU interchange caps: 0.2% consumer debit, 0.3% consumer credit of transaction value, effective 9 Dec 2015 | Regulation (EU) 2015/751 (eur-lex.europa.eu legal-content EN/TXT/?uri=oj:JOL_2015_123_R) | EEA consumer cards; commercial cards and non-EEA issuers uncapped |
| F8 | Interchange is paid by the merchant side to the issuer; scheme fees go to the network; acquirer markup on top — total is the merchant discount rate | decta.com card scheme fees; pspmatcher.com payment-fee-structure | — |
| F9 | Stripe EU standard pricing: 1.5% + €0.25 per successful EEA-card transaction (2.5% + €0.25 non-EEA) | stripe.com pricing pages (en-ee, en-be) | Public blended rate, convenient visible example of MDR |
| F10 | Settlement flow: issuer transfers funds to the network/for the acquirer; net positions are computed so only net amounts move; acquirers receive funds through central-bank accounts, then credit merchants minus fees; T+1 to T+2 typical | marqeta.com clearing & settlement; paymentexpert.com payment lifecycle (2026); paymentsandrisk.com settlement lifecycle | — |
| F11 | PSD2 Strong Customer Authentication (in force 14 Sep 2019): online payments in the EEA require two independent factors (knowledge/possession/inherence); 3-D Secure 2 is the standard mechanism; low-value exemption up to €30 accumulated | freenance.io PSD2 SCA guide; mastercard.com SCA page; gpayments.com 3DS/SCA guide | EEA scope |
| F12 | Authorization places a hold (not a transfer) on the cardholder account — familiar from fuel-pump and hotel pre-authorization holds | energizeglobal.com; paymentbrief.com authorization/capture/settlement | — |

## Numbers worth computing rather than citing

- Fee split of a given amount under (a) EU caps (interchange 0.2% debit /
  0.3% credit), (b) a blended MDR like Stripe's 1.5% + €0.25. These make an
  honest computed visual: every displayed cent is arithmetic on stated public
  rates, labeled as such.
- Authorization timeline beats (illustrative pacing of the ~2 s round trip).

## Conflicts / caveats

- "65,000 msg/s" is a stated *capacity/stress-test* figure — must be labeled
  capacity, not traffic.
- Settlement timing varies by acquirer/region: "1–3 business days" is the
  range sources give; the article should say "typically 1–3 business days".
- Interchange outside EEA consumer cards (US credit, premium/commercial) is
  far higher and uncapped; if shown, it must be scoped, not generalized.
- The exact internal message flow differs per network/gateway; the article's
  hop sequence (terminal → gateway/processor → acquirer → network → issuer)
  is the standard simplification and is honest at this resolution.

## Illustrative values (must be labeled illustrative in the page)

- The €4.50 coffee, merchant names, specific timestamps (DAY 0 19:42 etc.).
- Any specific ledger-entry rendering of bank accounts.
- Pacing of authorization stages within the ~2 s.
