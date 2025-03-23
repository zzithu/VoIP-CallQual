#We use this class in order to get the packet information

#Either we keep this simple, or we consider seperating important information here for further analysis

#Keep pull information / Store the packets somewhere in the case they need to be revisited.


import pyshark
import pandas as pd

class PacketGatherer:
    def __init__(self, source='ExampleCapture/aaa.pcap'): #default packet to open
        self.source = source  
        self.packets = []  
        self.df = pd.DataFrame()  # DataFrame for the processed data

    def gather_packets(self):
        """Gather packets from the source (PCAP or live interface)."""
        
        #This is live gatherign
        # cap = pyshark.LiveCapture(interface='eth0')

        #if you want to get a capture from a predetermined file
        cap = pyshark.FileCapture(self.source)

        # Process the packets
        for packet in cap:
            packet_info = self.process_packet(packet)
            self.packets.append(packet_info)

        # Convert to DataFrame
        self.df = pd.DataFrame(self.packets)

    #rather than directly managing the frame, we can more easily call this for any machine training.
    def process_packet(self, packet):
        """Process each packet and extract relevant data."""
        packet_info = {
            'timestamp': packet.sniff_time,  # Packet timestamp
            'source_ip': packet.ip.src if 'IP' in packet else None,  # Source IP
            'destination_ip': packet.ip.dst if 'IP' in packet else None,  # Destination IP
            'protocol': packet.highest_layer,  # Protocol (e.g., TCP, UDP, SIP, etc.)
            'packet_length': len(packet),  # Length of the packet
            'port': packet[packet.transport_layer].dstport if 'TCP' in packet or 'UDP' in packet else None,  # Destination port (for transport layer)
        }
        return packet_info

    def get_dataframe(self):
        """Return the DataFrame containing packet data."""
        return self.df

    def update_dataframe(self, packet_info):
        """Update the DataFrame with new packet info."""
        self.df = self.df.append(packet_info, ignore_index=True)

# This is how to use it
if __name__ == "__main__":
    packet_gatherer = PacketGatherer("ExampleCapture/aaa.pcap")
    
    #for live data, loop these
    packet_gatherer.gather_packets()

    df = packet_gatherer.get_dataframe()
  
    print(df.head())  
