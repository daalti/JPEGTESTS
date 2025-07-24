import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using pjlpaper.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:pjlpaper.pcl=51901250b28964230dfa7547500dae882e24d09e5f4472ab90f10939c2069fa6
    +test_classification:System
    +name: test_pcl5_testfiles_pjl_pjlpaper
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_pjl_pjlpaper
        +guid:0218af93-8a56-45a4-bcdf-adae59f492ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaSizeSupported=na_legal_8.5x14in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pjl_pjlpaper(udw, setup_teardown, printjob, tray, outputsaver, outputverifier):
    # printjob.print_verify('51901250b28964230dfa7547500dae882e24d09e5f4472ab90f10939c2069fa6', timeout=600)
    # outputsaver.save_output()
    outputsaver.operation_mode('TIFF')
    # expected_media_size = MediaSize.letter

    default = tray.get_default_source()
    if tray.is_size_supported('na_legal_8.5x14in', default):
        tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
        # expected_media_size = MediaSize.legal
    else:
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
    udw_result = udw.mainApp.execute('PrintAppUw PUB_isUelAsNewJob')
    if(int(udw_result)):
        printjob.print_verify_multi('51901250b28964230dfa7547500dae882e24d09e5f4472ab90f10939c2069fa6', timeout=600,expected_jobs=2)
    else:
        printjob.print_verify('51901250b28964230dfa7547500dae882e24d09e5f4472ab90f10939c2069fa6', timeout=600)
    outputsaver.save_output()
