import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using cpDown.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cpDown.pcl=33facdac66ba7f80018ecdcff857d94d108ca1b09955322698510a8847e0a5b9
    +test_classification:System
    +name: test_pcl5_testfiles_gl_cpdown
    +test:
        +title: test_pcl5_testfiles_gl_cpdown
        +guid:91c6aefa-dfe3-45fc-8629-295193445252
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_cpdown(setup_teardown, printjob, outputsaver):
    printjob.print_verify('33facdac66ba7f80018ecdcff857d94d108ca1b09955322698510a8847e0a5b9', timeout=600)
    outputsaver.save_output()
