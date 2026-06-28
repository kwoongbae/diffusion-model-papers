"""Fetch the latest *generative* diffusion-model papers (the DDPM lineage:
arxiv.org/abs/2006.11239 and its descendants — score-based, latent diffusion,
text-to-image, video/audio/3D generation, etc.) from arXiv and append a
structured Korean summary to README.md.

For each paper the summary lists, as bullet points:
  - 논문 종류 (paper type keyword)
  - 목적 (purpose)
  - 방법론 (methodology)
  - 결론 (conclusions)

Papers that merely mention "diffusion" in an unrelated sense (information
diffusion, diffusion MRI, molecular diffusion, ...) are filtered out by an
LLM relevance check.

Runs weekly via .github/workflows/weekly.yml. Requires the GEMINI_API_KEY
environment variable (set as a GitHub Actions secret). Get a free key at
https://aistudio.google.com/apikey (no credit card required).

To switch to a paid provider later (e.g. Anthropic Claude), you only need to
rewrite the `analyze()` function and swap the API-key env var.
"""

import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from google import genai
from google.genai import types

# --- Config ---
README = "README.md"
MARKER = "<!-- LOG -->"
MODEL = "gemini-2.5-flash"  # free-tier model
MAX_PAPERS = 5              # how many relevant papers to keep
CANDIDATE_POOL = 15         # how many recent papers to screen for relevance
SLEEP_SECONDS = 3           # pause between API calls to respect the free-tier rate limit

# arXiv search: diffusion-generation vocabulary within the main ML/CV/AI cats.
# The LLM relevance check below does the precise filtering.
QUERY = (
    '(abs:"diffusion model" OR abs:"denoising diffusion" '
    'OR abs:"score-based generative" OR abs:"latent diffusion" '
    'OR abs:"diffusion probabilistic") '
    'AND (cat:cs.CV OR cat:cs.LG OR cat:cs.AI OR cat:stat.ML)'
)

ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}

# Static instruction block. Kept free of str.format placeholders so the literal
# JSON braces below survive — title/abstract are appended separately.
ANALYZE_INSTRUCTIONS = """다음 arXiv 논문의 제목과 초록을 분석해서 아래 JSON 형식으로만 답하세요. 설명 문장 없이 JSON만 출력하세요.

독자 눈높이 (매우 중요):
- 독자는 디퓨전 모델이 "노이즈를 점점 제거하며 데이터를 생성한다" 정도만 아는 비전공자에 가깝습니다.
- 전문 용어(예: classifier-free guidance, latent space, ODE solver, score function 등)는 그대로 쓰지 말고, 쉬운 우리말로 풀어 쓰거나 괄호로 한 줄 부연하세요. 예: "잠재 공간(이미지를 압축한 작은 표현 공간)".
- 수식이나 약어를 나열하지 말고, "무엇을 왜 했는지"를 직관적으로 설명하세요. 비유를 써도 좋습니다.
- 단, 핵심 정보는 빠뜨리지 말고 정확하게 전달하세요. 쉽게 쓰되 틀리지 않게.

판단 기준:
- is_generative_diffusion: 이 논문이 DDPM, score-based, latent diffusion 등 데이터(이미지·비디오·오디오·3D 등)를 생성하기 위한 "확산 생성모델(generative diffusion model)" 계열과 직접 관련되면 true. 정보 확산(information diffusion), 확산 MRI, 분자 확산 등 생성모델과 무관한 'diffusion'이면 false.
- type: 논문 종류를 한국어 키워드 하나로. 예: "새로운 방법론 제안", "리뷰/서베이", "벤치마크·데이터셋", "이론 분석", "응용 연구", "효율화·가속".
- purpose: 이 논문이 풀려는 문제와 목적 (한국어 한 문장).
- methods: 사용한 핵심 방법론 (한국어, 1~3개 항목의 문자열 리스트).
- conclusions: 핵심 결과와 결론 (한국어, 1~3개 항목의 문자열 리스트).

JSON 형식:
{"is_generative_diffusion": true, "type": "새로운 방법론 제안", "purpose": "...", "methods": ["...", "..."], "conclusions": ["...", "..."]}"""


def fetch_arxiv(max_results):
    """Return a list of the most recently submitted diffusion-related papers."""
    params = {
        "search_query": QUERY,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": max_results,
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "diffusion-paper-log/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()

    root = ET.fromstring(raw)
    papers = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = " ".join(entry.findtext("atom:title", "", ARXIV_NS).split())
        abstract = " ".join(entry.findtext("atom:summary", "", ARXIV_NS).split())
        published = entry.findtext("atom:published", "", ARXIV_NS)[:10]
        link = entry.findtext("atom:id", "", ARXIV_NS).strip()
        authors = [
            a.findtext("atom:name", "", ARXIV_NS)
            for a in entry.findall("atom:author", ARXIV_NS)
        ]
        papers.append(
            {
                "title": title,
                "abstract": abstract,
                "published": published,
                "link": link,
                "authors": authors,
            }
        )
    return papers


def analyze(client, paper):
    """Ask Gemini to classify + structure one paper. Returns a dict or None."""
    prompt = (
        ANALYZE_INSTRUCTIONS
        + f"\n\n제목: {paper['title']}\n\n초록: {paper['abstract']}"
    )
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        return json.loads(resp.text or "{}")
    except Exception as e:  # noqa: BLE001 - skip a bad paper rather than crash the run
        print(f"분석 실패 (건너뜀): {paper['title'][:50]} ({e})", file=sys.stderr)
        return None


def format_block(items, today):
    """Render the week's papers as a markdown section with bullet points."""
    lines = [f"## {today} 주간 요약\n"]
    for paper, info in items:
        authors = ", ".join(paper["authors"][:3])
        if len(paper["authors"]) > 3:
            authors += " 외"
        lines.append(f"### [{paper['title']}]({paper['link']})")
        lines.append(f"*{authors} · {paper['published']}*\n")
        lines.append(f"**🏷️ 논문 종류:** {info.get('type', '-')}\n")
        lines.append(f"**🎯 목적:** {info.get('purpose', '-')}\n")
        lines.append("**🔧 방법론**")
        for m in info.get("methods", []) or ["-"]:
            lines.append(f"- {m}")
        lines.append("")
        lines.append("**📌 결론**")
        for c in info.get("conclusions", []) or ["-"]:
            lines.append(f"- {c}")
        lines.append("")
    return "\n".join(lines)


def update_readme(block):
    with open(README, "r", encoding="utf-8") as f:
        content = f.read()
    if MARKER not in content:
        raise SystemExit(f"README.md에 '{MARKER}' 마커가 없습니다.")
    head, tail = content.split(MARKER, 1)
    new = f"{head}{MARKER}\n\n{block}\n{tail.lstrip()}"
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    candidates = fetch_arxiv(CANDIDATE_POOL)
    if not candidates:
        print("arXiv에서 논문을 찾지 못했습니다.", file=sys.stderr)
        sys.exit(1)

    items = []
    for i, paper in enumerate(candidates):
        if i:
            time.sleep(SLEEP_SECONDS)
        info = analyze(client, paper)
        if info and info.get("is_generative_diffusion"):
            items.append((paper, info))
            print(f"채택: {paper['title'][:60]}")
            if len(items) >= MAX_PAPERS:
                break
        elif info is not None:
            print(f"제외(생성 디퓨전 아님): {paper['title'][:60]}")

    if not items:
        print("관련된 생성 디퓨전 논문을 찾지 못했습니다.", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today().isoformat()
    block = format_block(items, today)
    update_readme(block)
    print(f"{len(items)}편의 논문을 README.md에 추가했습니다.")


if __name__ == "__main__":
    main()
