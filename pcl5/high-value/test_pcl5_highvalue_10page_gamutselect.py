import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 10Page_gamutselect.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:10Page-gamutselect.obj=d8d1db0b39826021425cb6586edb48a9dab00144148a47d4bdceb9c306d3a896
    +test_classification:System
    +name: test_pcl5_highvalue_10page_gamutselect
    +test:
        +title: test_pcl5_highvalue_10page_gamutselect
        +guid:82f9f47a-064f-41a0-b00c-a37f0173ae73
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_10page_gamutselect(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d8d1db0b39826021425cb6586edb48a9dab00144148a47d4bdceb9c306d3a896', timeout=300)
    outputsaver.save_output()
