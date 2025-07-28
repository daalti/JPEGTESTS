import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf iso sra4 225x320 from *iso_sra4_225x320.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:iso_sra4_225x320.urf=decebc46d96c90fdc2190bc5e39b6df2482a78f770fc30876d9d9319aa2f020c
    +name:test_urf_iso_sra4_225x320_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_iso_sra4_225x320_page
        +guid:e49586f2-f35e-4551-8418-3d7d5bf35e6d
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
def test_urf_iso_sra4_225x320_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
    media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]

    if tray.is_size_supported('iso_sra4_225x320mm', default):
        tray.configure_tray(default, 'iso_sra4_225x320mm', 'stationery')
    elif tray.is_size_supported('custom', default) and media_width_maximum >= 88567 and media_length_maximum >= 125984:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('decebc46d96c90fdc2190bc5e39b6df2482a78f770fc30876d9d9319aa2f020c')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF iso sra4 225x320 Page - Print job completed successfully")
