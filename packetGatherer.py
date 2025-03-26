#We use this class in order to get the packet information

#Either we keep this simple, or we consider seperating important information here for further analysis

#Keep pull information / Store the packets somewhere in the case they need to be revisited.


import pyshark
import pandas as pd

class PacketGatherer:
    def __init__(self, source='ExampleCapture/aaa.pcap'): #default packet to open
        self.source = source  
        self.packets = []
        self.classified = {}
        self.df = pd.DataFrame()  # DataFrame for the processed data

    def gather_packets(self):
        
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
        packet_info = {
            'timestamp': packet.sniff_time,  # Packet timestamp
            'source_ip': packet.ip.src if 'IP' in packet else None,  # Source IP
            'destination_ip': packet.ip.dst if 'IP' in packet else None,  # Destination IP
            'protocol': packet.highest_layer,  # Protocol (TCP, UDP, SIP, etc.)
            'packet_length': len(packet),  # Length of the packet
            'port': packet[packet.transport_layer].dstport if 'TCP' in packet or 'UDP' in packet else None,  # Destination port (for transport layer)
        }
        return packet_info


    #These will help for live updates
    def get_dataframe(self):
        return self.df

    def update_dataframe(self, packet_info):
        self.df = self.df.append(packet_info, ignore_index=True)

#In order to best categorize information, we can seperate into packet errors, and we can also seperate
#based on the connection identity. Think databases.

    #this is responsible for seperating into the types of packets, we also get a nice little array to reference them
    def classify_by_ip(self):
        self.classified = {}


        for pkt in self.packets:
            src_ip = pkt['source_ip']

            # Initialize source IP if not seen before
            if src_ip not in self.classified:
                self.classified[src_ip] = {}

            # Create connection ID (destination + port)
            conn_id = (pkt['destination_ip'], pkt['port'])

            # Initialize connection under this IP
            if conn_id not in self.classified[src_ip]:
                self.classified[src_ip][conn_id] = {
                    'sip_packets': [],
                    'rtp_packets': [],
                    'rtcp_packets': [],
                    'other_packets': []
                }

            # Classify the packet by protocol
            if pkt['protocol'] == 'SIP':
                self.classified[src_ip][conn_id]['sip_packets'].append(pkt)
            elif pkt['protocol'] == 'RTP':
                self.classified[src_ip][conn_id]['rtp_packets'].append(pkt)
            elif pkt['protocol'] == 'RTCP':
                self.classified[src_ip][conn_id]['rtcp_packets'].append(pkt)
            else:
                self.classified[src_ip][conn_id]['other_packets'].append(pkt) #essentially, undefinied at least at the moment

# This is how to use it
if __name__ == "__main__":
    packet_gatherer = PacketGatherer("ExampleCapture/aaa.pcap")
    
    #for live data, loop these
    packet_gatherer.gather_packets()

    df = packet_gatherer.get_dataframe()
  
    print(df.head())  
