#!/usr/bin/env python3
PROFILES={
 'direct':{'min_panels':0,'min_appearances':0,'min_unique_roles':0,'min_peer_cycles':0},
 'low':{'min_panels':2,'min_appearances':10,'min_unique_roles':6,'min_peer_cycles':1},
 'medium':{'min_panels':4,'min_appearances':24,'min_unique_roles':12,'min_peer_cycles':2},
 'high':{'min_panels':6,'min_appearances':48,'min_unique_roles':20,'min_peer_cycles':3},
 'xhigh':{'min_panels':10,'min_appearances':80,'min_unique_roles':32,'min_peer_cycles':5},
 'max':{'min_panels':16,'min_appearances':128,'min_unique_roles':48,'min_peer_cycles':8},
 'ultra':{'min_panels':24,'min_appearances':200,'min_unique_roles':72,'min_peer_cycles':10},
}
