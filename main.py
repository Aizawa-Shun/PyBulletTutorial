"""
PyBullet ロボットアームシミュレーション メインファイル
--------------------------------------------------
このファイルは、シミュレーションの全体的な実行と管理を担当します。
"""

import pybullet as p
from setup import setup_simulation
from control import run_simulation
from visualization import plot_joint_angles
from data_storage import save_data_to_excel

def main():
    """メイン関数 - シミュレーションの実行と管理"""
    try:
        # シミュレーション環境のセットアップ
        print("シミュレーション環境を準備中...")
        robot, obj = setup_simulation()
        
        # シミュレーションの実行
        print("シミュレーションを実行中...")
        time_data, joint_angles_data = run_simulation(robot, obj)
        
        # 結果のプロット
        plot_joint_angles(time_data, joint_angles_data, robot)
        
        # データの保存
        save_data_to_excel(joint_angles_data)
        
        # 物理エンジンの切断
        p.disconnect()
        
        print("シミュレーションが正常に完了しました！")
        
    except Exception as e:
        print(f"シミュレーション中にエラーが発生しました: {e}")
        p.disconnect()

if __name__ == "__main__":
    main()
