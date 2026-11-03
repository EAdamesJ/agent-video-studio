# Export and publishing

Every render creates a ready-to-share folder with MP4, SRT/VTT captions, thumbnail, social metadata, and an editable project JSON. Direct posting is optional and always starts with a platform preflight.

## YouTube

1. Create an OAuth desktop client in Google Cloud and enable YouTube Data API v3.
2. Set `YOUTUBE_CLIENT_SECRET_FILE` to the downloaded client JSON path.
3. Install `agent-video-studio[youtube]`.
4. In the web app, open a rendered export, review its title/description/privacy, then choose **Publish**.

The first upload opens Google's local OAuth flow and requests the YouTube upload scope. The default privacy is private. The uploader uses the official [`videos.insert`](https://developers.google.com/youtube/v3/docs/videos/insert) endpoint.

## TikTok

1. Register an app and add TikTok's Content Posting API product.
2. Request and obtain the `video.publish` scope for the user's account.
3. Set `TIKTOK_ACCESS_TOKEN` locally.
4. Run preflight to retrieve the creator's available privacy options, then select one and confirm the post.

The connector uses the official [Direct Post flow](https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post). TikTok restricts unaudited clients to private visibility; the connector does not claim public posting is available until the platform allows it. AI-generated content is labeled when `ai_generated` is enabled.

## Instagram Reels

1. Use an eligible Instagram professional account and a Meta app with content-publishing permission.
2. Set `INSTAGRAM_GRAPH_TOKEN`, `INSTAGRAM_ACCOUNT_ID`, `INSTAGRAM_GRAPH_HOST`, and the currently supported `AVS_META_GRAPH_VERSION`.
3. Configure `AVS_PUBLIC_MEDIA_BASE_URL` to a public HTTPS origin that serves the app's export endpoint as a direct MP4 response.
4. Run preflight, then review the caption/feed choice and confirm.

The connector creates a Reels media container from the public video URL, polls its processing state, then calls `media_publish`, following [Meta's Instagram API collection](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api). A local `localhost` URL cannot be fetched by Meta; configure a trusted public origin if using direct publishing.

## Confirmation and retries

Preflight reports missing credentials and platform requirements without uploading. A separate publish action is required. A network interruption can leave an upload processing at the platform; check the platform before retrying to avoid duplicate posts.

Scheduling, account management, and credential acquisition through a hosted service are not part of the local 0.1 workflow. Tokens remain under operator control.
