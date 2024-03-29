![Python](https://img.shields.io/badge/Python-v3.9.2-blue)

# Implementaion Lists
* Energy Platform Frontend
    * Jinja template engine 
* Energy Platform Backend (http)
    * Flask 
* WebSocket Handler (thread programming)
* Hierarchical Deterministic Wallet
    * ECDSA-based
* Relational Database for accounts
    * SQLite 
* Cryptographic Process
* Directed Acyclic-based Ledger with LevelDB
* Bash scripts 
    * Platform initialization
    * DB initialization
    * Clear process
* Simple simulation with visualization
    * OpenCV-based 
### CSS opensource
```
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
```
# Setting
## Install
```
conda env create -f environment.yml
pip install -e ./kudag
pip install -e ./dagapi

```

## Server Up & Down
```bash
conda activate energy

# 1. Start DAG service
./script/init_script --http <API_PORT> --ws <P2P_PORT> --local --peers <peer_list> [--new] # init_script --help for more details

# 2. Set genesis after write genesis.json
# -> All nodes must use the same genesis.json
curl http://127.0.0.1:<API_PORT>/api/genesis

## 3. Check my peers for P2P networking
curl http://127.0.0.1:<API_PORT>/api/peers

# Force all services down
./script/kill_server

```
## CSS
```
sass static/sass/main.scss static/css/main.css
```

## Jinja
```
{% block sidebar %}
    {% block inner_sidebar %}
        ...
    {% endblock inner_sidebar %}
{% endblock sidebar %}
```

# Smart Contract
```python
md5_hash = hashlib.md5()

a_file = open("test.txt", "rb")
content = a_file.read()
md5_hash.update(content)

digest = md5_hash.hexdigest()
print(digest)
```
특정 폴더에 개별 스마트 컨트랙트를 개별 파일로 저장, 이에 대한 해쉬 값을 set으로 구성  
해당 set에 그 해쉬 값 없으면 스마트 컨트랙트를 개별 `.py`로 저장

# Details

P2P network에서는 처음에 본인이 주변 노드 정보 가지고 있고 gossip형태로 전파한다.  
torrent에서도 peer들의 정보들을 가지고 있는 서버인 Tracker가 있다. (semi-private 느낌으로 처음 노드 구성 시 추천(or 기본) peer list를 거점 노드로부터 받아오게 하자)  
peer table은 Distributed Hash Table(DHT)로 구성 시도해보자. (이더리움은 Kademlia 사용)  

<br>
The timestamp of TX is the time which the TX was generated  
The timestamp of Block is the time which The miner start to calculate nonce

트랜잭션이 ledger에 포함되기 전까지 전파/생성된 TX들을 저장해놓을 mempool이 필요함. (어떻게 뽑을 건지도 생각해야함)  
소규모 행정구역별로 TX를 수집할 코어노드 만들기 (초창기에는 DAG로 자리잡기 힘드니까)  
-> 시스템이 성숙됨에 따라 거래신뢰도 기반 집중노드 변경 건의 가능  

## Broadcast
다른 코어노드들과 연결이 끊기면 그순간 스냅샷을 찍고 현재 ledger 기반으로 account 상태정보 저장 및 local 내에서 거래 시작. 이 때 새로운 root TX로 시작  
다시 다른 코어노드들과 연결되면 이 root TX는 새로운 terminal tx에 붙는다. 동기화되면서 해당 local network의 상태를 global network에 전파  
Dos(Denial-of-service) 공격을 막기 위해 안전장치 필요 -> 최소 하한 수수료 or 가벼운 PoW

## Finality (Irreversible Transactions)
분산장부에서는 100% 확정을 짓기 매우 어려움 (각 노드는 자기 시점으로 트랜잭션을 생성하고 등록된 peer로부터 데이터를 전달받기 때문에)  
어떤 상태를 잠정 확정된 상태로 생각할 것인가 (Bitcoin은 6개의 블록이 뒤에 더 붙고나서 해당 블록을 잠정 확정 + coinbase TX로 생성된 BTC는 100block 이후 사용가능)

## Attack vectors
### 1) Race attack
판매자에게 대금 지불하는 TX 보내고 나머지 네트워크 노드들에게는 본인의 다른 계정에 대금을 지불하는 TX를 보내서 double-spending 유도 (후자가 채굴될 가능성 높게 조절)
### 2) Finney attack
race attack이랑 비슷한데 조건만 맞으면 좀 더 확정적.  
attacker는 자기 주소 A에서 B로 특정 금액을 전송시키는 TX 만들고 이를 포함하여 블록을 채굴함. (채굴 시 전파 안하고 일단 홀딩)  
다른 판매자에게 구매하는 TX 생성해서 보내고 그걸 증거로 물건 받음  
물건 받자마자 나는 내가 채굴한 블록 전파 (판매자에게 보낸 TX는 double-spending TX가 되서 invalidated)  
-> 성립시키긴 매우 어려움 (다른 miner보다 빠르게 먼저 채굴시키고 다른 miner가 채굴하기 전까지 판매자와의 거래도 성립시켜야 함)

### 3) Vector76 attack (one-confirmation attack)
race + finney attack 느낌. 공격하려는 노드에게만 합법적으로 채굴된 그러나 double-spending을 유도하는 TX를 포함한 블록 전송  
해쉬 값 확인 시 멀쩡하니까 해당 노드는 안심함 (앞선 방법들은 판매자가 TX가 unconfirmed 상태인데도 믿고 그냥 보내는 경우)  
따라서 채굴 성공 시 성공확률은 높지만 그만큼 기회비용도 큼 (채굴 보상 + 포함된 트랜잭션들의 수수료)보다 커야 이득임

### 4) Majority attack
Bitcoin에서의 51% attack 같은거 -> 해당 플랫폼의 consensus를 제어할 수 있을정도로 리소스 장악

## security
### 1) Key stretching
Do hash function several times to prevent burte-force attack  
#### 1-1) sha-256d
sha256 twice by "Cryptography Engineering" to make SHA-256 invulnerable to "length-extension" attack
### 2) Salt
Append random string on original data against rainbow table



## Wallet
ECDSA = (Private Key : 32 bytes), (Public Key : 64 bytes)  
Address = 16 bytes, (sha3_256 -> blake2s)

Save (private key : public key) pair  
Account-based (Not UTXO)
