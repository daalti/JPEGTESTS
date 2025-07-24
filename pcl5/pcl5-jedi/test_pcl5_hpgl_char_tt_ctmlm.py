import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ctmlm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ctmlm.obj=fb376142e14b31c3384cd94fb53029ffe75042c60c94c70ed14428be74459cf6
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_ctmlm
    +test:
        +title: test_pcl5_hpgl_char_tt_ctmlm
        +guid:b7456fd0-32b6-4a31-aa05-b3c940d95471
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_ctmlm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fb376142e14b31c3384cd94fb53029ffe75042c60c94c70ed14428be74459cf6', timeout=600)
    outputsaver.save_output()
