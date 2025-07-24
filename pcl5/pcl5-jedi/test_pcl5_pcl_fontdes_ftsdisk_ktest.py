import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ktest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:700
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ktest.obj=f0b9c8aa4b6b679435cd25551f3c8ad8e2f02b2c1ed1a050ca522da771359ea8
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_ktest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_ktest
        +guid:acfd48e8-81c7-4659-ba2b-97bd36e7eb2e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_ktest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f0b9c8aa4b6b679435cd25551f3c8ad8e2f02b2c1ed1a050ca522da771359ea8', timeout=700)
    outputsaver.save_output()
