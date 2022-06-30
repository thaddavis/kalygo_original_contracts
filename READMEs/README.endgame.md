```
./sandbox goal wallet list
./sandbox goal wallet new endgame_wallet
./sandbox goal account new -w endgame_wallet
```

*** CREATOR ***

pub_key: T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI
priv_key: 

mneumonic:
lake absurd afford fire sauce scorpion convince clutch artwork alarm pepper network regret snap fiscal normal fragile win treat ginger spring auction utility ability faculty

*** SELLER ***

pub_key: QHGMAMCTEHZ2RQV2DRXSPAKIIT3REVK46CHNDJSW6WNXJLSJ7BB76NHDGY
priv_key: 

mneumonic: illness disorder message diamond cluster much damage can enrich action various pilot release gasp air fancy design sunset modify off blanket make spice ability nasty

*** BUYER ***

pub_key: RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM
priv_key: 

mneumonic: tennis blouse junior catch purse earth make purse honey hidden coral usage dilemma body long guitar document become good mammal coast increase caught about maid

```
./sandbox goal clerk send --from FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 --to T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI --amount 10000000

./sandbox goal clerk send --from FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 --to RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM --amount 100000000

./sandbox goal clerk send --from FXPAVJ5QYIPPXRBXMLAIPCMBB72RMZDC5TNFBDAVD22N7ODY6NFYDUHIL4 --to T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI --amount 100000000
```


./sandbox goal account balance -a T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI
./sandbox goal account list -w endgame_wallet
./sandbox goal account info -a T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI
./sandbox goal account export -a T4N73AL4F4ZL6VJZWJ2QP2KV5VJEHJYFTFMVNTWG45MP4S4EDPJIWC45WI -w endgame_wallet