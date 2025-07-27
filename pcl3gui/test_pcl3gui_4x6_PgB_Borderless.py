import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a 4x6 file with non supported media type
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-107615
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:abbey4x6_PgB_borderless.pcl=1c10ea84f73b42be5abd5d72c2b78500401baadfc19a1e84fa58b121c49e5a24
    +name:test_pcl3gui_4x6_PgB_Borderless
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_4x6_PgB_Borderless
        +guid:63307d12-d06c-4fa7-b2a0-65b0a85f6cf3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaType=HPPhotoPapers & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_4x6_PgB_Borderless(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy'):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy')

        printjob.print_verify('1c10ea84f73b42be5abd5d72c2b78500401baadfc19a1e84fa58b121c49e5a24')
        outputsaver.save_output()
        tray.reset_trays()

        logging.info("PCL3GUI 4x6 advanced photo one pagecompleted successfully")
    else:
        logging.info("PCL3GUI 4x6 advanced photo media combination NOT supported")
