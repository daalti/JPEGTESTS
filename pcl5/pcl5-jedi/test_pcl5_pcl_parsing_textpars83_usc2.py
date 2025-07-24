import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using textpars83_USC2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:textpars83_USC2.obj=b23dc5c3f63d4a64ac83ba2dd8ab64bf33820961be50cfca2ca68470c4955641
    +test_classification:System
    +name: test_pcl5_pcl_parsing_textpars83_usc2
    +test:
        +title: test_pcl5_pcl_parsing_textpars83_usc2
        +guid:30417aad-96e9-4f91-b819-b1277d868f2c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$ 
"""

def test_pcl5_pcl_parsing_textpars83_usc2(udw, setup_teardown, printjob, outputsaver):
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify('b23dc5c3f63d4a64ac83ba2dd8ab64bf33820961be50cfca2ca68470c4955641', timeout=600,expected_jobs=5)
    else:
        printjob.print_verify('b23dc5c3f63d4a64ac83ba2dd8ab64bf33820961be50cfca2ca68470c4955641', timeout=600,expected_jobs=2)
    outputsaver.save_output()
