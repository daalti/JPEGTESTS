import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kvrtest.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:kvrtest.obj=7d55fe6e9a954470fb4a5a87c46d829c2990c0a121adcbfc57dd036de11e0392
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_kvrtest
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_kvrtest
        +guid:10d6756f-fa80-4d04-9a48-862c5919a569
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_kvrtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7d55fe6e9a954470fb4a5a87c46d829c2990c0a121adcbfc57dd036de11e0392', timeout=600)
    outputsaver.save_output()
