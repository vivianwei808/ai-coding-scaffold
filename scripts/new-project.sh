#!/bin/bash
# 从本模板新建一个 AI 编码项目
# 用法: ./scripts/new-project.sh <目标路径> [项目名]
set -e

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="$1"
[ -z "$DST" ] && { echo "用法: $0 <目标路径> [项目名]"; exit 1; }
[ -e "$DST" ] && { echo "目标已存在: $DST"; exit 1; }

mkdir -p "$DST"
# 复制模板（排除 git 历史与本脚本自身的运行残留）
rsync -a --exclude '.git' "$SRC/" "$DST/"

# 清理模板携带的示例任务与日志，保持新项目干净
rm -rf "$DST/.trellis/tasks/00-bootstrap-guidelines" 2>/dev/null
find "$DST/.trellis/workspace" -name 'journal-*.md' -delete 2>/dev/null

echo "✅ 新项目已创建: $DST"
echo "下一步:"
echo "  cd $DST"
echo "  打开 Claude Code，说: /setup-matt-pocock-skills 初始化本仓库"
echo "  详细用法见 $DST/GUIDE.md"
