import numpy as np
from scipy.spatial import KDTree
import os


def compute_avg_spacing(points, sample_ratio=0.1):
    """
    计算点云的平均点间距（平均最近邻距离）
    points: (N, 3) 点云数组
    sample_ratio: 由于计算所有点的最近邻耗时，可以随机采样一部分点来计算
    """
    if len(points) == 0:
        return 0.0

    # 随机采样部分点来计算，以提高速度
    n_samples = max(1, int(len(points) * sample_ratio))
    idx = np.random.choice(len(points), n_samples, replace=False)
    sampled_points = points[idx]

    # 构建 KDTree 加速最近邻搜索
    tree = KDTree(points)
    # 查询每个采样点的最近邻距离（排除自身，所以 k=2）
    dists, _ = tree.query(sampled_points, k=2)
    # dists 的 shape 是 (n_samples, 2)，第二列是到最近邻的距离
    nearest_dists = dists[:, 1]

    return np.mean(nearest_dists)


# =============================================
# 请修改为您的实际数据路径
# =============================================
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, default='./data/train_points.npy')
args = parser.parse_args()
data_path = args.data_path

# 读取数据
if not os.path.exists(data_path):
    print(f"错误：文件 {data_path} 不存在！")
    exit()

data = np.load(data_path)
print(f"数据形状: {data.shape}")  # 预期为 (样本数, 2048, 3)

# 取前 20 个样本计算平均间距（如果样本很多，取一部分即可）
num_samples = min(20, data.shape[0])
spacings = []

for i in range(num_samples):
    points = data[i]  # (2048, 3)
    avg_dist = compute_avg_spacing(points, sample_ratio=0.2)
    spacings.append(avg_dist)

overall_avg_spacing = np.mean(spacings)
print(f"\n点云平均点间距 (基于前 {num_samples} 个样本): {overall_avg_spacing:.6f}")

# =============================================
# 根据间距给出噪声标准差推荐值
# =============================================
print("\n========== 噪声标准差建议 ==========")
print(f"推荐范围 (间距的 2% ~ 5%):")
print(f"  - 最小值: {overall_avg_spacing * 0.02:.6f}")
print(f"  - 推荐值: {overall_avg_spacing * 0.03:.6f}")
print(f"  - 最大值: {overall_avg_spacing * 0.05:.6f}")
print("\n您可以在数据增强中使用类似: np.random.normal(0, 0.003, size=points.shape)")