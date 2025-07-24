import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 22Page_colorpat.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:22Page-colorpat.obj=8ca078d16b633b8d6ede3c7cba745fde4cc43ae58df41030a26ef6f29fa68b89
    +test_classification:System
    +name: test_pcl5_highvalue_22page_colorpat
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_22page_colorpat
        +guid:75c56922-5994-4175-8fce-f634696d7e46
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_22page_colorpat(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8ca078d16b633b8d6ede3c7cba745fde4cc43ae58df41030a26ef6f29fa68b89', timeout=600)
    outputsaver.save_output()
