# Streaming Platform using Sockets

## Introduction
This project, conducted for the "Redes de Computadoras" course, involves the development of a streaming platform between different hosts using socket programming. The primary goal was to explore the implementation of sockets at the code level and understand the intricacies of networked communication in a practical context.

## Project Overview
The streaming platform enables video streaming from a server to multiple client hosts. Key components include server-client architecture, TCP/UDP socket management, and integration with VLC for video handling.

## Server
Socket Management: Utilization of UDP sockets for video streaming and TCP sockets for command transmission.
Client Handling: A map structure for managing client connections with threading for synchronization.
Video Redirection: Integration with VLC for handling video data and redirecting it to clients.
## Client
TCP Socket: For sending control commands (connect, interrupt, continue, disconnect) to the server.
UDP Socket: To receive streaming data from the server.
VLC Redirection: Using a local VLC player to display the streamed video content.
Technical Challenges
TCP Connection Establishment: Overcoming firewall issues that were initially blocking TCP connections.
Streaming Efficiency: Handling high-resolution video streams efficiently.
Resource Optimization: Improving resource usage when no clients are connected or receiving data.
Future Work
Performance Enhancement: Improving the performance for higher resolution videos.
Resource Usage: Implement synchronization methods to optimize server resource consumption.
Datagram Handling: Improving the scalability of the solution by optimizing how datagrams are sent to clients.
# Experimentation
The development process included initial local testing with a single client, followed by scaling to multiple clients. Challenges such as firewall restrictions and video streaming efficiency were addressed through iterative testing and development.

## Conclusion
The project highlighted the complexities of network programming, especially in a real-world application scenario like video streaming. Future enhancements are aimed at addressing performance and scalability challenges.

