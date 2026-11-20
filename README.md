# 日前出力训练样本的时点联接与撤回

这是本地演练用的合成来源资料。CSV 使用 UTF-8、有首行字段名，空字段表示未提供。除非字段语义明确为零，空值没有数值含义。

## 资料契约

所有时刻为 2026-11 的 UTC 日及 HH:MM。一个预报轮次含 irr 和 cloud 两个字段，同一次 run_id 的向量必须齐全。多个合格轮次按 issued_at 取最近。alias_links 将站号映射到物理样址，shared_asset 用于组间隔离。认定时刻与生效范围为独立轴。标签既有目标段也有量测观察起止，训练标签的观察止点不晚于 split_by_decision_at。withdrawals 只限制所列 scope、站点、时间与用途，目标窗口任何一部分相交即禁止使用该行。allowed_retention=receipt_only 表示可留标识、适用范围和状态，禁止继续读出资料值。

以下文件位于 `data/`。

- `decision_windows.csv`（5 条）：`case_id`、`alias`、`decided_at`、`target_from`、`target_to`
- `alias_links.csv`（5 条）：`alias`、`physical_site`、`shared_asset`、`from_day`、`to_day`、`known_at`、`rev`
- `forecasts.csv`（13 条）：`physical_site`、`target_from`、`target_to`、`run_id`、`issued_at`、`available_at`、`field`、`value`
- `labels.csv`（6 条）：`site`、`target_from`、`target_to`、`observed_from`、`observed_to`、`known_at`、`rev`、`quality`、`mwh`
- `publication_intents.csv`（4 条）：`request`、`cutoff`、`split_by_decision_at`、`train_aliases`、`holdout_aliases`、`purpose`
- `withdrawals.csv`（1 条）：`known_at`、`site`、`target_from`、`target_to`、`scope`、`purpose`、`allowed_retention`

`manifest.json` 记录完整资料包的列名、行数、校验值和跨表引用。完整资料包可含业务冲突或同一来源的多次投递，校验器保留这些原始记录。

## 本地查看

适用 Python 3.11，无需安装第三方库或构建。

```sh
python3 inspect_inputs.py
python3 -m unittest -v test_input_pack
```

查看命令打印各原始表的记录数。单元测试校验资料结构、引用与文件完整性，可离线执行。
