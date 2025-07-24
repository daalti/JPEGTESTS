import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL6 high value test using **81037-50pgs_a4_Plain_dpxLE.prn
    +test_tier: 3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:81037-50pgs_a4_Plain_dpxLE.prn=dc0a76792ab227d968d88502f8c0d5b74619ed7b2e14abc1bb20cc92b4f0bee1
    +name:test_pcl5_conf_hv_81037_50pgs_a4_plain_dpxle
    +test:
        +title:test_pcl5_conf_hv_81037_50pgs_a4_plain_dpxle
        +guid:26d18baf-d5dd-41ab-aba2-6c516323fc4b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_81037_50pgs_a4_plain_dpxle(setup_teardown, printjob, outputverifier):
    printjob.print_verify('dc0a76792ab227d968d88502f8c0d5b74619ed7b2e14abc1bb20cc92b4f0bee1', timeout=300)
    outputverifier.save_and_parse_output()
