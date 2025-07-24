import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using wu.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:wu.obj=87c0f050c4d7d1c3543a023341a7d5feac3817ac72bb094f58f600f964616afc
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_wu
    +test:
        +title: test_pcl5_hpgl_lfatt_wu
        +guid:d66e9131-a24a-4c88-8303-c589cda6b23a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_wu(setup_teardown, printjob, outputsaver):
    printjob.print_verify('87c0f050c4d7d1c3543a023341a7d5feac3817ac72bb094f58f600f964616afc', timeout=600)
    outputsaver.save_output()
