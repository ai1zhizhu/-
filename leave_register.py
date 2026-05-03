#!/usr/bin/env python3
"""简单的请假登记程序（命令行版）。"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("leave_records.json")
DATE_FMT = "%Y-%m-%d"


@dataclass
class LeaveRecord:
    name: str
    department: str
    leave_type: str
    start_date: str
    end_date: str
    reason: str
    created_at: str


def load_records() -> list[LeaveRecord]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)
    return [LeaveRecord(**item) for item in raw]


def save_records(records: list[LeaveRecord]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump([asdict(record) for record in records], f, ensure_ascii=False, indent=2)


def validate_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, DATE_FMT)
        return True
    except ValueError:
        return False


def register_leave() -> None:
    print("\n=== 新增请假记录 ===")
    name = input("姓名：").strip()
    department = input("部门：").strip()
    leave_type = input("请假类型（事假/病假/年假等）：").strip()

    while True:
        start_date = input("开始日期（YYYY-MM-DD）：").strip()
        end_date = input("结束日期（YYYY-MM-DD）：").strip()
        if not (validate_date(start_date) and validate_date(end_date)):
            print("日期格式不正确，请按 YYYY-MM-DD 输入。")
            continue
        if start_date > end_date:
            print("开始日期不能晚于结束日期。")
            continue
        break

    reason = input("请假原因：").strip()

    record = LeaveRecord(
        name=name,
        department=department,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    records = load_records()
    records.append(record)
    save_records(records)
    print("\n✅ 请假记录已保存。")


def list_records() -> None:
    print("\n=== 请假记录列表 ===")
    records = load_records()
    if not records:
        print("暂无记录。")
        return

    for idx, r in enumerate(records, start=1):
        print(
            f"{idx}. {r.name} | {r.department} | {r.leave_type} | "
            f"{r.start_date} 至 {r.end_date} | 原因：{r.reason} | 登记时间：{r.created_at}"
        )


def main() -> None:
    while True:
        print("\n===== 请假登记系统 =====")
        print("1. 新增请假记录")
        print("2. 查看请假记录")
        print("3. 退出")
        choice = input("请选择（1/2/3）：").strip()

        if choice == "1":
            register_leave()
        elif choice == "2":
            list_records()
        elif choice == "3":
            print("已退出。")
            break
        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()
