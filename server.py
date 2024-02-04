import socket
import threading
import MetaTrader5 as mt5

account = #enter your account number here 
password = "your account passwoard"
server = "your broker server name"


# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# now connect to  trading account specifying the password
authorized=mt5.login(login=account, password=password,server=server)
if authorized:

    # display trading account data in the form of a list
    print("connecting to terminal success")

else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))




#orders = mt5.positions_get(magic = 9347538)

#print(orders[0])


#local addres
host = "0.0.0.0"

#lockal port
port = 12345

#set up socket value
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding connection
server_socket.bind((host, port))

#starting server
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

#starting connection
while True :

    print("Waiting for connection...")

    #accepting connect request
    client_socket, address = server_socket.accept()

    #listen at the port
    server_socket.listen(5)

    print(f"Accepted connection from {address}")

    #start trading
    while True:
        
        counter = 0

        #reset the value
        reciv = ""

        #reciving dta from client
        data = client_socket.recv(1024)

        #change binary to utf8
        reciv = str(data.decode('utf-8'))

        #if there is not a connection wait for connection
        if not data:
            print(f"Connection with {address} closed.")
            break

        #if recived a value
        if reciv :

            print(reciv)
            
            #change recived message to list format
            reciv = reciv.split()

            if (reciv[0] == "trade_buy"):

                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_DEAL,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_BUY,"magic": int(reciv[3]),})
                  
            elif (reciv[0] == "trade_sell"):
                
                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_DEAL,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_SELL,"magic": int(reciv[3]),})

            elif (reciv[0] == "buy_limit"):

                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_PENDING,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_BUY_LIMIT,"price": float(reciv[3]),"magic": int(reciv[4]),})

            elif (reciv[0] == "sell_limit"):

                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_PENDING,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_SELL_LIMIT,"price": float(reciv[3]),"magic": int(reciv[4]),})
            
            elif (reciv[0] == "buy_stop"):

                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_PENDING,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_BUY_STOP,"price": float(reciv[3]),"magic": int(reciv[4]),})

            elif (reciv[0] == "sell_stop"):

                # send a trading request
                mt5.order_send({"action": mt5.TRADE_ACTION_PENDING,"symbol": str(reciv[1]),"volume": float(reciv[2]),"type": mt5.ORDER_TYPE_SELL_STOP,"price": float(reciv[3]),"magic": int(reciv[4]),})

            elif (reciv[0] == "trade_sl/tp"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (position_info[counter][6] == int(reciv[6])):

                        #put ticket in variable
                        ticket_num = int(position_info[counter][0])

                        # send changing sl/tp request
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP,"position": ticket_num,"symbol": str(reciv[1]),"sl": float(reciv[4]),"tp": float(reciv[5]),"magic": int(reciv[6]),})

                        #breaking the while
                        break

                    counter += 1

            elif (reciv[0] == "order_change"):

                #getting position info
                order_info = mt5.orders_get()

                #gett number of all open trades
                total_order = mt5.orders_total()

                #checking all open position
                while (total_order != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (order_info[counter][10] == int(reciv[6])):

                        #put ticket in variable
                        ticket_num = int(order_info[counter][0])

                        # send changing sl/tp request
                        mt5.order_send({"action": mt5.TRADE_ACTION_MODIFY ,"order": ticket_num,"symbol": str(reciv[1]),"price": float(reciv[3]),"sl": float(reciv[4]),"tp": float(reciv[5]),"magic": int(reciv[6]),})

                        #breaking the while
                        break

                    counter += 1

            elif (reciv[0] == "order_delete"):

                #getting position info
                order_info = mt5.orders_get()

                #gett number of all open trades
                total_order = mt5.orders_total()

                #checking all open position
                while (total_order != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (order_info[counter][10] == int(reciv[4])):

                        #put ticket in variable
                        ticket_num = int(order_info[counter][0])

                        # send delete request
                        mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE ,"order": ticket_num,"symbol": str(reciv[1]),"price": float(reciv[3]),"magic": int(reciv[4]),})

                        #breaking the while
                        break

                    counter += 1

            elif (reciv[0] == "close_sell"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (position_info[counter][6] == int(reciv[4])):

                        #put ticket in variable
                        ticket_num = int(position_info[counter][0])

                        #sending close request
                        mt5.Close(symbol = str(reciv[1]),ticket = ticket_num)

                        #breaking the while
                        break

                    counter += 1

            elif (reciv[0] == "close_position"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (position_info[counter][6] == int(reciv[4])):

                        #put ticket in variable
                        ticket_num = int(position_info[counter][0])

                        #sending close request
                        mt5.Close(symbol = str(reciv[1]),ticket = ticket_num)

                        #breaking the while
                        break

                    counter += 1

            elif (reciv[0] == "tp_change"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :

                    #if the trade magic number == trade ticket recived from server
                    if (position_info[counter][16] == reciv[1]):

                        #put ticket in variable
                        ticket_num = int(position_info[counter][0])

                        # send changing sl request
                        resault=mt5.order_send({"action": mt5.TRADE_ACTION_SLTP,"position": ticket_num,"symbol": str(reciv[1]),"sl": 0.00,"tp": float(reciv[2]),})
                    
                        # send changing tp request
                        resault=mt5.order_send({"action": mt5.TRADE_ACTION_SLTP,"position": ticket_num,"symbol": str(reciv[1]),"sl": float(reciv[2]),"tp": 0.00,})

                    counter += 1

                counter = 0

                #getting position info
                order_info = mt5.orders_get()

                #gett number of all open trades
                total_order = mt5.orders_total()

                #checking all open position
                while (total_order != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (order_info[counter][21] == str(reciv[1])):

                        #put ticket in variable
                        ticket_num = int(order_info[counter][0])

                        # send changing sl request
                        mt5.order_send({"action": mt5.TRADE_ACTION_MODIFY ,"order": ticket_num,"symbol": str(reciv[1]),"price": float(order_info[counter][16]),"sl": float(reciv[2]),"tp": 0.00,})
                        
                        # send changing tp request
                        mt5.order_send({"action": mt5.TRADE_ACTION_MODIFY ,"order": ticket_num,"symbol": str(reciv[1]),"price": float(order_info[counter][16]),"sl": 0.00,"tp": float(reciv[2]),})

                    counter += 1

            elif (reciv[0] == "all_orders_delete"):

                #getting position info
                order_info = mt5.orders_get()

                #gett number of all open trades
                total_order = mt5.orders_total()

                #checking all open position
                while (total_order != counter) :
                    
                    #put ticket in variable
                    ticket_num = int(order_info[counter][0])

                    # send delete request
                    mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE ,"order": ticket_num,"symbol": str(reciv[1]),})

                    counter += 1

            elif (reciv[0] == "current_symbol_orders_delete"):

                #getting position info
                order_info = mt5.orders_get()

                #gett number of all open trades
                total_order = mt5.orders_total()

                #checking all open position
                while (total_order != counter) :
                    
                    #if the trade magic number == trade ticket recived from server
                    if (order_info[counter][21] == reciv[1]):

                        #put ticket in variable
                        ticket_num = int(order_info[counter][0])

                        # send delete request
                        mt5.order_send({"action": mt5.TRADE_ACTION_REMOVE ,"order": ticket_num,"symbol": str(reciv[1]),})

                    counter += 1

            elif (reciv[0] == "all_positions_close"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :
                    
                    #put ticket in variable
                    ticket_num = int(position_info[counter][0])

                    #sending close request
                    mt5.Close(symbol = str(reciv[1]),ticket = ticket_num)

                    counter += 1

            elif (reciv[0] == "current_symbol_positions_close"):

                #getting position info
                position_info = mt5.positions_get()

                #gett number of all open trades
                total_position = mt5.positions_total()

                #checking all open position
                while (total_position != counter) :
                                        
                    #if the trade magic number == trade ticket recived from server
                    if (position_info[counter][16] == reciv[1]):
    
                        #put ticket in variable
                        ticket_num = int(position_info[counter][0])

                        #sending close request
                        mt5.Close(symbol = str(reciv[1]),ticket = ticket_num)

                    counter += 1
