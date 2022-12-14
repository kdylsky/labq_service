# RainFall and DrainPipe service

### 서울시 Open API를 활용한 실기간 강수량, 하수도 수위 데이터 조회  REST API 서비스 


<br>

## 목차

  * [개발 기간](#개발-기간)
  * [개발 인원](#개발-인원)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 설명](#01-프로젝트-설명)
      - [개발 조건](#02-개발-조건)
      - [사용 기술](#03-사용-기술)
      - [모델링](#04-모델링)
      - [디렉토리 구조](#05-디렉토리-구조)
      - [API Test](#06-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)



<br>

## 개발 기간
**2022.11.07 ~ 2022.11.10** 

<br>
<br>
  
## 개발 인원
**Back-end  : 김도연**

<br>
<br>


## 프로젝트 개요


<br>

#### 01. 프로젝트 설명

<u> 서울시 OpenAPI를 이용, API호출시 구분코드에 대한 하수도와 강수량 데이터 조합해서 출력 </u>
 
<br>
<br>

#### 02. 개발 조건

> <br>
>
> * **데이터**
> 	* 서울시 OpenAPI 요청시 응답데이터
> 	* 주어진 데이터셋이 효과적으로 이용될 수 있게 자유롭게 모델링하여 구현 
>
><br>
>
> * **API**
>
>   *   **서울시 OpenAPI 데이터 출력 API**
>       * 서울시 하수관로 수위 현황과 강우량 정보 데이터를 수집
>       * 출력값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합
>       * 데이터는 JSON으로 전달
>
>   *   **1차 목표**
>       * OpenAPI 요청 후 실시간으로 데이터를 출력     
>
>   *   **2차 목표**
>       * Database에 OpenAPI 호출 최신 데이터 저장 후 출력
>       * Scheduler를 이용해서 정해진 시간마다 DB데이터 최신화
>       * 강수량과 하수도수위가 일정 수준 넘었을시 Slack bot을 이용한 메시지 보내기
> <br>
<br>
<br>


<br>


#### 03. 사용 기술 

- **Back-End** : Python, Django, Django REST Framework
- **Database** : MySQL, ERDCloud
- **HTTP**     : Postman
- **ETC**      : Git, Github, Miniconda


<br>
<br>

#### 04. 모델링

<br>


<p align="center"><img width="800" src="image/labq_modeling.png"></p>

<br>

- 1차 목표에서의 데이터를 바로 반환하기 때문에, DB에 저장할 필요가 없었으나, 2차 목표는 DB에 저장 후 데이터를 반환하기 때문에 데이터모델리이 필요하다
- 주어진 데이터를 처리하는 과정을 고려하여 `RainFall(강수량)`, `DrainPipe(하수관)`, `DetailRainFall(강수량상세정보)`, `DetailDrainPipe(하수관상세정보)` 4개의 테이블을 정의했다. 

	- `RainFall(강수량)`는 **여러 개**의 `DetailRainFall(강수량상세정보)`를 생성할 수 있다..
	- `DrainPipe(하수관)`는 **여러 개**의 `DetailDrainPipe(하수관상세정보)` 를 생성할 수 있다..

<br>

- `RainFall`와 `DrainPipe` 는 별개의 데이터이기 때문에 관계를 설정하지 않았다.
    - 두개의 공통된 `서울시 구` 정보를 따로 저장한다면 별개의 테이블(ex)`SeoulGuTable`)을 생성하여 `RainFall`와 `DrainPipe`를 각각 1대1로 연결해줄 수 있으나 요청을 후 데이터를 반환하는 현재의 API에서는 필요없다고 생각하여 따로 설정하지 않았다. 

<br>
<br>

#### 05. 디렉토리 구조
<br>


```
.
├── __pycache__
├── api(1차목표)
├── api2(2차목표)
    ├── utils(    
├── api2(2차목표)
    ├── data_schedule
    ├── slack_bot
    ├── utils    
├── configs
├── decorators
├── labq_service
├── exceptions.py
├── manage.py
└── requiremenets.py
 
``` 



<br>
<br>

#### 06. API Test
<br>

- DB에 저장된 데이터 조회 성공 & 실패 케이스를 구현

<p align="center"><img width="800" src="image/labq_test.png"></p>



<br>
<br>

## 프로젝트 분석

<br>

- 1차 목표와 2차 목표를 `api`와 `api2` 2개의 앱으로 분리
- OpenAPI 관련 서비스는 utils 작성 

<br>

- (1차, 2차) OpenAPI 최신데이터 요청 
    - utils에 UrlSetter클래스를 정의
        - OpenAPI 요청주소의 양식이 비슷하기 때문에 파라미터에 따른 OpenAPI요청 함수를 설정
        - 하수도의 데이터가 시간을 기준으로 오름차순으로 되어있기 때문에 최신데이터를 위해서 어떻게 해야할지 고민
            - 두번의 요청으로 문제를 해결. 처음의 요청에서 전체 리스트의 수를 반환. 뒤에서 부터 "구"별로 가지고 있는 IDN수를 뺌으로써 데이터 요청 시 start_idx를 도출
            - 두번의 요청으로 해결을 했으나 좋은방법인지에대한 의문. 
            - 한번의 요청으로 해결을 위해서는 대략 몇천건의 데이터를 받아와서 뒤에서 짤라야한다는 점에서 무의미한 데이터를 받는게 아닌가 하는 생각이 들어서 두번의 요청으로 문제를 해결했으나, 다른 방법이 있을 지 의문
        - 서비스 로직 안에 기능을 구현하지 않았기 때문에, 2차 목표를 구현시 사용할 수 있다는 점에서 재사용성이 높아짐
<br>
<br>
<br>

- (1차) 최신데이터 출력 API
    - Serializers를 활용한 데이터 반환
        - 구분 코드 입력시 위에서 구현한 최신데이터 요청 받은 데이터를 serializer를 통해 유효성 검사를 한 뒤 데이터 반환
        - `SerializerMethodField`를 활용, 강수량과 하수도 수위가 특정 범위를 이상인 경우 위험을 출력하는 코드를 작성

<br>
<br>
<br>

- (2차) Scheduler
    - 실시간 데이터를 위해서, 서버가 돌아가는 동안 백그라운드로 정해진 시간에 한번씩 OpenAPI 최신데이터를 요청

<br>
<br>
<br>

- (2차) 최신데이터 DB에 저장
    - serializer를 이용해서 요청에 대한 응답 데이터에 대한 유효성검사를 진행 후 데이터 저장
    - model의 필드명과 serializer의 필드명, 응답하는 데이터의 변수명이 다르기 때문에, serializer의 `souerce옵션`을 이용해서 serializer에 해당하는 필드명 맵핑

<br>
<br>
<br>

- (2차) 최신데이터 출력
    - 데이터베이스에 저장된 최신 정보를 출력
    - `get_or_create()`를 이용해서 저장된 데이터의 객체를 가지고 와서 변경된 수위 및 일장 정보를 변경 
<br>
<br>
<br>

- (2차) Slack Bot
    - 데이터 최신화 될 때마다 변경된 값의 체크 함으로써 Slack Bot을 통해서  메시지를 보내 주었다.

    
</br>

## API ENDPOINT

URL|Method|Description|</br>

### 01.api

URL|Method|Description|
|------|---|---|
|"/api/\<str:gubn>"|GET|최신데이터 출력|

<br>
<br>


DB에 접근하지 않고 OpenAPI 요청 후 바로 데이터 반환


```json
    {
    "DrainPipi": [
        {
            "IDN": "01-0004",
            "GUBN": 1,
            "GUBN_NAM": "종로",
            "MEA_YMD": "2022-11-10T21:54:05+09:00",
            "MEA_WAL": 0.11,
            "SIG_STA": "통신양호",
            "REMARK": "종로구 세종대로178 뒤 맨홀(KT광화문사옥뒤 자전거보관소앞 종로1길, 미대사관~종로소방서 남측, 중학천 하스박스)",
            "RISK": "경고"
        },
        {
            "IDN": "01-0003",
            "GUBN": 1,
            "GUBN_NAM": "종로",
            "MEA_YMD": "2022-11-10T21:54:05+09:00",
            "MEA_WAL": 0.11,
            "SIG_STA": "통신양호",
            "REMARK": "종로구 자하문로 21 앞 맨홀(영해빌딩앞코너 측구측, 백운동천 하수박스)",
            "RISK": "경고"
        },
        {
            "IDN": "01-0002",
            "GUBN": 1,
            "GUBN_NAM": "종로",
            "MEA_YMD": "2022-11-10T21:54:05+09:00",
            "MEA_WAL": 0.1,
            "SIG_STA": "통신양호",
            "REMARK": "중로구 세종대로 지하189 (세종로지하주차장 6층 천장)",
            "RISK": "경고"
        },
        {
            "IDN": "01-0001",
            "GUBN": 1,
            "GUBN_NAM": "종로",
            "MEA_YMD": "2022-11-10T21:54:05+09:00",
            "MEA_WAL": 0.05,
            "SIG_STA": "통신양호",
            "REMARK": "종로구 새문안로9길 9 앞 맨홀(세븐일레븐앞, 현대해상화재빌딩뒤, 백운동천하수박스)",
            "RISK": "경고"
        }
    ],
    "Rainfall": [
        {
            "RAINGAUGE_CODE": 1002.0,
            "RAINGAUGE_NAME": "부암동",
            "GU_CODE": 110.0,
            "GU_NAME": "종로구",
            "RAINFALL10": 0,
            "RECEIVE_TIME": "2022-11-10T21:29:00+09:00",
            "RISK": "안전"
        },
        {
            "RAINGAUGE_CODE": 1001.0,
            "RAINGAUGE_NAME": "종로구청",
            "GU_CODE": 110.0,
            "GU_NAME": "종로구",
            "RAINFALL10": 0,
            "RECEIVE_TIME": "2022-11-10T21:29:00+09:00",
            "RISK": "안전"
        }
    ]
}
```

<br>
<br>


### 02.api2

URL|Method|Description|
|------|---|---|
|"/api2/\<str:gubn>"|GET|최신데이터 출력|

<br>
<br>

DB에 최신데이터 업데이트 후 데이터 반환

``` json
    {
    "하수관": [
        {
            "id": 1,
            "gubn": 1,
            "gubn_nam": "종로"
        },
        [
            {
                "id": 1,
                "idn": "01-0004",
                "mea_ymd": "2022-11-10 17:54:05.0",
                "mea_wal": 0.11,
                "sig_sta": "통신양호",
                "remark": "종로구 세종대로178 뒤 맨홀(KT광화문사옥뒤 자전거보관소앞 종로1길, 미대사관~종로소방서 남측, 중학천 하스박스)",
                "gubn": 1
            },
            {
                "id": 2,
                "idn": "01-0003",
                "mea_ymd": "2022-11-10 17:54:05.0",
                "mea_wal": 0.11,
                "sig_sta": "통신양호",
                "remark": "종로구 자하문로 21 앞 맨홀(영해빌딩앞코너 측구측, 백운동천 하수박스)",
                "gubn": 1
            },
            {
                "id": 3,
                "idn": "01-0002",
                "mea_ymd": "2022-11-10 17:54:05.0",
                "mea_wal": 0.1,
                "sig_sta": "통신양호",
                "remark": "중로구 세종대로 지하189 (세종로지하주차장 6층 천장)",
                "gubn": 1
            },
            {
                "id": 4,
                "idn": "01-0001",
                "mea_ymd": "2022-11-10 17:54:05.0",
                "mea_wal": 0.03,
                "sig_sta": "통신양호",
                "remark": "종로구 새문안로9길 9 앞 맨홀(세븐일레븐앞, 현대해상화재빌딩뒤, 백운동천하수박스)",
                "gubn": 1
            }
        ]
    ],
    "강우량": [
        {
            "id": 1,
            "gu_code": 110,
            "gu_name": "종로구"
        },
        [
            {
                "id": 1,
                "raingauge_code": 1002,
                "raingauge_name": "부암동",
                "rainfall10": 0,
                "receive_time": "2022-11-10 17:29",
                "gu_code": 1
            },
            {
                "id": 2,
                "raingauge_code": 1001,
                "raingauge_name": "종로구청",
                "rainfall10": 0,
                "receive_time": "2022-11-10 17:29",
                "gu_code": 1
            }
        ]
    ]

```    
