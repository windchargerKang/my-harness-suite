# 数据库与 SQL 规范

## 基本规则

- **不允许无条件 UPDATE / DELETE**
- 批量更新必须明确 WHERE 条件和影响范围
- 分页查询必须明确排序条件
- 不允许在高频接口中引入明显的 N+1 查询
- 修改 Mapper / XML / SQL 时，必须关注索引命中情况

## 必须说明的内容

以下场景必须在 design.md 或 review 摘要中说明：

- 是否影响索引
- 是否会放大扫描范围
- 是否会引入锁竞争
- 是否需要数据修复或迁移
- 是否影响历史数据兼容性

## SQL 编写规范

### SELECT

```sql
-- ✅ 正确：明确列出需要的字段
SELECT id, name, status FROM user WHERE id = ?;

-- ❌ 错误：使用 SELECT *
SELECT * FROM user WHERE id = ?;
```

### UPDATE

```sql
-- ✅ 正确：带有 WHERE 条件
UPDATE user SET status = 1 WHERE id = ?;

-- ❌ 错误：无条件更新
UPDATE user SET status = 1;
```

### DELETE

```sql
-- ✅ 正确：带有 WHERE 条件
DELETE FROM user WHERE id = ?;

-- ❌ 错误：无条件删除
DELETE FROM user;
```

### 批量操作

```sql
-- ✅ 正确：有限制条件
UPDATE order SET status = 1 WHERE id IN (?, ?, ?) AND status = 0;

-- ❌ 错误：无范围限制的批量更新
UPDATE order SET status = 1 WHERE status = 0;  -- 可能影响大量数据
```

## 高风险目录

- `**/src/main/resources/mapper/`
- `**/src/main/resources/db/`
- `sql/`

修改以上目录内容时需额外谨慎。

## 索引设计原则

1. **区分度**高的字段优先
2. **避免**在频繁更新的字段上建索引
3. **复合索引**遵循最左前缀原则
4. **定期**检查慢查询，评估索引有效性
