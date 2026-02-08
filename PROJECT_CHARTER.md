# PROJECT CHARTER (プロジェクト憲章)

## 最終ゴール
Python + (CrewAI or LangGraph) を中核にして、OpenAI / Claude / Gemini API と OpenInterpreter / OpenClaw を統合した
「最強の自律型AI開発チーム」を、あなた（CEO）のPC環境で動かす。

## いま到達している地点（ログから確定）
- docker compose の api/runner が起動し、localhost:8010 の openapi.json が 200 OK で返る
- /workspace/generated_app で ruff / pytest が通り、テストは 2 passed まで到達
- 認証フロー（/register, /login, /me）を含む FastAPI の最小機能が実装・テスト通過

## 決定していること
- Docker Compose で開発・テストを回す
- ruff と pytest を品質ゲートにする
- sqlite + DATABASE_PATH でテストDBを差し替える
- FastAPI の認証フローは最低限 /register /login /me を持つ

## 未決定事項（重要）
- CrewAI と LangGraph のどちらを中核にするか
- OpenAI / Claude / Gemini のAPIキー管理（dotenv/環境変数/secret管理）
- 自律型AI開発チームの役割設計とワークフロー（計画→実装→テスト→修正→完了）
- OpenInterpreter / OpenClaw をどの権限と安全ルールで組み込むか
- “AI-ORG Dashboard” の最終仕様（何を可視化・制御するか）

## 次にやること（候補）
1) 設定管理の標準化（.env + settings）
2) エージェント基盤の決定（CrewAI or LangGraph）
3) 最小の自律ループを実装（要件→実装→テスト→修正）
4) OpenClaw/OpenInterpreter を安全に統合（権限・ログ・ブロックルール）
