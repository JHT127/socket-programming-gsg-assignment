
# Socket Programming
# Server Side

import socket

# we first create a socket object
try:
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)  #AF_INET is the address for IPv4,SOCK_STREAM is for TCP
except socket.error as msg:
    print(f"Socket creation failed with error {msg}")  # failed to create socket


# second we bind the socket to a port
port_number = 12345
try:
    s.bind(('127.0.0.1', port_number))  # Bind to the specified IP address and port
    print(f"Server started on localhost:{port_number}")
except socket.error as msg:
    print(f"Binding failed with error {msg}")  # failed to bind


# third we listen for incoming connections
try:
    s.listen(200)  # listen for 200 connections max
except socket.error as msg:
    print(f"Listening failed with error {msg}")  # failed to listen


# fourth we accept incoming connections
# we use a while loop to accept incoming connections until the server is closed
message_response = " " # initialize the message response
try:
    while True:
            c, addr = s.accept()  # accept incoming connections
            print(f"Connected by {addr}")

            # the inner loop is for handling multiple messages from the client
            while True:
                try:
                    # fifth we receive data from the client
                    data = c.recv(2048).decode()

                    # if no data is received, close the connection
                    if not data:
                        break
                    # if the client sends "quit", close the connection
                    if data.lower() == "quit":
                        break

                    # split the data into tokens
                    token = data.strip().split()
                    if len(token) != 3:
                        message_response ="Invalid input expression please make sure it is in the correct format : (operand1 operator operand2) eg. (2 + 2)"

                    else:

                        try:
                            # convert the tokens to numbers and operators
                            operand1 = float(token[0])
                            operator = token[1]
                            operand2 = float(token[2])

                            # perform the operations (addition, subtraction, multiplication, division, modulus, exponentiation)
                            if operator == "+":
                                message_response = f"{operand1} + {operand2} = {operand1 + operand2}"
                            elif operator == "-":
                                message_response = f"{operand1} - {operand2} = {operand1 - operand2}"
                            elif operator == "*":
                                message_response = f"{operand1} * {operand2} = {operand1 * operand2}"
                            elif operator == "/":
                                try:
                                    message_response = f"{operand1} / {operand2} = {operand1 / operand2}"
                                except ZeroDivisionError:
                                    message_response = "Cannot divide by zero"
                            elif operator == "%":
                                try:
                                    message_response = f"{operand1} % {operand2} = {operand1 % operand2}"
                                except ZeroDivisionError: # cannot perform modulus by zero (no division by zero)
                                    message_response = "Cannot perform modulus by zero"
                            elif operator == "^":
                                # m ^ (-n) = 1 / (m ^ n) so 0 ^ (-n) = 1 / (0 ^ n) if n is not 0 then the result would be 1 / 0 which is undefined
                                try:
                                    if operand2 < 0 and operand1 == 0:
                                        message_response = "Cannot raise 0 to a negative power"
                                    else:
                                        message_response = f"{operand1} ^ {operand2} = {operand1 ** operand2}"
                                except ZeroDivisionError:
                                    message_response = "Cannot raise 0 to a negative power"
                            else:
                                message_response = "Invalid operator" # if the operator is invalid

                        except ValueError:
                            message_response = "Invalid numbers" # if the tokens cannot be converted to numbers

                    # sixth we send the response to the client
                    try:
                        c.send(message_response.encode())
                    except socket.error as msg:
                        print(f"Error during sending: {msg}")
                        break

                except socket.error as msg:
                    print(f"Error during receiving: {msg}")
                    break

            # seventh we close the connection
            try:
                c.close()
            except socket.error as msg:
                print(f"Error during closing: {msg}")

# if an error occurs, print the error message
except socket.error as msg:
    print(f"Accept failed with error: {msg}")