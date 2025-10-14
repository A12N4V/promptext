# Terminal Chat - P2P Messenger

A simple peer-to-peer terminal-based chat application for direct communication between two users over the internet.

## Features

- Direct P2P connection with no intermediary servers
- Permission-based connections (server explicitly accepts requests)
- Clean message interface with color-coded output
- Automatic public IP detection
- Real-time bidirectional messaging
- Session chat history on exit

## Requirements

- Python 3.6+
- Internet connection
- Port forwarding capability or ngrok

## Installation

Clone the repository:

```bash
git clone https://github.com/A12N4V/promptext.git
cd promptext
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 terminal_chat.py
```

## Usage

### Listener (Person A)

1. Run `python3 terminal_chat.py`
2. Select option 1
3. Share your public IP with the other person
4. Accept or reject the incoming connection
5. Start chatting

### Connector (Person B)

1. Run `python3 terminal_chat.py`
2. Select option 2
3. Enter the listener's public IP
4. Wait for acceptance
5. Start chatting

### Commands

- `Ctrl+C` - Exit immediately
- `\exit` - Graceful exit

Messages appear in this format:
```
(123.45.67.89): your message
(98.76.54.321): their message
```

## SECURITY WARNING

**This application sends ALL messages in PLAIN TEXT with NO ENCRYPTION.**

Do not use this for:
- Passwords or credentials
- Financial information
- Personal identifying information
- Medical records
- Confidential business data
- Anything sensitive

This tool is appropriate for:
- Casual conversations
- Educational/learning purposes
- Non-sensitive communication only

### Known Security Issues

- All messages can be intercepted on the network
- No authentication system
- Vulnerable to man-in-the-middle attacks
- Port forwarding exposes your network
- Public IP reveals approximate location
- No message integrity verification

Use at your own risk.

## Network Setup

### Port Forwarding

The listener must configure port forwarding on their router:

1. Access router settings (typically 192.168.1.1 or 192.168.0.1)
2. Navigate to Port Forwarding or Virtual Server
3. Add rule:
   - External Port: 12345
   - Internal Port: 12345
   - Internal IP: Your local IP
   - Protocol: TCP
4. Save changes

### Alternative: ngrok

If port forwarding isn't an option:

1. Download ngrok from https://ngrok.com/download
2. Run `ngrok tcp 12345`
3. Share the ngrok address instead of your public IP

## Troubleshooting

**Connection failed**
- Verify port 12345 is forwarded
- Check firewall settings
- Confirm stable internet connection

**Connection timed out**
- Listener didn't respond within 15 seconds
- Firewall blocking connection
- Wrong IP address

**Connection lost**
- Network interruption
- Connection closed by other party
- Router/IP change

**Public IP not detected**
- Internet connectivity issue
- Try manually checking at whatismyip.com

## Future Development

### Planned for v2.0

- End-to-end encryption (AES-256)
- Built-in ngrok support
- Multi-user support
- Group chat functionality
- File transfers
- Persistent message history
- Username system
- Audio/video calls

### Long-term (v3.0+)

- GUI option
- Mobile applications
- Decentralized relay network
- Message delivery receipts
- Typing indicators
- Markdown support
- Screen sharing

## Security Roadmap

Critical improvements needed before production use:

- RSA + AES hybrid encryption
- Certificate pinning
- User authentication
- Automatic key rotation
- Perfect forward secrecy
- Key fingerprint verification

## Contributing

This is an educational project. Contributions welcome, particularly in:

- Encryption implementation
- Error handling
- Cross-platform testing
- Documentation
- Unit tests

## Technical Details

Built using Python standard library:

- `socket` for network communication
- `threading` for concurrent I/O
- `urllib` for IP detection

No external dependencies means easy deployment and portability.

## License

MIT License

## Disclaimer

This software is provided as-is without warranty. Authors are not responsible for:

- Data interception or breaches
- Software misuse
- Network security vulnerabilities
- Any damages from use

Users must understand and accept all risks before use.

## Educational Value

This project demonstrates:

- Socket programming fundamentals
- TCP/IP networking
- NAT traversal and port forwarding
- Client-server architecture
- Concurrent I/O with threading

Not intended for production without major security enhancements.

## Known Limitations

- Single connection per instance
- No encryption
- No message persistence
- Requires manual IP sharing
- Port forwarding complexity
- No offline messaging
- Limited error recovery

These limitations make it unsuitable for serious communication needs.

---

**Remember: Unencrypted communication. Never share sensitive information.**
