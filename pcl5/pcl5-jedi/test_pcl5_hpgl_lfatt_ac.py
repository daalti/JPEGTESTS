import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ac.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:ac.obj=90891762429c5c35f0f31435ed150e56cb6c1b137e176ff2ca4a3bd9aae9ab41
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_ac
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_hpgl_lfatt_ac
        +guid:ca9c8604-19da-4092-9014-90911696a6bb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_ac(setup_teardown, printjob, outputsaver):
    printjob.print_verify('90891762429c5c35f0f31435ed150e56cb6c1b137e176ff2ca4a3bd9aae9ab41', timeout=600)
    outputsaver.save_output()
