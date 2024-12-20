from classes.source_server_info import SourceServer
import ast

def source_server_info_obj_builder_for_csv(server):
    source_server_info_obj = SourceServer(**server)
    return source_server_info_obj

def source_server_info_obj_builder(row):
    source_server_info_obj = SourceServer()
    source_server_info_obj.sourceServerID = row[1]
    source_server_info_obj.stagingArea = ast.literal_eval(row[3])
    source_server_info_obj.stagingSourceServerID = row[36]
    # when building the CSV, we take the account number from the source server ARN to figure out the Target Account ID which is why this is named arn. 
    # When building the source server obj from the CSV to use in future API calls, taking the Target Account ID field from the CSV and setting to source_server_info_obj.arn.
    source_server_info_obj.arn = ast.literal_eval(row[4])
    return source_server_info_obj
    
