import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fontm5.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fontm5.obj=a449c07af1e79198ebb0b54a40de9977b956e0cc0a888d77c821f5f0c22e50b2
    +test_classification:System
    +name: test_pcl5_pcl_fontmgmt_fontm5
    +test:
        +title: test_pcl5_pcl_fontmgmt_fontm5
        +guid:e7603f76-2edf-46ed-87a5-6a95b693afee
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontmgmt_fontm5(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a449c07af1e79198ebb0b54a40de9977b956e0cc0a888d77c821f5f0c22e50b2', timeout=600)
    outputsaver.save_output()
