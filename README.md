```markdown
# PCT (Point Cloud Transformer) for ModelNet40 Classification

本仓库提供基于 **Jittor** 框架的 PCT 模型实现，用于 ModelNet40 三维点云形状分类任务。  
代码为计图比赛示例基线，可直接运行训练并生成测试集预测结果 `result.json`。

---

## 环境安装

- Python 版本：**3.8+**
- 依赖安装：
```bash
pip install jittor numpy
```

需要使用 GPU，请参照 [Jittor 官方文档](https://cg.cs.tsinghua.edu.cn/jittor/) 安装 CUDA 版本。

---

## 数据准备

### 数据集格式
- 训练集：`data/train_points.npy`（形状 `(N, 2048, 3)`）和 `data/train_labels.npy`（形状 `(N,)`）
- 测试集：`data/test_points.npy`（形状 `(N_test, 2048, 3)`，无标签）

### 下载与存放
请自行下载 ModelNet40 预处理后的 `.npy` 文件，并放置于同一目录下（例如 `./data/`）。  
目录结构示例：
```
data/
├── train_points.npy
├── train_labels.npy
└── test_points.npy
```

### 数据路径配置
通过命令行参数 `--data_dir` 指定数据根目录。

---

## 训练

运行以下命令开始训练（会自动进行测试集推理并生成 `result.json`）：

```bash
python run_jittor.py --data_dir /path/to/your/data --epochs 200 --batch_size 32 --lr 0.01
```

**可用参数**（均带有默认值）：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--data_dir` | str | `./data` | 数据目录 |
| `--n_points` | int | `1024` | 采样点数量 |
| `--batch_size` | int | `32` | 批大小 |
| `--epochs` | int | `2` | 训练轮数（请自行调大） |
| `--lr` | float | `0.01` | 初始学习率 |
| `--seed` | int | `42` | 随机种子 |

> **注意**：代码中默认只训练 2 个 epoch，仅为演示。正式训练建议设置 `--epochs 200` 以上。

---

## 评测/推理

训练结束后，程序会自动对测试集进行预测并保存 `result.json`。  
若需要单独对已保存的模型进行推理，可修改 `main()` 函数中的模型加载部分，或直接运行训练脚本（会重新训练并推理）。

生成的 `result.json` 格式为：
```json
{
  "0": 12,
  "1": 5,
  ...
}
```
键为样本索引（字符串），值为预测类别（0~39）。

---

## 结果说明

- **训练指标**：交叉熵损失（Loss）和训练集准确率（Acc，%），每个 epoch 输出。
- **最终提交**：`result.json` 文件用于线上评测。
- **注意事项**：
  - 由于测试集无标签，本代码不计算测试集准确率。
  - 线上最终成绩可能与本机训练准确率存在差异（原因包括数据增强、随机采样、模型初始化等），本基线仅作为参考。

---

## 代码结构

```
.
├── configs/                  # 配置文件目录
│   └── train_base.yaml       # 训练配置参考
├── outputs/                  # 输出目录（日志、模型、结果）
│   ├── .         # 日志
│   ├── pct_model.pkl         # 输出模型
│   └── result.json           # 测试集预测结果（自动生成）
├── tool/                     # 工具脚本
│   └── Data_Analysis.py      # 数据分析工具
├── .gitignore                # Git 忽略文件
├── LICENSE                   # 许可证
├── README.md                 # 本文档
├── requirements.txt          # 依赖列表
└── run_jittor.py             # 主程序（含数据集、模型、训练、推理）
```

---

## 可复现性说明

- 随机种子已固定（`--seed 42`），使用 Jittor 和 NumPy 的全局种子。
- 训练日志直接输出到终端，如需落盘可重定向：`python run_jittor.py ... > train.log 2>&1`。
- 所有关键超参数均通过命令行暴露，便于记录。

---

## 依赖与许可

- 本代码基于 Jittor 框架，参考了 PCT 原始论文实现。
- 代码采用 **MIT License**，详见 `LICENSE` 文件。

---
