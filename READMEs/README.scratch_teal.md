./build.sh contracts.counter.step_01

goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 1 --global-ints 1 --local-byteslices 0 --local-ints 0

goal app info --app-id 45

goal app read --global --app-id 45
goal app read --global --app-id 45 --guess-format

goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 1 --global-ints 1 --local-byteslices 0 --local-ints 0

goal app call --app-id 46 --from $ONE --app-arg "str:inc"

goal app read --global --app-id 46 --guess-format

goal app call --app-id 46 --from $ONE --app-arg "str:dec"

goal app call --app-id 46 --from $ONE --app-arg "str:dec" --dryrun-dump -o tx.dr

tealdbg debug -d tx.dr --listen 0.0.0.0

goal app create --creator $ONE --approval-prog /data/build/approval.teal --clear-prog /data/build/clear.teal --global-byteslices 1 --global-ints 1 --local-byteslices 0 --local-ints 0


