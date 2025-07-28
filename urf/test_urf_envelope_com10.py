import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Envelope-Com10 urf from *Envelope-Com10.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope-Com10.urf=a79c3047781d536af7c066818f2e861121e8d27a7d9ed5408d2fcbdbd0911294
    +name:test_urf_envelope_com10_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_envelope_com10_page
        +guid:01bf28ce-d2d8-422d-bf7e-c54b3df8d850
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=na_number-10_4.125x9.5in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_envelope_com10_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_number-10_4.125x9.5in', default):
        tray.configure_tray(default, 'na_number-10_4.125x9.5in', 'stationery')

    printjob.print_verify('a79c3047781d536af7c066818f2e861121e8d27a7d9ed5408d2fcbdbd0911294')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Envelope-Com10 page - Print job completed successfully")
