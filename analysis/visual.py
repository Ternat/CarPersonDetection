import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# 解决中文乱码问题
sys.stdout.reconfigure(encoding='utf-8')

# 设置输出目录
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
os.makedirs(output_dir, exist_ok=True)

# 设置绘图风格 - 兼容不同Matplotlib版本
try:
    plt.style.use('seaborn')
except:
    try:
        plt.style.use('seaborn-v0_8')  # 新版本Matplotlib
    except:
        sns.set_style("whitegrid")  # 如果都不行，使用seaborn的默认样式
sns.set_palette("husl")

# 读取数据
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.csv')
if not os.path.exists(data_path):
    print(f"错误: 找不到结果文件 {data_path}")
    print("请确保:")
    print("1. 文件存在于脚本所在目录")
    print("2. 文件名为'results.csv'")
    exit()

try:
    df = pd.read_csv(data_path)
    print("数据预览:")
    print(df.head())
except Exception as e:
    print(f"读取文件时出错: {str(e)}")
    exit()

# 1. 训练损失变化趋势
plt.figure(figsize=(15, 8))
plt.subplot(2, 2, 1)
plt.plot(df['epoch'], df['train/box_loss'], label='Box Loss')
plt.plot(df['epoch'], df['train/cls_loss'], label='Class Loss')
plt.plot(df['epoch'], df['train/dfl_loss'], label='DFL Loss')
plt.title('Training Losses Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# 2. 验证损失变化趋势
plt.subplot(2, 2, 2)
plt.plot(df['epoch'], df['val/box_loss'], label='Val Box Loss')
plt.plot(df['epoch'], df['val/cls_loss'], label='Val Class Loss')
plt.plot(df['epoch'], df['val/dfl_loss'], label='Val DFL Loss')
plt.title('Validation Losses Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# 3. 评估指标变化趋势
plt.subplot(2, 2, 3)
plt.plot(df['epoch'], df['metrics/precision(B)'], label='Precision')
plt.plot(df['epoch'], df['metrics/recall(B)'], label='Recall')
plt.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50')
plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP50-95')
plt.title('Evaluation Metrics Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Score')
plt.legend()
plt.grid(True)

# 4. 学习率变化
plt.subplot(2, 2, 4)
plt.plot(df['epoch'], df['lr/pg0'], label='Learning Rate')
plt.title('Learning Rate Schedule')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'training_metrics.png'), dpi=300, bbox_inches='tight')
plt.close()

# 关键指标分析
final_metrics = df.iloc[-1][['metrics/precision(B)', 'metrics/recall(B)', 
                            'metrics/mAP50(B)', 'metrics/mAP50-95(B)']]
initial_metrics = df.iloc[0][['metrics/precision(B)', 'metrics/recall(B)', 
                             'metrics/mAP50(B)', 'metrics/mAP50-95(B)']]

analysis_text = f"""关键指标变化分析:
初始值: Precision={initial_metrics[0]:.4f}, Recall={initial_metrics[1]:.4f}, 
mAP50={initial_metrics[2]:.4f}, mAP50-95={initial_metrics[3]:.4f}
最终值: Precision={final_metrics[0]:.4f}, Recall={final_metrics[1]:.4f}, 
mAP50={final_metrics[2]:.4f}, mAP50-95={final_metrics[3]:.4f}
mAP50-95提升: {(final_metrics[3]-initial_metrics[3])/initial_metrics[3]*100:.2f}%
"""

# 损失收敛分析
train_loss = df[['train/box_loss', 'train/cls_loss', 'train/dfl_loss']].sum(axis=1)
val_loss = df[['val/box_loss', 'val/cls_loss', 'val/dfl_loss']].sum(axis=1)

plt.figure(figsize=(12, 6))
plt.plot(df['epoch'], train_loss, label='Total Training Loss')
plt.plot(df['epoch'], val_loss, label='Total Validation Loss')
plt.title('Total Loss Convergence')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'loss_convergence.png'), dpi=300, bbox_inches='tight')
plt.close()

# 最佳epoch分析
best_mAP50_epoch = df['metrics/mAP50(B)'].idxmax()
best_mAP50_95_epoch = df['metrics/mAP50-95(B)'].idxmax()

analysis_text += f"""
最佳性能分析:
最佳mAP50出现在epoch {best_mAP50_epoch+1}, 值为{df.iloc[best_mAP50_epoch]['metrics/mAP50(B)']:.4f}
最佳mAP50-95出现在epoch {best_mAP50_95_epoch+1}, 值为{df.iloc[best_mAP50_95_epoch]['metrics/mAP50-95(B)']:.4f}
"""

# 训练与验证损失对比
plt.figure(figsize=(12, 6))
plt.plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')
plt.plot(df['epoch'], df['val/box_loss'], label='Val Box Loss', linestyle='--')
plt.title('Box Loss: Training vs Validation')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(output_dir, 'box_loss_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

# 评估指标相关性分析
metrics = df[['metrics/precision(B)', 'metrics/recall(B)', 
              'metrics/mAP50(B)', 'metrics/mAP50-95(B)']]
correlation_matrix = metrics.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Evaluation Metrics Correlation Matrix')
plt.savefig(os.path.join(output_dir, 'metrics_correlation.png'), dpi=300, bbox_inches='tight')
plt.close()

# 保存分析结果为文本文件
with open(os.path.join(output_dir, 'analysis_report.txt'), 'w', encoding='utf-8') as f:
    f.write(analysis_text)

# 保存处理后的数据为CSV
df.to_csv(os.path.join(output_dir, 'processed_results.csv'), index=False)

print(f"分析完成！结果已保存到: {output_dir}")