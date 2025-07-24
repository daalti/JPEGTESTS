import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tvrtest.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:tvrtest.obj=7983db96afc4a3f2c87be3a09bd26c2a2a819d7fc74748302fed6fc64b3079a8
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_tvrtest
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_tvrtest
        +guid:6db152ff-0d6c-4f1b-a6c9-8fadadce4e4c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_tvrtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7983db96afc4a3f2c87be3a09bd26c2a2a819d7fc74748302fed6fc64b3079a8', timeout=600)
    outputsaver.save_output()
