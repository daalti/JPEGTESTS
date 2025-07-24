import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jtest.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:jtest.obj=9620522f111d932411b3c59ca722470c6f59f97c56ef275180a254e0a485db02
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_jtest
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_jtest
        +guid:befe0026-8766-4905-a89f-4fab1261d4ae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_jtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9620522f111d932411b3c59ca722470c6f59f97c56ef275180a254e0a485db02', timeout=600)
    outputsaver.save_output()
