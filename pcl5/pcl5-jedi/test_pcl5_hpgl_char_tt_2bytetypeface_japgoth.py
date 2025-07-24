import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using japgoth.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:japgoth.obj=3c7a079523629524b84f21e5afe0754173aa5fe9072f7d275f2e8bff103ef7c1
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_japgoth
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_japgoth
        +guid:ed6ab7a8-61c6-4738-bd11-495ca35649eb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_japgoth(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3c7a079523629524b84f21e5afe0754173aa5fe9072f7d275f2e8bff103ef7c1', timeout=600)
    outputsaver.save_output()
