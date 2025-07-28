import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf B5 from *B5.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:B5.urf=205a5282c389f85e494cf9390b549af77be7ead207937cb3713ed766c2a8780c
    +name:test_urf_b5_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_b5_page
        +guid:03b2199b-5f92-44a9-b581-dae59f3d0b83
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=iso_b5_176x250mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_b5_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_b5_176x250mm', default):
        tray.configure_tray(default, 'iso_b5_176x250mm', 'stationery')

    printjob.print_verify('205a5282c389f85e494cf9390b549af77be7ead207937cb3713ed766c2a8780c')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF B5 Page - Print job completed successfully")
