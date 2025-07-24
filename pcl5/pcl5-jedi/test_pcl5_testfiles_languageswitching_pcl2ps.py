import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pcl2ps.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:800
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pcl2ps.pcl=164480679b8c64beea00f365c205cee4a217a890421f06e810f034b903d6309c
    +test_classification:System
    +name: test_pcl5_testfiles_languageswitching_pcl2ps
    +test:
        +title: test_pcl5_testfiles_languageswitching_pcl2ps
        +guid:f6e101ec-3db0-47f6-a3cf-7bde42d1c975
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_languageswitching_pcl2ps(setup_teardown, printjob, outputsaver):
    printjob.print_verify('164480679b8c64beea00f365c205cee4a217a890421f06e810f034b903d6309c', timeout=600, expected_jobs=2)
    outputsaver.save_output()
