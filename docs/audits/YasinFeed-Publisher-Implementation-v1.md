# YasinFeed — PWA & RSS Publisher Implementation v1

- Repository: `yusi20006-max/Yasinfeed`
- Status: **Implemented**

## PWA

`PWAPublisher` now writes a real UTF-8 JSON datasource.

Default output:

```text
data/pwa/feed.json
```

Schema:

```json
{
  "version": "1.0",
  "generated_at": "...",
  "count": 1,
  "items": [
    {
      "id": "...",
      "source_id": "...",
      "title": "...",
      "content": "...",
      "original_url": "...",
      "url": "...",
      "published_at": "...",
      "rewrite_status": "completed",
      "published_outputs": [],
      "pipeline_metadata": {}
    }
  ]
}
```

The publisher prefers `rewritten_content` and falls back to the original article content. Writes are atomic through a temporary file followed by `os.replace`, reducing the chance of a frontend reading a partially written JSON file.

## RSS

`RSSPublisher` now generates a real RSS 2.0 document.

Default output:

```text
data/rss/feed.xml
```

Each article is emitted as an RSS `<item>` with:

- `title`
- `link`
- `guid`
- `description`
- `pubDate`

The publisher prefers rewritten content and emits UTF-8 XML with an XML declaration. Output writes are atomic.

## PublisherModule integration

`PublisherModule` now initializes and owns both publishers independently:

```text
PublisherModule
├── EitaaPublisher
├── PWAPublisher
└── RSSPublisher
```

PWA and RSS can be enabled independently. Neither requires Eitaa, YasinHub, or Yasin-Agent.

`publish_all()` provides a common boundary for publishing an article collection to the enabled output channels.

## Configuration

```yaml
publisher:
  eitaa:
    enabled: false
  pwa:
    enabled: false
    output_path: "data/pwa/feed.json"
    base_url: ""
  rss:
    enabled: false
    output_path: "data/rss/feed.xml"
    title: "YasinFeed"
    link: "http://127.0.0.1:8000/api/feed"
    description: "YasinFeed published news"
```

The outputs remain disabled by default, preserving safe installation behavior. They can be enabled independently through the existing configuration/environment override system.

## Tests added

`tests/test_publishers.py` covers:

1. PWA JSON generation and persistence.
2. RSS 2.0 generation and XML parsing.
3. Rewritten-content preference.
4. Empty-feed generation.
5. Output-directory creation.

## Architectural decision

YasinFeed remains the owner of publishing implementations. YasinHub and Yasin-Agent remain external control/orchestration components. This preserves independent operation of each service as previously agreed.
