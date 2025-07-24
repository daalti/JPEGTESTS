import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 7Page_line68.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:7Page-line68.obj=5a3308014a443dd338e846104f11297b4cb5e409228d01995a2d6840b1abecf2
    +test_classification:System
    +name: test_pcl5_lowvaluenew_7page_line68
    +test:
        +title: test_pcl5_lowvaluenew_7page_line68
        +guid:84f59dbc-9c0d-45bf-bad8-0b7830cc7f8b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_7page_line68(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a3308014a443dd338e846104f11297b4cb5e409228d01995a2d6840b1abecf2', timeout=600)
    outputsaver.save_output()
