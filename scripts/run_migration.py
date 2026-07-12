"""用项目自带的 SQLAlchemy 引擎执行迁移 SQL 文件（mysql CLI 不在 PATH 时用）。

用法：python scripts/run_migration.py database/migration_color_fee_model.sql
逐句执行，遇到 "Duplicate column" 之类的幂等错误跳过并提示。
"""
import sys
import io
import os
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 让 import app.* 生效：把 backend 加入 sys.path
HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.join(HERE, "..", "backend")
sys.path.insert(0, os.path.abspath(BACKEND))

from sqlalchemy import text  # noqa: E402
from app.database import engine  # noqa: E402


def split_statements(sql: str):
    """去掉行注释后按分号切分（简单场景够用，无存储过程）。"""
    lines = []
    for ln in sql.splitlines():
        s = ln.strip()
        if s.startswith("--") or not s:
            continue
        lines.append(ln)
    body = "\n".join(lines)
    return [st.strip() for st in body.split(";") if st.strip()]


def main():
    if len(sys.argv) < 2:
        sys.exit("用法: python scripts/run_migration.py <sql文件>")
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        sql = f.read()

    stmts = split_statements(sql)
    print(f"共 {len(stmts)} 条语句，开始执行 {path}")
    with engine.begin() as conn:
        for i, st in enumerate(stmts, 1):
            preview = re.sub(r"\s+", " ", st)[:70]
            try:
                conn.execute(text(st))
                print(f"  [{i}] OK  {preview}")
            except Exception as e:
                msg = str(e).split("\n")[0]
                # 幂等错误容忍：重复列、USE 语句在部分驱动下的告警
                if "Duplicate column" in msg or "1060" in msg:
                    print(f"  [{i}] 跳过(列已存在)  {preview}")
                else:
                    print(f"  [{i}] 失败  {preview}\n      -> {msg}")
                    raise
    print("迁移完成。")


if __name__ == "__main__":
    main()
