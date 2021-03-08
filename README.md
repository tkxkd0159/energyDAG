# Implementation

P2P network에서는 처음에 본인이 주변 노드 정보 가지고 있고 gossip형태로 전파한다.  
torrent에서도 peer들의 정보들을 가지고 있는 서버인 Tracker가 있다.
peer table은 Distributed Hash Table(DHT)로 구성 시도해보자. (이더리움은 Kademlia 사용)