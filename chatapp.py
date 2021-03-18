from chat import create_socket, create_app

app = create_app()
socket = create_socket()


if __name__ == "__main__":
    socket.run(app)
