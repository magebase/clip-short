export interface Env {
  DB: D1Database;
  BUCKET: R2Bucket;
  CRITIC_TOKEN: string;
  CRITIC_MODEL: string;
  CRITIC_PROVIDER: string;
  CRITIC_EFFORT: string;
}

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "access-control-allow-origin": "*" } });

const authorized = (request: Request, env: Env) =>
  request.headers.get("authorization") === `Bearer ${env.CRITIC_TOKEN}`;

const sha256 = async (data: ArrayBuffer) => {
  const digest = await crypto.subtle.digest("SHA-256", data);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { "access-control-allow-origin": "*", "access-control-allow-methods": "GET,POST,PUT,OPTIONS", "access-control-allow-headers": "authorization,content-type" } });
    }
    if (url.pathname === "/health") {
      return json({ ok: true, model: env.CRITIC_MODEL, provider: env.CRITIC_PROVIDER, effort: env.CRITIC_EFFORT });
    }
    if (url.pathname === "/api/model") {
      return json({ model: env.CRITIC_MODEL, provider: env.CRITIC_PROVIDER, requested_effort: env.CRITIC_EFFORT, fallback: false, ensembles: false });
    }
    if (!authorized(request, env)) {
      return json({ error: "unauthorized" }, 401);
    }

    if (request.method === "PUT" && url.pathname.startsWith("/api/assets/")) {
      const key = decodeURIComponent(url.pathname.slice("/api/assets/".length));
      if (!key || !request.body) return json({ error: "asset key and body required" }, 400);
      const data = await request.arrayBuffer();
      const digest = await sha256(data);
      await env.BUCKET.put(key, data, { httpMetadata: { contentType: request.headers.get("content-type") || "application/octet-stream" } });
      await env.DB.prepare("INSERT OR REPLACE INTO assets (key, sha256, content_type, size, created_at) VALUES (?, ?, ?, ?, ?)")
        .bind(key, digest, request.headers.get("content-type"), data.byteLength, new Date().toISOString()).run();
      return json({ key, sha256: digest, size: data.byteLength });
    }

    if (request.method === "GET" && url.pathname.startsWith("/api/assets/")) {
      const key = decodeURIComponent(url.pathname.slice("/api/assets/".length));
      const object = await env.BUCKET.get(key);
      if (!object) return json({ error: "not_found" }, 404);
      return new Response(object.body, { headers: { "content-type": object.httpMetadata?.contentType || "application/octet-stream", "access-control-allow-origin": "*" } });
    }

    if (request.method === "POST" && url.pathname === "/api/critiques") {
      const body = await request.json<any>();
      const record = body.record || {};
      const critique = body.critique || {};
      const id = crypto.randomUUID();
      const findings = critique.findings || [];
      await env.DB.prepare(
        "INSERT INTO critiques (id, video_sha256, model, provider, effort, decision, editorial_score, request_id, r2_key, payload_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
      ).bind(
        id, record.video_sha256 || "", record.model || "", record.provider || "", record.confirmed_effort || "",
        critique.overall?.decision || "HUMAN_REVIEW", critique.overall?.editorial_score ?? null,
        record.request_id || null, body.r2_key || null, JSON.stringify(body), new Date().toISOString()
      ).run();
      const statements = findings.map((finding: any) =>
        env.DB.prepare("INSERT INTO critique_findings (critique_id, timestamp_sec, severity, category, evidence, explanation) VALUES (?, ?, ?, ?, ?, ?)")
          .bind(id, finding.timestamp_sec ?? null, finding.severity || "MAJOR", finding.category || "general", finding.evidence || "", finding.explanation || "")
      );
      if (statements.length) await env.DB.batch(statements);
      return json({ id, findings: findings.length }, 201);
    }

    if (request.method === "GET" && url.pathname === "/api/critiques") {
      const videoSha = url.searchParams.get("video_sha");
      const query = videoSha
        ? env.DB.prepare("SELECT id, video_sha256, model, effort, decision, editorial_score, created_at FROM critiques WHERE video_sha256 = ? ORDER BY created_at DESC LIMIT 50").bind(videoSha)
        : env.DB.prepare("SELECT id, video_sha256, model, effort, decision, editorial_score, created_at FROM critiques ORDER BY created_at DESC LIMIT 50");
      const { results } = await query.all();
      return json({ results });
    }

    if (request.method === "POST" && url.pathname === "/api/trajectories") {
      const body = await request.json<any>();
      const id = crypto.randomUUID();
      await env.DB.prepare(
        "INSERT INTO edit_trajectories (id, video_id, query_id, action_id, features_json, label, label_provenance, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
      ).bind(id, body.video_id, body.query_id, body.action_id, JSON.stringify(body.features || {}), body.label, body.label_provenance, new Date().toISOString()).run();
      return json({ id }, 201);
    }

    if (request.method === "POST" && url.pathname === "/api/preferences") {
      const body = await request.json<any>();
      const id = crypto.randomUUID();
      await env.DB.prepare(
        "INSERT INTO preference_labels (id, query_id, winner_action_id, loser_action_id, reviewer_id, note, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
      ).bind(id, body.query_id, body.winner_action_id, body.loser_action_id, body.reviewer_id, body.note || null, new Date().toISOString()).run();
      return json({ id }, 201);
    }

    return json({ error: "not_found" }, 404);
  },
};
