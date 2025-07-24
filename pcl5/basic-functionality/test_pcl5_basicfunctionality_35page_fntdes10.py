import pytest
import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 35Page_fntdes10.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:35Page-fntdes10.obj=016c79d495c86c70478e01c1fdc50fabb82fa10f9e641d7ed349e9c5d22381e6
    +test_classification:System
    +name: test_pcl5_basicfunctionality_35page_fntdes10
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_35page_fntdes10
        +guid:0caacf1a-5852-4a0f-ba97-728ed622b4a6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:800
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_basicfunctionality_35page_fntdes10(setup_teardown, printjob, outputsaver,print_emulation, configuration):
    if print_emulation.print_engine_platform == 'emulator' and configuration.familyname == 'enterprise':
        # Get list of installed trays
        installed_trays = print_emulation.tray.get_installed_trays()
        selected_tray = None

        # Check each tray for Letter/Plain support
        for tray_id in installed_trays:
            supported_sizes = print_emulation.tray.get_supported_media_sizes(tray_id, edge='short')
            supported_types = print_emulation.tray.get_supported_media_types(tray_id)

            # Check if this tray supports Letter and Plain
            if MediaSize.Letter.name in supported_sizes and MediaType.Plain.name in supported_types:
                selected_tray = tray_id
                break

        if selected_tray is None:
            raise ValueError("No tray found supporting Letter size and Plain type paper")

        # Open and load the selected tray
        print_emulation.tray.open(selected_tray)
        print_emulation.tray.load(selected_tray, MediaSize.Letter.name, MediaType.Plain.name,
                                  media_orientation=MediaOrientation.Portrait.name)
        print_emulation.tray.close(selected_tray)
    printjob.print_verify('016c79d495c86c70478e01c1fdc50fabb82fa10f9e641d7ed349e9c5d22381e6', timeout=800)
    outputsaver.save_output()
