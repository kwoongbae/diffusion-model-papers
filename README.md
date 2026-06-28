# Diffusion Paper Log

매주 월요일(한국시간 오전 9시경) arXiv 최신 디퓨전 모델 논문 5편을 자동으로 모아 한국어로 요약합니다.

<!-- LOG -->

## 2026-06-28 주간 요약

### [Focusing on What Matters: Saliency-Harnessing Accurate Routing for Diffusion MoE](http://arxiv.org/abs/2606.26938v1)
*Haoyou Deng, Keyu Yan, Chaojie Mao 외 · 2026-06-25*

기존 확산 MoE 모델의 라우터는 노이즈가 낀 잠재 특징에 의존하여 중요한(salient) 토큰에 자원을 정확히 할당하지 못하는 문제를 발견했습니다. 이를 해결하기 위해 SharpMoE를 제안하며, 노이즈가 없는 '깨끗한 잠재 특징'을 라우팅의 가이드 신호로 활용하여 주요 토큰 식별을 개선합니다. 더 나아가, 다단계 디노이징 과정 전반에 걸쳐 컴퓨팅 자원 할당을 정밀하게 제어하기 위한 '궤적 라우팅 손실(trajectory routing loss)'을 도입했습니다. SharpMoE는 사전 학습된 MoE 모델의 성능을 추가로 향상시키는 플러그 앤 플레이 솔루션으로, 시각 생성에서 최신 성능을 달성합니다.

### [PhysRAG: Enhancing Physics-Awareness in Video Generation via Retrieval-Augmented Generation](http://arxiv.org/abs/2606.26916v1)
*Kexu Cheng, Zicheng Liu, Mingju Gao 외 · 2026-06-25*

본 논문은 물리적 현상 인식이 부족한 비디오 생성의 한계를 해결하기 위해 RAG(Retrieval-Augmented Generation) 기반의 PhysRAG를 제안합니다. 이를 위해 WISA-80K 데이터셋 기반의 2단계 데이터 필터링 파이프라인을 구축하여 7천 개의 고품질 비디오를 선별했습니다. 또한, 물리 비디오 데이터베이스를 구축하고 학습 가능한 쿼리를 활용하여 물리 지식을 비디오 확산 모델에 주입하는 메커니즘을 개발했습니다. 그 결과, 기존 모델들을 능가하며 시각적 품질과 물리 법칙 준수 측면에서 최첨단 성능을 달성했습니다.

### [NaviCache: Test-Time Self-Calibration Caching for Video Generation](http://arxiv.org/abs/2606.26795v1)
*Zheqi Lv, Zhibo Zhu, Jinke Wang 외 · 2026-06-25*

이 논문은 비디오 확산 모델(VDM)의 높은 계산 비용 문제를 해결하기 위해, 테스트-시점 자체 보정 캐싱 방식인 NaviCache를 제안합니다. NaviCache는 특징(feature) 진화를 관성 항법 시스템(INS) 문제로 재개념화하여, 입력과 출력 변화 간의 상대적 연결성을 모델링함으로써 확산 과정의 비정상적 특성을 다룹니다. 이 시스템은 이중 상태 추정 아키텍처로 특징 변화율과 잠재적 드리프트를 추적하고, 불확실성을 고려한 측정 업데이트를 통해 오류가 보장되는 계산 건너뛰기(computation skipping)를 가능하게 하는 플러그-앤-플레이 방식입니다.

### [Escaping Iterative Parameter-Space Noise: Differentially Private Learning with a Hypernetwork](http://arxiv.org/abs/2606.26772v1)
*Naoki Nishikawa, Shokichi Takakura, Satoshi Hasegawa · 2026-06-25*

이 논문은 DP-SGD의 반복적인 고차원 파라미터 공간 잡음 주입 문제를 해결하기 위해, 파라미터 공간에서의 반복 최적화를 회피하는 새로운 차분 프라이버시 학습 프레임워크를 제안합니다. 구체적으로, 공개 데이터셋으로 학습된 하이퍼네트워크를 사용하여 비공개 데이터셋을 대상 모델의 파라미터로 직접 매핑합니다. 이는 비공개 데이터셋의 각 예시를 저차원 임베딩으로 변환하고, 이를 집계하여 단 한 번 잡음을 주입한 후 하이퍼네트워크에 전달하여 모델 파라미터를 생성하는 방식으로 이루어집니다. 이로써 잡음 주입이 단 한 번의 저차원 데이터셋 표현에만 이루어져 잡음의 부정적인 영향을 크게 줄이며, DP-SGD 대비 더 높은 유용성을 달성하고 확산 모델 미세 조정에서 낮은 FID를 보입니다.

### [ResilPhase: Plug-and-Play Phase Mapping and Noise-Resilient Macro-Trajectory Extrapolation for Diffusion Acceleration](http://arxiv.org/abs/2606.26769v1)
*Qicheng Zhao, Yu Li, Qi Sun 외 · 2026-06-25*

ResilPhase는 확산 모델 가속화 시 기존 미분 기반 외삽 방식의 불안정성과 노이즈 문제를 해결합니다. 이를 위해 추론을 ODE 공간에서의 안정적인 거시 궤적(macro-trajectory) 외삽으로 재정의하고, 모델의 전반적인 상태 변화인 'Global Drift'에 예측을 정렬합니다. 특히, 내재적으로 노이즈가 많은 미분을 회피하고자 미분 없는 barycentric Lagrange 외삽기를 도입합니다. 또한 외삽 영역을 제한하여 오차 증가를 억제하는 유계 위상 매핑(Phase Mapping)을 제안, 공격적인 가속화 비율에서도 최첨단 충실도를 달성합니다.

