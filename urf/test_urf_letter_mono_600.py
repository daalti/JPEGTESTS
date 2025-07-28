import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:URF test using **Letter_Mono_600.urf
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Mono_600.urf=ad52981b4cb632be4ab779e4a38616c8c90c58e62127dbd10823b44cdda57676
    +name:test_urf_letter_mono_600
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_letter_mono_600
        +guid:b90b4c0b-4fb5-44c7-b902-248eb3b06238
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_letter_mono_600(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ad52981b4cb632be4ab779e4a38616c8c90c58e62127dbd10823b44cdda57676')
    outputsaver.save_output()
