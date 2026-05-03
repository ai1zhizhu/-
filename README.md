# 请假登记程序

一个简单的命令行请假登记程序，支持：

- 新增请假记录
- 查看请假记录
- 数据持久化到 `leave_records.json`

## 运行方式

```bash
python3 leave_register.py
```

## 输入说明

- 日期格式为 `YYYY-MM-DD`
- 程序会校验开始日期不能晚于结束日期
