import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using lsg00121921.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:lsg00121921.pcl=99999247e9fc53507804459abb7a9490126b8f8836b12cc71724397f10a3a1fb
    +test_classification:System
    +name: test_pcl5_testfiles_color_lsg00121921
    +test:
        +title: test_pcl5_testfiles_color_lsg00121921
        +guid:76208799-9dce-4b24-a1fd-a440e3353d76
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_color_lsg00121921(setup_teardown, printjob, outputsaver):
    printjob.print_verify('99999247e9fc53507804459abb7a9490126b8f8836b12cc71724397f10a3a1fb', timeout=600)
    outputsaver.save_output()
