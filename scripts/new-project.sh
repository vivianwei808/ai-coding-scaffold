#!/bin/bash
# 从本模板新建一个 AI 编码项目
# 用法: ./scripts/new-project.sh <目标路径>
set -e

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="$1"
[ -z "$DST" ] && { echo "用法: $0 <目标路径>"; exit 1; }
[ -e "$DST" ] && { echo "目标已存在: $DST"; exit 1; }

mkdir -p "$DST"
# 复制模板（排除 git 历史与本脚本自身的运行残留）
rsync -a --exclude '.git' "$SRC/" "$DST/"

# 清理模板作者的身份残留：示例任务、开发者配置、会话日志/索引
rm -rf "$DST/.trellis/tasks/00-bootstrap-guidelines" 2>/dev/null
rm -f  "$DST/.trellis/.developer" 2>/dev/null
rm -rf "$DST/.trellis/workspace/"*/ 2>/dev/null

echo "✅ 新项目已创建: $DST"
echo "下一步:"
echo "  cd $DST && git init && git add -A && git commit -m 'init: from scaffold'"
echo "  打开 Claude Code（claude），首次会话 Trellis 会询问你的开发者名（用于 workspace 日志目录）"
echo "  然后说: /setup-matt-pocock-skills 完成技能初始化（三个问题都可选 local files / 默认）"
echo "  详细用法见 $DST/GUIDE.md"
