import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using sm.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:sm.obj=1889df4abb60269c1ade95730cd64a6cdc6c3f3814ddc1e0c5be0660aeddf128
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_sm
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_hpgl_lfatt_sm
        +guid:4863ad6e-cbfb-467e-bd51-a8afdb32667b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_sm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1889df4abb60269c1ade95730cd64a6cdc6c3f3814ddc1e0c5be0660aeddf128', timeout=600)
    outputsaver.save_output()
