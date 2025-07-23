import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600X8 color two page 4c from *letter-600x8-color-2p4c-sim.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-600x8-color-2p4c-sim.pwg=63ac052df55d1e361b86d1aa21a06d21300d0c7c60792ff9c62198ec876a14c2
    +name:test_pwg_letter_600X8_color_two_page_4c
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600X8_color_two_page_4c
        +guid:de2669dc-e131-4cab-91fa-8c4d802da42a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_letter_600X8_color_two_page_4c(setup_teardown, printjob, outputsaver):
    printjob.print_verify('63ac052df55d1e361b86d1aa21a06d21300d0c7c60792ff9c62198ec876a14c2')
    outputsaver.save_output()

    logging.info("PWG-letter 600X8 color two page 4ccompleted successfully")
