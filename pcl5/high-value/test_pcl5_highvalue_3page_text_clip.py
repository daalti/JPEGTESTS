import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 3Page_text_clip.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:120
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:3Page-text_clip.obj=7799be63cc9a4744418112a1f5ad4837424926f846ff1b461354106d7799dd1e
    +test_classification:System
    +name: test_pcl5_highvalue_3page_text_clip
    +test:
        +title: test_pcl5_highvalue_3page_text_clip
        +guid:2f3f42ad-704f-4e0b-8e1c-d94c12337d6f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_3page_text_clip(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7799be63cc9a4744418112a1f5ad4837424926f846ff1b461354106d7799dd1e')
    outputsaver.save_output()
