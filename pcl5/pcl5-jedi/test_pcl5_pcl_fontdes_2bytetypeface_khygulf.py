import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulf.obj=baf0ae4241e11668cb96ee61773970b7d9147c17c1b67156e5a9457f58cd3dc9
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulf
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulf
        +guid:89f0f876-ac94-4fa5-b2a5-953901030600
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('baf0ae4241e11668cb96ee61773970b7d9147c17c1b67156e5a9457f58cd3dc9', timeout=600)
    outputsaver.save_output()
