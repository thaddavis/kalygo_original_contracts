./sandbox enter algod

SELLER=QHGMAMCTEHZ2RQV2DRXSPAKIIT3REVK46CHNDJSW6WNXJLSJ7BB76NHDGY

goal app call --app-id 97 --from $SELLER --app-arg "str:seller_withdraw_funds" --dryrun-dump -o tx.dr

goal clerk send -a 333 -f RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM -t LNXKLFFEAH6ZJW7IFOLCDJRXXYD5UJK2AE2FX3MAXTT6YNQ53SNRCM4TOE --dryrun-dump -o tx.dr

tealdbg debug -d tx.dr --listen 0.0.0.0

https://developer.algorand.org/tutorials/using-the-teal-debugger-to-debug-a-smart-contract/#3-buggy-smart-contract-call

// --- vvv --- vvv --- vvv --- vvv ---

goal clerk send -a 1222333 -f RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM -t 36XJYDRIBTRGEYOY3QJG732PAKTVEHWSKL7E66ITYDBGZGIJLS5UF6JCBQ  -w seller_wallet -o unsignedtransaction1.tx

goal app call --app-id 106 --from RHKHUONCBB7JOIQ2RDCSV3NUX5JFKLLOG2RKN4LRIJ6DQMAIBTFLLO72DM --out ./unsignedtransaction2.tx

cat unsignedtransaction1.tx unsignedtransaction2.tx > combinedtransactions.tx

goal clerk group -i combinedtransactions.tx -o groupedtransactions.tx

goal clerk sign -w seller_wallet -i groupedtransactions.tx -o signout.tx

goal clerk dryrun -t signout.tx --dryrun-dump -o dr.msgp

tealdbg debug -d dr.msgp --listen 0.0.0.0

// --- ^^^ --- ^^^ --- ^^^ --- ^^^ ---

echo "iaRhcGFhkcQPc2lnbmFsX3B1bGxfb3V0pGFwaWTM9aNmZWXNA+iiZnbOAAGUeaNnZW6qc2FuZG5ldC12MaJnaMQg3SI23LH1Eec0kQDmcZSH8O1P+36mkI0y2z1WMYK+DoWibHbOAAGYYaNzbmTEIInUejmiCH6XIhqIxSrttL9SVS1uNqKm8XFCfDgwCAzKpHR5cGWkYXBwbA==" | base64 -d | msgpacktool -d