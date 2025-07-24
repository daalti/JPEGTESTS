import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 22Page_duplexm5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:22Page-duplexm5.obj=dcc18061f4bd0ff8377736a5c3afefc80a4eedf70515d8cc58052db62b2415dd
    +test_classification:System
    +name: test_pcl5_highvalue_22page_duplexm5
    +test:
        +title: test_pcl5_highvalue_22page_duplexm5
        +guid:0b8e322a-b4e0-49f5-bf45-8120e27d85e4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_22page_duplexm5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('dcc18061f4bd0ff8377736a5c3afefc80a4eedf70515d8cc58052db62b2415dd', timeout=600)
    outputsaver.save_output()
