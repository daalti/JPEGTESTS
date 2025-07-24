import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using downloadFont.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:downloadFont.pcl=d5eaca2b0ffa619b015e2a70ccfa1324ab933a3d835bbb9f78cf3fc94d93df6e
    +test_classification:System
    +name: test_pcl5_testfiles_text_downloadfont
    +test:
        +title: test_pcl5_testfiles_text_downloadfont
        +guid:a3b3e79c-8c26-4468-a39a-5e2f1ff66b39
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_downloadfont(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d5eaca2b0ffa619b015e2a70ccfa1324ab933a3d835bbb9f78cf3fc94d93df6e', timeout=600)
    outputsaver.save_output()
