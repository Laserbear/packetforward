import socket
import threading

def handle_tcp_client(client_socket, forward_ip, forward_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
        forward_socket.connect((forward_ip, forward_port))
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                print("Forwarded TCP")
                forward_socket.sendall(data)
        except Exception as e:
            print(f"Error forwarding data: {e}")
        finally:
            client_socket.close()

def handle_udp_client(server_udp, forward_ip, forward_port):
    while True:
        data, addr = server_udp.recvfrom(4096)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as forward_socket:
            print("Forwarded UDP")
            forward_socket.sendto(data, (forward_ip, forward_port))

def start_tcp_server(listen_ip, listen_port, forward_ip, forward_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
        server_tcp.bind((listen_ip, listen_port))
        server_tcp.listen(5)
        print(f"[*] Listening for TCP on {listen_ip}:{listen_port}")
        while True:
            client_socket, addr = server_tcp.accept()
            print(f"[*] Accepted TCP connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_tcp_client, args=(client_socket, forward_ip, forward_port))
            client_handler.start()

def start_udp_server(listen_ip, listen_port, forward_ip, forward_port):
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((listen_ip, listen_port))
    print(f"[*] Listening for UDP on {listen_ip}:{listen_port}")
    udp_handler = threading.Thread(target=handle_udp_client, args=(server_udp, forward_ip, forward_port))
    udp_handler.start()

def main():
    TARGET_IP = "" #ip of host
    listen_ip = "127.0.0.1"
    listen_port_tcp = 47624
    listen_port_udp = 3457
    forward_ip = TARGET_IP
    forward_port_tcp = 42069 #port host has forwarded
    forward_port_udp = 47624

    # Start TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server, args=(listen_ip, listen_port_tcp, forward_ip, forward_port_tcp))
    tcp_thread.start()
    
    # Start UDP server in a separate thread
    udp_thread = threading.Thread(target=start_udp_server, args=(listen_ip, listen_port_udp, forward_ip, forward_port_udp))
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()

if __name__ == "__main__":
    main()
