import socket
import threading
import sys
from datetime import datetime

class TerminalChat:
    def __init__(self, port=12345):
        self.port = port
        self.socket = None
        self.connection = None
        self.running = False
        self.messages = []
        self.my_public_ip = ""
        self.their_public_ip = ""
        
    def get_local_ip(self):
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def get_public_ip(self):
        """Get the public IP address"""
        try:
            import urllib.request
            response = urllib.request.urlopen('https://api.ipify.org', timeout=3)
            return response.read().decode('utf-8')
        except:
            try:
                response = urllib.request.urlopen('https://ifconfig.me/ip', timeout=3)
                return response.read().decode('utf-8').strip()
            except:
                return "Unable to fetch"
    
    def log_message(self, sender, message, sender_ip=""):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages.append((timestamp, sender, message, sender_ip))
        self.print_message(timestamp, sender, message, sender_ip)
    
    def print_message(self, timestamp, sender, message, sender_ip=""):
        """Print a single message with formatting"""
        if sender == "You":
            print(f"\033[92m({self.my_public_ip}): {message}\033[0m")
        else:
            print(f"\033[94m({sender_ip}): {message}\033[0m")
    
    def print_system(self, message):
        """Print system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\033[93m[{timestamp}] SYSTEM: {message}\033[0m")
    
    def receive_messages(self):
        """Thread for receiving messages"""
        while self.running:
            try:
                message = self.connection.recv(1024).decode('utf-8')
                if message:
                    self.log_message("Them", message, self.their_public_ip)
                else:
                    break
            except:
                break
        
        if self.running:
            self.print_system("Connection lost!")
            self.running = False
    
    def start_server(self):
        """Start as server (receiver) - waits for connection requests"""
        local_ip = self.get_local_ip()
        public_ip = self.get_public_ip()
        self.my_public_ip = public_ip
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        
        print("\n" + "="*60)
        print("TERMINAL CHAT - LISTENING MODE")
        print("="*60)
        self.print_system(f"Local IP: {local_ip}")
        self.print_system(f"Public IP: {public_ip}")
        self.print_system(f"Listening on port {self.port}")
        self.print_system("Share your PUBLIC IP with others!")
        self.print_system("Waiting for incoming connection requests...")
        print("="*60 + "\n")
        
        # Accept connection
        conn, addr = self.socket.accept()
        
        # Receive the connection request with sender's IP
        try:
            request_data = conn.recv(1024).decode('utf-8')
            sender_ip = request_data.split('|')[0] if '|' in request_data else addr[0]
            self.their_public_ip = sender_ip
            
            self.print_system(f"Connection request from {sender_ip}")
            
            # Ask for permission
            print("\n" + "-"*60)
            response = input(f"Someone from {sender_ip} wants to chat. Accept? (yes/no): ").strip().lower()
            print("-"*60 + "\n")
            
            if response in ['yes', 'y']:
                conn.send("ACCEPTED".encode('utf-8'))
                self.connection = conn
                self.running = True
                
                self.print_system(f"Connection accepted! Connected to {sender_ip}")
                self.print_system("Type your messages and press Enter to send")
                self.print_system("Press Ctrl+C or type \\exit to quit")
                print("-"*60 + "\n")
                
                # Start receiving thread
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.daemon = True
                receive_thread.start()
                
                # Send messages
                try:
                    while self.running:
                        message = input()
                        if message == '\\exit':
                            break
                        if message.strip():  # Only send non-empty messages
                            self.connection.send(message.encode('utf-8'))
                            self.log_message("You", message)
                except KeyboardInterrupt:
                    print()  # New line after Ctrl+C
                    self.print_system("Exiting chat...")
                    pass
            else:
                conn.send("REJECTED".encode('utf-8'))
                self.print_system("Connection rejected.")
                conn.close()
                
        except Exception as e:
            self.print_system(f"Error during connection: {e}")
            conn.close()
        
        self.cleanup()
    
    def start_client(self, server_ip):
        """Start as client (sender) - initiates connection request"""
        my_public_ip = self.get_public_ip()
        self.my_public_ip = my_public_ip
        self.their_public_ip = server_ip
        
        print("\n" + "="*60)
        print("TERMINAL CHAT - CLIENT MODE")
        print("="*60)
        self.print_system(f"Your public IP: {my_public_ip}")
        self.print_system(f"Connecting to {server_ip}:{self.port}...")
        self.print_system("Sending connection request...")
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(15)  # 15 second timeout for response
        
        try:
            self.socket.connect((server_ip, self.port))
            
            # Send connection request with your IP
            request = f"{my_public_ip}|REQUEST"
            self.socket.send(request.encode('utf-8'))
            
            self.print_system("Waiting for them to accept...")
            
            # Wait for acceptance
            response = self.socket.recv(1024).decode('utf-8')
            
            if response == "ACCEPTED":
                self.connection = self.socket
                self.running = True
                
                self.print_system("Connection accepted!")
                self.print_system("Type your messages and press Enter to send")
                self.print_system("Press Ctrl+C or type \\exit to quit")
                print("-"*60 + "\n")
                
                # Start receiving thread
                receive_thread = threading.Thread(target=self.receive_messages)
                receive_thread.daemon = True
                receive_thread.start()
                
                # Send messages
                try:
                    while self.running:
                        message = input()
                        if message == '\\exit':
                            break
                        if message.strip():  # Only send non-empty messages
                            self.connection.send(message.encode('utf-8'))
                            self.log_message("You", message)
                except KeyboardInterrupt:
                    print()  # New line after Ctrl+C
                    self.print_system("Exiting chat...")
                    pass
            else:
                self.print_system("Connection was rejected by the other person.")
            
        except socket.timeout:
            self.print_system("Connection timed out. They may not have responded.")
        except Exception as e:
            self.print_system(f"Connection failed: {e}")
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up connections"""
        self.running = False
        if self.connection:
            self.connection.close()
        if self.socket:
            self.socket.close()
        self.print_system("Chat session ended.")
        if self.messages:
            self.print_summary()
    
    def print_summary(self):
        """Print chat summary"""
        print("\n" + "="*60)
        print(f"CHAT SUMMARY - {len(self.messages)} messages")
        print("="*60)
        for timestamp, sender, message, sender_ip in self.messages:
            self.print_message(timestamp, sender, message, sender_ip)
        print("="*60 + "\n")

def main():
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║            TERMINAL CHAT - P2P Messenger                 ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    chat = TerminalChat()
    
    print("Choose mode:")
    print("  [1] Listen for connections (wait for others to connect to you)")
    print("  [2] Connect to someone (you need their public IP)\n")
    
    mode = input("Enter 1 or 2: ").strip()
    
    if mode == '1':
        chat.start_server()
    elif mode == '2':
        print("\n" + "-"*60)
        server_ip = input("Enter the public IP of the person you want to chat with: ").strip()
        print("-"*60)
        chat.start_client(server_ip)
    else:
        print("Invalid choice!")
        sys.exit(1)

if __name__ == "__main__":
    main()
