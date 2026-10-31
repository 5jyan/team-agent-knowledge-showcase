# Available team knowledge infrastructure

You can investigate the team's knowledge using the local Hindsight HTTP API at http://127.0.0.1:8888. `GET /v1/default/banks` lists available banks. Memory search is `POST /v1/default/banks/{bank_id}/memories/recall` with JSON fields `query` and optionally `budget` and `types`.

The existing Git checkout at `../../team-agent-knowledge` contains the team's approved source documents. For any knowledge you intend to rely on, check its source metadata and current Git main, applicability, and limitations before applying it. Treat search output as a lead, not an approval. Do not modify the source repository or the Bank.
