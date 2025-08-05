import pytest
from dunetuf.print.output.intents import Intents, Plex, MediaSource, PlexBinding, MediaSize

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: IPP test for printing a pdf file using attribute value sides_two_sided_long_edge
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-129624
    +timeout:360
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:5Page-IE556CP1.pdf=5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982
    +test_classification:System
    +name:test_pdl_intent_ipp_pdf_sides_two_sided_long_edge
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_intent_ipp_pdf_sides_two_sided_long_edge
        +guid:7aa05d94-233d-4b4f-92a7-2a1c97799c39
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP & Duplexer=True & MediaSizeSupported=na_letter_8.5x11in & MediaInputInstalled=Tray2

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_intent_ipp_pdf_sides_two_sided_long_edge(setup_teardown, printjob, outputsaver, outputverifier):
    outputsaver.operation_mode('TIFF')
    ipp_test_attribs = {'document-format': 'application/pdf', 'sides': 'two-sided-long-edge', 'media-source': 'tray-2', 'copies':3, 'media': 'na_letter_8.5x11in'}
    ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    printjob.ipp_print(ipp_test_file, '5fa8ec534404cc09d0c8448e518a290e54f08867b53e707e9fc010efb6634982')
    outputverifier.save_and_parse_output()
    outputverifier.verify_page_count(Intents.printintent, 6)
    outputverifier.verify_collated_copies(Intents.printintent, 1)
    outputverifier.verify_uncollated_copies(Intents.printintent, 3)
    outputverifier.verify_media_size(Intents.printintent, MediaSize.letter)
    outputverifier.verify_media_source(Intents.printintent, MediaSource.tray2)
    outputverifier.verify_plex(Intents.printintent, Plex.duplex)
    outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
