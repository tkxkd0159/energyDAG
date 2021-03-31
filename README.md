# Implementation

P2P network에서는 처음에 본인이 주변 노드 정보 가지고 있고 gossip형태로 전파한다.  
torrent에서도 peer들의 정보들을 가지고 있는 서버인 Tracker가 있다.  
peer table은 Distributed Hash Table(DHT)로 구성 시도해보자. (이더리움은 Kademlia 사용)  

<br>
The timestamp of TX is the time which the TX was generated  
The timestamp of Block is the time which The miner start to calculate nonce

트랜잭션이 ledger에 포함되기 전까지 전파/생성된 TX들을 저장해놓을 mempool이 필요함. (어떻게 뽑을 건지도 생각해야함)  
소규모 행정구역별로 TX를 수집할 코어노드 만들기 (초창기에는 DAG로 자리잡기 힘드니까)  
-> 시스템이 성숙됨에 따라 거래신뢰도 기반 집중노드 변경 건의 가능  

### Broadcast
다른 코어노드들과 연결이 끊기면 그순간 스냅샷을 찍고 현재 ledger 기반으로 account 상태정보 저장 및 local 내에서 거래 시작. 이 때 새로운 root TX로 시작  
다시 다른 코어노드들과 연결되면 이 root TX는 새로운 terminal tx에 붙는다. 동기화되면서 해당 local network의 상태를 global network에 전파  
Dos(Denial-of-service) 공격을 막기 위해 안전장치 필요 -> 최소 하한 수수료 or 가벼운 PoW

## security
### 1) Key stretching
Do hash function several times
### 2) Salt
append random string on original data


## Wallet
ECDSA = (Private Key : 32 bytes), (Public Key : 64 bytes)  
Address = 16 bytes, (sha3_256 -> blake2s)

Save (private key : public key) pair  
Account-based (Not UTXO)
