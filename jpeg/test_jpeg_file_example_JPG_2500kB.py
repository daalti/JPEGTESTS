import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg file of 2500kB from *file_example_JPG_2500kB.jpg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-17136
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:file_example_JPG_2500kB.jpg=b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb
    +name:test_jpeg_file_example_JPG_2500kB
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_file_example_JPG_2500kB
        +guid:83e8883b-9ab7-4d07-99a8-f719d50587c4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_file_example_JPG_2500kB(setup_teardown, printjob, outputsaver, udw, tray, media):
    outputsaver.validate_crc_tiff(udw)

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    # Not using print_verify for a reason
    # We want to handle media mismatch alert on roll products before job completion
    jobid = printjob.start_print('b6630f7d0ff76f53f21b472f0d383b41a0b8a730a29282f12db435dc390dfdeb')

    # This jpeg job has large dimensions
    # On non-roll products, it will print on Letter
    if 'main-roll' in tray.trays:
        # On Beam, it will print on main-roll after out of range media check clipping target size leading to a prompt
        media.wait_for_alerts('mediaMismatchUnsupportedSize', 100)
        # Handle the prompt displayed to user to continue printing
        media.alert_action('mediaMismatchUnsupportedSize', 'continue')
    elif 'roll-1' in tray.trays:
        # Apply same workaround for multi-roll products, alert is mediaMismatchSizeFlow
        media.wait_for_alerts('mediaMismatchSizeFlow', 100)
        media.alert_action("mediaMismatchSizeFlow", "continue")


    jobstate = printjob.wait_verify_job_completion(jobid, timeout=600)

    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("Jpeg file example JPG 2500kB Page - Print job completed successfully")
