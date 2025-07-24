import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using textbg.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:textbg.pcl=bc48c04f1388ea9d9c2f67839558533a9b40aacb09927baaa63fe222367c4754
    +test_classification:System
    +name: test_pcl5_testfiles_gl_text_bg
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_gl_text_bg
        +guid:852fc8ab-768b-460f-8d0b-61088f092e21
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_text_bg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('bc48c04f1388ea9d9c2f67839558533a9b40aacb09927baaa63fe222367c4754', timeout=600)
    outputsaver.save_output()
