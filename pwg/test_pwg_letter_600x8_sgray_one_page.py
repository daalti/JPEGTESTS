import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600x8 sgray one page from *onepage-letter-sgray-8-600dpi.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15113
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:onepage-letter-sgray-8-600dpi.pwg=df51655e8f48eead0b875dd30e532ef5f6badacd2caab8b875cd9b2fc3ad1957
    +name:test_pwg_letter_600x8_sgray_one_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600x8_sgray_one_page
        +guid:39216c48-baa9-4a83-95d0-db05a46f3ba4
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_letter_600x8_sgray_one_page(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')

    printjob.print_verify('df51655e8f48eead0b875dd30e532ef5f6badacd2caab8b875cd9b2fc3ad1957')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

    logging.info("PWG Letter 600x8 sgray One Page - Print job completed successfully")
