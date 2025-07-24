import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using lm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lm.obj=7ecc33a4122dcff25b9d0580ab2c2a5beefe89c4a80f279f95c4ac760508cb0f
    +test_classification:System
    +name: test_pcl5_hpgl_char_lm
    +test:
        +title: test_pcl5_hpgl_char_lm
        +guid:b9bd798f-5efd-4039-a511-13102ed94bd6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_lm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7ecc33a4122dcff25b9d0580ab2c2a5beefe89c4a80f279f95c4ac760508cb0f', timeout=600)
    outputsaver.save_output()
