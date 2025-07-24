import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_rasbars3.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:420
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:6Page-rasbars3.obj=681b7bbb208cf68d854754bf6fcd05f0aacd0c3e08c87538faedad8e6180db7d
    +test_classification:System
    +name: test_pcl5_highvalue_6page_rasbars3
    +test:
        +title: test_pcl5_highvalue_6page_rasbars3
        +guid:9433adc2-ff86-47d7-8529-5aab3386a6e1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_6page_rasbars3(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'na_legal_8.5x14in', 'stationery'):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')

        printjob.print_verify('681b7bbb208cf68d854754bf6fcd05f0aacd0c3e08c87538faedad8e6180db7d')
        outputsaver.save_output()
    else:
        # if the media combination is not supported, just print a log and let the test pass
        logging.info("PCL5 na_legal_8.5x14in stationery - Media combination not supported")
