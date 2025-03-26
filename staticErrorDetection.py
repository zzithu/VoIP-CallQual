#You can call this in order to determine errors given static contexts
# all that means is we call this without using machine learning, just inferenced errors

#NOTE while this works on uncategorized packets, it performs better for already seperated packets

# Specifically, we analyze timestamps, if there is a long gap, we assume there is a conneciton error
def latencyError():
    return 0

# Inspects packets for standard sip errors
def sipErrors():
    return 0 

#Inspects for RTCP errors
def rtpErrors():
    #we can check for nacks and what not here
    return 0 

# If we are constantly resending packets, there can be an issue
def retryErrors():
    return 0

# This checks for all types of errors
def detectErrors():
    #in terms of architecture, I do not know exactly how to do this
    # what I mean is that every single error, do we want a connection associated to it?
    #or perhaps another consideration, is what sort of connection are we detecting? IE rtp vs webrtc
    return 0