import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **ptchgmt.cht
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:ptchgmt.cht=61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48
    +name:test_pcl5_conf_hv_ptchgmt
    +test:
        +title:test_pcl5_conf_hv_ptchgmt
        +guid:632112ab-c9ed-4604-9b3c-90e2d715200d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_ptchgmt(udw, setup_teardown, printjob, outputsaver):
    # printjob.print_verify('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48',expected_jobs=3)
    # outputverifier.save_and_parse_output()
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48', timeout=600,expected_jobs=5)
    else:
        printjob.print_verify('61229fda64e53a2de3d5a8034db5e0917464e4f0d5d163e35f55e602532d1a48', timeout=600, expected_jobs=2)
    outputsaver.save_output()
