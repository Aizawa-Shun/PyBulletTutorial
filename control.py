"""
ロボット制御とシミュレーション実行
------------------------------
このモジュールは、ロボットの制御とシミュレーション実行を担当します。
"""

import pybullet as p
import time
import numpy as np
from setup import set_camera

# 設定パラメータ
SIM_DURATION = 5.0    # シミュレーション時間（秒）
DT = 0.01             # タイムステップ（秒）
TARGET_OFFSET = [-0.05, -0.05, 0.1]  # ロボットハンドのオブジェクトからのオフセット

def run_simulation(robot, obj):
    """シミュレーションを実行し、ロボットを制御する"""
    # プロット用のデータストレージ
    time_data = []
    joint_angles_data = []
    
    # シミュレーション時間と接触フラグの初期化
    t = 0
    contact = False
    
    while t < SIM_DURATION:
        # シミュレーションステップを実行
        p.stepSimulation()
        time.sleep(DT)  # 可視化のためにシミュレーションを遅くする
        t += DT
        time_data.append(t)
        
        # カメラビューを設定
        set_camera(robot)
        
        # オブジェクトの位置を取得し、ロボットハンドのターゲット位置を計算
        obj_pos = p.getBasePositionAndOrientation(obj)[0]
        target_pos = [
            obj_pos[0] + TARGET_OFFSET[0],
            obj_pos[1] + TARGET_OFFSET[1],
            obj_pos[2] + TARGET_OFFSET[2]
        ]
        
        # ターゲット位置に対応する関節角度を逆運動学で計算
        target_angles = p.calculateInverseKinematics(robot, 6, target_pos)
        
        # ロボットとオブジェクト間の接触チェック
        contact_points = p.getContactPoints(robot, obj)
        if contact_points and not contact:
            print(f'接触検出位置: {contact_points[0][5]}')
            p.changeVisualShape(obj, -1, rgbaColor=[1, 0, 0, 1])  # 接触時に赤に変更
            contact = True
        elif not contact_points:
            p.changeVisualShape(obj, -1, rgbaColor=[1, 0.65, 0, 1])  # オレンジに戻す
            contact = False
        
        # ターゲット位置に向かってロボット関節を制御
        for i in range(len(target_angles)):
            p.setJointMotorControl2(
                bodyUniqueId=robot,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=target_angles[i],
                targetVelocity=0.05,  # 滑らかな動きのための低速移動
                positionGain=0.2,
                velocityGain=1.0,
                force=3000
            )
        
        # 関節角度の記録
        joint_angles = []
        for i in range(p.getNumJoints(robot)):
            joint_angles.append(p.getJointState(robot, i)[0])
        joint_angles_data.append(joint_angles)
    
    return time_data, np.array(joint_angles_data)
