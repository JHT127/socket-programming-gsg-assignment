
# Socket Programming
# Client Side

import socket

# we first create a socket object
try:
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)  # AF_INET is the address for IPv4,SOCK_STREAM is for TCP
except socket.error as msg:
    print(f"Socket creation failed with error {msg}")  # failed to create socket

# second we connect to the server
port_number = 12345
try:
    s.connect(('127.0.0.1', port_number))  # Connect to the specified IP address and port
    print(f"Connected to server at localhost:{port_number}")
except socket.error as msg:
    print(f"Connection failed with error {msg}")  # failed to connect

# we tell the user to enter expressions or quit
print("Enter expressions like '12 + 7' or 'quit' to exit:")

# third we send data to the server and receive responses
# we use a while loop to continuously send data until the user says "quit"

while True:
    try:
        # get user input
        user_choice = input("> ") # print the prompt (>) and wait for user input

        # send the data to the server
        s.send(user_choice.encode())

        # if the user says "quit", break the loop
        if user_choice.lower() == "quit":
            break

        # receive the response from the server
        response = s.recv(2048).decode()

        # if no response is received, break the loop
        if not response:
            break

        # display the response
        print(f"Result: {response}")

    except socket.error as msg:
        print(f"Error during communication: {msg}")
        break
    except KeyboardInterrupt:
        print("\nClient interrupted by user")
        break

# fourth we close the connection
s.close()
print("Connection closed")