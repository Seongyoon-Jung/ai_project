import torch
from ultralytics import YOLO

# YOLO v5 모델 로드
yolo_v5_model_path = 'best.pt'
yolo_v5_model = torch.load(yolo_v5_model_path)

# YOLO v8 모델 초기화
yolo_v8_model = YOLO('yolov8n.pt')  # YOLO v8 기본 모델 (여기서는 예시로 'n' 버전 사용)

# YOLO v5 모델의 가중치 추출
v5_state_dict = yolo_v5_model['model'].state_dict()

# YOLO v8 모델의 가중치에 YOLO v5 가중치 적용
v8_state_dict = yolo_v8_model.model.state_dict()

# 필요한 레이어 가중치 매핑 (레이어 이름과 구조가 다르기 때문에 직접 매핑 필요)
# 예시: v8_state_dict['backbone.layer1.conv.weight'] = v5_state_dict['backbone.0.conv.weight']
for key in v8_state_dict.keys():
    if key in v5_state_dict:
        v8_state_dict[key] = v5_state_dict[key]

# 새로운 가중치로 YOLO v8 모델 업데이트
yolo_v8_model.model.load_state_dict(v8_state_dict)

# YOLO v8 모델 저장
yolo_v8_model.save('converted_yolov8_model.pt')
