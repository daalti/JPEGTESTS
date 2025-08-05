import pytest
from dunetuf.print.output.intents import Intents, MediaSize, Plex

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file has different media_size and confirm blank page is inserted when different back side media found.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-142738
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:mixed_page_letter-us_executive.pdf=af68b3e3cff3970aef1e9b0758eb6bfcaaed196ca25575106b40e56f54e145df
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_duplex_mixed_media_size
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_duplex_mixed_media_size
        +guid:59c99537-7923-4436-b0c0-6e399614d444
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & PrintColorMode=Color & Duplexer=True & PrintDuplexerMediaSize=Letter & PrintDuplexerMediaSize=Executive

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_duplex_mixed_media_size(setup_teardown, printjob, tray, outputverifier):
    default = tray.get_default_source()
    if tray.is_size_supported('any', default):
        tray.configure_tray(default, 'any', 'any')
        printjob.ipp_print_using_attribute_file('pdf_duplex_no_media_size.test', 'af68b3e3cff3970aef1e9b0758eb6bfcaaed196ca25575106b40e56f54e145df')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 4)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        tray.reset_trays()
