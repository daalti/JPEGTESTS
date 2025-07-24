import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kittest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kittest.obj=bf2f0a6638cd17bb6fa9dc8328d96dac6832e52698d1c91005a606646f93771d
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_kittest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_kittest
        +guid:bdbab323-a6bc-4bff-bb15-7f2b265d684c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_kittest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bf2f0a6638cd17bb6fa9dc8328d96dac6832e52698d1c91005a606646f93771d', timeout=600)
    outputsaver.save_output()
