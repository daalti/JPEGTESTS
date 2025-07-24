import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using fmt16sym.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:fmt16sym.obj=2481f591c935c470a4c45c9ca1f615a7e1de53d6c6cc134c37670bf478b1e5e8
    +test_classification:System
    +name: test_pcl5_pcl_symset_fmt16sym
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_symset_fmt16sym
        +guid:90f686f6-82cd-4cac-ad15-99525defc7f9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_symset_fmt16sym(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2481f591c935c470a4c45c9ca1f615a7e1de53d6c6cc134c37670bf478b1e5e8', timeout=600)
    outputsaver.save_output()
