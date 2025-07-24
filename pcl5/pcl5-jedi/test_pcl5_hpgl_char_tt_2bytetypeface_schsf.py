import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using schsf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:schsf.obj=ffead46d2cac62b40d7b3d729b19b76e6749f78eb6924b24667c972ea2cd841e
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_schsf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_schsf
        +guid:97b4f323-2bab-4e5a-a79a-dc8aa79f8926
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_schsf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ffead46d2cac62b40d7b3d729b19b76e6749f78eb6924b24667c972ea2cd841e', timeout=600)
    outputsaver.save_output()
