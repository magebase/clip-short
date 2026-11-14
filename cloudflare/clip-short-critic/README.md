# clip-short-critic Worker

Cloudflare Worker + D1 + R2 persistence for Muse Spark critique records, findings, edit trajectories, and preference labels.

## Create resources

```bash
npx wrangler d1 create clip-short-critic
npx wrangler r2 bucket create clip-short-critic-assets
npx wrangler secret put CRITIC_TOKEN
```

Copy the D1 `database_id` into `wrangler.toml`, then:

```bash
npm install
npx wrangler d1 execute clip-short-critic --file=schema.sql --remote
npx wrangler deploy
```

## Client env

```bash
export CLIP_SHORT_CRITIC_WORKER_URL="https://clip-short-critic.<account>.workers.dev"
export CLIP_SHORT_CRITIC_TOKEN="same-secret"
```

`muse_spark_critic.py` uploads the MP4 to R2 and records the critique + findings in D1 when these are set. Without them, the critique JSON remains local only.

## Endpoints

- `GET /health`
- `GET /api/model`
- `PUT /api/assets/:key`
- `GET /api/assets/:key`
- `POST /api/critiques`
- `GET /api/critiques?video_sha=...`
- `POST /api/trajectories`
- `POST /api/preferences`

All `/api/*` routes require `Authorization: Bearer $CRITIC_TOKEN`.
