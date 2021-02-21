"""
This test case is written to validate the configuration of cisco virtual port-channel.  
"""
import regex as re
import requests
import logging
import json
import logging 
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
class vpc_validate():

  def __init__(self,username_cpy,password_cpy,myheaders_cpy,nexus1,nexus2):

    self.username=username_cpy
    self.password=password_cpy
    self.myheaders=myheaders_cpy
    self.nexus1=nexus1
    self.nexus2=nexus2


  def vpc_feature_switch(self,url):
    """
    this function is testing the domain no ,peer link and peer-keepalive link status.
    The domain number should be same for both the switch . A peer keep alive link (L3) link should be up 
    and rechable . The peer link should be up and reachable as well as this link is used to sync all the 
    control plane information
    """
    logger.info("################################ Starting vpc validation check ##################################")
    logger.info("############################ Command used: show vpc brief #######################################")
    feature_check="show vpc brief"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": feature_check,
    "output_format": "json"}
    }

    vpc_feature=[]
    response_feature_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    dumping = json.dumps(response_feature_config,sort_keys=True,indent=4)
    loading_json_output = json.loads(dumping)
    parsing_json = (loading_json_output['ins_api']['outputs']['output']['body'].split('\n'))
    #print(parsing_json)
    list_variable=parsing_json[3].split(":")
    
    #print(type(a[0]))
    #print(a[0].strip())
    if list_variable[1].strip() == '10':
      #print("vpc domain no for switch {} is:".format(url.split("/")[2]),list_variable[1].strip())
      #return("vpc domain no for switch 1 is ",list_variable[1])
      #print("vpc domain id",a[1])
      logger.info("######################## EXtracting vpc domain #######################")
      vpc_feature.append(list_variable[1].strip())
      logger.info("vpc domain for switch {} is :{}".format(url.split("/")[2],list_variable[1]))
    else:
      logger.warning("domain no is not found for switch {}".format(url.split("/")[2]))

    logger.info("########################### checking the peer link status #############################")
    Peer_link_Check=parsing_json[4].split(":")
    #print(Peer_link_Check)
    if Peer_link_Check[1].strip()=="peer adjacency formed ok":
      #print("peer link is fine for switch {}:".format(url.split("/")[2]),Peer_link_Check[1].strip())
      vpc_feature.append(Peer_link_Check[1].strip())
      logger.info("vpc peer link is fine for switch {} with status :{}".format(url.split("/")[2],Peer_link_Check[1].strip()))
    else:
      logger.warning("peer link has some issue on the switch {}".format(url.split("/")[2]))
    #print(len(a))
    
    logger.info("######################### checking the peer keep alive link status #####################")
    Peer_keep_alive_link_check=parsing_json[5].split(":")
    if Peer_keep_alive_link_check[1].strip()=="peer is alive":
      #print("peer keep alive link is working fine for switch {}:".format(url.split("/")[2]),Peer_keep_alive_link_check[1].strip())
      logger.info("peer keep alive link is working fine for switch {} with status:{}".format(url.split("/")[2],Peer_keep_alive_link_check[1].strip()))
      vpc_feature.append(Peer_keep_alive_link_check[1].strip())
    else:
      logger.warning("peer keep alive link is broken for switch {}".format(url.split("/")[2]))
    #print(vpc_feature)
    return vpc_feature
  
  def consistency_check(self,url):
    """
    Checking the Consistency parameter . there are two consistency parameter . We are checking the type1 global 
    parameter. 
    """
    logger.info("################################ checking the global consistency status ####################")
    logger.info("################################ Command used : show vpc brief ###############################")
    vpc_consistency="show vpc brief"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_consistency,
    "output_format": "json"}
    }
    consistency_check_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    dumping_consistency_check = json.dumps(consistency_check_config,sort_keys=True,indent=4)
    loading_consistency_output = json.loads(dumping_consistency_check)
    parsing_consistency_json = (loading_consistency_output['ins_api']['outputs']['output']['body'].split('\n'))
    try:
      logger.info("checking global consistency for switch {} ".format(url.split("/")[2]))
      global_consistency_check=[]
      filtering_global_consistency=re.compile(".*Configuration consistency status")
      newlist4=list(filter(filtering_global_consistency.match,parsing_consistency_json))
      consistency_check_listing=newlist4[0].split(":",1)[1].strip()
      global_consistency_check.append(consistency_check_listing)
      return global_consistency_check
    except Exception as e:
      print(e)
  
  #logger.info("########################################################################################")

  def running_config(self,url,pk1_source,pk1_destination,pk2_source,pk2_destination):
    logger.info("############# checking the peer keep alive config ####################")
    logger.info("############# Command used: show run vpc #############################")
    """
    checking the peer keepalive config.
    """
    vpc_running_config="show run vpc"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_running_config,
    "output_format": "json"}
    }

    response_running_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    config_dump = json.dumps(response_running_config,sort_keys=True,indent=4)
    loading_config_json = json.loads(config_dump)
    parsing_json = (loading_config_json['ins_api']['outputs']['output']['body'].split('\n'))
    filtering=re.compile(".*peer-keepalive")
    newlist=list(filter(filtering.match,parsing_json))
    splitting_newlist=newlist[0].split()
    nexus_device=[self.nexus1,self.nexus2]

    try:
        if ((pk1_destination==splitting_newlist[2] and pk1_source==splitting_newlist[4]) or (pk2_destination==splitting_newlist[2] and pk2_source==splitting_newlist[4])):
            #print("keep alive configuration for switch {} is correct".format(url.split("/")[2]))
            logger.info("keep alive configuration for switch {} is correct".format(url.split("/")[2]))
            logger.info("RESULT: peer keep alive config is fine")
        else:
            logger.warning("keep alive configuration is not correct")
    except Exception as error:
        print(error)

  #logger.info("########################################################################################")
  def vpc_pk_link_check(self,url,url_cpy,url1_cpy,pk1_source,pk1_destination,pk2_source,pk2_destination):
    logger.info("############################### checking the reachability of peer keep alive link##############")
    logger.info("######################### Command used : show vpc peer-keepalive ##############################")
    """
    Finding the vrf used for peer-keepalive link . A seperate vrf is recommended or we can use the managment 
    vrf for the pk link.
    """
    vpc_pk_config="show vpc peer-keepalive"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_pk_config,
    "output_format": "json"}
    }

    pk_link_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    pk_dump = json.dumps(pk_link_config,sort_keys=True,indent=4)
    loading_json_pk_config=json.loads(pk_dump)
    parsing_pk_config=(loading_json_pk_config['ins_api']['outputs']['output']['body'].split('\n'))
    #print(parsing_pk_config)
    matching_string=re.compile(".*--Keepalive vrf")
    newlist=list(filter(matching_string.match,parsing_pk_config))
    newlist[0].split(":")
    newlist[0].replace(" ","")
    vrf_name=newlist[0].split(":",1)[1].strip()
    #print(vrf_name)
   # logger.info("#################### pinging destination PK link  using source PK link #################")
    
    if url==url_cpy:
      checking_pk_rechability="ping {} source {} vrf {} ".format(pk1_destination,pk1_source,vrf_name)
    else:
      checking_pk_rechability="ping {} source {} vrf {} ".format(pk2_destination,pk2_source,vrf_name)   
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": checking_pk_rechability,
    "output_format": "json"}
    }
    """
    Checking the reachability of the peer keep alive using the vrf we have found from the above
    """
    pk_link_reachability=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    pk_link_dump = json.dumps(pk_link_reachability,sort_keys=True,indent=4)
    loading_pk_link=json.loads(pk_link_dump)
    Parsing_reachability=loading_pk_link['ins_api']['outputs']['output']['body'].split('\n')
    #print(Parsing_reachability)
    finding_reachbility_percentage=re.compile(".*packets transmitted")
    newlist1 = list(filter(finding_reachbility_percentage.match,Parsing_reachability))
    reachibility_status=newlist1[0].split(",",2)[2].strip() 
    #print(Parsing_reachability)

    #logger.info("############## checking if the packet loss is null while reaching the destination #################")
    
    if url==url_cpy:
      if reachibility_status=="0.00% packet loss":
        logger.info("keep alive reachibility is fine for switch {}".format(url.split("/")[2]))
        logger.info("RESULT: peer keep alive link is reachable from switch 1 ")
      else:
        logger.warning("keep alive reachibility is having issue for switch {} ".format(url.split("/")[2]))
    else:
      if reachibility_status=="0.00% packet loss":
        logger.info("keep alive reachibility is fine for switch {}".format(url.split("/")[2]))
        logger.info("RESULT: peer keep alive link is reachable from switch 2 ")
      else:
        logger.warning("keep alive reachibility is having issue for switch {} ".format(url.split("/")[2]))
  #logger.info("######################################################################################")   
    
  def system_mac_check(self,url):

    logger.info("################# checking the vpc system mac which is derived from domain no #######")
    logger.info("########################## command used: show vpc role ##############################")
    """
    We are finding the system mac from both the switch .System mac is same for both the switches to give an illusion to downstream
    device that it is connected to a single device
    """
    vpc_system_mac_config="show vpc role"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_system_mac_config,
    "output_format": "json"}
    }
    try:
      finding_system_mac=[]
      system_mac_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
      system_mac_dump = json.dumps(system_mac_config,sort_keys=True,indent=4)
      loading_system_mac=json.loads(system_mac_dump)
      Parsing_system_mac=loading_system_mac['ins_api']['outputs']['output']['body'].split('\n')
      #print(Parsing_system_mac)
      finding_system_mac_value=re.compile(".*vPC system-mac")
      newlist2 = list(filter(finding_system_mac_value.match,Parsing_system_mac))
      newlist2[0].replace(" ","")
      system_mac_status=newlist2[0].split(":",1)[1].strip()
      finding_system_mac.append(system_mac_status)  
      logger.info("vpc system mac for switch {}:{}".format(url.split("/")[2],system_mac_status))
      return finding_system_mac
    except Exception as error:
      print(error)
  #logger.info("#####################################################################################")

  def vpc_peer_link(self,url):
    """
    We are finding the port-channel no used for peer link so that we can check the status of the port in the 
    port-channel.
    """
    vpc_peer_link_check="show run vpc"
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_peer_link_check,
    "output_format": "json"}
    }
    peer_link_config=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    peer_link_dumping = json.dumps(peer_link_config,sort_keys=True,indent=4)
    loading_peer_link=json.loads(peer_link_dumping)
    Parsing_peer_link=loading_peer_link['ins_api']['outputs']['output']['body'].split('\n')
    #print(Parsing_peer_link)
    Parsing_peer_link=list(dict.fromkeys(Parsing_peer_link))
    newlist3 = Parsing_peer_link[-2].split(" ",1)[1].strip()
    #print(newlist3)
    
    logger.info("########################checking port channel summary for peer link ############################")
    logger.info("################## command used : show port-channel summary interface port-channel-no ##########")
    vpc_peer_link_check="show port-channel summary interface {} ".format(newlist3)
    payload={
    "ins_api": {
    "version": "1.0",
    "type": "cli_conf",
    "chunk": "0",
    "sid": "1",
    "input": vpc_peer_link_check,
    "output_format": "json"}
    }
    peer_link_summary=requests.post(url,data=json.dumps(payload),headers=self.myheaders,auth=(self.username,self.password)).json()
    peer_link_summary_dumping = json.dumps(peer_link_summary,sort_keys=True,indent=4)
    loading_peer_link_summary=json.loads(peer_link_summary_dumping)
    Parsing_port_channel_summary=loading_peer_link_summary['ins_api']['outputs']['output']['body'].split('\n')
    #print(Parsing_port_channel_summary)
    port_channel_reg=re.compile(".*LACP")
    newlist4=list(filter(port_channel_reg.match,Parsing_port_channel_summary))
    final_intreface_list=newlist4[1].split("LACP",1)[1].strip()
    no_of_interface_in_peer_link=final_intreface_list.count("Eth")
    no_of_interface_up_in_peer_link=final_intreface_list.count("(P)")
    if no_of_interface_in_peer_link==no_of_interface_in_peer_link:
      logger.info("all the links are up in peer link port-channel for switch {}".format(url.split("/")[2]))
      logger.info("RESULT: All the ports are up in the peer link ")
    else:
      logger.info("there is some issue with the interface in peer link for switch {}".format(url.split("/")[2]))
      
    
