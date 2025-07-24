import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using UserDefinedCustomMedia.pcl
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:UserDefinedCustomMedia.pcl=05a2240ba1fafe1d0bdb1ea831af202ac64aa859dec4796bf3395415f3e4877a
    +test_classification:System
    +name: test_pcl5_testfiles_media_handling_userdefinedcustommedia
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_testfiles_media_handling_userdefinedcustommedia
        +guid:3826032e-8af5-4996-bf06-c48a92193691
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaSizeSupported=custom & MediaType=Plain

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_media_handling_userdefinedcustommedia(setup_teardown, printjob, outputsaver, tray):

    media_source = ''
    for source in tray.trays:
        # added the any condition because this was how the test was executed in all the cases
        if tray.is_media_combination_supported(source, 'any', 'any'):
            selected_media_source = source
            break
        elif tray.is_media_combination_supported(source, 'custom', 'stationery'):
            tray.configure_tray(source, 'custom', 'stationery')
            media_source = source
            break
    
    if media_source == '':
        logging.info("No tray supports custom stationery")
        return

    printjob.print_verify('05a2240ba1fafe1d0bdb1ea831af202ac64aa859dec4796bf3395415f3e4877a', timeout=600)
    outputsaver.save_output()

    tray.reset_trays()
