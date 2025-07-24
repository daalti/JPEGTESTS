import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 6Page_raslogp3.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:420
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:6Page-raslogp3.obj=068f39cdd3a14c651d275f16a5675692a7f33f6273bf67dce816995b0b6b90cf
    +test_classification:System
    +name: test_pcl5_highvalue_6page_raslogp3
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_highvalue_6page_raslogp3
        +guid:5d400066-febd-4fcd-9033-195e78bc9ef0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5 & MediaSizeSupported=na_legal_8.5x14in & MediaType=Plain

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_6page_raslogp3(setup_teardown, printjob, outputsaver,tray):
    default = tray.get_default_source()
    if tray.is_media_combination_supported(default, 'na_legal_8.5x14in','stationery'):
        tray.configure_tray(default, 'na_legal_8.5x14in','stationery')

        printjob.print_verify('068f39cdd3a14c651d275f16a5675692a7f33f6273bf67dce816995b0b6b90cf')
        outputsaver.save_output()
    else:
        # if the media combination is not supported, just print a log and let the test pass
        logging.info("PCL5 na_legal_8.5x14in stationery - Media combination not supported")
