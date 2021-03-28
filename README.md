# Implementation

P2P network에서는 처음에 본인이 주변 노드 정보 가지고 있고 gossip형태로 전파한다.  
torrent에서도 peer들의 정보들을 가지고 있는 서버인 Tracker가 있다.  
peer table은 Distributed Hash Table(DHT)로 구성 시도해보자. (이더리움은 Kademlia 사용)  

<br>
The timestamp of TX is the time which the TX was generated
The timestamp of Block is the time which The miner start to calculate nonce

트랜잭션이 ledger에 포함되기 전까지 전파/생성된 TX들을 저장해놓을 mempool이 필요함. (어떻게 뽑을 건지도 생각해야함)

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
