"""
データ可視化関連機能
----------------
このモジュールは、シミュレーションデータの可視化を担当します。
"""

import pybullet as p
import matplotlib.pyplot as plt
import os

def plot_joint_angles(time_data, joint_angles_data, robot):
    """関節角度の時間推移をプロットする"""
    fig = plt.figure(figsize=(10, 6))
    
    # プロットしやすいようにデータを転置
    joint_angles_transposed = joint_angles_data.T
    
    # 各関節角度をプロット
    for i in range(p.getNumJoints(robot)):
        joint_name = p.getJointInfo(robot, i)[1].decode('utf-8')
        plt.plot(time_data, joint_angles_transposed[i], label=f"{joint_name}")
    
    plt.title("関節角度の時間推移")
    plt.xlabel("時間 [秒]")
    plt.ylabel("角度 [ラジアン]")
    plt.legend()
    plt.grid()
    
    # ディレクトリが存在しない場合は作成
    os.makedirs("./graph", exist_ok=True)
    plt.savefig("./graph/joint_angle_graph.png")
    plt.show()
