# blockchain
A basic blockchain implementation with a cryptocurrency element. 

Done as part of my Distributed Systems course's Term Project. 

## BlockChainAPI
### Description

### Endpoints
`/mine` - mines a new coin, returns the coin and some other information.

`/transactions/new` - adds a new transaction. 
Transaction must be of format 
```
{
 "sender": SENDER,
 "recipient": RECIPIENT,
 "amount": 1
}
```

`/chain` - returns the blockchain in json format.
