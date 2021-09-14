aws 사용법 4개
- AWS Management Console (Browser)
- CLI
- SDK
- API

AWS sevice
- EC2 (server - db server, web server, etc.)
	only computing (computation)
	storage 기능은 option ( 이 때 사용하는 것이 아래 S3, EBS )
	리소스에 태그들을(key/value) 달아서 어떤 기능을 하는 지 관리해야함 (웹서버인지, 앱서버인지, 어떤 팀에서 만들었는 지 등을 리소스 아이디만 보고 판단할 수 없으니까)
	instance user-data: pending->running 될 때 실행되는 script를 전달할 수 있음. (인스턴스 ID 당 단 한번만)
			서비스 시작, pre-install 등 사용 가능.
	인스턴스 스토리지가 있는데, 휘발성임 Reboot(호스트 서버 그대로)과 Stop-Run(새로운 호스트 서버에서 생성)의 차이 때문임.
	EBS와 같은 애들은 EBS Storage server에서 따로 생성되어 instance에 attach (network로) 되어 쓰는 것이기 때문에 stop-run도 그대로 (비휘발)
- S3: 얘는 EC2랑 안쓰고 단독으로도 사용될 수 있음
	인터넷용 스토리지. HTTP 기반이기 때문에 편함.
	Object storage 이기 때문에 객체 단위 저장 (파일 + 파일의 메타데이터) 를 함께 저장하는 형태.
	Object storage는 파일의 일부분만 변경해도 Overwrite가 되기 때문에 자주 변경되지 않는 데이터를 올리는 게 좋다. (일반 file/block storage는 일부만 변경됨)
	명목상 folder는 있지만 tree 구조가 아니라서 폴더가 있나 없나 엑세스 속도도 똑같음 (하나의 객체 키 "2020/asdf.pdf" "asdf.pdf")
- EBS: 얘는 EC2랑 함께 사용되어야 함
	Block storage. 파일을 block 단위로 나누고 저장하기 때문에 일부 변경시 해당 block만 변경하게 됨.
	스냅샷이 Amazon S3에 저장됨.
- VPC (Virtual Private Cloud): 인터넷 기반의 서버이기 때문에 성능보장/보안 을 보장하기 힘듦
	EC2를 만드는 공간 (반드시 VPC 내에 만들어야 안전)
	기본적으로 격리공간이므로 end user가 접근할 수 없고(설정해줘야하고) 내부는 AWS network로 통신 (내부에서 private IP로 접근가능) 외부는 인터넷으로.
	* region 기반으로 설정되며, IP할당 기준을 선택할 수 있는데(CIDR), 10.0.0.0/16 이라고 하면 (한 자리에 8비트이고 앞에 두 자리 고정하고 뒤에 두 자리가 유동적으로 변하여 내부 EC2에 할당된다)
	AZ 내 서브넷으로 쪼개서 (IP대역) 사용함.
	외부 인터넷과 통신하기 위해선 게이트웨이 설정을 해줘야한다.
	* 서브넷당 하나씩 Route Table을 설정한다. (IP를 갖고 Route table을 쭉 훑어보면서 어디로 가야할지)
		1. IGW (외부 인터넷)
		2. NAT (퍼블릭 서브넷 <-> 프라이빗 서브넷): 보여줄 수는 없지만 외부에서 다운로드 등을 해야할 때는 퍼블릭과 프라이빗을 연결해서 사용할 수 있지.
		3. VGW (가상 프라이빗 게이트웨이, 고객사네트워크와 / VPN)

보안과 인증
- VPC의 보안
	1. 보안 그룹: 리소스(EC2 인스턴스 같은)에 설정하는 가상 방화벽
		기본적으로 들어오는 것 (inbound traffic) 이 차단되어있으므로, 허용규칙 포함시켜야함.
	2. 네트워크의 ACL(엑세스 제어 목록): 서브넷에 설정하는 가상 방화벽
		얘는 기본적으로 허용임. 제어하고 싶을 때 차단을 세부적으로 설정해줘야함.
	3. 키 페어:  처음 end user가 EC2 인스턴스에 접근할 때 (root / pw 지원이 안되므로 퍼블릭/프라이빗 키를 이용해)
- IAM (Identity and Access Management): 인증과 권한을 다룬다.
	한 AWS 계정에 접근하는 데에 사용자 이름과 암호를 이용 (Management 에 접근 시)
	AWS CLI 또는 SDK API 호출 시 액세스 키, 보안 키를 이용.
	권한 부여는 JSON 문서를 이용한다 (정책). -> 사용자별로 설정해줄 수도 있고, AWS 서비스에도 설정해줄 수 있음(IAM 역할)
		예컨대, 배포된 EC2 앱 인스턴스가 S3를 사용할 때 API 콜을 해야하는데, 사용자에게 부여된 액세스 키, 보안 키를 하드코딩 하는 것보다는 서비스에 IAM 역할을 설정하는 방법으로 해결할 수 있다.


데이터베이스
- DynamoDB: NoSQL 디비
	항목 중 두 개를 (파티션 키 / 정렬 키)로 하여 인덱싱을 한다.
- RDS: RDB 디비, Oracle, MySQL, PostgreSQL 등의 기능을 사용할 수 있는 디비 인스턴스를 생성한다.
	Multi-AZ 지원 (다른 AZ에 Primary, Secondary DB 만들고 하나 장애나면 자동으로 스위치) -> 하지만 하나의 엔드포인트를 제공


AWS 관리 도구
* 클라우드의 장점은 확장성
- Auto Scaling
- CloudWatch: 언제 축소 / 확장할 것이냐를 모니터링
	예컨대 EC2의 CPU 사용률이 올라가면 EC2를 늘린다
	임계치를 설정하여 경보 설정 가능.
- ELB (load balancing): EC2가 확장될 때, 하나의 IP로 end user에게 뿌리고 알아서 분할해주는
	하나의 IP는 AWS에서 도메인을 제공함.
	- Application LB (HTTP/HTTPS): 경로 기반 라우팅 제공
	- Network LB (TCP/UDP): AZ까지 선택 가능
- Trusted Advisor: 문제점을 판단하고 어드바이즈 해줌.

실습 내용
1. VPC 구축 및 EC2 웹서버 시작과 EBS 연결
2. RDS를 이용한 디비 서버 구축 후 1과 연동
3. 오토 스케일링, 로드밸런싱, 모니터링

글로벌 인프라
- 데이터센터 2개 이상이 모여서 AZ(가용영역)
- 가용영역 2개 이상이 모여서 Region
- Edge location은 region 외에 존재하는 데이터센터, 고객이 선택 불가능하며 이름도 없음. (자동선택됨)
	cloud front, route 53, waf, shield 4개 서비스만 edge location에서 제공
- 각 구성요소간의 연결은 AWS 네트워크로 연결되어있다.
- 서울 region 코드는 ap-northeast-2 (a/b/c/d 는 AZ 코드) 
