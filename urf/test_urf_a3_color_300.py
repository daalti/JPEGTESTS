import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf A3 Color 300 from *A3_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A3_Color_300.urf=a9df31fe77f816529f0be95b0ccc27e9bebe9367fbb12659a1a0cecba3e92094
    +name:test_urf_a3_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a3_color_300_page
        +guid:79f74376-707f-494f-87a8-bba777dc8d74
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
def test_urf_a3_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a3_297x420mm', default):
        tray.configure_tray(default, 'iso_a3_297x420mm', 'stationery')

    printjob.print_verify('a9df31fe77f816529f0be95b0ccc27e9bebe9367fbb12659a1a0cecba3e92094')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF A3 Color 300 page - Print job completed successfully")
