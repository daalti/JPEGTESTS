import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf B5 Color from *B5_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5_Color.urf=42af2b01b81d1952e2153ac44556f687db1f43479e94587e85a6e3ec79a988c1
    +name:test_urf_b5_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b5_color_page
        +guid:d6707cc3-e182-4bde-b341-bb3183b877c7
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b5_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')

    printjob.print_verify('42af2b01b81d1952e2153ac44556f687db1f43479e94587e85a6e3ec79a988c1')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF B5 Color page - Print job completed successfully")
