import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 7Page_ftbyt0.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:7Page-ftbyt0.obj=c8e31d1f22063f73424f584fe89da3bfa771b65ce674e4109fcaf4bad2c1a730
    +test_classification:System
    +name: test_pcl5_highvalue_7page_ftbyt0
    +test:
        +title: test_pcl5_highvalue_7page_ftbyt0
        +guid:0ab7301b-afb1-4caa-a5d5-67ba969c4838
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_7page_ftbyt0(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c8e31d1f22063f73424f584fe89da3bfa771b65ce674e4109fcaf4bad2c1a730')
    outputsaver.save_output()
