import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using deftext1.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:deftext1.obj=7ea6b2a15a079530859e519730186bd5018a4909b9717ccc0f7d1fea3b0caa1a
    +test_classification:System
    +name: test_pcl5_pcl_parsing_deftext1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_pcl_parsing_deftext1
        +guid:47a95983-737d-43be-aba1-041d47832b19
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_parsing_deftext1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7ea6b2a15a079530859e519730186bd5018a4909b9717ccc0f7d1fea3b0caa1a', timeout=600)
    outputsaver.save_output()
