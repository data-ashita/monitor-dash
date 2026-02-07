# Task Logs Dashboard

## 📊 概述

这是一个基于 Streamlit 的专业 Dashboard，用来可视化和分析 Supabase 中的任务执行日志。

### 主要功能

- ✅ **关键指标**：总运行次数、成功/失败数、成功率
- 📈 **执行趋势**：每日执行次数、成功/失败分布
- 📋 **脚本统计**：每个脚本的执行情况统计
- 🌐 **运行源分析**：GitHub Actions vs 本地执行对比
- 📝 **详细日志**：可过滤的日志表格
- 🚨 **错误分析**：错误追踪和排名
- ⏱️ **性能分析**：脚本执行时间统计

---

## 🚀 快速开始

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2：配置环境变量

1. 复制 `.env.example` 为 `.env`
2. 填入你的 Supabase Logger 项目凭证：

```ini
LOGGER_SUPABASE_URL="https://your-project.supabase.co"
LOGGER_SUPABASE_KEY="your-anon-key"
```

### 步骤 3：运行 Dashboard

```bash
streamlit run app.py
```

Dashboard 会在浏览器中打开，地址通常是 `http://localhost:8501`

---

## 📋 功能说明

### 1. 关键指标（顶部）

| 指标 | 说明 |
| :--- | :--- |
| 总运行次数 | 所有脚本的总执行次数 |
| 成功 | 执行成功的次数 |
| 失败 | 执行失败的次数 |
| 成功率 | 成功执行的百分比 |
| 脚本数 | 不同脚本的数量 |

### 2. 执行趋势

- **每日执行次数趋势**：显示每天的执行次数变化
- **执行结果分布**：成功和失败的比例

### 3. 脚本执行统计

显示每个脚本的：
- 成功次数
- 失败次数
- 总次数
- 成功率

### 4. 运行源分布

- **运行源分布**：本地执行 vs GitHub Actions 执行
- **脚本按运行源分布**：每个脚本在不同运行源的执行情况

### 5. 详细日志

可以按以下条件过滤日志：
- 脚本名称
- 日志级别（INFO、ERROR、CRITICAL）
- 运行源（local、github）

### 6. 错误分析

- **最近的错误**：显示最近 5 个错误的详细信息
- **错误脚本排名**：显示错误最多的脚本

### 7. 性能分析

- **平均执行时间**：所有脚本的平均执行时间
- **最长执行时间**：执行时间最长的脚本
- **执行时间分布**：每个脚本的执行时间分布（箱线图）

---

## 🔧 配置选项

### 侧边栏设置

- **时间范围**：选择显示最近几天的数据（1-30 天）
- **刷新按钮**：手动刷新数据

---

## 📊 数据来源

Dashboard 从 Supabase 的 `task_logs` 表中读取数据。

### 表结构

| 列名 | 类型 | 说明 |
| :--- | :--- | :--- |
| id | int | 记录 ID |
| timestamp | timestamp | 记录时间 |
| task_name | text | 脚本名称 |
| level | text | 日志级别（INFO、ERROR、CRITICAL） |
| message | text | 日志消息 |
| metadata | json | 元数据（已弃用） |
| run_source | text | 运行源（local、github） |
| details | jsonb | 详细信息（JSON） |

---

## 💡 使用技巧

### 1. 定期检查 Dashboard

建议每天检查一次 Dashboard，以监控脚本的执行情况。

### 2. 关注错误

重点关注"错误分析"部分，及时发现和解决问题。

### 3. 性能优化

查看"性能分析"部分，识别执行时间过长的脚本，进行优化。

### 4. 对比分析

使用时间范围选择器，对比不同时期的执行情况。

---

## 🆘 故障排除

### 问题 1：无法连接到 Supabase

**错误信息：** `❌ 错误：Supabase 凭证未配置`

**解决方案：**
1. 检查 `.env` 文件是否存在
2. 检查 `LOGGER_SUPABASE_URL` 和 `LOGGER_SUPABASE_KEY` 是否正确填写
3. 检查网络连接

### 问题 2：没有数据显示

**症状：** Dashboard 显示"没有数据"

**解决方案：**
1. 确保已有脚本执行记录
2. 检查时间范围设置
3. 确保脚本已正确记录到 Supabase

### 问题 3：Dashboard 加载缓慢

**症状：** Dashboard 响应速度慢

**解决方案：**
1. 减少时间范围（选择较少的天数）
2. 检查网络连接速度
3. 重启 Streamlit 应用

### 问题 4：图表显示不正常

**症状：** 图表无法正常显示

**解决方案：**
1. 清除浏览器缓存
2. 刷新页面
3. 尝试使用不同的浏览器

---

## 📈 数据刷新

Dashboard 会自动缓存数据 60 秒。如果需要立即看到最新数据，可以：

1. 点击侧边栏的"🔄 刷新数据"按钮
2. 按 `F5` 刷新浏览器
3. 等待 60 秒后自动刷新

---

## 🎨 自定义

### 修改时间范围

在 `app.py` 中修改：

```python
days = st.slider(
    "选择时间范围（天）",
    min_value=1,
    max_value=30,  # 修改这个值
    value=7,
    step=1
)
```

### 修改缓存时间

在 `app.py` 中修改：

```python
@st.cache_data(ttl=60)  # 修改这个值（秒）
def fetch_task_logs(days=7):
    ...
```

### 修改颜色

在 `app.py` 中修改颜色定义：

```python
colors = {'INFO': '#00CC96', 'ERROR': '#EF553B', 'CRITICAL': '#AB63FA'}
```

---

## 📚 依赖库

- **streamlit**: Web 应用框架
- **pandas**: 数据处理
- **plotly**: 交互式图表
- **python-dotenv**: 环境变量管理
- **supabase**: Supabase Python 客户端

---

## 🔗 相关资源

- [Streamlit 官方文档](https://docs.streamlit.io/)
- [Plotly 官方文档](https://plotly.com/python/)
- [Supabase 官方文档](https://supabase.com/docs)
- [Pandas 官方文档](https://pandas.pydata.org/docs/)

---

## 📝 许可证

MIT License

---

## 💬 反馈

如有问题或建议，欢迎提出！
