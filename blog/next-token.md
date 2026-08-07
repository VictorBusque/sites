---
title: Predict the next token.
author: Víctor Busqué
date: 2026-02-20
status: draft
tags: [LLM, Tokenization, AI]
category: AI/Basics
figures: 3
reading-time: 4
---

# Predict the next token

*AI · Basics · Víctor Busqué — draft · ~4 min · 3 figures*

An LLM is a next-token predictor. Tokens in, probabilities out, one token at a
time. This note builds the smallest honest version of that machine — a model
small enough to read — and runs it. Every number below is computed by the
algorithms on this page (the animated version lives at
[next-token.html](next-token.html)).

## 01 · What an LLM does

Every answer an LLM gives you is written one token at a time. The model looks
at what it has written so far, computes a probability for every token it
knows, and picks one. Then it repeats with the longer text. That loop is the
whole machine — the rest is scale.

> An LLM is a next-token predictor. Chat, code, reasoning — all of it is that
> single step, repeated.

## 02 · Tokens, not letters

A model does not read letters, and it does not really read words. It reads
**tokens** — chunks a tokenizer learned to split text into. The classic
learning rule is byte-pair encoding: count how often every adjacent pair
appears, merge the most common pair, repeat until nothing repeats.

The toy corpus (20 words):

| word | copies |
| --- | --- |
| est | 4 |
| er | 3 |
| low | 3 |
| new | 3 |
| newer | 2 |
| newest | 2 |
| widest | 3 |

**Figure 1 — the merge sequence, computed by the algorithm.** Ties go to the
pair seen first. Each row is the pair merged that step and its real count:

| # | merge | count |
| --- | --- | --- |
| 1 | e + s → es | 9 |
| 2 | es + t → est | 9 |
| 3 | n + e → ne | 7 |
| 4 | ne + w → new | 7 |
| 5 | e + r → er | 5 |
| 6 | l + o → lo | 3 |
| 7 | lo + w → low | 3 |
| 8 | w + i → wi | 3 |
| 9 | wi + d → wid | 3 |
| 10 | wid + est → widest | 3 |
| 11 | new + er → newer | 2 |
| 12 | new + est → newest | 2 |

Ten alphabet letters become twenty-two tokens: the letters plus the twelve
learned merges.

## 03 · The table

Once the text is tokens, the model learns a table: given the tokens seen so
far, what comes next, and how often. This toy uses a trigram table — the next
token depends on the last two.

**Figure 2 — the entire model, 16 contexts.** `a b → c ×n` means token `c`
followed context `a b` exactly `n` times in the corpus:

| context | next tokens |
| --- | --- |
| the fox | met ×1, slept ×1 |
| fox met | a ×1 |
| met a | crow ×1 |
| a crow | the ×1 |
| crow the | crow ×1 |
| the crow | sang ×1 |
| crow sang | a ×1 |
| sang a | song ×1 |
| a song | the ×1 |
| song the | song ×1 |
| the song | went ×1 |
| song went | on ×1 |
| went on | and ×1 |
| on and | on ×1 |
| and on | the ×1 |
| on the | fox ×1 |

A production LLM is the same shape with billions of rows, learned by attention
layers over billions of tokens. The toy's table fits on screen.

## 04 · The loop

Running the model is a loop of three lines: take the last two tokens, read the
row, pick the most likely next token, append it. That is everything.

```js
// the whole model: one lookup, one argmax
// counts[ctx] = tokens that followed ctx during training
function next(ctx) {
    var row = counts[ctx];          // e.g. { met: 1, slept: 1 }
    var best = null, n = 0;
    for (var tok in row)            // pick the most frequent
        if (row[tok] > n) { n = row[tok]; best = tok; }
    return best;                    // one token — call it again
}
```

**Figure 3 — the generated text.** Seeded with `the fox`, greedily picking the
most frequent continuation each step:

```
the fox met a crow the crow sang a song the song went on and on
the fox met a crow the crow sang a song the song …
```

It reads almost like English. Then the context `the fox` comes back and the
toy re-enters its sixteen-token loop. It cannot stop, because the corpus never
showed it an end. Fluency without understanding is exactly what this loop
buys, at every scale.

## 05 · The ceiling

The loop also explains the failure modes. The toy loops because the corpus
ended; a real model confabulates because it only ever samples the table. A
confident falsehood is not a malfunction of next-token prediction — it *is*
next-token prediction: the token that best fits the table, written whether or
not it is true.

> Next-token prediction is not understanding. It is the best-fitting
> continuation, sampled one token at a time.
