import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using wg.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:wg.obj=4a3c374acc522aaccf959c0a82b2ba5d6dd74e7ef4330b897059d4cceed64582
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_wg
    +test:
        +title: test_pcl5_hpgl_polygon_wg
        +guid:468aaba1-2e64-44ae-8a67-e484d27c098f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_wg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4a3c374acc522aaccf959c0a82b2ba5d6dd74e7ef4330b897059d4cceed64582', timeout=600)
    outputsaver.save_output()
