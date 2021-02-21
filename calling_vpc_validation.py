from vpc_validation import *
import pathlib
import yaml

#Loading yaml file to extract data.
current_dir = pathlib.Path(__file__).parent
current_dir = str(current_dir)
variable = yaml.safe_load(open(current_dir + '/vpc_var.yaml','r'))

#extracting values from yaml file
url_cpy=(variable['url'])
url1_cpy=(variable['url1'])
username_cpy=(variable['username'])
password_cpy=(variable['password'])
myheaders_cpy=(variable['myheaders'])
nexus1 = (variable['nexus1'])
nexus2 = (variable['nexus2'])
url_list= [url_cpy, url1_cpy]
pk1_source= (variable['pk1_source'])
pk2_source= (variable['pk2_source'])
pk1_destination=(variable['pk1_destination'])
pk2_destination=(variable['pk2_destination'])


#input_var = sys.argv[1]e
class vpc_nexus_validation(vpc_validate):
        def __init__(self,*args):
                vpc_validate.__init__(self,*args)
        #def __init__(self,username_cpy,password_cpy,url_cpy,url1_cpy,myheaders_cpy):
                #super().__init__(username_cpy,password_cpy,url_cpy,url1_cpy,myheaders_cpy)

"""
Comparing the domain no ,peer link and peer keep alive link status.
"""
def compare_domain_peer_check(compare_list):

    try:
        logger.info("################## comparing the configuration of the two switches###################")
        
        if (compare_list[0][0]==compare_list[1][0]):
           logger.info("domain no is same for both the switch")
           logger.info(" RESULT : Domain comparison is fine ")
        else:
            logger.warning("domain no is not equal")
        if (compare_list[0][1]==compare_list[1][1]):
            logger.info("peer link configuration  is fine for both the switches ")
        else:
            logger.warning("peer link configuration has some issues")
            logger.info(" RESULT : PEER LINK COMPARISION IS FINE ")

        if (compare_list[0][2]==compare_list[1][2]):
            logger.info("peer keep alive link is up for both the switches ")
            logger.info(" RESULT : PEER-KEEP-LINK comparison is fine ")
        else:
            logger.warning("peer keep alive link has some reachability issue")
    except:
        logger.error("comparsion check for vpc domain and peer failed")

"""
compare function to check the global type 1 consistency check.
"""
def global_consistency_check(global_consistency_check_list):
    try:
        logger.info("################## comparing global consistency parameter for vpc ####################")
        if(global_consistency_check_list[0]==global_consistency_check_list[1]):
            logger.info("vpc global consistency parameter is ok and matching")
            logger.info(" RESULT: COMPARISION of global consistency parameter is ok ")
        else:
            logger.warning("consistency parameter is not fine between the switches")
    except Exception as error:
        logger.error("not able to find the parameters for global consistency")

"""
compare function to test the system mac of the two switches.
"""
def system_mac_checking(system_mac_list):
    try:
        logger.info("comparing system mac of both the switches") 
        if (system_mac_list[0]==system_mac_list[1]):
            logger.info("vpc system mac is same")
            logger.info(" RESULT: COMPARISION of system mac is ok ")
        else:
            logger.warning("vpc system mac is different which is not an ideal scenario")
    except Exception as error:
        logger.error("comparison for system mac failed")

"""
calling function to retrive the output to be compared.
"""

def vpc_check_feature(creating_object,compare_list,system_mac_list,global_consistency_check_list):
    i=0
    while i < len(url_list):
        compare_list.append(creating_object.vpc_feature_switch(url_list[i]))
        global_consistency_check_list.append(creating_object.consistency_check(url_list[i]))
        creating_object.running_config(url_list[i],pk1_source,pk1_destination,pk2_source,pk2_destination)
        creating_object.vpc_pk_link_check(url_list[i],url_cpy,url1_cpy,pk1_source,pk1_destination,pk2_source,pk2_destination)
        system_mac_list.append(creating_object.system_mac_check(url_list[i]))
        creating_object.vpc_peer_link(url_list[i])
        i=i+1

"""
Driver function
"""

def main():
    compare_list=[]
    system_mac_list=[]
    global_consistency_check_list=[]
    
    creating_object = vpc_nexus_validation(username_cpy,password_cpy,myheaders_cpy,nexus1,nexus2)
    vpc_check_feature(creating_object,compare_list,system_mac_list,global_consistency_check_list)
    compare_domain_peer_check(compare_list)
    system_mac_checking(system_mac_list)
    global_consistency_check(global_consistency_check_list)

if __name__ == '__main__':
        main()
