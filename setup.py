"""
シミュレーション環境のセットアップ機能
----------------------------------
このモジュールは、PyBulletシミュレーション環境のセットアップを担当します。
"""

import pybullet as p
import pybullet_data

def setup_simulation():
    """シミュレーション環境、オブジェクト、ロボットをセットアップする"""
    # GUI付きで物理エンジンに接続
    physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    
    # 重力を設定
    p.setGravity(0, 0, -9.8)
    
    # 床、テーブル、ロボットを読み込む
    floor = p.loadURDF("plane.urdf")
    table_pos = [0.5, 0.5, 0.2]
    table = p.loadURDF("cube.urdf", table_pos, globalScaling=0.4, useFixedBase=1)
    p.changeVisualShape(table, -1, rgbaColor=[0, 0, 0, 0.6])  # テーブルを暗い色に
    
    # ロボットアームを読み込み、関節センサーを有効化
    robot = p.loadURDF("kuka_iiwa/model.urdf", flags=p.URDF_USE_SELF_COLLISION)
    p.enableJointForceTorqueSensor(robot, 6)  # エンドエフェクタのトルクセンサーを有効化
    
    # インタラクションするオブジェクトを読み込む
    obj_pos = [0.5, 0.5, 0.45]
    obj = p.loadURDF("cube.urdf", obj_pos, globalScaling=0.1, flags=p.URDF_USE_SELF_COLLISION)
    p.changeVisualShape(obj, -1, rgbaColor=[1, 0.65, 0, 1])  # オブジェクトをオレンジ色に
    
    # 参考のため関節情報を表示
    print("ロボット関節情報:")
    for i in range(p.getNumJoints(robot)):
        print(f"関節 {i}: {p.getJointInfo(robot, i)[1].decode('utf-8')}")
        
    return robot, obj

def set_camera(model):
    """カメラをモデルに焦点を合わせるように設定"""
    focus_pos, _ = p.getBasePositionAndOrientation(model)
    p.resetDebugVisualizerCamera(
        cameraDistance=2.5,  # カメラ距離
        cameraYaw=60,        # カメラのヨー角度
        cameraPitch=-25,     # カメラのピッチ角度
        cameraTargetPosition=focus_pos  # カメラのターゲット位置
    )
