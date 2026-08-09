# YasinPress — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasinpress`
- Documented version: `2.0.0`
- Role: automated Persian news collection and Eitaa publishing application

## Responsibility

YasinPress collects Persian news from multiple RSS sources, detects duplicates, filters stale content, categorizes and prioritizes stories, optionally uses Cloudflare Workers AI for rewriting/summarization/classification/hashtags/breaking-news detection/daily digest, then publishes to Eitaa.

## Module Map

```text
run.py
config.py
pipeline.py
fetch_news.py / rss_engine.py
duplicate_engine.py / duplicate_detector.py / similarity.py
category_engine.py
ai_engine.py
daily_digest.py
news_builder.py / message_builder.py / formatter.py
tag_engine.py
post_counter.py
source_names.py
logo_manager.py
send_queue.py / queue_manager.py / rate_limiter.py
eitaa_sender.py / media_sender.py
publish_engine.py
main_controller.py
process_lock.py
database.py
logger.py
```

## Data / Reliability Model

The application uses SQLite, a persistent publishing queue, rate limiting, a process lock, continuous post numbering and a fallback from AI processing to rule-based processing when AI is unavailable.

## Runtime Target

The project is designed for Termux/Android while also supporting Python 3.10+ generally.

## AI Boundary

The documented optional AI integration is Cloudflare Workers AI. Credentials are kept outside Git. AI is an optional processing layer, not the application's only execution path.

## External Platform Boundary

Eitaa publishing is an application responsibility. Documented Eitaayar API limitations include lack of HTML/Markdown parse mode and reply-markup support.

## Audit Status

**Level 3:** application workflow, modules, persistence, fallback and external publishing boundaries are documented. Exact API/provider contracts, CI and cross-project dependencies require source audit.
