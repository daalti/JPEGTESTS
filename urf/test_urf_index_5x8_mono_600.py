import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf na index 5x8 Page from *Index-5x8_Mono_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Index-5x8_Mono_600.urf=94b6d3da4945089dd0b3b9e7424155af19bac2ab2bd41f452cf4b8c794877bc8
    +name:test_urf_index_5x8_mono_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_index_5x8_mono_600_page
        +guid:a40589d9-7dd6-4b29-8962-49ced3547480
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_index-5x8_5x8in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_index_5x8_mono_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_index-5x8_5x8in', default):
        tray.configure_tray(default, 'na_index-5x8_5x8in', 'stationery')

    printjob.print_verify('94b6d3da4945089dd0b3b9e7424155af19bac2ab2bd41f452cf4b8c794877bc8')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF na index 5x8 Page - Print job completed successfully")
