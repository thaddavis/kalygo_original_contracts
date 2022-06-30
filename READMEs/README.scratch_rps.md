 ./sandbox enter algod

 ONE=BCU6RH2MWO4X46BQPAQ4MFUFJKJDX2MBEUZ4W4VLPJVUMSFJM2GJJ345VA 

 goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1

 goal app optin --from $ONE --app-id 58

 goal app read --local --from $ONE --app-id 58

goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 0 --global-ints 0 --local-byteslices 3 --local-ints 1

goal app info --app-id 60

goal app optin --app-id 63 --from $ONE

goal app optin --app-id 63 --from $TWO

goal app read --local --from $ONE --app-id 63 --guess-format
goal app read --local --from $ONE --app-id 63 --guess-format