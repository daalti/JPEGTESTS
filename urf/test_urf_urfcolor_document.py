import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of URF Color Document Page from *URFColorDocument.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:URFColorDocument.urf=80fa051b8acfe2091bcd1802714248045e5ecd85877445fa8baeacde2d8ac378
    +name:test_urf_color_document_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_color_document_page
        +guid:1c457710-266b-4fcb-b4f3-f8b14bdfd4d6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_color_document_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('80fa051b8acfe2091bcd1802714248045e5ecd85877445fa8baeacde2d8ac378')
    outputsaver.save_output()
