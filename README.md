# Plastic Surgery Recommender System
> 성형 추천을 위한 얼굴 랜드마크 추출 및 워너비 이미지간 유사도 측정 웹 서비스

## About
본 서비스는 사용자의 안면 이미지에서 눈, 코, 입(이하 랜드마크) 이미지를 추출하여 다양한 한국인 연예인(이하 워너비)들과 유사도를 비교한 뒤 가장 유사한 워너비를 찾아주는 서비스입니다.

사용자는 웹 UI를 통해 본인 증명사진 등의 안면 이미지를 업로드하여 눈, 코, 입 랜드마크 이미지를 얻을 수 있습니다. 또한 각 랜드마크 이미지가 어떤 워너비의 랜드마크 이미지와 가장 유사한지를 그 점수와 함께 확인할 수 있습니다. 

본 서비스를 통해 사용자는 비가역적인 부작용이 동반될 수 있는 물리적인 성형수술을 실제로 시행하기 전에 가장 유사한 워너비를 확인하여 여러 기준점 중 하나로 삼을 수 있고, 이를 활용해 부작용을 줄이는 방향으로 수술 계획을 세울 수 있습니다.

## 시스템 구성
서비스의 시스템은 크게 세 부분으로 나눌 수 있습니다.
- 시스템의 가장 앞단에서 사용자와 상호작용을 하는 **[웹 UI](#웹-ui--웹-백엔드-레이어)**
- 웹 UI를 통해 전달된 사용자의 요청을 직접적으로 처리하는 **[웹 백엔드 레이어](#웹-ui--웹-백엔드-레이어)**
- 시스템의 가장 뒷단에 위치하여 웹 백엔드 레이어가 호출하도록 설계된 API들의 집합인 **[API 레이어](#api-레이어)**

### 워크플로우
사용자가 웹 UI를 통해 안면 이미지를 업로드하면 웹 애플리케이션 서버에서 구동되는 Java Spring 애플리케이션이 사용자의 요청을 1차적으로 처리합니다. 이후 별도의 API 서버에서 구동되는 Flask 애플리케이션이 안면 인식, 랜드마크 추출, 벡터 DB 쿼리 전송 등의 작업을 수행하게 되고 이 작업 결과를 Spring 애플리케이션에 반환합니다. 반환된 결괏값을 활용하여 Spring 애플리케이션이 사용자 요청에 대한 응답을 보내면 웹 UI가 변화하게 되고, 모든 작업이 마무리됩니다.

## 웹 UI & 웹 백엔드 레이어
팀 멤버 [Jung Chan-ho](https://github.com/ONECHANHO)에 의해 개발되었습니다. [웹 서비스 코드 레포지토리](https://github.com/yeardreamxneuroflow/plastic-surgery-recommender-system-web-service)를 참고해주세요 :)

## API 레이어
구현된 API는 총 두 가지 입니다. ......

## Members
- [Yi Hong-ju](https://github.com/yi-hongju)
- [Jung Chan-ho](https://github.com/ONECHANHO)

## License
본 프로젝트는 [Apache-2.0 license](https://github.com/yeardreamxneuroflow/plastic-surgery-recommender-system?tab=Apache-2.0-1-ov-file#readme)가 적용되었습니다.
