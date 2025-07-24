import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_lsg48174.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:1Page-lsg48174.obj=955cffba4e840f89223bc4dd09653208fc2eda2863be720684c34f2efccb22d3
    +test_classification:System
    +name: test_pcl5_highvalue_1page_lsg48174
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_1page_lsg48174
        +guid:bbc61e3e-9f98-4a29-b15f-02cf2bc2aec8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_1page_lsg48174(setup_teardown, printjob, outputsaver):
    printjob.print_verify('955cffba4e840f89223bc4dd09653208fc2eda2863be720684c34f2efccb22d3', timeout=600)
    outputsaver.save_output()
