# Diffusion Paper Log

매주 월요일(한국시간 오전 9시경) arXiv 최신 디퓨전 모델 논문 5편을 자동으로 모아 한국어로 요약합니다.

<!-- LOG -->

## 2026-06-28 주간 요약

### [PhysiFormer: Learning to Simulate Mechanics in World Space](http://arxiv.org/abs/2606.27364v1)
*Yiming Chen, Yushi Lan, Andrea Vedaldi · 2026-06-25*

**🏷️ 논문 종류:** 새로운 방법론 제안

**🎯 목적:** 물리적으로 타당한 3D 객체 움직임을 월드 좌표계에서 시뮬레이션하고 미래 궤적을 예측합니다.

**🔧 방법론**
- 월드 좌표계에서 직접 작동하는 확산 트랜스포머(PhysiFormer) 사용
- 정점 궤적 예측을 단일 노이즈 제거 확산 프로세스로 정식화
- 시간, 공간, 객체에 대해 분리된 어텐션 메커니즘 활용

**📌 결론**
- 경직 및 탄성 역학 시뮬레이션에서 뛰어난 성능을 보임
- 다양한 재료 설정, 미등록 실제 기하학, 더 많은 객체 수에 대해 효과적으로 일반화됨
- 기존 자기회귀(autoregressive) 기준 모델보다 궤적 정확도, 강성 보존, 운동량 기반 물리적 일관성 면에서 우수함

### [LISA: Likelihood Score Alignment for Visual-condition Controllable Generation](http://arxiv.org/abs/2606.27192v1)
*Yanghao Wang, Hongxu Chen, Jiazhen Liu 외 · 2026-06-25*

**🏷️ 논문 종류:** 새로운 방법론 제안

**🎯 목적:** 시각적 조건부 생성 모델의 이중 분기 패러다임에서 사이드 네트워크의 학습 효율과 조건부 제어 능력을 개선하는 것.

**🔧 방법론**
- 이중 분기 패러다임을 스코어 기반 생성 모델링 관점에서 재해석
- 사이드 네트워크의 중간 특징을 근사된 가능도 스코어와 명시적으로 정렬하는 LISA 정규화 방법 제안
- 표준 확산 손실과 정규화 손실을 함께 사용하여 사이드 네트워크 및 디코더 공동 최적화

**📌 결론**
- LISA는 학습 수렴을 가속화하고 최종 생성 결과를 향상시킨다.
- 사이드 네트워크 특징이 조건부 모델링에 더 잘 분리되도록 유도한다.
- 추가 학습 비용은 미미하며 추론 비용은 발생하지 않는다.

### [Focusing on What Matters: Saliency-Harnessing Accurate Routing for Diffusion MoE](http://arxiv.org/abs/2606.26938v1)
*Haoyou Deng, Keyu Yan, Chaojie Mao 외 · 2026-06-25*

**🏷️ 논문 종류:** 새로운 방법론 제안

**🎯 목적:** 확산 MoE 프레임워크에서 라우터가 중요한 토큰에 계산 자원을 정확하게 할당하지 못하는 문제를 해결하고 시각 생성 성능을 향상시키는 것.

**🔧 방법론**
- SharpMoE 프레임워크 제안
- 라우팅을 위한 노이즈 없는 가이드 신호로 깨끗한 잠재 특징 활용
- 다단계 노이즈 제거 과정 동안 계산 자원 할당을 제어하기 위한 경로 라우팅 손실(trajectory routing loss) 도입

**📌 결론**
- SharpMoE가 사전 훈련된 MoE 모델의 성능을 더욱 향상시키는 다목적 플러그 앤 플레이 솔루션임을 입증
- 시각 생성에서 최첨단 성능을 달성함

### [PhysRAG: Enhancing Physics-Awareness in Video Generation via Retrieval-Augmented Generation](http://arxiv.org/abs/2606.26916v1)
*Kexu Cheng, Zicheng Liu, Mingju Gao 외 · 2026-06-25*

**🏷️ 논문 종류:** 새로운 방법론 제안

**🎯 목적:** 다양한 물리 현상 포착의 어려움을 해결하고 물리적 인식을 강화한 영상 생성 모델을 개발하는 것을 목표로 한다.

**🔧 방법론**
- 검색 증강 생성(RAG)을 활용하여 물리 인식 비디오 생성을 위한 PhysRAG 파이프라인 제안
- 고품질 훈련 데이터 확보를 위한 2단계 데이터 필터링 파이프라인 설계
- 학습 가능한 쿼리를 사용하여 비디오 확산 모델에 물리 지식을 주입하는 메커니즘 개발

**📌 결론**
- 시각적 품질과 물리 규칙 준수 측면에서 최첨단 성능을 달성
- PhyGenBench 및 VBench와 같은 벤치마크에서 기존 모델들을 능가하는 성능 입증
- 데이터 필터링 파이프라인, RAG 메커니즘 등 핵심 구성 요소의 효과를 광범위한 Ablation 연구를 통해 검증

### [NaviCache: Test-Time Self-Calibration Caching for Video Generation](http://arxiv.org/abs/2606.26795v1)
*Zheqi Lv, Zhibo Zhu, Jinke Wang 외 · 2026-06-25*

**🏷️ 논문 종류:** 효율화·가속

**🎯 목적:** 비디오 확산 모델의 막대한 계산 비용 문제를 해결하고, 기존 가속 방법론의 한계점을 극복하는 효율적인 테스트 시간 자체 보정 캐싱 방법을 제안하는 것이 목적이다.

**🔧 방법론**
- 특징 진화를 관성 항법 시스템(INS) 문제로 재개념화
- 이중 상태 추정 아키텍처 도입
- 시간 의존적 노이즈 스케줄과 불확실성 인식 측정 업데이트 메커니즘을 통합한 오차 제한적 계산 건너뛰기

**📌 결론**
- NaviCache가 계산 건너뛰기를 위한 더 정확한 오류 판단 제공
- 비디오 확산 모델 가속화에서 뛰어난 종합 성능 달성
- HunyuanVideo, Wan, Open-Sora 시리즈에서 효과 입증
