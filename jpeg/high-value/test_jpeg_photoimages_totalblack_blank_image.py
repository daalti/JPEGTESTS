import pytest
import logging

from dunetuf.print.print_common_types import MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of photoimages_totalblack_blank_image
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_TotalBlack_Blank_image.JPG=3de1610f16b15c0e583399fed0580633c25758ab0ce4f8ebecda9836f21f6fc2
    +test_classification:System
    +name:test_jpeg_photoimages_totalblack_blank_image
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_totalblack_blank_image
        +guid:a73e507d-d995-45f1-a372-d58546ef3cee
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
def test_jpeg_photoimages_totalblack_blank_image(setup_teardown, printjob, outputsaver, print_emulation, tray):
    if print_emulation.print_engine_platform == 'emulator':
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None

        for tray_id in installed_trays:
            system_tray_id = tray_id.lower().replace('tray', 'tray-')
            if tray.is_size_supported('anycustom', system_tray_id):
                selected_tray = tray_id
                break

        if selected_tray is None:
            raise ValueError("No tray found supporting anycustom in enterprise emulator")

        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Custom.name, MediaType.Plain.name)
        print_emulation.tray.close(selected_tray)

    printjob.print_verify('3de1610f16b15c0e583399fed0580633c25758ab0ce4f8ebecda9836f21f6fc2')
    outputsaver.save_output()

    logging.info("Jpeg photoimages_TotalBlack_Blank_image file")
