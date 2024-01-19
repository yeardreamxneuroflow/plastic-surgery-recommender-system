# Plastic Surgery Recommender System

> 성형 추천을 위한 얼굴 랜드마크 이미지 추출 및 이미지간 유사도 측정 웹 서비스

## About

본 서비스는 사용자의 얼굴(안면) 이미지에서 눈, 코, 입 등 주요 랜드마크에 해당하는 이미지를 추출하여 다양한 한국인 연예인(이하 워너비)들의 랜드마크 이미지와 유사도를 비교한 뒤 가장 유사한 워너비를 찾아주는 서비스입니다.

사용자는 본 서비스를 통해 비가역성이 짙고 부작용이 동반될 수 있는 물리적인 성형수술을 실제로 시행하기 전에 본인과 가장 유사한 워너비를 확인하여 구체적이고 실현 가능한 목표를 설정할 수 있습니다. 또한 수술을 집도할 의사와의 상담 시에 참고자료로써 활용하여 부작용을 줄일 수 있는 보다 안전한 방향으로 수술 계획을 세울 수 있습니다.

## Table of Contents

- [System Architecture](#system-architecture)
    - [Workflow Overview](#workflow-overview)
    - [Layers](#layers)
    - [Web UI & Web Backend Layer](#web-ui--web-backend-layer)
- [API Layer](#api-layer)
    - [/recommend](#recommend)
    - [/scrape](#scrape)
    - [Tech Stack](#tech-stack)
- [Core Components within The API Layer](#core-components-within-the-api-layer)
    - [Scrapy: Wannabe Image Scraper](#scrapy-wannabe-image-scraper)
    - [MediaPipe: Face Landmark Extractor](#mediapipe-face-landmark-extractor)
    - [Marqo: Vector Database](#marqo-vector-database)
- [Contact Us](#contact-us)
    - [Yi Hong-ju](#yi-hong-ju)
    - [Jung Chan-ho](#jung-chan-ho)
- [License](#license)

## System Architecture

![psrs_architecture](https://github.com/yeardreamxneuroflow/plastic-surgery-recommender-system/assets/102594161/e0737753-73a9-44c7-8d01-220fa6ba9da8)
*System Architecture Diagram*

### Workflow Overview

1. 사용자가 웹 UI를 통해 안면 이미지를 업로드하면 웹 애플리케이션 서버에서 구동되는 Java Spring 애플리케이션이 사용자의 요청을 1차적으로 처리합니다.
1. 이후 별도의 API 서버에서 구동되는 Flask 애플리케이션이 안면 인식, 랜드마크 추출, 벡터 DB 쿼리 전송 등의 작업을 수행하게 되고 이 작업 결과를 Spring 애플리케이션에 반환합니다.
1. 반환된 결괏값을 활용하여 Spring 애플리케이션이 사용자 요청에 대한 응답을 보내면 웹 UI가 변화하게 되고, 모든 작업이 마무리됩니다.

### Layers

본 서비스의 시스템은 총 세 개의 레이어로 구성됩니다.
- 시스템의 가장 앞단에서 사용자와 상호작용을 하는 **[Web UI Layer](#웹-ui--웹-백엔드-레이어)**
- 웹 UI를 통해 전달된 사용자의 요청을 직접적으로 처리하는 **[Web Backend Layer](#웹-ui--웹-백엔드-레이어)**
- 시스템의 가장 뒷단에 위치하여 웹 백엔드 레이어가 호출하도록 설계된 API들의 집합인 **[API Layer](#api-레이어)**

### Web UI & Web Backend Layer

팀 멤버 [Jung Chan-ho](https://github.com/ONECHANHO)에 의해 개발되었습니다. 자세한 내용은 [웹 서비스 코드 레포지토리](https://github.com/yeardreamxneuroflow/plastic-surgery-recommender-system-web-service)를 참고해주세요 :)

## API Layer

### /recommend

/recommend API는 웹 백엔드 레이어로부터 들어온 요청을 end-to-end로 처리하는 역할을 합니다.
- 사용자가 업로드한 안면 이미지에서 안면에 해당하는 영역을 탐지
- 해당 영역에서 눈(양쪽), 코, 입 랜드마크에 해당하는 영역을 탐지 및 버킷에 적재
- 탐지된 랜드마크 이미지를 Marqo에 질의하여 가장 유사한 워너비와 유사도 및 랜드마크 이미지를 반환받음
- 상기 작업 결과물을 요청 주체(웹 백엔드 레이어, Spring 애플리케이션)에 반환

### /scrape

워너비 이미지를 웹에서 스크래핑하고 S3 버킷에 적재까지 하는 작업을 수행하는 end-to-end API를 구현 예정이었습니다.

### Tech Stack
- Python
- AWS EC2, S3
- Docker
- Flask
- Scrapy
- MediaPipe
- Marqo

## Core Components within The API Layer

### Scrapy: Wannabe Image Scraper

웹에서 워너비 이미지를 수집하기 위한 모듈입니다.

### MediaPipe: Face Landmark Extractor

안면 이미지에서 랜드마크를 추출하기 위한 모듈입니다.

### Marqo: Vector Database

Marqo는 사용자와 워너비의 랜드마크 이미지를 임베딩하여 저장하여 관리하고 유사도 측정 등의 질의를 처리하기 위해 도커 환경에서 운용되는 벡터 데이터베이스입니다.

## Contact Us

### [Yi Hong-ju](https://github.com/y1hongju)

- Project Management
- API Layer Development

### [Jung Chan-ho](https://github.com/ONECHANHO)

- Web UI Layer Development
- Web Backend Layer Development

## License

본 프로젝트는 [Apache-2.0 license](https://github.com/yeardreamxneuroflow/plastic-surgery-recommender-system?tab=Apache-2.0-1-ov-file#readme)가 적용되었습니다.
