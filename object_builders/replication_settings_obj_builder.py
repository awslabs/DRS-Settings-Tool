from classes.replication_settings import ReplicationSettings
from classes.replication_settings import PitPolicy
from utils.str2bool import str2bool
from utils.obj_to_dict import obj_to_dict
import ast

def replication_settings_obj_builder_for_csv(info):
    info.pop('ResponseMetadata')
    replication_settings_obj = ReplicationSettings(**info)
    return replication_settings_obj

def pit_policy_obj_builder_for_csv(info):
    for policy in info:
        if policy['units'] == 'DAY':
            pit_policy_obj = PitPolicy(**policy)
    return pit_policy_obj



def replication_settings_obj_builder(row):
    replication_settings_obj = ReplicationSettings()
    pit_settings_obj = PitPolicy(enabled=True, interval=1, ruleID=3, units='DAY')

    replication_settings_obj.associateDefaultSecurityGroup = str2bool(row[21])
    replication_settings_obj.autoReplicateNewDisks = None
    if row[19].upper != "":
        replication_settings_obj.autoReplicateNewDisks = str2bool(row[22])
    replication_settings_obj.bandwidthThrottling = ast.literal_eval(row[23])
    replication_settings_obj.createPublicIP = str2bool(row[24])
    replication_settings_obj.dataPlaneRouting = row[25].upper()
    replication_settings_obj.defaultLargeStagingDiskType = row[26].upper()
    pit_settings_obj.retentionDuration = ast.literal_eval(row[27])
    replication_settings_obj.pitPolicy = obj_to_dict(pit_settings_obj)
    replication_settings_obj.replicationServerInstanceType = row[28].lower()
    replication_settings_obj.replicatedDisks = ast.literal_eval(row[29])
    replication_settings_obj.ebsEncryption = row[30]
    replication_settings_obj.ebsEncryptionKeyArn = row[31]
    if row[32] != "":
        replication_settings_obj.replicationServersSecurityGroupsIDs = row[32].split(', ')
    replication_settings_obj.stagingAreaSubnetId = row[33]
    replication_settings_obj.useDedicatedReplicationServer = str2bool(row[34])
    replication_settings_obj.stagingAreaTags = ast.literal_eval(row[35])
    replication_settings_obj.sourceServerID = row[36]

    return replication_settings_obj
