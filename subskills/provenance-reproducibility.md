# Subskill: Provenance and Reproducibility

A Git SHA alone does not prove which implementation rendered the file.

---

## 1. Required Per Output

| Field | Meaning |
| :--- | :--- |
| `git_sha` | Commit used |
| `git_clean` | Worktree clean/dirty at render time |
| `renderer_source_hash` | SHA-256 of the renderer source |
| `dependency_lock_hash` | Lockfile hash |
| `build_config_hash` | Effective configuration hash |
| `output_sha256` | Final MP4 digest |
| `reviewer_version` | Must match artifact version |

## 2. Rules

- Do not use a renderer filename as the version identifier.
- Record per-clip provenance; never aggregate ambiguous scalars at batch level.
- A dirty worktree is reported, not hidden.
- The reviewer version must match the artifact version.

## 3. Codes

- `PROVENANCE_INCOMPLETE`
- `DIRTY_WORKTREE`
- `ARTIFACT_VERSION_MISMATCH`
- `REVIEWER_VERSION_MISMATCH`
- `BATCH_MANIFEST_SINGLE_CLIP_FIELD`
