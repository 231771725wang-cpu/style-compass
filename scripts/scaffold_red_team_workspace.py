#!/usr/bin/env python3
"""Scaffold a repeatable red-team workspace for style-compass evals."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "eval"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def review_template(eval_item: dict) -> str:
    return f"""# {eval_item['slug']} 评审记录

## 基本信息
- 组别：{eval_item.get('group', '未分组')}
- Prompt：{eval_item['prompt']}
- 预期：{eval_item['expected_output']}

## 人工评分
- 发现性：
- 推荐可信度：
- 候选区分度：
- 产物可交接性：
- 诚实度 / 不装懂：

## 与 baseline 对比
- 明显更好：
- 没有明显更好：
- 反而更差：

## 证据
- 关键片段：
- 最大问题：
- 是否需要立即修：

## 结论
- 风险级别：
- 是否通过：
- 修复提示：
"""


def with_skill_runbook(skill_path: Path, eval_dir: Path, eval_item: dict) -> str:
    return f"""执行 this task:
- Skill path: {skill_path}
- Task: {eval_item['prompt']}
- Input files: none
- Save outputs to: {eval_dir / 'with_skill' / 'outputs'}
- Outputs to save:
  - 风格卡 Markdown 或最终推荐结果
  - 如果有：DESIGN.md / UI-REFACTOR.md
  - 如果有：结构化 handoff prompt

要求：
- 必须走真实 style-compass 流程
- 不允许只用一句总结替代推荐链
- 缺信息时必须诚实表达置信度和边界
"""


def baseline_runbook(eval_dir: Path, eval_item: dict) -> str:
    return f"""执行 this task:
- Task: {eval_item['prompt']}
- No skill path
- Input files: none
- Save outputs to: {eval_dir / 'baseline' / 'outputs'}
- Outputs to save:
  - 普通回答或最小流程输出

要求：
- 不依赖 style-compass
- 保留对比价值，不故意做差
- 输出尽量接近真实“没有这个 skill 时会怎么回”
"""


def workspace_readme(iteration_dir: Path, evals: list[dict]) -> str:
    groups: dict[str, int] = {}
    for item in evals:
        groups[item.get("group", "未分组")] = groups.get(item.get("group", "未分组"), 0) + 1
    group_lines = "\n".join(f"- {group}：{count} 条" for group, count in groups.items())
    return f"""# style-compass 红队工作区

- 当前迭代：`{iteration_dir.name}`
- Eval 总数：{len(evals)}

## 分组统计
{group_lines}

## 目录约定

- `eval-xx-<slug>/prompt.txt`：原始用户说法
- `eval-xx-<slug>/eval_metadata.json`：结构化元数据
- `eval-xx-<slug>/with_skill/outputs/`：使用 style-compass 的真实产物
- `eval-xx-<slug>/baseline/outputs/`：无 skill baseline
- `eval-xx-<slug>/review.md`：人工评审
- `eval-xx-<slug>/verdict.json`：结构化结论

## Stop-Ship

- 任意 `P0`：不开源，先修
- 高频 `P1`：列入首轮修复清单
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--evals",
        default=str(Path(__file__).resolve().parents[1] / "evals" / "evals.json"),
        help="Path to evals.json",
    )
    parser.add_argument(
        "--workspace",
        default=str(Path(__file__).resolve().parents[2] / "style-compass-workspace"),
        help="Workspace root path",
    )
    parser.add_argument("--iteration", default="iteration-1", help="Iteration directory name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    evals_path = Path(args.evals)
    payload = json.loads(evals_path.read_text(encoding="utf-8"))
    evals = payload["evals"]

    skill_path = evals_path.parents[1]
    workspace_root = Path(args.workspace)
    iteration_dir = workspace_root / args.iteration
    iteration_dir.mkdir(parents=True, exist_ok=True)

    write_text(workspace_root / "README.md", workspace_readme(iteration_dir, evals))

    created = 0
    skipped = 0
    for item in evals:
        slug = item.get("slug") or slugify(str(item["id"]))
        eval_name = f"eval-{int(item['id']):02d}-{slug}"
        eval_dir = iteration_dir / eval_name

        files = {
            eval_dir / "prompt.txt": item["prompt"] + "\n",
            eval_dir / "eval_metadata.json": json.dumps(
                {
                    "eval_id": item["id"],
                    "eval_name": eval_name,
                    "group": item.get("group"),
                    "prompt": item["prompt"],
                    "expected_output": item.get("expected_output", ""),
                    "review_focus": item.get("review_focus", []),
                    "assertions": item.get("assertions", []),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            eval_dir / "review.md": review_template(item),
            eval_dir / "verdict.json": json.dumps(
                {
                    "eval_name": eval_name,
                    "risk_level": None,
                    "pass": None,
                    "primary_failure_mode": None,
                    "evidence": [],
                    "fix_hint": None,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            eval_dir / "with_skill" / "run.md": with_skill_runbook(skill_path, eval_dir, item),
            eval_dir / "baseline" / "run.md": baseline_runbook(eval_dir, item),
            eval_dir / "with_skill" / "outputs" / ".gitkeep": "",
            eval_dir / "baseline" / "outputs" / ".gitkeep": "",
        }

        for path, content in files.items():
            if path.exists() and not args.force:
                skipped += 1
                continue
            write_text(path, content)
            created += 1

    print(json.dumps({"created": created, "skipped": skipped, "eval_count": len(evals)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
