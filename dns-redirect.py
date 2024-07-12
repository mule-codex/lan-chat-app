import os
from pydivert import WinDivert
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE

FLASK_SERVER_ADDRESS = "127.0.0.1"
FLASK_SERVER_PORT = 5000

def main():
    # Open a WinDivert handle to capture outgoing UDP packets on port 53 (DNS)
    with WinDivert("outbound and udp.DstPort == 53") as w:
        print("WinDivert running...")
        
        for packet in w:
            try:
                dns = DNSRecord.parse(packet.payload)
                if dns.q.qtype == QTYPE.A:  # Query type A (IPv4 address)
                    qname = str(dns.q.qname)
                    if "localhost" in qname:  # Redirect DNS queries for 'localhost'
                        # Create DNS response to redirect to your Flask server
                        reply = DNSRecord(DNSHeader(id=dns.header.id, qr=1, aa=1, ra=1), q=dns.q)
                        reply.add_answer(RR(qname, QTYPE.A, ttl=10, rdata=A(FLASK_SERVER_ADDRESS)))
                        
                        # Send the modified packet back
                        packet.payload = reply.pack()
                        w.send(packet)
                        print(f"Redirected DNS query for {qname} to {FLASK_SERVER_ADDRESS}")
                    else:
                        w.send(packet)
            except Exception as e:
                print(f"Error handling packet: {e}")
                w.send(packet)

if __name__ == "__main__":
    main()
