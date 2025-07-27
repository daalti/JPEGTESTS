import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of a 4x6 photo normal one page PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15284
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Lily_4x6_HPPhoto_N.pcl=948e77bea01535a5f11cc8ab95ab562a2cb42dcff3d4431fe0fc44bd79ca8ba1
    +name:test_pcl3gui_4x6_Pht_N
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_4x6_Pht_N
        +guid:b752a21d-5adc-445d-8c06-274ded7c05c9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI & MediaType=HPPhotoPapers & MediaSizeSupported=na_index-4x6_4x6in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_4x6_Pht_N(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()

    if tray.is_media_combination_supported(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy'):
        tray.configure_tray(default, 'na_index-4x6_4x6in', 'com.hp-photographic-glossy')

        printjob.print_verify('948e77bea01535a5f11cc8ab95ab562a2cb42dcff3d4431fe0fc44bd79ca8ba1')
        outputsaver.save_output()
        tray.reset_trays()

        logging.info("PCL3GUI 4x6 photo normal one pagecompleted successfully")
    else:
        logging.info("PCL3GUI 4x6 photo normal media combination NOT supported")
