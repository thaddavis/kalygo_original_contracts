from re import M
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))
from pyteal import *
from pyteal_helpers import program

UINT64_MAX=0xffffffffffffffff

def approval_program():
    # vvv vvv vvv
    GLOBAL_CREATOR=Bytes("creator") # byteslice
    GLOBAL_SELLER=Bytes("seller") # byteslice
    GLOBAL_ARBITER=Bytes("arbiter") # byteslice
    GLOBAL_BUYER=Bytes("buyer") # byteslice
    GLOBAL_INSPECTION_BEGIN = Bytes("inspection_begin") # int
    GLOBAL_INSPECTION_END = Bytes("inspection_end") # int
    GLOBAL_INSPECTION_EXTENSION = Bytes("inspection_extension") # int
    GLOBAL_CLOSING_DATE = Bytes("closing_date") # int
    GLOBAL_CLOSING_DATE_EXTENSION = Bytes("closing_date_extension") # int
    GLOBAL_SALE_PRICE=Bytes("sale_price") # int
    GLOBAL_1st_ESCROW_AMOUNT = Bytes("1st_escrow_amount") # int
    GLOBAL_2nd_ESCROW_AMOUNT = Bytes("2nd_escrow_amount") # int
    GLOBAL_SIGNAL_PULL_OUT = Bytes("signal_pull_out") # int
    GLOBAL_SIGNAL_ARBITRATION = Bytes("signal_arbitration") # int
    GLOBAL_ENABLE_TIME_CHECKS = Bytes("enable_time_checks") # int
    GLOBAL_CONTRACT_BALANCE = Bytes("contract_balance") # int
    GLOBAL_CONTRACT_ADDRESS = Bytes("contract_address") # byteslice
    # ^^^ ^^^ ^^^
    SIGNAL_PULL_OUT=Bytes("signal_pull_out") # CONSTANT
    SIGNAL_ARBITRATION=Bytes("signal_arbitration") # CONSTANT
    BUYER_WITHDRAW_FUNDS=Bytes("buyer_withdraw_funds") # CONSTANT
    SELLER_WITHDRAW_FUNDS=Bytes("seller_withdraw_funds") # CONSTANT
    ARBITER_WITHDRAW_FUNDS=Bytes("arbiter_withdraw_funds") # CONSTANT
    FUND_CONTRACT=Bytes("fund_contract")
    FUND_MINIMUM_BALANCE=Bytes("fund_minimum_balance")
    
    @Subroutine(TealType.none)
    def signal_pull_out():
        return Seq(
            If(
                And(
                    Txn.sender() == App.globalGet(GLOBAL_BUYER),
                    And(
                        App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                        Global.latest_timestamp() < App.globalGet(GLOBAL_INSPECTION_END)
                    )
                )
            )
            .Then(
                Seq(
                    App.globalPut(GLOBAL_CONTRACT_ADDRESS, Global.current_application_address()),
                    App.globalPut(GLOBAL_CONTRACT_BALANCE, Balance(Global.current_application_address())),
                    App.globalPut(GLOBAL_SIGNAL_PULL_OUT, App.globalGet(GLOBAL_SIGNAL_PULL_OUT) + Int(1))
                )
            )
            .Else(
                Reject()
            ),
            Approve()
        )

    @Subroutine(TealType.none)
    def signal_arbitration():
        return Seq(
            If(
                And(
                    Txn.sender() == App.globalGet(GLOBAL_BUYER),
                    And(
                        App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                        Global.latest_timestamp() < App.globalGet(GLOBAL_CLOSING_DATE_EXTENSION)  
                    )
                )
            )
            .Then(
                App.globalPut(GLOBAL_SIGNAL_ARBITRATION, App.globalGet(GLOBAL_SIGNAL_ARBITRATION) + Int(1))
            )
            .Else(
                Reject()
            ),
            Approve()
        )

    @Subroutine(TealType.none)
    def seller_withdraw_funds():
        return Seq(
            If(
                And(
                    Txn.sender() == App.globalGet(GLOBAL_SELLER),
                    App.globalGet(GLOBAL_SIGNAL_PULL_OUT) == Int(0),
                    App.globalGet(GLOBAL_SIGNAL_ARBITRATION) == Int(0),
                    And(
                        App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                        Global.latest_timestamp() > App.globalGet(GLOBAL_CLOSING_DATE)
                    ) 
                )
            )
            .Then(
                Seq(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields({
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.amount: Balance(Global.current_application_address()) - Global.min_balance() - Global.min_txn_fee(),
                        TxnField.sender: Global.current_application_address(),
                        TxnField.receiver: Txn.sender(),
                        TxnField.fee: Global.min_txn_fee(),
                    }),
                    InnerTxnBuilder.Submit()
                )
            )
            .Else(
                Reject()
            ),
            Approve()
        )

    @Subroutine(TealType.none)
    def buyer_withdraw_funds(): 
        return Seq(
            If(
                And(
                    Txn.sender() == App.globalGet(GLOBAL_BUYER),
                    And(
                        App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                        Global.latest_timestamp() < App.globalGet(GLOBAL_INSPECTION_END)
                    ),
                    Or(
                        And(
                            App.globalGet(GLOBAL_SIGNAL_PULL_OUT) > Int(0),
                            (
                                Balance(Global.current_application_address())
                                    - Global.min_balance() - Global.min_txn_fee()
                            ) >= App.globalGet(GLOBAL_1st_ESCROW_AMOUNT) - Global.min_txn_fee()
                        )
                    )   
                )
            )
            .Then(
                Seq(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields({
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.amount: App.globalGet(GLOBAL_1st_ESCROW_AMOUNT) - Global.min_txn_fee(),
                        TxnField.sender: Global.current_application_address(),
                        TxnField.receiver: Txn.sender(),
                        TxnField.fee: Global.min_txn_fee(),
                    }),
                    InnerTxnBuilder.Submit(),
                    Approve()
                )
            )
            .Else(
                Reject()
            )
        )

    @Subroutine(TealType.none)
    def arbiter_withdraw_funds():
        return Seq(
            If(
                And(
                    Txn.sender() == App.globalGet(GLOBAL_ARBITER),
                    App.globalGet(GLOBAL_SIGNAL_ARBITRATION) > Int(0),
                    And(
                        App.globalGet(GLOBAL_ENABLE_TIME_CHECKS) == Int(1),
                        Global.latest_timestamp() > App.globalGet(GLOBAL_CLOSING_DATE)
                    ),
                    Or(
                        App.globalGet(GLOBAL_SELLER) == Txn.application_args[1],
                        App.globalGet(GLOBAL_BUYER) == Txn.application_args[1]
                    )
                )
            )
            .Then(
                Seq(
                    InnerTxnBuilder.Begin(),
                    InnerTxnBuilder.SetFields({
                        TxnField.type_enum: TxnType.Payment,
                        TxnField.amount: Balance(Global.current_application_address()) - Global.min_balance() - Global.min_txn_fee(),
                        TxnField.sender: Global.current_application_address(),
                        TxnField.receiver: Txn.accounts[1],
                        TxnField.fee: Global.min_txn_fee(),
                    }),
                    InnerTxnBuilder.Submit()
                )
            )
            .Else(
                Reject()
            ),
            Approve()
        )

    @Subroutine(TealType.none)
    def fund_account():
        return Seq([
            If(
                Or(
                    And(
                        Gtxn[0].sender() == App.globalGet(GLOBAL_BUYER),
                        Gtxn[0].amount() == App.globalGet(GLOBAL_1st_ESCROW_AMOUNT)
                    ),
                    And(
                        Gtxn[0].sender() == App.globalGet(GLOBAL_BUYER),
                        Gtxn[0].amount() == App.globalGet(GLOBAL_2nd_ESCROW_AMOUNT)
                    )
                )
            )
            .Then(
                Seq(
                    App.globalPut(GLOBAL_CONTRACT_ADDRESS, Global.current_application_address()),
                    App.globalPut(GLOBAL_CONTRACT_BALANCE, Balance(Global.current_application_address())),
                    Approve(),
                )
            )
            .Else(
                Reject()
            )
        ])

    @Subroutine(TealType.none)
    def delete_app():
        return Seq(
            [
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: Balance(Global.current_application_address()) - Global.min_txn_fee(),
                    TxnField.sender: Global.current_application_address(),
                    TxnField.receiver: App.globalGet(GLOBAL_CREATOR),
                    TxnField.fee: Global.min_txn_fee(),
                    TxnField.close_remainder_to: Txn.sender()
                }),
                InnerTxnBuilder.Submit(),
                Approve()
            ]
        )

    @Subroutine(TealType.none)
    def fund_minimum_balance():
        return Seq([
            If(
                Or(
                    Gtxn[0].sender() == App.globalGet(GLOBAL_BUYER),
                    Gtxn[0].sender() == App.globalGet(GLOBAL_CREATOR),
                    Gtxn[0].sender() == App.globalGet(GLOBAL_SELLER),
                    Gtxn[0].sender() == App.globalGet(GLOBAL_ARBITER)
                )
            )
            .Then(
                Approve()
            )
            .Else(
                Reject()
            )
        ])

    return program.event(
        init=Seq(
            App.globalPut(GLOBAL_CREATOR, Txn.sender()), # byte_slice
            App.globalPut(GLOBAL_INSPECTION_BEGIN, Btoi(Txn.application_args[0])), # int
            App.globalPut(GLOBAL_INSPECTION_END, Btoi(Txn.application_args[1])), # int
            App.globalPut(GLOBAL_INSPECTION_EXTENSION, Btoi(Txn.application_args[2])), # int
            App.globalPut(GLOBAL_CLOSING_DATE, Btoi(Txn.application_args[3])), # int
            App.globalPut(GLOBAL_CLOSING_DATE_EXTENSION, Btoi(Txn.application_args[4])), # int
            App.globalPut(GLOBAL_SALE_PRICE, 
                If(
                    And(
                        Btoi(Txn.application_args[5]) == Btoi(Txn.application_args[6]) + Btoi(Txn.application_args[7]),
                        Btoi(Txn.application_args[6]) < Btoi(Txn.application_args[7]),
                        Btoi(Txn.application_args[5]) > Int(100000) # Value of Escrow must be at least .1 ALGO
                    )
                )
                .Then(
                    Btoi(Txn.application_args[5])
                )
                .Else(
                    Reject()
                )
            ), # int
            App.globalPut(GLOBAL_1st_ESCROW_AMOUNT, Btoi(Txn.application_args[6])), # int
            App.globalPut(GLOBAL_2nd_ESCROW_AMOUNT, Btoi(Txn.application_args[7])), # int
            App.globalPut(GLOBAL_BUYER, Txn.application_args[8]), # byte_slice
            App.globalPut(GLOBAL_SELLER, Txn.application_args[9]), # byte_slice
            App.globalPut(GLOBAL_ARBITER, Txn.sender()), # byte_slice
            App.globalPut(GLOBAL_SIGNAL_PULL_OUT, Int(0)), # int
            App.globalPut(GLOBAL_SIGNAL_ARBITRATION, Int(0)), # int
            App.globalPut(GLOBAL_ENABLE_TIME_CHECKS, Btoi(Txn.application_args[11])), # int
            Approve()
        ),
        close_out=Seq(Approve()),
        update=Seq(Approve()),
        delete=Seq([
            delete_app(),
            Reject()
        ]),
        no_op=Seq(
            Cond(
                [ Txn.application_args[0] == SIGNAL_PULL_OUT, signal_pull_out() ],
                [ Txn.application_args[0] == SIGNAL_ARBITRATION, signal_arbitration() ],
                [ Txn.application_args[0] == SELLER_WITHDRAW_FUNDS, seller_withdraw_funds()],
                [ Txn.application_args[0] == BUYER_WITHDRAW_FUNDS, buyer_withdraw_funds()],
                [ Txn.application_args[0] == ARBITER_WITHDRAW_FUNDS, arbiter_withdraw_funds()],
                [ 
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.Payment,
                        Gtxn[1].type_enum() == TxnType.ApplicationCall,
                        Gtxn[1].application_args[0] == FUND_CONTRACT
                    ),
                    fund_account()
                ],
                [
                    And(
                        Global.group_size() == Int(2),
                        Gtxn[0].type_enum() == TxnType.Payment,
                        Gtxn[1].type_enum() == TxnType.ApplicationCall,
                        Gtxn[1].application_args[0] == FUND_MINIMUM_BALANCE
                    ),
                    fund_minimum_balance()
                ]
            ),
            Reject()
        )
    )

def clear_state_program():
    return Approve()